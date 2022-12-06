#!/usr/bin/env python3
# Modülleri yüklemek için
# sudo python3 -m pip install -U pandas==1.3.5
# sudo python3 -m pip install -U numexpr==2.8.4
# sudo python3 -m pip install -U numpy==1.21.6
import sys
sys.dont_write_bytecode = True

import pandas as pd
from os import path
import re
import sabitler

def kbs_bordro_verileri():
	df = pd.DataFrame(pd.read_excel('./kbs/BordroDokumu.xlsx', sheet_name=0, skiprows=1))
	df = df.dropna(how='all', axis=1)
	df = df[['Personel No TC.Kimlik No','Adı Soyadı','Hizmet Sın.-Ünvan','Öd.Es.D.-K. Em.Es.D.-K.',
	 		'Öd.Ekgös-Em.Ekgös','Kıdem Ay-Kıdem Yıl','Aylık Tutar','Ek Gös.Ay.','Yan Ödeme Aylık',
	 		'Kıdem Aylık', 'Özel Hiz.Taz.',	'Makam Taz.','Dil Tazminatı','Ek Öde.(666 KHK',
	 		'Sendika Aidatı']]
	#df.rename(columns={'Personel No TC.Kimlik No': 'TC Kimlik'}, inplace = True)
	#df.rename(columns={'Hizmet Sın.-Ünvan': 'Sınıf'}, inplace = True)

	# Adı Soyadı sütununu büyük harflere çeviriyoruz.
	df['Adı Soyadı'] = df['Adı Soyadı'].str.replace("i", "İ").str.upper()

	# Personel No TC.Kimlik No sütununu 'Personel No' ve 'TC Kimlik' olarak iki sutüna ayırıyoruz.
	df[['Personel No', 'TC Kimlik']] = df['Personel No TC.Kimlik No'].str.split('-', expand=True)

	# Hizmet Sın.-Ünvan sütununu Sınıf ve Unvan olarak iki sutüna ayırıyoruz.
	df['Hizmet Sın.-Ünvan'].replace(regex=True, inplace=True, to_replace=r'-Hat.', value=r'.Hat.')
	
	df[['Sınıf', 'Unvan']] = df['Hizmet Sın.-Ünvan'].str.split('-', expand=True)

	# Öd.Es.D.-K. Em.Es.D.-K. sütununu 'Derece-Kademe' ve 'Yan Ödeme' olarak iki sutüna ayırıyoruz.
	df[['Derece-Kademe', 'Yan Ödeme']] = df['Öd.Es.D.-K. Em.Es.D.-K.'].str.split(' ', expand=True)

	# Derece-Kademe sütununu 'Derece' ve 'Kademe' olarak iki sutüna ayırıyoruz.
	df[['Derece', 'Kademe']] = df['Derece-Kademe'].str.split('-', expand=True)

	# Öd.Ekgös-Em.Ekgös sütununu 'Ek Gösterge' ve 'Em-EkGösterge' olarak iki sutüna ayırıyoruz.
	df[['Ek Gösterge', 'Em-EkGösterge']] = df['Öd.Ekgös-Em.Ekgös'].str.split('-', expand=True)

	# Kıdem Ay-Kıdem Yıl sütununu 'Hizmet Süresi (Ay)' ve 'Hizmet Süresi (Yıl)' olarak iki sutüna ayırıyoruz.
	df[['Hizmet Süresi (Ay)', 'Hizmet Süresi (Yıl)']] = df['Kıdem Ay-Kıdem Yıl'].str.split('-', expand=True)

	df[['TC Kimlik', 'Derece', 'Kademe', 'Yan Ödeme', 'Ek Gösterge', 'Hizmet Süresi (Yıl)']] = df[['TC Kimlik', 'Derece', 'Kademe', 'Yan Ödeme', 'Ek Gösterge', 'Hizmet Süresi (Yıl)']].apply(pd.to_numeric).fillna(0)		

	df = df.drop_duplicates(subset=['TC Kimlik'], ignore_index=True, keep='last', inplace=False)

	df['Gösterge Puanı'] = df.apply(lambda row: sabitler.yan_odeme_puani_kbs(row['TC Kimlik']), axis=1)
	
	df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan', 'Derece', 'Kademe', 'Yan Ödeme', 'Ek Gösterge',
	 		'Gösterge Puanı', 'Hizmet Süresi (Yıl)', 'Aylık Tutar', 'Ek Gös.Ay.', 'Yan Ödeme Aylık',
	 		'Kıdem Aylık'
	 		]]

	#'Özel Hiz.Taz.',	'Makam Taz.', 'Dil Tazminatı', 'Ek Öde.(666 KHK', 'Sendika Aidatı'
	df.sort_values(by=['TC Kimlik'], inplace=True)
	df.to_excel('./rapor/kbs_bordro_verileri.ods', index=False)

if __name__ == "__main__":
	kbs_bordro_verileri()
