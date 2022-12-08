#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import pandas as pd
import numpy as np
from os import path
import re
import sabitler


def ikys_personel_verileri():
	dfs = pd.read_html('./ikys/Personel Rapor.xls')
	dfs[0].to_excel('./ikys/Personel Rapor.ods')
	df = pd.DataFrame(pd.read_excel('./ikys/Personel Rapor.ods'))
	df = df.dropna(how='all', axis=1)
	df = df.groupby('Kadro Tipi').get_group('Memur')
	df = df.drop_duplicates(subset=['Sicil'], ignore_index=True)
	df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan',
			'Öğrenim Durumu-Okul-Fakülte-Bölüm', 'Sendika', 'Diyanete Giriş Tarihi',
			'Ödenilecek Derece/Kademe', 'Hizmet Süresi (Ay)', 'Hizmet Süresi (Yıl)']]

	for i in df["Öğrenim Durumu-Okul-Fakülte-Bölüm"].tolist():
		ogrenimnul = re.search("Doktora|Lisansüstü|Üniversite|Lisans Tamamlama|Yüksek Okul|İmam Hatip Lisesi|Lise|Ortaokul|İlköğretim|İlkokul|Okur-Yazar", i)
		df['Öğrenim Durumu-Okul-Fakülte-Bölüm'] = df['Öğrenim Durumu-Okul-Fakülte-Bölüm'].replace([i], ogrenimnul.group(0))
		
	#for i in df["Sınıf"].tolist():
	##	sinifbul = re.search("(^G|D|Y|T)", i)
	#	df['Sınıf'] = df['Sınıf'].replace([i], sinifbul.group(0))

	#Sınıf sütunundaki büyük harfler hariç herşeyi siliyoruz ve geriye sadece GİH,DH,TH,YH ibareleri kalıyor
	df['Sınıf'].replace(regex=True, inplace=True, to_replace=r'([a-z]|\s|ı|ü|ş|ç|ğ|ö|)', value=r'')

	#Unvan sütunundaki ikys sisteminde bulunan unvanları kbs sistemindekine uyarlıyoruz.
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(.*Yar.*)', value=r'İl Müft.Yr')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(İlçe.*)', value=r'İlçe Müft.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Şube.*)', value=r'Şube Md.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Veri.*)', value=r'V.H.K.İ.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Vaiz.*)', value=r'Vaiz')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Cez.*)', value=r'Cezv.Vaizi')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Din.*)', value=r'Din Hz.Uzm')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(İma.*)', value=r'İmam.Hat.')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Kuran.*)', value=r'Kur.Krs.Öğ')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Müez.*)', value=r'Müez.Kayyı')
	df['Unvan'].replace(regex=True, inplace=True, to_replace=r'^(Uzman.İmam.*)', value=r'Uz.İm.Hat')

	# Ödenilecek Derece/Kademe sütunundaki parantezleri siliyoruz
	df['Ödenilecek Derece/Kademe'].replace(regex=True, inplace=True, to_replace=r'[()]', value=r'')

	# Ödenilecek Derece/Kademe sütununu Derece, Kademe ve Ek Gösterge olarak üç sutüna ayırıyoruz. NaN olan değerleri
	# 0 olarak değiştiriyoruz ve tipini integer olarak belirliyoruz.
	df[['Derece', 'Kademe', 'Ek Gösterge']] = df['Ödenilecek Derece/Kademe'].str.split('-', expand=True).fillna(0).astype(int)

	df['Yan Ödeme'] = df.apply(lambda row: sabitler.gosterge_puani(row["Derece"], row["Kademe"]), axis=1)

	df['Gösterge Puanı'] = df.apply(lambda row: sabitler.yan_odeme_puani(row["Unvan"], row["Derece"]), axis=1)

	df['Aylık Tutar'] = round(df.apply(lambda row: sabitler.aylik_katsayi(row["Yan Ödeme"], row["Unvan"]), axis=1), 2)
	
	df['Ek Gös.Ay.'] = round(df.apply(lambda row: sabitler.ek_gosterge(row["Ek Gösterge"], row["Unvan"]), axis=1), 2)

	df['Yan Ödeme Aylık'] = round(df.apply(lambda row: sabitler.yan_odeme(row["Gösterge Puanı"], row["Unvan"]), axis=1), 2)

	df['Kıdem Aylık'] = round(df.apply(lambda row: sabitler.kidem_ayligi(row["Hizmet Süresi (Yıl)"], row["Unvan"]), axis=1), 2)

	df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan', 'Derece', 'Kademe', 'Yan Ödeme', 'Ek Gösterge', 'Gösterge Puanı',
			 'Hizmet Süresi (Yıl)', 'Aylık Tutar', 'Ek Gös.Ay.', 'Yan Ödeme Aylık', 'Kıdem Aylık'
	 		]]

	# Listeyi TC ye göre sıralıyoruz.
	df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)

	# Küsuratlı sayıları virgülden sonra iki basamak içerecek şekilde formatlıyoruz. Binlik işaretini kullanmayacağız.
	#pd.set_option('display.float_format', lambda x: locale.format_string('%.2f', x, grouping=False))
	#for row in df.itertuples(index=False, name='Pandas'):

	df.to_excel('./rapor/ikys_personel_verileri.ods', index=False)
	#print(df['Unvan'])

if __name__ == "__main__":
	ikys_personel_verileri()

