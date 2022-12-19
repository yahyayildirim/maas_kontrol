#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

from glob import glob
import pandas as pd
import re
import time

def kbs_personel_verileri():
	dosya = glob('./kbs/_reports_MemurRaporlar*', recursive=False)
	data = [pd.read_excel(f, sheet_name=0, skiprows=15) for f in dosya]
	df = pd.DataFrame(data[0])
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

	# Listeyi TC veya Adı-Soyadına göre sıralayabilirsiniz, dikkat etmeniz gereken ise ikys_personel ve kbs_bordro da aynı değişikliği yapmanızdır.
	#df.sort_values(by=['TC Kimlik'], inplace=True, ignore_index=True)
	df.sort_values(by=['Adı Soyadı'], inplace=True, ignore_index=True)

	df.to_excel('./kbs/kbs_personel_verileri.xlsx', index=False, freeze_panes=(1,2))
	print('1. KBS personel maaş kontrol bilgileri uygun formata getirildi...')
	time.sleep(2)

if __name__ == "__main__":
	kbs_personel_verileri()
