#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

import numpy as np
import pandas as pd
import time
from datetime import datetime

bu_yil = datetime.now().year
bu_ay = datetime.now().strftime("%B")

def raporla():
	try:
		# KBS ve İKYS verilerini DataFrame ekliyoruz.
		kbs_verisi = pd.DataFrame(pd.read_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/kbs_bordro_verileri.xlsx'))
		ikys_verisi = pd.DataFrame(pd.read_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/ikys_personel_verileri.xlsx'))
		print('%40')

		# KBS Sisteminde bilgisi bulunup, İKYS Sisteminde kaydı bulunmayan Personel
		kbs_in_ikys_out = kbs_verisi[~kbs_verisi['TC Kimlik'].isin(ikys_verisi['TC Kimlik'])]
		kbs_in_ikys_out.to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/kbsde_olup_ikysde_olmayanlar.xlsx', index=False, header=True, freeze_panes=(1,0))
		print('%50')

		kbs_ikys_esitle = kbs_verisi.loc[kbs_verisi['TC Kimlik'].isin(ikys_verisi['TC Kimlik'])]
		kbs_ikys_esitle.to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/kbs_bordro_verileri.xlsx', index=False, header=True, freeze_panes=(1,0))
		print('%60')

		# İKS Sisteminde bilgisi bulunup, KBS Sisteminde kaydı bulunmayan Personel
		ikys_in_kbs_out = ikys_verisi[~ikys_verisi['TC Kimlik'].isin(kbs_verisi['TC Kimlik'])]
		ikys_in_kbs_out.to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/ikysde_olup_kbsde_olmayanlar.xlsx', index=False, header=True, freeze_panes=(1,0))
		print('%70')

		ikys_kbs_esitle = ikys_verisi.loc[ikys_verisi['TC Kimlik'].isin(kbs_verisi['TC Kimlik'])]
		ikys_kbs_esitle.to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/ikys_personel_verileri.xlsx', index=False, header=True, freeze_panes=(1,0))
		print('%80')
	except:
		print("Raporlama hatası....")

if __name__ == '__main__':
	raporla()