#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

import re
import time
import sabitler
import pandas as pd
from pathlib import Path
from glob import glob
from datetime import datetime

def kbs_temiz_veri():
	#İKYSden indirdiğimiz dosya, html formatında olduğu için önce read_html metodu ile açıp, xlsx formatında tekrar kaydediyoruz.
	bu_dizin = Path.cwd() / "kbs"
	kbs_raporlar = list(Path(bu_dizin).glob("BordroDokumu*.xlsx"))
	df = pd.DataFrame()

	for rapor in kbs_raporlar:
		dfs = pd.read_excel(rapor, sheet_name=1, skiprows=6)
		df = df.append(dfs, ignore_index=True)
		df.dropna(axis=0, thresh=5, inplace=True)
		df.dropna(axis=1, thresh=2, inplace=True)
		df.drop(df.tail(2).index,inplace=True)		

	say = 0
	df_list = []
	for c in range(len(df.columns)):
		col = df.columns[say].split('\n')
		#print(col)
		sutun = []
		for cl in col:
			sutun.append(cl.strip())
		#print(len(df.columns[c]))
		if len(df.columns[c]) < 15:
			df_say = df[df.columns[c]]
		else:
			df_say = df[df.columns[c]].str.split('\n', expand=True)
		df_list.append(pd.DataFrame(df_say.values, columns=sutun))
		say = say + 1
	df = pd.concat(df_list, axis=1)
	df.to_excel('./kbs/Bordro_Dokumu_Temiz.xlsx', index=False)
	print('%10')

def kbs_bordro_verileri():
	dosya = glob('./kbs/Bordro_Dokumu*', recursive=False)
	data = [pd.read_excel(f) for f in dosya]
	df = pd.DataFrame(data[0])

	#df = df.dropna(how='all', axis=1)
	if 'Ek Tazminat' in df.columns:
		df['Ek Tazminat'] = df['Ek Tazminat']
	else:
		df['Ek Tazminat'] = 0

	df = df[['Personel No TC.Kimlik No','Adı Soyadı','Hizmet Sın.-Ünvan','Öd.Es.D.-K. Em.Es.D.-K.',
	 		'Öd.Ekgös-Em.Ekgös','Kıdem Ay-Kıdem Yıl','Aylık Tutar','Ek Gös.Ay.','Yan Ödeme Aylık',
	 		'Kıdem Aylık', 'Özel Hiz.Taz.',	'Makam Taz.','Dil Tazminatı','Ek Öde.(666 KHK', 'Ek Tazminat',
	 		'Sendika Aidatı', 'Net Ödenen']]
	#df.rename(columns={'Personel No TC.Kimlik No': 'TC Kimlik'}, inplace = True)
	#df.rename(columns={'Hizmet Sın.-Ünvan': 'Sınıf'}, inplace = True)

	# Adı Soyadı sütununu büyük harflere çeviriyoruz.
	df['Adı Soyadı'] = df['Adı Soyadı'].str.replace('i', 'İ').str.upper()

	# Personel No TC.Kimlik No sütununu 'Personel No' ve 'TC Kimlik' olarak iki sutüna ayırıyoruz.
	df[['Personel No', 'TC Kimlik']] = df['Personel No TC.Kimlik No'].str.split('-', expand=True)

	# Hizmet Sın.-Ünvan sütununu Sınıf ve Unvan olarak iki sutüna ayırıyoruz.
	#df['Hizmet Sın.-Ünvan'].replace(regex=True, inplace=True, to_replace=r'-Hat.', value=r'.Hat.')
	
	df[['Sınıf', 'Unvan']] = df['Hizmet Sın.-Ünvan'].str.split('-', n=1, expand=True)

	# Öd.Es.D.-K. Em.Es.D.-K. sütununu 'Derece-Kademe' ve 'Yan Ödeme' olarak iki sutüna ayırıyoruz.
	df[['Derece-Kademe', 'Yan Ödeme']] = df['Öd.Es.D.-K. Em.Es.D.-K.'].str.split(' ', n=1, expand=True)

	# Derece-Kademe sütununu 'Derece' ve 'Kademe' olarak iki sutüna ayırıyoruz.
	df[['Derece', 'Kademe']] = df['Derece-Kademe'].str.split('-', expand=True).apply(pd.to_numeric).fillna(0)

	# derece ve kademeyi alarak gösterge puanını maas_verileri.xlsx dosyasından çekiyoruz.
	df['Yan Ödeme'] = df.apply(lambda row: sabitler.gosterge_puani(row["Derece"], row["Kademe"]), axis=1)

	# Öd.Ekgös-Em.Ekgös sütununu 'Ek Gösterge' ve 'Em-EkGösterge' olarak iki sutüna ayırıyoruz.
	df[['Ek Gösterge', 'Em-EkGösterge']] = df['Öd.Ekgös-Em.Ekgös'].str.split('-', expand=True)

	# Kıdem Ay-Kıdem Yıl sütununu 'Hizmet Süresi (Ay)' ve 'Hizmet Süresi (Yıl)' olarak iki sutüna ayırıyoruz.
	df[['Hizmet Süresi (Ay)', 'Hizmet Süresi (Yıl)']] = df['Kıdem Ay-Kıdem Yıl'].str.split('-', expand=True)

	df[['TC Kimlik', 'Derece', 'Kademe', 'Yan Ödeme', 'Ek Gösterge', 'Hizmet Süresi (Yıl)']] = df[['TC Kimlik', 'Derece', 'Kademe', 'Yan Ödeme', 'Ek Gösterge', 'Hizmet Süresi (Yıl)']].apply(pd.to_numeric).fillna(0)

	#df = df.drop_duplicates(subset=['TC Kimlik'], ignore_index=True, keep=False, inplace=False)
	df = df.sort_values('Net Ödenen', ascending=False).drop_duplicates('TC Kimlik').sort_index()
	#df = df.groupby('TC Kimlik').agg('max').reset_index()

	#df['Gösterge Puanı'] = df.apply(lambda row: sabitler.yan_odeme_puani_kbs(row['TC Kimlik']), axis=1)
	df['Gösterge Puanı'] = round(df.apply(lambda row: sabitler.tutardan_yan_odeme_puani_bul(row['Yan Ödeme Aylık']), axis=1))

	df['Ek Tazminat Puanı'] = round(df.apply(lambda row: sabitler.tutardan_ek_tazminat_puani_bul(row['Ek Tazminat']), axis=1))

	df['Özel Hiz. Taz. Puanı'] = round(df.apply(lambda row: sabitler.tutardan_ozel_hizmet_orani_bul(row['Özel Hiz.Taz.']), axis=1))

	df['666 KHK Oranı'] = round(df.apply(lambda row: sabitler.tutardan_666_orani_bul(row['Ek Öde.(666 KHK']), axis=1))


	# df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan', 'Derece', 'Kademe', 'Yan Ödeme', 'Aylık Tutar', 'Ek Gösterge',
	#  		'Gösterge Puanı', 'Hizmet Süresi (Yıl)', 'Ek Gös.Ay.', 'Yan Ödeme Aylık',
	#  		'Kıdem Aylık', 'Özel Hiz.Taz.', 'Ek Öde.(666 KHK'
	#  		]]
	df = df[['TC Kimlik', 'Adı Soyadı', 'Sınıf', 'Unvan', 'Derece', 'Kademe', 'Yan Ödeme', 'Aylık Tutar',
	'Ek Gösterge', 'Ek Gös.Ay.', 'Gösterge Puanı', 'Yan Ödeme Aylık', 'Ek Tazminat Puanı', 'Özel Hiz. Taz. Puanı',
	'Özel Hiz.Taz.', '666 KHK Oranı', 'Ek Öde.(666 KHK']].fillna(0)

	# Listeyi TC veya Adı-Soyadına göre sıralayabilirsiniz, dikkat etmeniz gereken ise ikys_personel ve kbs_personelde de aynı değişikliği yapmanızdır.
	#df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)
	df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)

	# DataFrame içinde topladığımız ve sütunlarını belirlediğimiz verilerimizi excele xlsx formatında aktarıyoruz. freeze_panes değeri ile ilk satır ve ilk iki sütunu donduruyoruz.
	df.to_excel('./kbs/kbs_bordro_verileri.xlsx', index=False, freeze_panes=(1,2))
	print('%20')

if __name__ == '__main__':
	kbs_temiz_veri()
	kbs_bordro_verileri()
