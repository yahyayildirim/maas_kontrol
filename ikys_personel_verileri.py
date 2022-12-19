#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import pandas as pd
from datetime import datetime
import re
import time
import sabitler

def ikys_personel_verileri():
	#İKYSden indirdiğimiz dosya, html formatında olduğu için önce read_html metodu ile açıp, xlsx formatında tekrar kaydediyoruz.
	dfs = pd.read_html('./ikys/Personel Rapor.xls')
	dfs[0].to_excel('./ikys/Personel Rapor.xlsx', index=False)
	
	#xlsx formatına çevirdiğimiz dosyamızı read_excel metodu ile açıp, DataFrame aktarıyoruz.
	df = pd.DataFrame(pd.read_excel('./ikys/Personel Rapor.xlsx'))

	# Boş olan ve değeri bulunmayan satır ve sütunları siliyoruz.
	df = df.dropna(how='all', axis=1)

	# Sadece memur ve vekil personel ile işlem yapacağımız için onları alıyoruz ve sözleşmelileri çıkarıyoruz.
	df = df[df['Personel Tipi'].isin(['Memur', 'Vekil'])]

	# Mükerrer kayıtlarıda çıkarıyoruz.
	df = df.drop_duplicates(subset=['Sicil'], ignore_index=True)

	# Bize lazım olan sütunları çekiyoruz.
	df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan',
			'Öğrenim Durumu-Okul-Fakülte-Bölüm', 'Sendika', 'Diyanete Giriş Tarihi', 'İlk Memuriyete Başlama Tarihi',
			'Ödenilecek Derece/Kademe', 'Hizmet Süresi (Ay)', 'Hizmet Süresi (Yıl)']]

	# İKYS raporundaki öğrenim durumu çok uzun ve karmaşık olduğu için, regex ve replace metodları ile istediğimiz formata çeviriyoruz.
	for i in df["Öğrenim Durumu-Okul-Fakülte-Bölüm"].tolist():
		ogrenimnul = re.search("Doktora|Lisansüstü|Üniversite|Lisans Tamamlama|Yüksek Okul|İmam Hatip|Lise|Ortaokul|İlköğretim|İlkokul|Okur-Yazar", i)
		df['Öğrenim Durumu-Okul-Fakülte-Bölüm'] = df['Öğrenim Durumu-Okul-Fakülte-Bölüm'].replace([i], ogrenimnul.group(0))

	# Özel Hizmet Tazminatı için öğrenim durumunu Yüksek Okul, İHL ve Diğer olarak değiştiriyoruz.
	df['ogrenim'] = df['Öğrenim Durumu-Okul-Fakülte-Bölüm'].replace(['Doktora', 'Lisansüstü', 'Üniversite', 'Lisans Tamamlama', 'İmam Hatip', 'Lise', 'Ortaokul', 'İlköğretim', 'İlkokul', 'Okur-Yazar'], ['Yüksek Okul', 'Yüksek Okul', 'Yüksek Okul', 'Yüksek Okul', 'İHL', 'Diğer', 'Diğer', 'Diğer', 'Diğer', 'Diğer'])

	# Adı ve Soyadını büyük harfe çeviriyoruz. Büyük harfe çevirdiğimizde, küçük i harfi I olarak geçiyor. bunu düzeltmek için de ayrıca replace etmemiz gerekiyor.
	df['Adı Soyadı'] = df['Adı Soyadı'].str.replace('i', 'İ').str.upper()

	# Sınıf sütunundaki büyük harfler hariç herşeyi siliyoruz ve geriye sadece GİH,DH,TH,YH ibarelerini bırakıyoruz.
	df['Sınıf'].replace(regex=True, inplace=True, to_replace=r'([a-z]|\s|ı|ü|ş|ç|ğ|ö|)', value=r'')

	# Unvan sütunundaki ikys sisteminde bulunan unvanları kbs sistemindekine uyarlıyoruz.
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(.*Yar.*)', value=r'İl Müft.Yr')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(İlçe.*)', value=r'İlçe Müft.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Şube.*)', value=r'Şube Md.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Veri.*)', value=r'V.H.K.İ.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Memur.*Ş.*)', value=r'Memur')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Hiz.*Ş.*)', value=r'Hzmetli(Ş)')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Kaloriferci)', value=r'Kaloriferc')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Vaiz.*)', value=r'Vaiz')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Cez.*)', value=r'Cezv.Vaizi')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Din.*)', value=r'Din Hz.Uzm')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(İma.*)', value=r'İmam.Hat.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Kur.*Öğre.*)', value=r'Kur.Krs.Öğ')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Kur.*Uz.*)', value=r'Kur.Uz.Öğ')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Müez.*)', value=r'Müez.Kayyı')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Uzman.İmam.*)', value=r'Uz.İm.Hat')

	# Ödenilecek Derece/Kademe sütunundaki parantezleri siliyoruz
	df['Ödenilecek Derece/Kademe'].replace(regex=True, inplace=True, to_replace=r'[()]', value=r'')

	# KBS sistemindeki Kıdem Yılı ile İKYS Sistemindeki Hizmet Yılı birbirini tutmuyor. Yine de personelin Diyanete giriş tarihindeki yılı baz alarak, içinde bulunduğumuz yıldan çıkartıp Hizmet yılını buluyoruz.
	bu_yil = datetime.now().year
	df['Hizmet Süresi (Yıl)'] = bu_yil - pd.to_datetime(pd.Series(df['Diyanete Giriş Tarihi']), format='%d.%m.%Y').dt.year
	#df['Hizmet Süresi (Yıl)'] = bu_yil - pd.to_datetime(pd.Series(df['İlk Memuriyete Başlama Tarihi']), format='%d.%m.%Y').dt.year

	# Ödenilecek Derece/Kademe sütununu Derece, Kademe ve Ek Gösterge olarak üç sutüna ayırıyoruz. NaN olan değerleri 0 olarak değiştiriyoruz ve tipini integer olarak belirliyoruz.
	df[['Derece', 'Kademe', 'Ek Gösterge']] = df['Ödenilecek Derece/Kademe'].str.split('-', expand=True).fillna(0).astype(int)

	# Personelin Derece ve Kademesini alarak yan ödemesini sabitler.py dosyasındaki fonksiyon aracılığı ile maas_verileri.xlsx içerisinden çekiyoruz. 1/4 --> 1500 gibi
	df['Yan Ödeme'] = df.apply(lambda row: sabitler.gosterge_puani(row["Derece"], row["Kademe"]), axis=1)

	# Personelin İş Güçlüğü, İş Riski, Teminde Güçlük ve Mali Sorumluluk puanlarını, unvan ve dereceye göre sabitler.py dosyasındaki fonksiyon aracılığı ile maas_verileri.xlsx içerisinden çekiyoruz.
	df['Gösterge Puanı'] = df.apply(lambda row: sabitler.yan_odeme_puani(row["Unvan"], row["Derece"]), axis=1)

	# df['Yan Ödeme'] ile aldığımız oran ile unvan bilgisini alarak sabitler.py dosyasındaki fonksiyon aracılığı TL tutarı hesaplıyoruz.
	df['Aylık Tutar'] = round(df.apply(lambda row: sabitler.aylik_katsayi(row["Yan Ödeme"], row["Unvan"]), axis=1), 2)
	
	# Aynı şekilde İKYSden çektiğimiz ek gösterge miktarını ve unvan bilgisini sabitler.py dosyasındaki fonksiyon aracılığı ile hesaplıyoruz.
	df['Ek Gös.Ay.'] = round(df.apply(lambda row: sabitler.ek_gosterge(row["Ek Gösterge"], row["Unvan"]), axis=1), 2)

	# df['Gösterge Puanı'] ile aldığımız oran ile unvan bilgisini alarak sabitler.py dosyasındaki fonksiyon aracılığı TL tutarı hesaplıyoruz. 
	df['Yan Ödeme Aylık'] = round(df.apply(lambda row: sabitler.yan_odeme(row["Gösterge Puanı"], row["Unvan"]), axis=1), 2)

	# hizmet yılı baz alınarak kıdem aylığını fonksiyon aracılığı ile hesaplıyoruz.
	# burada maalesef çok hata alıyoruz. çümkü kbs ve ikys kıdem yılları birbirini tutmuyor.
	df['Kıdem Aylık'] = round(df.apply(lambda row: sabitler.kidem_ayligi(row["Hizmet Süresi (Yıl)"], row["Unvan"]), axis=1), 2)

	# maas_verileri.xlsx içerisindeki bilgileri, sabitler.py dosyasındaki fonksiyon ile unvan, derece ve ogrenim bilgisi değerlerini göndererek çekiyoruz.
	df['Özel Hiz. Taz. Puanı'] = df.apply(lambda row: sabitler.ozel_hizmet_orani(row["Unvan"], row["Derece"], row["ogrenim"]), axis=1)

	# aynı şekilde özel hizmet tazmınatı tutarını sabitler.py dosyasındaki fonsiyona gerekli parametreleri göndererek hesaplıyoruz.	
	df['Özel Hiz.Taz.'] = round(df.apply(lambda row: sabitler.ozel_hizmet(row["Unvan"], row["Derece"], row["ogrenim"]), axis=1), 2)

	# maas_verileri.xlsx içerisindeki bilgileri, sabitler.py dosyasındaki fonksiyon ile unvan, derece ve ogrenim bilgisi değerlerini göndererek çekiyoruz.
	df['Ek Tazminat Puanı'] = df.apply(lambda row: sabitler.ek_tazminat_puani(row["Unvan"], row["Derece"], row["ogrenim"]), axis=1)

	# Ek Ödeme oranını maas_verileri.xlsx dosyasından fonksiyon ile çekiyoruz.
	df['666 KHK Oranı'] = df.apply(lambda row: sabitler.ek_odeme_666_orani(row["Unvan"], row["Derece"], row["ogrenim"]), axis=1)

	# aynı şekilde ek ödeme 666 khk tutarını sabitler.py dosyasındaki fonsiyona gerekli parametreleri göndererek hesaplıyoruz.
	df['Ek Öde.(666 KHK'] = round(df.apply(lambda row: sabitler.ek_odeme_666(row["Unvan"], row["Derece"], row["ogrenim"]), axis=1), 2)

	# Son olarak excele aktaracağımız sütunları belirliyoruz.
	df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan', 'Derece', 'Kademe', 'Yan Ödeme', 'Aylık Tutar', 'Ek Gösterge', 'Ek Gös.Ay.', 'Gösterge Puanı', 'Yan Ödeme Aylık', 'Ek Tazminat Puanı', 'Özel Hiz. Taz. Puanı', 'Özel Hiz.Taz.', '666 KHK Oranı', 'Ek Öde.(666 KHK']]

	# Listeyi TC veya Adı-Soyadına göre sıralayabilirsiniz, dikkat etmeniz gereken ise kbs_bordro ve kbs_personelde de aynı değişikliği yapmanızdır.
	#df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)
	df.sort_values(by=['Adı Soyadı'], inplace=True, ignore_index=True)

	# DataFrame içinde topladığımız ve sütunlarını belirlediğimiz verilerimizi excele xlsx formatında aktarıyoruz. freeze_panes değeri ile ilk satır ve ilk iki sütunu donduruyoruz.
	df.to_excel('./ikys/ikys_personel_verileri.xlsx', index=False, freeze_panes=(1,2))
	print('1. İKYS personel bilgileri uygun formata getirildi...')
	time.sleep(2)

if __name__ == "__main__":
	ikys_personel_verileri()
