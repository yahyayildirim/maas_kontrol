#!/usr/bin/env python3

import pandas as pd
import natsort
import glob
import re
from datetime import datetime
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

bugun = datetime.today()
tarih = datetime.strftime(bugun, '%d%m%Y_%H%M')

bu_yil = str(datetime.now().year)
bu_ay = str(datetime.now().strftime("%B")).upper()

def bankaListesi(banka_listesi, data):
	# Taslak Excel Dosyamız
	excel_dosyasi = openpyxl.load_workbook(f'{data["dosya"]}')

	# Excel dosyamızda bulunan sayfa adımız
	excel_sayfasi = excel_dosyasi.worksheets[1]

	df_list = []
	for rapor in natsort.os_sorted(banka_listesi):
		sutun_adi = ['SIRA NO', 'TC KIMLIK NO', 'ADI SOYADI', 'UNVANI', 'BANKA HESAP NO', 'IBAN NO', 'MAAŞ TUTARI']
		if '4BKKRaporlar_BankaListesi' in rapor:
			print("4/B SÖZLEŞMELİ MAAŞ DOSYASI: ", rapor)
			dfs = pd.read_excel(rapor)
			dfs = dfs.drop(range(0, 16))
			dfs = dfs.dropna(axis=1, how='all')
			dfs = dfs.dropna(axis=0, how='all')
			dfs = dfs.dropna(axis=0, thresh=(7,))
			dfs = dfs.dropna(axis=1, thresh=(2,))
			df = pd.DataFrame(dfs.values, columns=sutun_adi)
			df.drop(df[(df['MAAŞ TUTARI'] == "MAAŞ TUTARI")].index, inplace=True)
			df['ADI SOYADI'] = df['ADI SOYADI'].str.upper()
			df['MAAŞ TUTARI'] = df['MAAŞ TUTARI'].str.replace(".", "", regex=False)
			df['MAAŞ TUTARI'] = df['MAAŞ TUTARI'].str.replace(",", ".", regex=False).astype(float)
			#aciklama = input(f"Lütfen {rapor} dosyası için açıklama giriniz: ")
			df['AÇIKLAMA'] = "MAAŞ ÖDEMESİ (4/B)"
			df_list.append(df)

		elif 'MemurRaporlar_BankaListesi' in rapor:
			print("KADROLU MAAŞ DOSYASI: ", rapor)
			dfs = pd.read_excel(rapor, skiprows=1)
			dfs.dropna(axis=0, how='all', inplace=True)
			dfs.dropna(axis=0, thresh=6, inplace=True)
			dfs.dropna(axis=1, thresh=5, inplace=True)
			dfs.drop(dfs.head(4).index, inplace=True)
			dfs.drop(dfs.tail(1).index, inplace=True)
			dfs.dropna(axis=0, how='all', inplace=True)
			df = pd.DataFrame(dfs.values, columns=sutun_adi)
			df.drop(df[(df['MAAŞ TUTARI'] == "MAAŞ TUTARI")].index, inplace=True)
			df['ADI SOYADI'] = df['ADI SOYADI'].str.upper()
			df['MAAŞ TUTARI'] = df['MAAŞ TUTARI'].str.replace(".", "", regex=False)
			df['MAAŞ TUTARI'] = df['MAAŞ TUTARI'].str.replace(",", ".", regex=False).astype(float)
			#aciklama = input(f"Lütfen {rapor} dosyası için açıklama giriniz: ")
			df['AÇIKLAMA'] ="MAAŞ ÖDEMESİ (KADROLU)"
			df_list.append(df)

		elif 'edBankaListe' in rapor:
			print("EK-DERS ÖDEME DOSYASI: ", rapor)
			dfs = pd.read_excel(rapor, skiprows=6)
			dfs.dropna(axis=0, how='all', inplace=True)
			dfs.dropna(axis=0, thresh=6, inplace=True)
			df = pd.DataFrame(dfs.values, columns=sutun_adi)
			df['IBAN NO'] = df['BANKA HESAP NO'].values
			df['ADI SOYADI'] = df['ADI SOYADI'].str.upper()
			#aciklama = input(f"Lütfen {rapor} dosyası için açıklama giriniz: ")
			df['AÇIKLAMA'] = "EK-DERS ÖDEMESİ (KBS)"
			df_list.append(df)

		elif 'fcBankaListe' in rapor:
			print("FAZLA ÇALIŞMA DOSYASI: ", rapor)
			sutun_adi = ['SIRA NO', 'TC KIMLIK NO', 'ADI SOYADI', 'BANKA HESAP NO', 'IBAN NO', 'MAAŞ TUTARI']
			dfs = pd.read_excel(rapor, skiprows=6)
			dfs.drop(dfs.tail(1).index, inplace=True)
			#dfs.dropna(axis=0, how='all', inplace=True)
			#dfs.dropna(axis=0, thresh=6, inplace=True)
			df = pd.DataFrame(dfs.values, columns=sutun_adi)
			df['ADI SOYADI'] = df['ADI SOYADI'].str.upper()
			#aciklama = input(f"Lütfen {rapor} dosyası için açıklama giriniz: ")
			df['AÇIKLAMA'] = "FAZLA MESAİ ÖDEMESİ (KBS)"
			df_list.append(df)

		elif 'BankaListesi.xlsx' in rapor:
			print("DİBBYS/İKYS BANKA DOSYASI: ", rapor)
			sutun = ['SIRA NO', 'TC KIMLIK NO', 'ADI SOYADI', 'IBAN NO', 'AGİ', 'ÜCRET', 'MAAŞ TUTARI']
			dfs = pd.read_excel(rapor, skiprows=10)
			dfs.dropna(axis=0, how='all', inplace=True)
			dfs.dropna(axis=0, thresh=5, inplace=True)
			dfs.dropna(axis=1, how='all', inplace=True)
			sutun_ad = dfs.columns
			df = pd.DataFrame(dfs.values, columns=sutun_ad)
			if 'Unvan' in df.columns:
				df.drop(['Unvan'], axis=1, inplace=True)
			df.columns = sutun
			#df = df.set_axis(sutun_ad, axis=1, inplace=False)
			df['ADI SOYADI'] = df['ADI SOYADI'].str.upper()
			#aciklama = input(f"Lütfen {rapor} dosyası için açıklama giriniz: ")
			#df['AÇIKLAMA'] = f"{aciklama}"
			df['AÇIKLAMA'] = "EK-DERS ÖDEMESİ (DİBBYS)"
			df_list.append(df)

		elif 'BankaListesi2022.xlsx' in rapor:
			print("DİBBYS/İKYS BANKA DOSYASI: ", rapor)
			sutun = ['SIRA NO', 'TC KIMLIK NO', 'ADI SOYADI', 'IBAN NO', 'MAAŞ TUTARI']
			dfs = pd.read_excel(rapor, skiprows=10)
			dfs.dropna(axis=0, how='all', inplace=True)
			dfs.dropna(axis=0, thresh=5, inplace=True)
			dfs.dropna(axis=1, how='all', inplace=True)
			sutun_ad = dfs.columns
			df = pd.DataFrame(dfs.values, columns=sutun_ad)
			if 'Unvan' in df.columns:
				df.drop(['Unvan'], axis=1, inplace=True)
			df.columns = sutun
			#df = df.set_axis(sutun_ad, axis=1, inplace=False)
			df['ADI SOYADI'] = df['ADI SOYADI'].str.upper()
			#aciklama = input(f"Lütfen {rapor} dosyası için açıklama giriniz: ")
			#df['AÇIKLAMA'] = f"{aciklama}"
			df['AÇIKLAMA'] = "4/D İŞÇİ ÖDEMESİ"
			df_list.append(df)

		#else:
			#sutun = ['SIRA NO', 'TC KIMLIK NO', 'ADI SOYADI', 'IBAN NO', 'MAAŞ TUTARI']
			#dfs = pd.read_excel(rapor, skiprows=10)
			#dfs.dropna(axis=0, how='all', inplace=True)
			#dfs.dropna(axis=0, thresh=5, inplace=True)
			#dfs.dropna(axis=1, how='all', inplace=True)
			#sutun_ad = dfs.columns
			#df = pd.DataFrame(dfs.values, columns=sutun_ad)
			#if 'Unvan' in df.columns:
				#df.drop(['Unvan'], axis=1, inplace=True)
			#df.columns = sutun
			##df = df.set_axis(sutun_ad, axis=1, inplace=False)
			#df['ADI SOYADI'] = df['ADI SOYADI'].str.upper()
			##aciklama = input(f"Lütfen {rapor} dosyası için açıklama giriniz: ")
			#df['AÇIKLAMA'] = "İŞÇİ ÖDEMESİ"
			#df_list.append(df)

	df = pd.concat(df_list, axis=0)
	if "ziraat" in f'{data["dosya_adi"]}'.lower():
		df['CARİ KODU'] = ""
		df['BANKA NO'] = ""
		df['SUBE NO'] = ""
		df['HESAP NO'] = ""	
		df['IBAN NO'] = df['IBAN NO'].astype(str)
		df['VERGI NO'] = ""
		df['ALICI EMAIL ADRESI'] = ""#df['IBAN NO'].str[13:22].apply(pd.to_numeric)
		df['OPSIYON GÜN SAYISI'] = "" #df['IBAN NO'].str[22:].apply(pd.to_numeric)
		df['ÖDEME SEBEBİ'] = "P-Personel Ödemeleri"
		df['Alıcı Yerleşik Bilgisi'] = "Yurtiçi Yerleşik"
		df['Ödeme Amacı Kategorisi'] = ""
		#df['TC KIMLIK NO'] = df['TC KIMLIK NO'].astype(str)
		df = df[['CARİ KODU', 'ADI SOYADI', 'BANKA NO', 'SUBE NO', 'HESAP NO', 'IBAN NO', 
		'MAAŞ TUTARI', 'VERGI NO', 'AÇIKLAMA', 'ALICI EMAIL ADRESI', 'OPSIYON GÜN SAYISI',
		'ÖDEME SEBEBİ', 'Alıcı Yerleşik Bilgisi', 'Ödeme Amacı Kategorisi']]

	elif "albaraka" in f'{data["dosya_adi"]}'.lower():
		# Albraka Türk kurum hesap numarası için albaraka_turk.xlsx excel dosyasını açıp
		# Şube Kodu
		# Hesap Numarası
		# Ek Hesap Numarası
		# alanlarını değiştirmeyi unutmayın.
		df['BOŞ VERİ 1'] = ""
		df['BOŞ VERİ 2'] = ""
		df['BOŞ VERİ 3'] = ""
		df = df[['ADI SOYADI', 'IBAN NO', 'BOŞ VERİ 1', 'BOŞ VERİ 2', 'BOŞ VERİ 3', 'AÇIKLAMA', 'MAAŞ TUTARI']]

	for veri in dataframe_to_rows(df, index=False, header=False):
		excel_sayfasi.append(veri)
	excel_dosyasi.save(f'{data["dosya_adi"]}_banka_listesi_{tarih}.xlsx')
	print("\nBanka Listesi başarılı bir şekilde oluşturulmuştur.")

if __name__ == '__main__':
	banka_listesi = glob.glob('*BankaListe*')
	data = [{'sira': 1, 'banka_adi': 'Ziraat Katılım', 'dosya_adi': 'ziraat_katilim', 'dosya': 'ziraat_katilim.xlsx'},
			{'sira': 2, 'banka_adi': 'Albaraka Türk', 'dosya_adi': 'albarakaturk', 'dosya': 'albaraka_turk.xlsx'}]

	datalist = [x for x in data]
	for n,i in enumerate(datalist, 1):
		print(n, "-->", i['banka_adi'])

	secim = input("\nHangi bankanın listesini almak istiyorsanız,\nsıra numarasını yazıp enter yapın.\nSeçiminiz: ")

	if int(secim) in [d['sira'] for d in datalist] and len([x for x in banka_listesi]) > 0:
		bankaListesi(banka_listesi, data[int(secim) - 1])
	else:
		print("Lütfen banka listesini /banka klasörüne kopyalayın ve sonra tekrar deneyin...")
