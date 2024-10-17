#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import os
from datetime import datetime as tarih

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

ana_dizin = os.getcwd()
yil = ana_dizin + '/rapor/' + str(tarih.today().year)
ay = ana_dizin + '/rapor/' + str(tarih.today().year) + '/' + str(tarih.today().strftime("%B"))

arsiv_dizini = [yil, ay] # list of file paths
for dizin in arsiv_dizini:
    if not os.path.exists(dizin):
        os.makedirs(dizin)

print("Lütfen bekleyiniz...")

if __name__ == "__main__":
	import kbs_bordro_verileri
	kbs_bordro_verileri.kbs_temiz_veri()

	import ikys_personel_verileri
	ikys_personel_verileri.ikys_personel_verileri()
	
	import verileri_raporla
	verileri_raporla.raporla()

	import kontrol_raporu_hazirla
	kontrol_raporu_hazirla.kontrol_raporu_v1()
	kontrol_raporu_hazirla.kontrol_raporu_v2()

	import emsan_veri_hazirla
	emsan_veri_hazirla.emsan_veri()

	import hatalar_icin_aciklama_ekle
	hatalar_icin_aciklama_ekle.aciklama_ekle()


