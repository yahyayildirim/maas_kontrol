#!/usr/bin/env python3

import pandas as pd
import re
import sabitler

df = pd.DataFrame(pd.read_excel('Personel Rapor.ods', skiprows=2))
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
	sinifbul = re.search("(^[G|D|Y|T])", i)
	df['Sınıf'] = df['Sınıf'].replace([i], sinifbul.group(0))

# Ödenilecek Derece/Kademe sütunundaki parantezleri siliyoruz
df['Ödenilecek Derece/Kademe'].replace(regex=True, inplace=True, to_replace=r'[()]', value=r'')

# Ödenilecek Derece/Kademe sütununu Derece, Kademe ve Ek Gösterge olarak üç sutüna ayırıyoruz. NaN olan değerleri
# 0 olarak değiştiriyoruz ve tipini integer olarak belirliyoruz.
df[['Derece', 'Kademe', 'Ek Gösterge']] = df['Ödenilecek Derece/Kademe'].str.split('-', expand=True).fillna(0).astype(int)

df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan', 'Derece', 'Kademe', 'Ek Gösterge', 'Hizmet Süresi (Yıl)']]


print(df)
#df.to_excel('deneme.ods', index=False)




# df = pd.DataFrame(pd.read_excel('BordroDokumu.xlsx', sheet_name=0, skiprows=1))
# df = df.dropna(how='all', axis=1)
# df = df[['Personel No TC.Kimlik No','Adı Soyadı','Hizmet Sın.-Ünvan','Öd.Es.D.-K. Em.Es.D.-K.',
#  				'Öd.Ekgös-Em.Ekgös','Kıdem Ay-Kıdem Yıl','Aylık Tutar','Ek Gös.Ay.','Yan Ödeme Aylık',
#  				'Kıdem Aylık', 'Özel Hiz.Taz.',	'Makam Taz.','Dil Tazminatı','Ek Öde.(666 KHK',
#  				'Sendika Aidatı']]
# #df.rename(columns={'Personel No TC.Kimlik No': 'TC Kimlik'}, inplace = True)
# #df.rename(columns={'Hizmet Sın.-Ünvan': 'Sınıf'}, inplace = True)
# df['Adı Soyadı'] = df['Adı Soyadı'].str.upper()

# cols = ['Personel No', 'TC Kimlik']
# df[cols] = df['Personel No TC.Kimlik No'].str.split('-', expand=True)

# cols = ['Sınıf', 'Unvan']
# df[cols] = df['Hizmet Sın.-Ünvan'].str.split('-', expand=True)

# cols = ['Derece-Kademe', 'Yan Ödeme']
# df[cols] = df['Öd.Es.D.-K. Em.Es.D.-K.'].str.split(' ', expand=True)

# cols = ['Öd-EkGösterge', 'Em-EkGösterge']
# df[cols] = df['Öd.Ekgös-Em.Ekgös'].str.split('-', expand=True)

# cols = ['Kıdem Ay', 'Kıdem Yıl']
# df[cols] = df['Kıdem Ay-Kıdem Yıl'].str.split('-', expand=True)

# df = df[['Personel No', 'TC Kimlik', 'Adı Soyadı','Sınıf', 'Unvan', 'Derece-Kademe', 'Yan Ödeme',
#  		'Öd-EkGösterge', 'Em-EkGösterge','Kıdem Ay', 'Kıdem Yıl','Aylık Tutar','Ek Gös.Ay.','Yan Ödeme Aylık',
#  		'Kıdem Aylık', 'Özel Hiz.Taz.',	'Makam Taz.','Dil Tazminatı','Ek Öde.(666 KHK',
#  		'Sendika Aidatı']]

# df.to_excel('deneme.ods')
# #print(df[['Sınıf', 'Unvan']])
# #cols = ['Personel No', 'TC Kimlik']
# #df[cols] = df['Personel No TC.Kimlik No'].str.split('-', expand=True)