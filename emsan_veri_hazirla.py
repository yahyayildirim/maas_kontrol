#!/usr/bin/env python3

import os
import pandas as pd
from glob import glob
from datetime import datetime

import sys
sys.dont_write_bytecode = True

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings(action='ignore', category=UserWarning, module='openpyxl')

ana_dizin = os.path.dirname(__file__) + '/'
bu_yil = datetime.now().year
bu_ay = datetime.now().strftime("%B")

df_1 = pd.DataFrame(pd.read_excel(f'{ana_dizin}maas_verileri.xlsx'.format(ana_dizin), sheet_name=1))

def emsan_veri():
	#İKYSden indirdiğimiz dosya, html formatında olduğu için önce read_html metodu ile açıp, xlsx formatında tekrar kaydediyoruz.
	bu_dizin = os.path.dirname(__file__) + '/kbs/'
	dosya =glob(bu_dizin + "BordroDokumu*.xlsx")
	if dosya:
		df = pd.read_excel(''.join(dosya), sheet_name=1, skiprows=6)
		df.dropna(axis=0, thresh=5, inplace=True)
		df.dropna(axis=1, thresh=2, inplace=True)
		df.drop(df.tail(2).index,inplace=True)		
	else:
		print("/kbs klasöründe BordroDokumu dosyası yok. Lütfen tekrar deneyin.")
		sys.exit()
		
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
	#df.to_excel('Bordro_Dokumu_Temiz.xlsx', index=False, freeze_panes=(1,0))
	#df.columns.duplicated(keep='first', inplace=True)
	df = df.loc[:, ~df.columns[::-1].duplicated()[::-1]]

	df[['Personel No', 'TC.Kimlik No']] = df['Personel No TC.Kimlik No'].str.split('-', expand=True)
	df[['Sicil No', 'Em. Sic. No']] = df['Sicil No-Em. Sic. No'].str.rsplit('-', expand=True, n=1)
	#df['TC.Kimlik No'] = df['TC.Kimlik No'].str.replace("<0xfeff>", "", regex=True)

	# Split into temporary DataFrame
	#split_df = df['Sicil No-Em. Sic. No'].str.split('-', expand=True)

	# Assign columns based on the actual number of split columns
	#if len(split_df.columns) == 2:
	#	df[['Sicil No', 'Em. Sic. No']] = split_df
	#else:
		# Handle the case where there might be more than 2 columns
		# You may need to adjust this based on your specific data and requirements
	#	df[['Sicil No', 'Em. Sic. No']] = split_df.iloc[:, :2]  # Take the first two columns

	# Öd.Es.D.-K. Em.Es.D.-K. sütununu 'Derece-Kademe' ve 'Yan Ödeme' olarak iki sutüna ayırıyoruz.
	df[['Derece-Kademe', 'Yan Ödeme']] = df['Öd.Es.D.-K. Em.Es.D.-K.'].str.split(' ', n=1, expand=True)

	#df[['YOK', 'Yan_Odeme_Puan']] = df['Yan Ödeme'].str.split(' ', expand=True)
	#df['OD_GUN_SAY'] = df['Yan_Odeme_Puan'].apply(lambda x: int(x) * 0.760871).round(2)

	# Derece-Kademe sütununu 'Derece' ve 'Kademe' olarak iki sutüna ayırıyoruz.
	df[['Derece', 'Kademe']] = df['Derece-Kademe'].str.split('-', expand=True).apply(pd.to_numeric).fillna(0)

	df['D.K.'] = " "

	df['TERFI TAR.'] = "0000"
	df['GHB'] = 0
	df['İPC'] = 0
	df['İNT. TAH.'] = 0

	#taban_aylik = 11909.08 / 30
	taban_aylik = (df_1['taban_aylik_katsayi'].iloc[-1] * 1000) / 30

	#df['PEK_OD_GUN_SAY'] = df['Taban Aylık'].apply(lambda x: int(float(x) / taban_aylik))
	df['PEK_OD_GUN_SAY'] = df['Taban Aylık'].apply(lambda x: int(float(x) / taban_aylik))

	df['GB_TAR'] = " "
	df['GB_SEB'] = 0
	df['GA_TAR'] = " "
	df['GA_SEB'] = 0

	df[['Ek Gösterge', 'Em-EkGösterge']] = df['Öd.Ekgös-Em.Ekgös'].str.split('-', expand=True)
	df = df.assign(**{'Adı': df['Adı Soyadı'].str.split().str[0:-1].str.join(' '),'Soyadı': df['Adı Soyadı'].str.split().str[-1]})
	df[['Hizmet Süresi (Ay)', 'Hizmet Süresi (Yıl)']] = df['Kıdem Ay-Kıdem Yıl'].str.split('-', expand=True)

	# Sayısal değerlere çevirmek istediğimiz sütunlar
	columns_to_convert = ['TC.Kimlik No', 'Derece', 'Kademe', 'Ek Gösterge', 'Em-EkGösterge', 'Hizmet Süresi (Yıl)', 'Hizmet Süresi (Ay)', 
	'Sağ.Sig.Pir(K)', 'Özel Hiz.Taz.', 'Aylık Tutar', 'Taban Aylık', 'Ek Gös.Ay.', 'Kıdem Aylık', 'Em.Kes. Kişi', 'Artış %100', 'Em. Kes. Dev.', 'Sağ.Sig.Pir(D)']

	# Bu sütunları sayısal değerlere dönüştürme
	df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')
	df['Ek Gösterge'] = df['Ek Gösterge'].fillna(0).astype(int)
	df['Em-EkGösterge'] = df['Em-EkGösterge'].fillna(0).astype(int)
	#df['Artış %100'] = df['Artış %100'].astype(str).apply(lambda x: if x.endswith(0) x.replace('.0',''))
	df['Artış %100'] = df['Artış %100'].astype(str).apply(lambda x: x.replace('.0', '') if x.endswith('.0') else x)

	df["Em.Es.K."] = df['Öd.Es.D.-K. Em.Es.D.-K.'].str.split('-').str[-1]
	df["em-kademe"] = df["Em.Es.K."].str.split(' ').str[0]

	df["Em.Es.D."] = df['Öd.Es.D.-K. Em.Es.D.-K.'].str.split('-').str[1]
	df["em-derece"] = df["Em.Es.D."].str.split(' ').str[-1]
	df['em-derece'] = df['em-derece'].str.slice(start=3).astype(int)
	df['em-derece'] = df['em-derece'].apply(lambda x: x if x < 13 else int(str(x)[-1]))

	df['asgari_ucret_pek_tutari'] = (20002.5 / 30) * df['PEK_OD_GUN_SAY']

	df['Hizmet Süresi'] = df['Hizmet Süresi (Yıl)'].apply(lambda x: f"{x:02d}") + df['Hizmet Süresi (Ay)'].apply(lambda x: f"{x:02d}") + "00"
	df['AYLIK'] = df[['Aylık Tutar', 'Taban Aylık', 'Ek Gös.Ay.', 'Kıdem Aylık']].sum(axis=1).round(2)
	df['PEK_GENEL'] = df[['AYLIK', 'Özel Hiz.Taz.']].sum(axis=1).round(2)
	#df['PEK_FARK'] = df.apply(lambda row: round(asgari_ucret_pek_tutari - row['PEK_GENEL'],2) if row['PEK_GENEL'] < 20002.5 else int(0), axis=1)
	df['PEK_FARK'] = df.apply(lambda row: round(row['asgari_ucret_pek_tutari'] - row['PEK_GENEL'], 2) if row['PEK_GENEL'] < row['asgari_ucret_pek_tutari'] else int(0), axis=1)
	df['PEK_GENEL'] = df[['AYLIK', 'Özel Hiz.Taz.', 'PEK_FARK']].sum(axis=1).round(2)

	#df['Özel Hiz.Taz.'] = df['Özel Hiz.Taz.'].astype(str).apply(lambda x: x.replace('.0', '') if x.endswith('.0') else x)
	#df['AYLIK'] = df['AYLIK'].astype(str).apply(lambda x: x.replace('.0', '') if x.endswith('.0') else x)
	#df['PEK_FARK'] = df['PEK_FARK'].astype(str).apply(lambda x: x.replace('.0', '') if x.endswith('.0') else x)
	#df['PEK_GENEL'] = df['PEK_GENEL'].astype(str).apply(lambda x: x.replace('.0', '') if x.endswith('.0') else x)
	#df['Sağ.Sig.Pir(D)'] = df['Sağ.Sig.Pir(D)'].astype(str).apply(lambda x: x.replace('.0', '') if x.endswith('.0') else x)

	# eğer personel 5510 sayılı kanuna tabi ise Sağ.Sig.Pir(K) sütünü 0'dan büyüktür.

	df_5510 = df[df['Sağ.Sig.Pir(K)'] > 0]

	df_5434 = df[df['Sağ.Sig.Pir(K)'] == 0]

	df_ayliksiz_izin = df_5434[df_5434['Em.Kes. Kişi'] == 0]

	df_5510_kist = df_5510[df_5510['PEK_OD_GUN_SAY'] < 29]
	df_5510 = df_5510[df_5510['PEK_OD_GUN_SAY'] >= 29]
	df_5434 = df_5434[df_5434['Em.Kes. Kişi'] > 0]

	df_5510_kist = df_5510_kist[['TC.Kimlik No', 'Em. Sic. No', 'Adı', 'Soyadı', 'D.K.', 'GB_TAR', 'GB_SEB', 'GA_TAR', 'GA_SEB','Derece', 'Kademe', 'Em-EkGösterge', 'Hizmet Süresi',
	'PEK_OD_GUN_SAY', 'Özel Hiz.Taz.', 'AYLIK', 'PEK_FARK', 'PEK_GENEL', 'Em.Kes. Kişi', 'Sağ.Sig.Pir(K)', 'Em.Kes. Dev.', 'Sağ.Sig.Pir(D)']]

	df_5510 = df_5510[['TC.Kimlik No', 'Em. Sic. No', 'Adı', 'Soyadı', 'D.K.', 'GB_TAR', 'GB_SEB', 'GA_TAR', 'GA_SEB','Derece', 'Kademe', 'Em-EkGösterge', 'Hizmet Süresi',
	'PEK_OD_GUN_SAY', 'Özel Hiz.Taz.', 'AYLIK', 'PEK_FARK', 'PEK_GENEL', 'Em.Kes. Kişi', 'Sağ.Sig.Pir(K)', 'Em.Kes. Dev.', 'Sağ.Sig.Pir(D)']]

	df_5434 = df_5434[['TC.Kimlik No', 'Em. Sic. No', 'Adı', 'Soyadı', 'D.K.', 'TERFI TAR.', 'em-derece', 'em-kademe', 'Em-EkGösterge', 'Derece', 'Kademe', 'Ek Gösterge', 'Hizmet Süresi',
	'Em.Kes. Kişi', 'Artış %100', 'Em. Kes. Dev.', 'Artış %100', 'Sağ.Sig.Pir(D)', 'GHB', 'İPC', 'İNT. TAH.',]]

	df_ayliksiz_izin = df_ayliksiz_izin[['TC.Kimlik No', 'Em. Sic. No', 'Adı', 'Soyadı', 'D.K.', 'TERFI TAR.', 'em-derece', 'em-kademe', 'Em-EkGösterge', 'Derece', 'Kademe', 'Ek Gösterge', 'Hizmet Süresi',
	'Em.Kes. Kişi', 'Artış %100', 'Em. Kes. Dev.', 'Artış %100', 'Sağ.Sig.Pir(D)', 'GHB', 'İPC', 'İNT. TAH.',]]

#	if df_ayliksiz_izin.empty == False:
#		df_ayliksiz_izin.reset_index(drop=True, inplace=True)
#		df_ayliksiz_izin.sort_values(by=['TC.Kimlik No'], inplace=True, ignore_index=True)
#		df_ayliksiz_izin.to_csv(f'{ana_dizin}/rapor/' + str(bu_yil) + '/' + str(bu_ay) + f'/5510_ve_5434(AyliksizIzin)_{bu_yil}-{bu_ay}.txt', index=False, header=False, sep=";", lineterminator='\r\n')

	if df_5434.empty == False:
		df_5434.reset_index(drop=True, inplace=True)
		df_5434.sort_values(by=['TC.Kimlik No'], inplace=True, ignore_index=True)
		emsan_5434 = f'{ana_dizin}/rapor/' + str(bu_yil) + '/' + str(bu_ay) + f'/5434Tabi_{bu_yil}-{bu_ay}_Emsan.txt'
		df_5434.to_csv(emsan_5434, index=False, header=False, sep=";", lineterminator='\r\n')
		#df_5434.to_csv(f'5434Tabi_{bu_yil}-{bu_ay}.txt', index=False, header=False, sep=";", lineterminator='\r\n') # eğer satırın sonuna ; konmak istenirse \r den önce ; eklenir.
		# Dosyaya iki yeni satır eklemek için mevcut dosyayı aç
		with open(emsan_5434, 'a') as dosya:
			dosya.write('/\r\n')
			dosya.write('1;1;1;1;1;1;1;0\r\n')

	if df_5510.empty == False:
		df_5510.reset_index(drop=True, inplace=True)
		df_5510.sort_values(by=['TC.Kimlik No'], inplace=True, ignore_index=True)
		emsan_5510 = f'{ana_dizin}/rapor/' + str(bu_yil) + '/' + str(bu_ay) + f'/5510Tabi_{bu_yil}-{bu_ay}_Emsan.txt'
		df_5510.to_csv(emsan_5510, index=False, header=False, sep=";", lineterminator='\r\n')
		# Dosyaya iki yeni satır eklemek için mevcut dosyayı aç
		with open(emsan_5510, 'a') as dosya:
			dosya.write('/\r\n')
			dosya.write('1;1;1;0\r\n')

#	if df_5510_kist.empty == False:
#		df_5510_kist.reset_index(drop=True, inplace=True)
#		df_5510_kist.sort_values(by=['TC.Kimlik No'], inplace=True, ignore_index=True)
#		emsan_5510_kist = f'{ana_dizin}/rapor/' + str(bu_yil) + '/' + str(bu_ay) + f'/5510(KistTerfi)_{bu_yil}-{bu_ay}.txt'
#		df_5510_kist.to_csv(emsan_5510_kist, index=False, header=False, sep=";", lineterminator='\r\n')
#		# Dosyaya iki yeni satır eklemek için mevcut dosyayı aç
#		with open(emsan_5510_kist, 'a') as dosya:
#			dosya.write('/\r\n')
#			dosya.write('1;1;1;0\r\n')

if __name__ == '__main__':
	emsan_veri()
