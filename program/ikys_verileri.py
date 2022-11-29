#!/usr/bin/env python3
# Modülleri yüklemek için
# sudo python3 -m pip install -U pandas==1.3.5
# sudo python3 -m pip install -U numexpr==2.8.4
# sudo python3 -m pip install -U numpy==1.21.6

import pandas as pd
import numpy as np
from os import path
import re
import sabitler

# Yerel ayarları Türkiye standartlarına çeviriyoruz.
import locale
locale.getlocale()
locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")

def ikys_personel_veri():
	if path.exists('../rapor/ikys_yeni.ods') == False:
		df = pd.DataFrame(pd.read_excel('../ikys/Personel Rapor.ods', skiprows=2))
		df = df.dropna(how='all', axis=1)
		df = df.groupby('Kadro Tipi').get_group('Memur')
		df = df.drop_duplicates(subset=['Sicil'], ignore_index=True)
		df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan',
				'Öğrenim Durumu-Okul-Fakülte-Bölüm', 'Sendika', 'Diyanete Giriş Tarihi',
				'Ödenilecek Derece/Kademe', 'Hizmet Süresi (Ay)', 'Hizmet Süresi (Yıl)']]

		for i in df["Öğrenim Durumu-Okul-Fakülte-Bölüm"].tolist():
			ogrenimnul = re.search("Lisansüstü|Yüksek Okul|Üniversite|Lisans Tamamlama|İmam Hatip Lisesi|Lise|Doktora|Ortaokul|İlkokul|İlköğretim|Okur-Yazar", i)
			df['Öğrenim Durumu-Okul-Fakülte-Bölüm'] = df['Öğrenim Durumu-Okul-Fakülte-Bölüm'].replace([i], ogrenimnul.group(0))

		for i in df["Sınıf"].tolist():
			sinifbul = re.search("(^G|D|Y|T)", i)
			df['Sınıf'] = df['Sınıf'].replace([i], sinifbul.group(0))

		# Ödenilecek Derece/Kademe sütunundaki parantezleri siliyoruz
		df['Ödenilecek Derece/Kademe'].replace(regex=True, inplace=True, to_replace=r'[()]', value=r'')

		# Ödenilecek Derece/Kademe sütununu Derece, Kademe ve Ek Gösterge olarak üç sutüna ayırıyoruz. NaN olan değerleri
		# 0 olarak değiştiriyoruz ve tipini integer olarak belirliyoruz.
		df[['Derece', 'Kademe', 'Ek Gösterge']] = df['Ödenilecek Derece/Kademe'].str.split('-', expand=True).fillna(0).astype(int)

		# Listeyi TC ye göre sıralıyoruz.
		df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)

		# Küsuratlı sayıları virgülden sonra iki basamak içerecek şekilde formatlıyoruz. Binlik işaretini kullanmayacağız.
		#pd.set_option('display.float_format', lambda x: locale.format_string('%.2f', x, grouping=False))

		#for row in df.itertuples(index=False, name='Pandas'):
		df['Aylık Tutar'] = round(sabitler.aylik_katsayi(df.apply(lambda row: sabitler.yan_odeme_puani(row["Derece"], row["Kademe"]), axis=1)), 2)
		df['Ek Gösterge Aylığı'] = round(sabitler.ek_gosterge(df['Ek Gösterge']), 2)

		df.to_excel('../rapor/ikys_yeni.ods', index=False)
		print(df)

if __name__ == "__main__":
	ikys_personel_veri()