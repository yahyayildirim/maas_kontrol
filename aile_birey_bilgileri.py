#!/usr/bin/env python3

import pandas as pd
import numpy as np
from datetime import datetime
from glob import glob
from datetime import date
import os
import sys
sys.dont_write_bytecode = True

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

def personel_aile_bilgileri(tcno):
	#df = pd.read_csv("/home/yahya/PersonellerinAileBilgileri.csv")
	bu_dizin = os.path.dirname(__file__) + '/ikys/'
	dosya =glob(bu_dizin + "*PersonellerinAileBilgileri*")
	if dosya:
		df = pd.read_csv(''.join(dosya))
	else:
		print("/ikys klasöründe PersonellerinAileBilgileri.csv dosyası yok. Lütfen tekrar deneyin.")
		sys.exit()

	indis = df[df['TCKIMLIKNO'] == tcno].first_valid_index()
	index = df[df.index.isin([indis])]


	df['FARK'] = datetime.now().year - pd.to_datetime(pd.Series(df['DOGUMTARIHI']), format='%d.%m.%Y').dt.year
	#df['DOGUMTARIHI'] = pd.to_datetime(pd.Series(df['DOGUMTARIHI']), format='%d.%m.%Y')
	df['UNVANADI'] = df['UNVANADI'].ffill()

	#df['FARK'] = df['DOGUMTARIHI'] +  pd.offsets.DateOffset(years=18)

	df['YAS'] = df['YAS'].fillna(df['FARK'])

	#df["satirSAYISI"] = df.groupby(['SIRALAMA']).size()
	#df = df[df['ADI2'].isin(['ASLAN'])]

	df["ADSOYAD"] = df['ADI'].astype(str) + " " + df['ADI2']
	#df = df[df[list(df)].isin(df).all(axis=0)]

	#df = df[df['TCKIMLIKNO'].isin([tcno])]
	df = df[df['SIRALAMA'].isin(index['SIRALAMA'])]


	df = df[['TCKIMLIKNO', 'ADSOYAD', 'UNVANADI', 'DOGUMTARIHI', 'YAKINLIK', 'YAS']].reset_index()
	aile_birey_sayisi = len(df.values.tolist())

	cocuk_sayisi = []
	alti_yas = []
	alti_yas_ustu = []
	onsekiz_ustu = []
	yirmibes_ustu = []
	evli_bekar = ""

	for satir in df.values:
		if "Oğlu" in satir or "Kızı" in satir:
			cocuk_sayisi.append(satir)

			if int(satir[-1]) < 7:
				alti_yas.append(satir)
			else:
				if int(satir[-1]) < 19:
					alti_yas_ustu.append(satir)
				else:
					if int(satir[-1]) < 26:
						onsekiz_ustu.append(satir)
					else:
						yirmibes_ustu.append(satir)

		elif "Eşi" in satir:
			evli_bekar = "Evli"
		else:
			evli_bekar = "Bekar"

	#print(f'Evli mi: {evli_bekar}')	
	#print(f'Toplam Çocuk Sayısı: {len(cocuk_sayisi)}')
	#print(f'7 Yaşından Küçük Olanların Sayısı: {len(alti_yas)}')
	#print(f'7-18 Yaş Arası Olanların Sayısı: {len(alti_yas_ustu)}')
	#print(f'18-25 Yaş Arası Olanların Sayısı: {len(onsekiz_ustu)}')
	#print(f'25 Yaşından Büyük Olanların Sayısı: {len(yirmibes_ustu)}')

	return evli_bekar, len(alti_yas), len(alti_yas_ustu)

#if __name__ == '__main__':
#	tcno = int(input("Personelin T.C No:"))
#	print(personel_aile_bilgileri(tcno))
