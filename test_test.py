#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import pandas as pd
import numpy as np
import xlrd


#Excel Dosyamızı çağırıyoruz, ilk iki satırı almıyoruz ve veri değişkenine atıyoruz
kbss_veriseti = pd.DataFrame(pd.read_excel('./rapor/kbss_yeni.ods', sheet_name=0))
ikys_veriseti = pd.DataFrame(pd.read_excel('./rapor/ikys_yeni.ods', sheet_name=0))

#print(kbss_veriseti.shape)
#print(ikys_veriseti.shape)

#Excel Dosyamızdaki Başlıkları alıyoruz ve listeye ekliyoruz.
#print(kbss_veriseti.columns)
#print(ikys_veriseti.columns)


# KBS sisteminde bulunan personel sayısı
kbss_personel_sayisi = len(kbss_veriseti.groupby("TC Kimlik"))
#print(kbss_personel_sayisi)

#İKYS sisteminde bulunan kadrolu personel sayısı
ikys_personel_sayisi = len(ikys_veriseti.groupby("TC Kimlik"))
#print(ikys_personel_sayisi)

ikys_derece_kademe = ikys_veriseti["Derece"]
kbss_derece_kademe = kbss_veriseti["Derece"]

#print(kbs_derece_kademe)

#for baslik in basliklar:
#	print(veri[baslik].tolist())

#Sicil sutunundaki verileri listeye alıyoruz.
#print(veri["Sicil"].tolist())

bir = pd.concat([kbss_veriseti, ikys_veriseti], axis=1)
bir.to_excel('birlestirildi.ods', index=False)

#Hizmet sınıfı ve unvana göre grupluyoruz ve for döngüsü ile listeye alıyoruz.
#for name, sinif in df.groupby(["Unvan", "Sınıf"]):
#	print(name)
#	print(sinif)


#Hizmet sınıflarında çalışan personel sayısı
#siniflar = df.groupby("Sınıf")["Unvan"].count()


#Hizmet sınıflarında çalışan personel sayısı
##yaslar = df.groupby("Sınıf")["Doğum Tarihi"].max()["Genel İdare Hizmetleri"]
#print(yaslar)







