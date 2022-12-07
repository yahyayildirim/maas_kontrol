#!/usr/bin/env python3
# Modülleri yüklemek için
# sudo python3 -m pip install -U pandas==1.3.5
# sudo python3 -m pip install -U numexpr==2.8.4
# sudo python3 -m pip install -U numpy==1.21.6

import sys
sys.dont_write_bytecode = True

import pandas as pd

# sabitler.ods dosyasında bulunan herbir sayfayı ayrı ayrı DataFramelere aktardık.
df_0 = pd.DataFrame(pd.read_excel('sabitler.ods', sheet_name=0))
df_1 = pd.DataFrame(pd.read_excel('sabitler.ods', sheet_name=1))
df_2 = pd.DataFrame(pd.read_excel('sabitler.ods', sheet_name=2))
df_3 = pd.DataFrame(pd.read_excel('sabitler.ods', sheet_name=3))
df_per = pd.DataFrame(pd.read_excel('./rapor/kbs_personel_verileri.ods', sheet_name=0))


def gosterge_puani(derece,kademe):
	puan = int(df_0.loc[derece-1].iloc[kademe-1])
	return puan
	# derece ve kademe girdisini alarak yan ödeme puanını verir

def aylik_katsayi(gosterge_puani, unvan):
	if unvan == "İl Müftüsü":
		gosterge_puani = 0

	return df_1['aylik_katsayi'].iloc[-1] * gosterge_puani
	# gosterge_puani x aylik_kaysayi = Aylık Tutar

def yan_odeme(gosterge_puani, unvan):
	if unvan == "İl Müftüsü":
		gosterge_puani = 0

	return df_1['yan_odeme_katsayi'].iloc[-1] * gosterge_puani
	# gosterge_puani x yan_odeme_katsayi

def taban_aylik(binlik, unvan):
	if unvan == "İl Müftüsü":
		binlik = 0
	else:
		binlik = 1000

	return df_1['taban_aylik_katsayi'].iloc[-1] * binlik
	# taban_aylik_katsayi x 1000

def ek_gosterge(ek_gosterge, unvan):
	if unvan == "İl Müftüsü":
		ek_gosterge = 0

	return df_1['aylik_katsayi'].iloc[-1] * ek_gosterge
	# aylik_katsayi x ek_gosterge

def kidem_ayligi(hizmetyili, unvan):
	#Hizmet Süresi x 20 x Maaş Katsayısı
	if unvan == "İl Müftüsü":
		hizmetyili = 0
	elif hizmetyili > 25:
		hizmetyili = 25
	return df_1['aylik_katsayi'].iloc[-1] * 20 * hizmetyili

def ozel_hizmet(tazminat_orani):
	#En Yüksek Devlet Memuru Aylığı X % Tazminat Oranı
	return df_1['aylik_katsayi'].iloc[-1] * 9500 * tazminat_orani / 100

def yan_odeme_puani(unvan, derece):
	if unvan == 'Şube Md.' or unvan == 'Din Hz.Uzm':
		is_guclugu = df_2.loc[(df_2['unvan'] == unvan) & (df_2['derece'] == derece), 'is_guclugu'].sum()
		is_riski = df_2.loc[(df_2['unvan'] == unvan) & (df_2['derece'] == derece), 'is_riski'].sum()
		tem_gucluk = df_2.loc[(df_2['unvan'] == unvan) & (df_2['derece'] == derece), 'tem_gucluk'].sum()
		mali_sorumluluk = df_2.loc[(df_2['unvan'] == unvan) & (df_2['derece'] == derece), 'mali_sorumluluk'].sum()
		return is_guclugu + is_riski + tem_gucluk + mali_sorumluluk

	else:
		is_guclugu = df_2.loc[df_2['unvan'] == unvan, 'is_guclugu'].sum()
		is_riski = df_2.loc[df_2['unvan'] == unvan, 'is_riski'].sum()
		tem_gucluk = df_2.loc[df_2['unvan'] == unvan, 'tem_gucluk'].sum()
		mali_sorumluluk = df_2.loc[df_2['unvan'] == unvan, 'mali_sorumluluk'].sum()
		return is_guclugu + is_riski + tem_gucluk + mali_sorumluluk

def yan_odeme_puani_kbs(tc):
	is_guclugu = df_per.loc[df_per['TC Kimlik'] == tc, 'İş Güçlüğü Puanı'].sum()
	is_riski = df_per.loc[df_per['TC Kimlik'] == tc, 'İş Riski Puanı'].sum()
	tem_gucluk = df_per.loc[df_per['TC Kimlik'] == tc, 'El.Tem.Güç Puanı'].sum()
	mali_sorumluluk = df_per.loc[df_per['TC Kimlik'] == tc, 'Mal.Sor.Taz Puanı'].sum()
	return is_guclugu + is_riski + tem_gucluk + mali_sorumluluk