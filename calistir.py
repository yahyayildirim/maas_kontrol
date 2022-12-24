#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

print("Lütfen bekleyiniz...")

if __name__ == "__main__":
	import kbs_bordro_verileri
	kbs_bordro_verileri.kbs_temiz_veri()
	kbs_bordro_verileri.kbs_bordro_verileri()

	import ikys_personel_verileri
	ikys_personel_verileri.ikys_personel_verileri()
	
	import verileri_raporla

	import kontrol_raporu_hazirla