#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import pandas as pd
#import kbs_personel_verileri

# maas_verileri.xlsx dosyasında bulunan herbir sayfayı ayrı ayrı DataFramelere aktardık.
df_0 = pd.DataFrame(pd.read_excel('maas_verileri.xlsx', sheet_name=0))
df_1 = pd.DataFrame(pd.read_excel('maas_verileri.xlsx', sheet_name=1))
df_2 = pd.DataFrame(pd.read_excel('maas_verileri.xlsx', sheet_name=2))
df_3 = pd.DataFrame(pd.read_excel('maas_verileri.xlsx', sheet_name=3))
#df_per = pd.DataFrame(pd.read_excel('./kbs/kbs_personel_verileri.xlsx', sheet_name=0))


def gosterge_puani(derece,kademe):
	puan = int(df_0.loc[derece-1].iloc[kademe-1])
	return puan
	# derece ve kademe girdisini alarak yan ödeme puanını verir

def aylik_katsayi(gosterge_puani, unvan, izin):
	vekilper = ['Vekil M.K', 'Vekil İ-H']	
	if izin == "Aylıksız İzin" or unvan == "İl Müftüsü":
		aylik_tutar = 0
	elif unvan in vekilper:
		aylik_tutar = (df_1['aylik_katsayi'].iloc[-1] * gosterge_puani / 3) * 2
	else:
		aylik_tutar = df_1['aylik_katsayi'].iloc[-1] * gosterge_puani
	return aylik_tutar
	print(aylik_tutar)
	# gosterge_puani x aylik_kaysayi = Aylık Tutar

def tutardan_yan_odeme_puani_bul(tutar):
	# yan ödeme aylık tutar / yan_odeme_katsayi
	return tutar / df_1['yan_odeme_katsayi'].iloc[-1]

def yan_odeme(gosterge_puani, unvan):
	if unvan == "İl Müftüsü":
		gosterge_puani = 0
	#print(unvan, gosterge_puani)
	return df_1['yan_odeme_katsayi'].iloc[-1] * gosterge_puani
	# gosterge_puani x yan_odeme_katsayi

def taban_aylik(binlik, unvan):
	if unvan == "İl Müftüsü":
		binlik = 0
	else:
		binlik = 1000
	return df_1['taban_aylik_katsayi'].iloc[-1] * binlik
	# taban_aylik_katsayi x 1000

def ek_gosterge(ek_gosterge, unvan, izin):
	vekilper = ['Vekil M.K', 'Vekil İ-H']	
	if izin == "Aylıksız İzin" or unvan == "İl Müftüsü":
		return 0
	elif unvan in vekilper:
		ek_gosterge = ((df_1['aylik_katsayi'].iloc[-1] * ek_gosterge) / 3) * 2
		return ek_gosterge
	else:
		return df_1['aylik_katsayi'].iloc[-1] * ek_gosterge
	# aylik_katsayi x ek_gosterge

def kidem_ayligi(hizmetyili, unvan):
	#Hizmet Süresi x 20 x Maaş Katsayısı
	if unvan == "İl Müftüsü":
		hizmetyili = 0
	elif hizmetyili > 25:
		hizmetyili = 25
	return df_1['aylik_katsayi'].iloc[-1] * 20 * hizmetyili

def ozel_hizmet_orani(unvan, derece, ogrenim, izin):
	if izin == "Aylıksız İzin":
		return 0

	else:
		unvanlar = ['İmam-Hat.', 'Müez.Kayyı', 'Kur.Krs.Öğ', 'Murakıp', 'Vekil M.K', 'Vekil İ-H']
		uz_unvanlar = ['Uzman Vaiz', 'Uz.İm.Hat', 'Kur.Uz.Öğ', 'Baş Müez.Kayyı', 'Baş Vaiz', 'Baş.İm.Hat', 'Kur.Baş.Öğ']
		#print(unvan, derece, ogrenim)
		if unvan in unvanlar:
			ozel_hizmet_orani = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'oht_orani'].sum()
		elif unvan in uz_unvanlar:
			ozel_hizmet_orani = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'oht_orani'].sum()
			#ozel_hizmet_orani_2 = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'ek_1'].sum()
			#ozel_hizmet_orani = ozel_hizmet_orani_1 + ozel_hizmet_orani_2
		else:
			ozel_hizmet_orani = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece), 'oht_orani'].sum()

		return ozel_hizmet_orani

def ozel_hizmet(unvan, derece, ogrenim, izin):
	if izin == "Aylıksız İzin":
		return 0
	else:
		unvanlar = ['İmam-Hat.', 'Müez.Kayyı', 'Kur.Krs.Öğ', 'Murakıp', 'Vekil M.K', 'Vekil İ-H']
		uz_unvanlar = ['Uzman Vaiz', 'Uz.İm.Hat', 'Kur.Uz.Öğ', 'Baş Müez.Kayyı', 'Baş Vaiz', 'Baş.İm.Hat', 'Kur.Baş.Öğ']
		#print(unvan, derece, ogrenim)

		#Özel Hizmet Tazminatı = 9500 X Memur Maaş Katsayısı X Özel Hizmet Puanı / 100 formülüyle hesaplanır.
		if unvan in unvanlar:
			ozel_hizmet_taz = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'oht_orani'].sum()
			ozel_hizmet_tutari = df_1['aylik_katsayi'].iloc[-1] * ozel_hizmet_taz * 9500 / 100
		elif unvan in uz_unvanlar:
			ozel_hizmet_taz = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'oht_orani'].sum()
			#ozel_hizmet_taz_ek = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'ek_1'].sum()
			ozel_hizmet_tutari = df_1['aylik_katsayi'].iloc[-1] * ozel_hizmet_taz * 9500 / 100
		elif unvan == "İl Müftüsü":
			ozel_hizmet_tutari = 0
		else:
			ozel_hizmet_taz = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece), 'oht_orani'].sum()
			ozel_hizmet_tutari = df_1['aylik_katsayi'].iloc[-1] * ozel_hizmet_taz * 9500 / 100

		return ozel_hizmet_tutari

def ek_odeme_666(unvan, derece, ogrenim, izin):
	if izin == "Aylıksız İzin":
		return 0
	else:
		unvanlar = ['İmam-Hat.', 'Müez.Kayyı', 'Kur.Krs.Öğ', 'Murakıp', 'Vekil M.K', 'Vekil İ-H']
		uz_unvanlar = ['Uzman Vaiz', 'Uz.İm.Hat', 'Kur.Uz.Öğ', 'Baş Müez.Kayyı', 'Baş Vaiz', 'Baş.İm.Hat', 'Kur.Baş.Öğ']
		#print(unvan, derece, ogrenim)

		#Ek Öde.(666 KHK) = 9500 X Memur Maaş Katsayısı X Ek Ödeme Oranı / 100 formülüyle hesaplanır.
		if unvan in unvanlar:
			khk_666 = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'ek_odeme_orani'].sum()
			return df_1['aylik_katsayi'].iloc[-1] * khk_666 * 9500 / 100
		elif unvan in uz_unvanlar:
			khk_666 = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'ek_odeme_orani'].sum()
			return df_1['aylik_katsayi'].iloc[-1] * khk_666 * 9500 / 100
		else:
			khk_666 = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece), 'ek_odeme_orani'].sum()
			return df_1['aylik_katsayi'].iloc[-1] * khk_666 * 9500 / 100

def ek_odeme_666_orani(unvan, derece, ogrenim, izin):
	if izin == "Aylıksız İzin":
		return 0
	else:
		unvanlar = ['İmam-Hat.', 'Müez.Kayyı', 'Kur.Krs.Öğ', 'Murakıp', 'Vekil M.K', 'Vekil İ-H']
		uz_unvanlar = ['Uzman Vaiz', 'Uz.İm.Hat', 'Kur.Uz.Öğ', 'Baş Müez.Kayyı', 'Baş Vaiz', 'Baş.İm.Hat', 'Kur.Baş.Öğ']
		#print(unvan, derece, ogrenim)
		if unvan in unvanlar:
			khk_666 = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'ek_odeme_orani'].sum()
			return khk_666
		elif unvan in uz_unvanlar:
			khk_666 = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'ek_odeme_orani'].sum()
			return khk_666
		else:
			khk_666 = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece), 'ek_odeme_orani'].sum()
			return khk_666

def yan_odeme_puani(unvan, derece, hizmetyili, izin):
	if izin == "Aylıksız İzin":
		return 0
	else:
		if unvan == 'Şube Md.' or unvan == 'Din Hz.Uzm':
			is_guclugu = df_2.loc[(df_2['unvan'] == unvan) & (df_2['derece'] == derece), 'is_guclugu'].sum()
			is_riski = df_2.loc[(df_2['unvan'] == unvan) & (df_2['derece'] == derece), 'is_riski'].sum()
			tem_gucluk = df_2.loc[(df_2['unvan'] == unvan) & (df_2['derece'] == derece), 'tem_gucluk'].sum()
			mali_sorumluluk = df_2.loc[(df_2['unvan'] == unvan) & (df_2['derece'] == derece), 'mali_sorumluluk'].sum()
			return is_guclugu + is_riski + tem_gucluk + mali_sorumluluk

		elif unvan == 'Tekniker' or unvan == 'Teknisyen':
			if hizmetyili <= 5:
				is_guclugu = df_2.loc[(df_2['unvan'] == unvan) & (df_2['hizmetyili'] == "<5"), 'is_guclugu'].sum()
				is_riski = df_2.loc[(df_2['unvan'] == unvan) & (df_2['hizmetyili'] == "<5"), 'is_riski'].sum()
				tem_gucluk = df_2.loc[(df_2['unvan'] == unvan) & (df_2['hizmetyili'] == "<5"), 'tem_gucluk'].sum()
				mali_sorumluluk = df_2.loc[(df_2['unvan'] == unvan) & (df_2['hizmetyili'] == "<5"), 'mali_sorumluluk'].sum()
				return is_guclugu + is_riski + tem_gucluk + mali_sorumluluk
			else:
				is_guclugu = df_2.loc[(df_2['unvan'] == unvan) & (df_2['hizmetyili'] == "5>"), 'is_guclugu'].sum()
				is_riski = df_2.loc[(df_2['unvan'] == unvan) & (df_2['hizmetyili'] == "5>"), 'is_riski'].sum()
				tem_gucluk = df_2.loc[(df_2['unvan'] == unvan) & (df_2['hizmetyili'] == "5>"), 'tem_gucluk'].sum()
				mali_sorumluluk = df_2.loc[(df_2['unvan'] == unvan) & (df_2['hizmetyili'] == "5>"), 'mali_sorumluluk'].sum()
				return is_guclugu + is_riski + tem_gucluk + mali_sorumluluk			
		else:
			is_guclugu = df_2.loc[df_2['unvan'] == unvan, 'is_guclugu'].sum()
			is_riski = df_2.loc[df_2['unvan'] == unvan, 'is_riski'].sum()
			tem_gucluk = df_2.loc[df_2['unvan'] == unvan, 'tem_gucluk'].sum()
			mali_sorumluluk = df_2.loc[df_2['unvan'] == unvan, 'mali_sorumluluk'].sum()
			return is_guclugu + is_riski + tem_gucluk + mali_sorumluluk

# def yan_odeme_puani_kbs(tc):
# 	is_guclugu = df_per.loc[df_per['TC Kimlik'] == tc, 'İş Güçlüğü Puanı'].sum()
# 	is_riski = df_per.loc[df_per['TC Kimlik'] == tc, 'İş Riski Puanı'].sum()
# 	tem_gucluk = df_per.loc[df_per['TC Kimlik'] == tc, 'El.Tem.Güç Puanı'].sum()
# 	mali_sorumluluk = df_per.loc[df_per['TC Kimlik'] == tc, 'Mal.Sor.Taz Puanı'].sum()
# 	return is_guclugu + is_riski + tem_gucluk + mali_sorumluluk

# def ozel_hizmet_orani_kbs(tc):
# 	ozel_hizmet_orani = df_per.loc[df_per['TC Kimlik'] == tc, 'Özel Hizmet'].sum()
# 	return ozel_hizmet_orani

def tutardan_ozel_hizmet_orani_bul(tutar):
	# Puan = Özel Hizmet Tazminatı Tutarı / (9500 X Memur Maaş Katsayısı) 100 formülüyle hesaplanır.
	return tutar / (9500 * df_1['aylik_katsayi'].iloc[-1]) * 100

def tutardan_666_orani_bul(tutar):
	# Puan = Özel Hizmet Tazminatı Tutarı / (9500 X Memur Maaş Katsayısı) 100 formülüyle hesaplanır.
	return tutar / (9500 * df_1['aylik_katsayi'].iloc[-1]) * 100

def tutardan_ek_tazminat_puani_bul(tutar):
	# Puan = Özel Hizmet Tazminatı Tutarı / (9500 X Memur Maaş Katsayısı) 100 formülüyle hesaplanır.
	return tutar / (9500 * df_1['aylik_katsayi'].iloc[-1]) * 100

def ek_tazminat_puani(unvan, derece, ogrenim):
	uz_unvanlar = ['Uzman Vaiz', 'Uz.İm.Hat', 'Kur.Krs.Uz.Öğ', 'Baş Müez.Kayyı', 'Baş Vaiz', 'Baş.İm.Hat', 'Kur.Krs.Baş.Öğ']

	if unvan in uz_unvanlar:
		ek_tazminat_puani = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece) & (df_3['ogrenim'] == ogrenim), 'ek_1'].sum()
	else:
		ek_tazminat_puani = df_3.loc[(df_3['unvan'] == unvan) & (df_3['derece'] == derece), 'ek_1'].sum()

	return ek_tazminat_puani
