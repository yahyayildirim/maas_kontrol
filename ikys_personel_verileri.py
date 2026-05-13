#!/usr/bin/env python3

import re
import os
import time
import sabitler
import pandas as pd
from glob import glob
from pathlib import Path
from datetime import datetime

import sys
sys.dont_write_bytecode = True

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

pd.options.mode.chained_assignment = None  # default='warn'

bu_yil = datetime.now().year
bu_ay = datetime.now().strftime("%B")

def ikys_unvan_verileri():
	unvan_df = pd.DataFrame(pd.read_excel(f'{os.path.dirname(__file__)}/maas_verileri.xlsx', sheet_name=4))
	return unvan_df

def ikys_personel_verileri():
	#İKYSden indirdiğimiz dosya, html formatında olduğu için önce read_html metodu ile açıp, xlsx formatında tekrar kaydediyoruz.
	bu_dizin = os.path.dirname(__file__) + '/ikys/'

	# Klasördeki tüm Excel dosyalarını listele
	dosyalar = glob(f"{bu_dizin}/*.xls")

	# Dosyaların varlığını kontrol et
	if not dosyalar:
	    raise FileNotFoundError("Klasörde .xls uzantılı herhangi dosya bulunamadı!")

	# İlk dosyanın ilk tablosunu okuyarak başlangıç noktası yap
	# İKYS Sistemi -> Personel Sorgulama alanından alınan Rapor
	# Sicil, TC Kimlik, Adı Soyadı, Kadro Ünvan Sıra No, Görevlendirme Ünvanı, Öğrenim Durumu-Okul-Fakülte-Bölüm, Diyanete Giriş Tarihi, Ödenilecek Derece/Kademe, İzin Adı

	ilk_tablo = pd.read_html(dosyalar[0])  # Tablolar listesi döner
	birlesik_df = ilk_tablo[0]  # İlk tabloyu al

	# Diğer dosyaların tablolarını sırayla birleştir
	for dosya in dosyalar[1:]:
	    tablolar = pd.read_html(dosya)  # Dosyadaki tüm tablolar
	    df = tablolar[0]  # İlk tabloyu al
	    if "Sicil" or "Kadro Ünvan Sıra No" not in df.columns:
	        raise KeyError(f"Dosyada 'Sicil' ve 'Kadro Ünvan Sıra No' sütunu bulunamadı: {dosya}")
	    birlesik_df = pd.merge(birlesik_df, df, on="Sicil", how="inner")  # Birleştirme işlemi

	# Sonuçları yeni bir Excel dosyasına kaydetmek
	#birlesik_df.to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/Personel_Raporu_Temiz.xlsx', index=False, freeze_panes=(1,0))

	#xlsx formatına çevirdiğimiz dosyamızı read_excel metodu ile açıp, DataFrame aktarıyoruz.
	#df = pd.DataFrame(pd.read_excel('./ikys/Personel_Rapor_Temiz.xlsx'))

	# Boş olan ve değeri bulunmayan satırları siliyoruz.
	df = birlesik_df.dropna(how='all', axis=0)

	#########################################################################################
	# Sicil sütunundaki birleşik hücreleri doldurmak için ffill kullanın
	df["Sicil"] = df["Sicil"].ffill()

	# Regex kullanarak öğrenim verisinde tarih ile biten kayıtları ayrı bir satır olarak ayırma
	ayrilan_satirlar = []

	for _, satir in df.iterrows():
	    sicil = satir["Sicil"]
	    ogrenim = satir["Öğrenim Durumu-Okul-Fakülte-Bölüm"]
	    diger_sutunlar = satir.drop(["Sicil", "Öğrenim Durumu-Okul-Fakülte-Bölüm"]).to_dict()

	    # Tarihler ile biten kayıtları yakalayın
	    eslesenler = re.findall(r".*?\d{2}\.\d{2}\.\d{4}", ogrenim)

	    # Her eşleşmeyi detay olarak ekle
	    for eslesen in eslesenler:
	        ayrilan_satir = {"Sicil": sicil, "Öğrenim Durumu-Okul-Fakülte-Bölüm": eslesen.strip()}
	        ayrilan_satir.update(diger_sutunlar)  # Diğer sütunları ekleyin
	        ayrilan_satirlar.append(ayrilan_satir)

	# Yeni DataFrame oluştur
	yeni_df = pd.DataFrame(ayrilan_satirlar)

	# En yüksek dereceli eğitimi seçme: Her Sicil için son satırı al
	df = yeni_df.groupby("Sicil").tail(1).reset_index(drop=True)

	#########################################################################################
	#maas_verileri.xlsx dosyasının kadro_unvan_sira_no sayfasında aynı ünvan birden fazla yazılmış ise teke düşür
	unvan_df = ikys_unvan_verileri().groupby('unvan_sira_no').first().reset_index()

	# unvan_df'deki unvan_sira_no değerlerini bir sözlük (dictionary) olarak kaydedelim
	#df['Kadro Ünvan Sıra No'] = df['Kadro Ünvan Sıra No'].fillna(9999)  # Varsayılan olarak 0 verelim
	unvan_bilgileri = unvan_df.set_index('unvan_sira_no')[['unvan_adi', 'unvan_sinifi', 'personel_tipi']].to_dict(orient='index')

	# df'ye yeni sütunları ekleyelim
	df['Ünvan'] = df['Kadro Ünvan Sıra No'].map(lambda x: unvan_bilgileri.get(x, {}).get('unvan_adi', None))
	df['Sınıf'] = df['Kadro Ünvan Sıra No'].map(lambda x: unvan_bilgileri.get(x, {}).get('unvan_sinifi', None))
	df['Personel Tipi'] = df['Kadro Ünvan Sıra No'].map(lambda x: unvan_bilgileri.get(x, {}).get('personel_tipi', 'Vekil'))
	#########################################################################################

	# Sadece memur ve vekil personel ile işlem yapacağımız için onları alıyoruz ve sözleşmelileri çıkarıyoruz.
	df = df[df['Personel Tipi'].isin(['Memur', 'Vekil'])]

	# Mükerrer kayıtları çıkarıyoruz.
	df = df.drop_duplicates(subset=['Sicil'], ignore_index=True)

	for i in df.index:
		Ünvan = df.iloc[i]['Ünvan']
		if pd.isna(Ünvan):
			#df['Ünvan'][i] = df.iloc[i]['Görevlendirme Ünvanı']
			df.loc[df['Ünvan'].isna(), 'Ünvan'] = df['Görevlendirme Ünvanı']

	# Bize lazım olan sütunları çekiyoruz.
	df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Ünvan', 'Öğrenim Durumu-Okul-Fakülte-Bölüm', 'Diyanete Giriş Tarihi', 'Ödenilecek Derece/Kademe', 'İzin Adı']]

	# Eğer Ünvan sütunu boş ise Vekil olarak değiştirmesini sağlıyoruz.
	#df['Ünvan'] = df['Ünvan'].fillna('Vekil')
	df.fillna({'Sınıf': 'Din Hizmetleri', 'Ünvan': 'Vekil'}, inplace=True)
	#df.to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/Personel_Raporu_Temiz.xlsx', index=False, freeze_panes=(1,0))

	# İKYS raporundaki öğrenim durumu çok uzun ve karmaşık olduğu için, regex ve replace metodları ile istediğimiz formata çeviriyoruz.
	for i in df["Öğrenim Durumu-Okul-Fakülte-Bölüm"].tolist():
		ogrenimbul = re.search("Doçentlik|Master|Doktora|Lisansüstü|Üniversite|Lisans Tamamlama|Yüksek Okul|İmam Hatip|Meslek|Lise|Birinci Devre|Ortaokul|İlköğretim|İlkokul|Okur - Yazar", i)
		df['Öğrenim Durumu-Okul-Fakülte-Bölüm'] = df['Öğrenim Durumu-Okul-Fakülte-Bölüm'].replace([i], ogrenimbul.group(0))

	# Özel Hizmet Tazminatı için öğrenim durumunu Yüksek Okul, İHL ve Diğer olarak değiştiriyoruz.
	df['ogrenim'] = df['Öğrenim Durumu-Okul-Fakülte-Bölüm'].replace(
		['Doçentlik', 'Master', 'Doktora', 'Lisansüstü', 'Üniversite', 'Lisans Tamamlama', 'İmam Hatip', 'Meslek', 'Lise', 'Birinci Devre', 'Ortaokul', 'İlköğretim', 'İlkokul', 'Okur-Yazar'],
		['Yüksek Okul', 'Yüksek Okul', 'Yüksek Okul', 'Yüksek Okul', 'Yüksek Okul', 'Yüksek Okul', 'İHL', 'Diğer', 'Diğer', 'Diğer', 'Diğer', 'Diğer', 'Diğer', 'Diğer']
		)

	# Adı ve Soyadını büyük harfe çeviriyoruz. Büyük harfe çevirdiğimizde, küçük i harfi I olarak geçiyor. bunu düzeltmek için de ayrıca replace etmemiz gerekiyor.
	df['Adı Soyadı'] = df['Adı Soyadı'].str.replace('i', 'İ').str.upper()
	df['Adı Soyadı'] = df['Adı Soyadı'].replace(regex=True, to_replace=r'^(DR. )', value=r'')

	# Sınıf sütunundaki büyük harfler hariç herşeyi siliyoruz ve geriye sadece GİH,DH,TH,YH ibarelerini bırakıyoruz.
	df['Sınıf'] = df['Sınıf'].replace(regex=True, to_replace=r'([a-z]|\s|ı|ü|ş|ç|ğ|ö|)', value=r'')

	# Ünvan kısaltmaları
	# Ünvan sütunundaki ikys sisteminde bulunan Ünvanları kbs sistemindekine uyarlıyoruz.
	unvan_kisaltma = {
		r'.*Yar.*': 'İl Müft.Yr',
		r'^İlçe.*': 'İlçe Müft.',
		r'^Şube.*': 'Şube Md.',
		r'^Veri.*': 'V.H.K.İ.',
		r'^Memur.*Ş.*': 'Memur(Ş)',
		r'^Hiz.*Ş.*': 'Hzmetli(Ş)',
		r'^Kaloriferci': 'Kaloriferc',
		r'^Uzman\sVaiz.*': 'Uzman Vaiz',
		r'^Vaiz.*': 'Vaiz',
		r'^Cez.*': 'Cezv.Vaizi',
		r'^Din.*Uzmanı': 'Din Hz.Uzm',
		r'^Eğit.*Uzmanı': 'Eğt.Uzmanı',
		r'^Eğit.*Görevlisi': 'Eğitim Gör',
		r'^İma.*': 'İmam-Hat.',
		r'^Baş.*İma.*': 'Başimam',
		r'^Baş.*Müe.*': 'Başmüezzin',
		r'^Kur.*Öğre.*': 'Kur.Krs.Öğ',
		r'^Kur.*Uz.*': 'Kur.Uz.Öğ',
		r'^Müez.*': 'Müez.Kayyı',
		r'^Uzman.*İmam.*': 'Uz.İm.Hat',
		r'^Ayniyat.*Saymanı': 'Ayn.Saym.',
		r'^Dini.*Müdürü':'Dini İhtisas Merkezi Müdürü'
	}

	for p, r in unvan_kisaltma.items():
		df['Ünvan'] = df['Ünvan'].replace(regex=True, to_replace=p, value=r)

	# Ödenilecek Derece/Kademe sütunundaki parantezleri siliyoruz
	df['Ödenilecek Derece/Kademe'] = df['Ödenilecek Derece/Kademe'].replace(regex=True, to_replace=r'[()]', value='')

	df['Hizmet Süresi (Yıl)'] = bu_yil - pd.to_datetime(pd.Series(df['Diyanete Giriş Tarihi']), format='%d.%m.%Y').dt.year
	#df['Hizmet Süresi (Yıl)'] = bu_yil - pd.to_datetime(pd.Series(df['İlk Memuriyete Başlama Tarihi']), format='%d.%m.%Y').dt.year

	# Ödenilecek Derece/Kademe sütununu Derece, Kademe ve Ek Gösterge olarak üç sutüna ayırıyoruz. NaN olan değerleri 0 olarak değiştiriyoruz ve tipini integer olarak belirliyoruz.
	df[['Derece', 'Kademe', 'Ek Gösterge']] = df['Ödenilecek Derece/Kademe'].str.split('-', expand=True).fillna(0).astype(int)
	df['Derece/Kademe'] = df['Ödenilecek Derece/Kademe'].str.split('-').str[:2].str.join('-')

	# Personelin Derece ve Kademesini alarak yan ödemesini sabitler.py dosyasındaki fonksiyon aracılığı ile maas_verileri.xlsx içerisinden çekiyoruz. 1/4 --> 1500 gibi
	df['Gösterge Puanı'] = df.apply(lambda row: sabitler.gosterge_puani(row["Derece"], row["Kademe"]), axis=1)

	# Personelin İş Güçlüğü, İş Riski, Teminde Güçlük ve Mali Sorumluluk puanlarını, Ünvan ve dereceye göre sabitler.py dosyasındaki fonksiyon aracılığı ile maas_verileri.xlsx içerisinden çekiyoruz.
	df['Yan Ödeme'] = df.apply(lambda row: sabitler.yan_odeme_puani(row["Ünvan"], row["Derece"], row["Hizmet Süresi (Yıl)"], row["İzin Adı"]), axis=1)

	# df['Yan Ödeme'] ile aldığımız oran ile Ünvan bilgisini alarak sabitler.py dosyasındaki fonksiyon aracılığı TL tutarı hesaplıyoruz.
	df['Aylık Tutar'] = round(df.apply(lambda row: sabitler.aylik_katsayi(row["Gösterge Puanı"], row["Ünvan"], row["İzin Adı"]), axis=1), 2)
	
	# Aynı şekilde İKYSden çektiğimiz ek gösterge miktarını ve Ünvan bilgisini sabitler.py dosyasındaki fonksiyon aracılığı ile hesaplıyoruz.
	df['Ek Gös.Ay.'] = round(df.apply(lambda row: sabitler.ek_gosterge(row["Ek Gösterge"], row["Ünvan"], row["İzin Adı"]), axis=1), 2)

	# df['Gösterge Puanı'] ile aldığımız oran ile Ünvan bilgisini alarak sabitler.py dosyasındaki fonksiyon aracılığı TL tutarı hesaplıyoruz. 
	df['Yan Ödeme Aylık'] = round(df.apply(lambda row: sabitler.yan_odeme(row["Yan Ödeme"], row["Ünvan"]), axis=1), 2)

	# hizmet yılı baz alınarak kıdem aylığını fonksiyon aracılığı ile hesaplıyoruz.
	# burada maalesef çok hata alıyoruz. çümkü kbs ve ikys kıdem yılları birbirini tutmuyor.
	df['Kıdem Aylık'] = round(df.apply(lambda row: sabitler.kidem_ayligi(row["Hizmet Süresi (Yıl)"], row["Ünvan"]), axis=1), 2)

	# maas_verileri.xlsx içerisindeki bilgileri, sabitler.py dosyasındaki fonksiyon ile Ünvan, derece ve ogrenim bilgisi değerlerini göndererek çekiyoruz.
	df['Özel Hiz. Taz. Puanı'] = round(df.apply(lambda row: sabitler.ozel_hizmet_orani(row["Ünvan"], row["Derece"], row["ogrenim"], row["İzin Adı"]), axis=1))

	# aynı şekilde özel hizmet tazmınatı tutarını sabitler.py dosyasındaki fonsiyona gerekli parametreleri göndererek hesaplıyoruz.	
	df['Özel Hiz.Taz.'] = round(df.apply(lambda row: sabitler.ozel_hizmet(row["Ünvan"], row["Derece"], row["ogrenim"], row["İzin Adı"]), axis=1), 2)

	# maas_verileri.xlsx içerisindeki bilgileri, sabitler.py dosyasındaki fonksiyon ile Ünvan, derece ve ogrenim bilgisi değerlerini göndererek çekiyoruz.
	df['Ek Tazminat Puanı'] = df.apply(lambda row: sabitler.ek_tazminat_puani(row["Ünvan"], row["Derece"], row["ogrenim"]), axis=1)

	# Ek Ödeme oranını maas_verileri.xlsx dosyasından fonksiyon ile çekiyoruz.
	df['666 KHK Oranı'] = df.apply(lambda row: sabitler.ek_odeme_666_orani(row["Ünvan"], row["Derece"], row["ogrenim"], row["İzin Adı"]), axis=1)

	# Ek Ödeme oranını maas_verileri.xlsx dosyasından fonksiyon ile çekiyoruz.
	df['İlaveÖd.(375.40'] = round(df.apply(lambda row: sabitler.ilave_odeme_97(row["Ünvan"], row["İzin Adı"]), axis=1), 2)

	# aynı şekilde ek ödeme 666 khk tutarını sabitler.py dosyasındaki fonsiyona gerekli parametreleri göndererek hesaplıyoruz.
	df['Ek Öde.(666 KHK'] = round(df.apply(lambda row: sabitler.ek_odeme_666(row["Ünvan"], row["Derece"], row["ogrenim"], row["İzin Adı"]), axis=1), 2)

	df['Ünvan'] = df['Ünvan'].replace(regex=True, to_replace=r'^(Vekil.*K)', value=r'Müez.Kayyı')
	df['Ünvan'] = df['Ünvan'].replace(regex=True, to_replace=r'^(Vekil.*H)', value=r'İmam-Hat.')

	# Son olarak excele aktaracağımız sütunları belirliyoruz.
	df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Ünvan', 'Derece/Kademe', 'Gösterge Puanı', 'Aylık Tutar', 'Ek Gösterge', 'Ek Gös.Ay.', 'Yan Ödeme', 'Yan Ödeme Aylık', 'Ek Tazminat Puanı', 'Özel Hiz. Taz. Puanı',
	'Özel Hiz.Taz.', '666 KHK Oranı', 'Ek Öde.(666 KHK', 'İlaveÖd.(375.40']]

	# Listeyi TC veya Adı-Soyadına göre sıralayabilirsiniz, dikkat etmeniz gereken ise kbs_bordro ve kbs_personelde de aynı değişikliği yapmanızdır.
	#df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)
	df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)

	# DataFrame içinde topladığımız ve sütunlarını belirlediğimiz verilerimizi excele xlsx formatında aktarıyoruz. freeze_panes değeri ile ilk satır ve ilk iki sütunu donduruyoruz.
	df.to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/.ikys_personel_verileri.xlsx', index=False, freeze_panes=(1,2))
	print('%30')

if __name__ == "__main__":
	ikys_personel_verileri()
