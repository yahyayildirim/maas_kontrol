#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import pandas as pd
import numpy as np
import xlrd


#Excel Dosyamızı çağırıyoruz, ilk iki satırı almıyoruz ve veri değişkenine atıyoruz
kbss_veriseti = pd.DataFrame(pd.read_excel('./rapor/ikys_personel_verileri.ods', sheet_name=0))
ikys_veriseti = pd.DataFrame(pd.read_excel('./rapor/kbs_bordro_verileri.ods', sheet_name=0))

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

df3 = pd.merge(kbss_veriseti, ikys_veriseti, how='outer', indicator='Exist')
df3 = df3.loc[df3['Exist'] != 'both']
df3.sort_values(by=['TC Kimlik'], inplace=True)
df3.to_excel('merge_rapor.ods', index=False)

#df_diff = pd.concat([df1,df2]).drop_duplicates(keep=False)
bir = pd.concat([kbss_veriseti, ikys_veriseti]).drop_duplicates(keep=False)
bir.sort_values(by=['TC Kimlik'], inplace=True)
bir.to_excel('concat_rapor.ods', index=False)



df_all = pd.concat([kbss_veriseti.set_index('TC Kimlik'), ikys_veriseti.set_index('TC Kimlik')], axis='columns', keys=['KBS', 'İKYS'])
df_final = df_all.swaplevel(axis='columns')[kbss_veriseti.columns[1:]]

def highlight_diff(data, color='yellow'):
    attr = 'background-color: {}'.format(color)
    other = data.xs('KBS', axis='columns', level=-1)
    return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''), index=data.index, columns=data.columns)

df_final.style.apply(highlight_diff, axis=None)
df_final.to_excel('fark_rapor.ods')




#Hizmet sınıfı ve unvana göre grupluyoruz ve for döngüsü ile listeye alıyoruz.
#for name, sinif in df.groupby(["Unvan", "Sınıf"]):
#	print(name)
#	print(sinif)


#Hizmet sınıflarında çalışan personel sayısı
#siniflar = df.groupby("Sınıf")["Unvan"].count()


#Hizmet sınıflarında çalışan personel sayısı
##yaslar = df.groupby("Sınıf")["Doğum Tarihi"].max()["Genel İdare Hizmetleri"]
#print(yaslar)







