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

def ikys_personel_verileri():
	#İKYSden indirdiğimiz dosya, html formatında olduğu için önce read_html metodu ile açıp, xlsx formatında tekrar kaydediyoruz.
	bu_dizin = os.path.dirname(__file__) + '/ikys/'
	dosya =glob(bu_dizin + "Personel Rapor*.xls")
	if dosya:
		df = pd.read_html(''.join(dosya))
		df = pd.DataFrame(df[0])

	else:
		print("/ikys klasöründe Personel Rapor dosyası yok. Lütfen tekrar deneyin.")
		sys.exit()

	df.to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/Personel_Raporu_Temiz.xlsx', index=False, freeze_panes=(1,0))

	#xlsx formatına çevirdiğimiz dosyamızı read_excel metodu ile açıp, DataFrame aktarıyoruz.
	#df = pd.DataFrame(pd.read_excel('./ikys/Personel_Rapor_Temiz.xlsx'))

	# Boş olan ve değeri bulunmayan satırları siliyoruz.
	df = df.dropna(how='all', axis=0)

	# Sadece memur ve vekil personel ile işlem yapacağımız için onları alıyoruz ve sözleşmelileri çıkarıyoruz.
	df = df[df['Personel Tipi'].isin(['Memur', 'Vekil'])]

	# Mükerrer kayıtlarıda çıkarıyoruz.
	df = df.drop_duplicates(subset=['Sicil'], ignore_index=True)

	for i in df.index:
		unvan = df.iloc[i]['Unvan']
		if pd.isna(unvan):
			#print(df.iloc[i]['Görevlendirme Unvanı'])
			df['Unvan'][i] = df.iloc[i]['Görevlendirme Unvanı']

	# Bize lazım olan sütunları çekiyoruz.
	df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan', 'Öğrenim Durumu-Okul-Fakülte-Bölüm', 'Sendika', 'Diyanete Giriş Tarihi', 'İlk Memuriyete Başlama Tarihi', 'Ödenilecek Derece/Kademe',
	'Hizmet Süresi (Ay)', 'Hizmet Süresi (Yıl)', 'İzin Adı']]

	# Eğer unvan sütunu boş ise Vekil olarak değiştirmesini sağlıyoruz.
	#df['Unvan'] = df['Unvan'].fillna('Vekil')
	df.fillna({'Sınıf': 'DH', 'Unvan': 'Vekil'}, inplace=True)

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
	df['Adı Soyadı'].replace(regex=True, inplace=True, to_replace=r'^(DR. )', value=r'')

	# Sınıf sütunundaki büyük harfler hariç herşeyi siliyoruz ve geriye sadece GİH,DH,TH,YH ibarelerini bırakıyoruz.
	df['Sınıf'].replace(regex=True, inplace=True, to_replace=r'([a-z]|\s|ı|ü|ş|ç|ğ|ö|)', value=r'')

	# Unvan sütunundaki ikys sisteminde bulunan unvanları kbs sistemindekine uyarlıyoruz.
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(.*Yar.*)', value=r'İl Müft.Yr')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(İlçe.*)', value=r'İlçe Müft.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Şube.*)', value=r'Şube Md.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Veri.*)', value=r'V.H.K.İ.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Memur.*Ş.*)', value=r'Memur(Ş)')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Hiz.*Ş.*)', value=r'Hzmetli(Ş)')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Kaloriferci)', value=r'Kaloriferc')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Vaiz.*)', value=r'Vaiz')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Cez.*)', value=r'Cezv.Vaizi')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Din.*)', value=r'Din Hz.Uzm')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(İma.*)', value=r'İmam-Hat.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Baş.*İma.*)', value=r'Başimam')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Kur.*Öğre.*)', value=r'Kur.Krs.Öğ')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Kur.*Uz.*)', value=r'Kur.Uz.Öğ')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Müez.*)', value=r'Müez.Kayyı')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Uzman.*İmam.*)', value=r'Uz.İm.Hat')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Ayniyat Saymanı)', value=r'Ayn.Saym.')	

	# Ödenilecek Derece/Kademe sütunundaki parantezleri siliyoruz
	df['Ödenilecek Derece/Kademe'].replace(regex=True, inplace=True, to_replace=r'[()]', value=r'')

	df['Hizmet Süresi (Yıl)'] = bu_yil - pd.to_datetime(pd.Series(df['Diyanete Giriş Tarihi']), format='%d.%m.%Y').dt.year
	#df['Hizmet Süresi (Yıl)'] = bu_yil - pd.to_datetime(pd.Series(df['İlk Memuriyete Başlama Tarihi']), format='%d.%m.%Y').dt.year

	# Ödenilecek Derece/Kademe sütununu Derece, Kademe ve Ek Gösterge olarak üç sutüna ayırıyoruz. NaN olan değerleri 0 olarak değiştiriyoruz ve tipini integer olarak belirliyoruz.
	df[['Derece', 'Kademe', 'Ek Gösterge']] = df['Ödenilecek Derece/Kademe'].str.split('-', expand=True).fillna(0).astype(int)

	# Personelin Derece ve Kademesini alarak yan ödemesini sabitler.py dosyasındaki fonksiyon aracılığı ile maas_verileri.xlsx içerisinden çekiyoruz. 1/4 --> 1500 gibi
	df['Gösterge Puanı'] = df.apply(lambda row: sabitler.gosterge_puani(row["Derece"], row["Kademe"]), axis=1)

	# Personelin İş Güçlüğü, İş Riski, Teminde Güçlük ve Mali Sorumluluk puanlarını, unvan ve dereceye göre sabitler.py dosyasındaki fonksiyon aracılığı ile maas_verileri.xlsx içerisinden çekiyoruz.
	df['Yan Ödeme'] = df.apply(lambda row: sabitler.yan_odeme_puani(row["Unvan"], row["Derece"], row["Hizmet Süresi (Yıl)"], row["İzin Adı"]), axis=1)

	# df['Yan Ödeme'] ile aldığımız oran ile unvan bilgisini alarak sabitler.py dosyasındaki fonksiyon aracılığı TL tutarı hesaplıyoruz.
	df['Aylık Tutar'] = round(df.apply(lambda row: sabitler.aylik_katsayi(row["Gösterge Puanı"], row["Unvan"], row["İzin Adı"]), axis=1), 2)
	
	# Aynı şekilde İKYSden çektiğimiz ek gösterge miktarını ve unvan bilgisini sabitler.py dosyasındaki fonksiyon aracılığı ile hesaplıyoruz.
	df['Ek Gös.Ay.'] = round(df.apply(lambda row: sabitler.ek_gosterge(row["Ek Gösterge"], row["Unvan"], row["İzin Adı"]), axis=1), 2)

	# df['Gösterge Puanı'] ile aldığımız oran ile unvan bilgisini alarak sabitler.py dosyasındaki fonksiyon aracılığı TL tutarı hesaplıyoruz. 
	df['Yan Ödeme Aylık'] = round(df.apply(lambda row: sabitler.yan_odeme(row["Yan Ödeme"], row["Unvan"]), axis=1), 2)

	# hizmet yılı baz alınarak kıdem aylığını fonksiyon aracılığı ile hesaplıyoruz.
	# burada maalesef çok hata alıyoruz. çümkü kbs ve ikys kıdem yılları birbirini tutmuyor.
	df['Kıdem Aylık'] = round(df.apply(lambda row: sabitler.kidem_ayligi(row["Hizmet Süresi (Yıl)"], row["Unvan"]), axis=1), 2)

	# maas_verileri.xlsx içerisindeki bilgileri, sabitler.py dosyasındaki fonksiyon ile unvan, derece ve ogrenim bilgisi değerlerini göndererek çekiyoruz.
	df['Özel Hiz. Taz. Puanı'] = round(df.apply(lambda row: sabitler.ozel_hizmet_orani(row["Unvan"], row["Derece"], row["ogrenim"], row["İzin Adı"]), axis=1))

	# aynı şekilde özel hizmet tazmınatı tutarını sabitler.py dosyasındaki fonsiyona gerekli parametreleri göndererek hesaplıyoruz.	
	df['Özel Hiz.Taz.'] = round(df.apply(lambda row: sabitler.ozel_hizmet(row["Unvan"], row["Derece"], row["ogrenim"], row["İzin Adı"]), axis=1), 2)

	# maas_verileri.xlsx içerisindeki bilgileri, sabitler.py dosyasındaki fonksiyon ile unvan, derece ve ogrenim bilgisi değerlerini göndererek çekiyoruz.
	df['Ek Tazminat Puanı'] = df.apply(lambda row: sabitler.ek_tazminat_puani(row["Unvan"], row["Derece"], row["ogrenim"]), axis=1)

	# Ek Ödeme oranını maas_verileri.xlsx dosyasından fonksiyon ile çekiyoruz.
	df['666 KHK Oranı'] = df.apply(lambda row: sabitler.ek_odeme_666_orani(row["Unvan"], row["Derece"], row["ogrenim"], row["İzin Adı"]), axis=1)

	# Ek Ödeme oranını maas_verileri.xlsx dosyasından fonksiyon ile çekiyoruz.
	df['İlaveÖd.(375.40'] = round(df.apply(lambda row: sabitler.ilave_odeme_97(row["İzin Adı"]), axis=1), 2)

	# aynı şekilde ek ödeme 666 khk tutarını sabitler.py dosyasındaki fonsiyona gerekli parametreleri göndererek hesaplıyoruz.
	df['Ek Öde.(666 KHK'] = round(df.apply(lambda row: sabitler.ek_odeme_666(row["Unvan"], row["Derece"], row["ogrenim"], row["İzin Adı"]), axis=1), 2)
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Vekil.*K)', value=r'Müez.Kayyı')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Vekil.*H)', value=r'İmam-Hat.')

	# Son olarak excele aktaracağımız sütunları belirliyoruz.
	df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan', 'Derece', 'Kademe', 'Gösterge Puanı', 'Aylık Tutar', 'Ek Gösterge', 'Ek Gös.Ay.', 'Yan Ödeme', 'Yan Ödeme Aylık', 'Ek Tazminat Puanı', 'Özel Hiz. Taz. Puanı',
	'Özel Hiz.Taz.', '666 KHK Oranı', 'Ek Öde.(666 KHK', 'İlaveÖd.(375.40']]

	# Listeyi TC veya Adı-Soyadına göre sıralayabilirsiniz, dikkat etmeniz gereken ise kbs_bordro ve kbs_personelde de aynı değişikliği yapmanızdır.
	#df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)
	df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)

	# DataFrame içinde topladığımız ve sütunlarını belirlediğimiz verilerimizi excele xlsx formatında aktarıyoruz. freeze_panes değeri ile ilk satır ve ilk iki sütunu donduruyoruz.
	df.to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/ikys_personel_verileri.xlsx', index=False, freeze_panes=(1,2))
	print('%30')

if __name__ == "__main__":
	ikys_personel_verileri()
