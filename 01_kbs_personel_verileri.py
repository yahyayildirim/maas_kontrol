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
import glob


def kbs_personel_verileri():
	dosya = glob.glob('./kbs/MemurRaporlar_PersonelBilgileri.xls', recursive = True)
	for file in dosya:
		df = pd.DataFrame(pd.read_excel(file, sheet_name=0, skiprows=15))
	df.dropna(axis=0, thresh=8, inplace=True)			
	df.dropna(axis=1, thresh=2, inplace=True)

	#print(df.shape)
	df.columns = ['SN','KK1','KK2', 'KK3', 'KK4', 'Birim Kodu', 'Personel No', 'Adı Soyadı', 'Unvan',
	'TC Kimlik', 'Hizmet Sın. Kodu', 'Kadro Derecesi', 'Ödeme D/K', 'Emekli D/K', 'Emekli Ek Gösterge',
	'Özel Hizmet', 'İş Güçlüğü Puanı', 'El.Tem.Güç Puanı', 'İş Riski Puanı', 'Mal.Sor.Taz Puanı', 'Kıdem Ay', 'Kıdem Yıl']
	
	# satır ve sütunlarda tamamen boş olanları siliyoruz.
	df.dropna(axis=0, how='all', inplace=True)
	df.dropna(axis=1, how='all', inplace=True)
	df = df[df.SN != 'Sıra No']
	
	df[['Personel No', 'TC Kimlik', 'Hizmet Sın. Kodu', 'Kadro Derecesi', 'Emekli Ek Gösterge', 'Özel Hizmet', 'İş Güçlüğü Puanı',
		'El.Tem.Güç Puanı', 'İş Riski Puanı', 'Mal.Sor.Taz Puanı', 'Kıdem Ay', 'Kıdem Yıl']] = df[['Personel No', 'TC Kimlik', 'Hizmet Sın. Kodu', 'Kadro Derecesi', 'Emekli Ek Gösterge', 'Özel Hizmet', 'İş Güçlüğü Puanı',
		'El.Tem.Güç Puanı', 'İş Riski Puanı', 'Mal.Sor.Taz Puanı', 'Kıdem Ay', 'Kıdem Yıl']].apply(pd.to_numeric).fillna(0)

	df = df[['Personel No', 'Adı Soyadı', 'Unvan', 'TC Kimlik', 'Hizmet Sın. Kodu', 'Kadro Derecesi',
			 'Ödeme D/K', 'Emekli D/K', 'Emekli Ek Gösterge', 'Özel Hizmet', 'İş Güçlüğü Puanı', 'El.Tem.Güç Puanı',
			 'İş Riski Puanı', 'Mal.Sor.Taz Puanı', 'Kıdem Ay', 'Kıdem Yıl']]

	df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)
	df.to_excel('./rapor/kbs_personel_verileri.ods', index=False)

if __name__ == "__main__":
	kbs_personel_verileri()
