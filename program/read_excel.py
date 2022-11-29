#!/usr/bin/env python3

import pandas as pd
import numpy as np
import xlrd

#Excel Dosyamızı çağırıyoruz, ilk iki satırı almıyoruz ve veri değişkenine atıyoruz
kbs_veriseti = pd.DataFrame(pd.read_excel('BordroDokumu38184990.xlsx', sheet_name=0, skiprows=1))
ikys_veriseti = pd.DataFrame(pd.read_excel('Personel Rapor.ods', skiprows=2))

print(kbs_veriseti.shape)
print(ikys_veriseti.shape)

#Excel Dosyamızdaki Başlıkları alıyoruz ve listeye ekliyoruz.
basliklar_1 = kbs_veriseti.columns.ravel()
basliklar_2 = ikys_veriseti.columns.ravel()

# KBS sisteminde bulunan personel sayısı
kbs_personel_sayisi = len(kbs_veriseti.groupby("Personel No TC.Kimlik No"))

#İKYS sisteminde bulunan kadrolu personel sayısı
ikys_personel_sayisi = len(ikys_veriseti.groupby("Kadro Tipi").get_group("Memur")["TC Kimlik"].unique())


ikys_derece_kademe = ikys_veriseti["Ödenilecek Derece/Kademe"]
kbs_derece_kademe = kbs_veriseti["Öd.Es.D.-K. Em.Es.D.-K."]

#print(kbs_derece_kademe)

#for baslik in basliklar:
#	print(veri[baslik].tolist())

#Sicil sutunundaki verileri listeye alıyoruz.
#print(veri["Sicil"].tolist())




#Hizmet sınıfı ve unvana göre grupluyoruz ve for döngüsü ile listeye alıyoruz.
#for name, sinif in df.groupby(["Unvan", "Sınıf"]):
#	print(name)
#	print(sinif)


#Hizmet sınıflarında çalışan personel sayısı
#siniflar = df.groupby("Sınıf")["Unvan"].count()


#Hizmet sınıflarında çalışan personel sayısı
##yaslar = df.groupby("Sınıf")["Doğum Tarihi"].max()["Genel İdare Hizmetleri"]
#print(yaslar)







