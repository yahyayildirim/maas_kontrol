#!/usr/bin/env python3
# Modülleri yüklemek için
# sudo python3 -m pip install -U pandas==1.3.5
# sudo python3 -m pip install -U numexpr==2.8.4
# sudo python3 -m pip install -U numpy==1.21.6

import pandas as pd
from os import path
import re

# Yerel ayarları Türkiye standartlarına çeviriyoruz.
import locale
locale.getlocale()
locale.setlocale(locale.LC_ALL, "tr_TR.UTF-8")

def kbs_personel_veri():
	if path.exists('../rapor/kbs_yeni.ods') == False:
		df = pd.DataFrame(pd.read_excel('../kbs/BordroDokumu.xlsx', sheet_name=0, skiprows=1))
		df = df.dropna(how='all', axis=1)
		df = df[['Personel No TC.Kimlik No','Adı Soyadı','Hizmet Sın.-Ünvan','Öd.Es.D.-K. Em.Es.D.-K.',
		 		'Öd.Ekgös-Em.Ekgös','Kıdem Ay-Kıdem Yıl','Aylık Tutar','Ek Gös.Ay.','Yan Ödeme Aylık',
		 		'Kıdem Aylık', 'Özel Hiz.Taz.',	'Makam Taz.','Dil Tazminatı','Ek Öde.(666 KHK',
		 		'Sendika Aidatı']]
		#df.rename(columns={'Personel No TC.Kimlik No': 'TC Kimlik'}, inplace = True)
		#df.rename(columns={'Hizmet Sın.-Ünvan': 'Sınıf'}, inplace = True)
		df['Adı Soyadı'] = df['Adı Soyadı'].str.upper()

		cols = ['Personel No', 'TC Kimlik']
		df[cols] = df['Personel No TC.Kimlik No'].str.split('-', expand=True)

		# Ödenilecek Derece/Kademe sütunundaki parantezleri siliyoruz
		df['Hizmet Sın.-Ünvan'].replace(regex=True, inplace=True, to_replace=r'-Hat.', value=r'.Hat.')

		# Ödenilecek Derece/Kademe sütununu Derece, Kademe ve Ek Gösterge olarak üç sutüna ayırıyoruz. NaN olan değerleri
		# 0 olarak değiştiriyoruz ve tipini integer olarak belirliyoruz.
		df[['Sınıf', 'Unvan']] = df['Hizmet Sın.-Ünvan'].str.split('-', expand=True)

		for i in df["Sınıf"].tolist():
			sinifbul = re.search("(^G|D|Y|T)", i)
			df['Sınıf'] = df['Sınıf'].replace([i], sinifbul.group(0))

		cols = ['Derece-Kademe', 'Yan Ödeme']
		df[cols] = df['Öd.Es.D.-K. Em.Es.D.-K.'].str.split(' ', expand=True)

		cols = ['Ek Gösterge', 'Em-EkGösterge']
		df[cols] = df['Öd.Ekgös-Em.Ekgös'].str.split('-', expand=True).fillna(0)

		cols = ['Hizmet Süresi (Ay)', 'Hizmet Süresi (Yıl)']
		df[cols] = df['Kıdem Ay-Kıdem Yıl'].str.split('-', expand=True)

		cols = ['Derece', 'Kademe']
		df[cols] = df['Derece-Kademe'].str.split('-', expand=True)

		df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan', 'Derece', 'Kademe', 'Yan Ödeme',
		 		'Ek Gösterge', 'Hizmet Süresi (Yıl)', 'Aylık Tutar', 'Ek Gös.Ay.', 'Yan Ödeme Aylık',
		 		'Kıdem Aylık', 'Özel Hiz.Taz.',	'Makam Taz.', 'Dil Tazminatı', 'Ek Öde.(666 KHK', 'Sendika Aidatı'
		 		]]

		df.sort_values(by=['Adı Soyadı'], inplace=True)
		df[['TC Kimlik', 'Derece', 'Kademe', 'Yan Ödeme', 'Ek Gösterge', 'Hizmet Süresi (Yıl)']] = df[['TC Kimlik', 'Derece', 'Kademe', 'Yan Ödeme', 'Ek Gösterge', 'Hizmet Süresi (Yıl)']].apply(pd.to_numeric)
		df.to_excel('../rapor/kbs_yeni.ods', index=False)

if __name__ == "__main__":
	kbs_personel_veri()
