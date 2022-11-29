#!/usr/bin/env python3
# Modülleri yüklemek için
# sudo python3 -m pip install -U pandas==1.3.5
# sudo python3 -m pip install -U numexpr==2.8.4
# sudo python3 -m pip install -U numpy==1.21.6

import pandas as pd

def yan_odeme_puani(derece,kademe):
	df = pd.DataFrame(pd.read_excel('sabitler.ods', sheet_name=0))
	puan = int(df.loc[derece-1].iloc[kademe-1])
	return puan
	# derece ve kademe girdisini alarak yan ödeme puanını verir

def aylik_katsayi(yan_odeme_puani):
	df = pd.DataFrame(pd.read_excel('sabitler.ods', sheet_name=1))
	return df['aylik_katsayi'].iloc[-1] * yan_odeme_puani
	# yan_odeme_puani x aylik_kaysayi = Aylık Tutar

def yan_odeme(yan_odeme_puani):
	df = pd.DataFrame(pd.read_excel('sabitler.ods', sheet_name=1))
	return df['yan_odeme_katsayi'].iloc[-1] * yan_odeme_puani
	# yan_odeme_puani x yan_odeme_katsayi

def taban_aylik():
	df = pd.DataFrame(pd.read_excel('sabitler.ods', sheet_name=1))
	return df['taban_aylik_katsayi'].iloc[-1] * 1000
	# taban_aylik_katsayi x 1000

def ek_gosterge(ek_gosterge):
	df = pd.DataFrame(pd.read_excel('sabitler.ods', sheet_name=1))
	return df['aylik_katsayi'].iloc[-1] * ek_gosterge
	# aylik_katsayi x ek_gosterge


