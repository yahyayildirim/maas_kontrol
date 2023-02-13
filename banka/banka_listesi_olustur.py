#!/usr/bin/env python3

import pandas as pd
import natsort
import glob
from datetime import datetime
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

# Taslak Excel Dosyamız
excel_dosyasi = openpyxl.load_workbook('OrnekMaasOdemeDosyasi.xlsx')

# Excel dosyamızda bulunan sayfa adımız
excel_sayfasi = excel_dosyasi['Sheet1']

bugun = datetime.today()
tarih = datetime.strftime(bugun, '%d%m%Y_%H%M%S')

def bankaListesi():
	#İKYSden indirdiğimiz dosya, html formatında olduğu için önce read_html metodu ile açıp, xlsx formatında tekrar kaydediyoruz.
	kbs_raporlar = glob.glob('*BankaListe*')
	sutun_adi = ['SIRA NO', 'TC KIMLIK NO', 'ADI SOYADI', 'UNVANI', 'BANKA HESAP NO', 'IBAN NO', 'MAAŞ TUTARI']
	df_list = []
	for rapor in natsort.os_sorted(kbs_raporlar):
		if '4BKKRaporlar_BankaListesi' in rapor:
			dfs = pd.read_excel(rapor, skiprows=1)
			#dfs.dropna(axis=0, how='all', inplace=True)
			dfs.dropna(axis=0, thresh=6, inplace=True)
			dfs.dropna(axis=1, how='all', inplace=True)	
			dfs.dropna(axis=1, thresh=2, inplace=True)		
			dfs.drop(dfs.head(4).index, inplace=True)
			dfs.dropna(axis=1, how='all', inplace=True)
			df = pd.DataFrame(dfs.values, columns=sutun_adi)
			df['MAAŞ TUTARI'] = df['MAAŞ TUTARI'].str.replace(".", "", regex=False)
			df['MAAŞ TUTARI'] = df['MAAŞ TUTARI'].str.replace(",", ".", regex=False).astype(float)
			#df[['SIRA NO', 'TC KIMLIK NO', 'BANKA HESAP NO']] = df[['SIRA NO', 'TC KIMLIK NO', 'BANKA HESAP NO']].apply(pd.to_numeric)
			df_list.append(df)

		elif 'MemurRaporlar_BankaListesi' in rapor:
			dfs = pd.read_excel(rapor, skiprows=1)
			dfs.dropna(axis=0, how='all', inplace=True)
			dfs.dropna(axis=0, thresh=6, inplace=True)
			dfs.dropna(axis=1, thresh=5, inplace=True)
			dfs.drop(dfs.head(4).index, inplace=True)
			dfs.drop(dfs.tail(1).index, inplace=True)
			dfs.dropna(axis=0, how='all', inplace=True)
			df = pd.DataFrame(dfs.values, columns=sutun_adi)
			df['MAAŞ TUTARI'] = df['MAAŞ TUTARI'].str.replace(".", "", regex=False)
			df['MAAŞ TUTARI'] = df['MAAŞ TUTARI'].str.replace(",", ".", regex=False).astype(float)
			#df[['SIRA NO', 'TC KIMLIK NO', 'BANKA HESAP NO']] = df[['SIRA NO', 'TC KIMLIK NO', 'BANKA HESAP NO']].apply(pd.to_numeric)
			df_list.append(df)

		elif 'edBankaListe' in rapor:
			dfs = pd.read_excel(rapor, skiprows=6)
			dfs.dropna(axis=0, how='all', inplace=True)
			dfs.dropna(axis=0, thresh=6, inplace=True)
			df = pd.DataFrame(dfs.values, columns=sutun_adi)
			df['IBAN NO'] = df['BANKA HESAP NO'].values
			df['ADI SOYADI'] = df['ADI SOYADI'].str.title()
			df_list.append(df)

		else:
			sutun_ad = ['SIRA NO', 'TC KIMLIK NO', 'ADI SOYADI', 'IBAN NO', 'MAAŞ TUTARI']
			dfs = pd.read_excel(rapor, skiprows=10)
			dfs.dropna(axis=0, how='all', inplace=True)
			dfs.dropna(axis=0, thresh=5, inplace=True)
			dfs.dropna(axis=1, how='all', inplace=True)
			df = pd.DataFrame(dfs.values, columns=sutun_ad)
			df['ADI SOYADI'] = df['ADI SOYADI'].str.title()
			df['BANKA HESAP NO'] = ""
			df['UNVANI'] = ""
			df_list.append(df)

	df = pd.concat(df_list, axis=0)
	df['ŞUBE KODU'] = ""
	df['HESAP NUMARASI'] = ""
	df['EK HESAP NUMARASI'] = ""
	df['AÇIKLAMA'] = "MARDİN MÜF. MAAŞ/EKDERS ÖDEMESİ"

	df = df[['ADI SOYADI', 'IBAN NO', 'ŞUBE KODU', 'HESAP NUMARASI', 'EK HESAP NUMARASI', 'AÇIKLAMA', 'MAAŞ TUTARI']]

	for veri in dataframe_to_rows(df, index=False, header=False):
		excel_sayfasi.append(veri)

	#OrnekMaasOdemeDosyasi.xlsx dosyasını banka_listesi_xxxxxxxx_xxxxxx.xlsx olarak kaydediyoruz.
	excel_dosyasi.save('banka_listesi_' + tarih + '.xlsx')

if __name__ == '__main__':
	bankaListesi()
