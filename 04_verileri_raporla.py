#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

#openpyxl==3.0.9
#pandas==1.5.2
#xlwings==0.25.3
#numexpr==2.8.4
#bottleneck==1.3.5
#odfpy==1.4.1

import numpy as np
import pandas as pd

# KBS ve İKYS verilerini DataFrame ekliyoruz.
kbs_verisi = pd.DataFrame(pd.read_excel('./rapor/kbs_bordro_verileri.ods'))
ikys_verisi = pd.DataFrame(pd.read_excel('./rapor/ikys_personel_verileri.ods'))


# KBS Sisteminde bilgisi bulunup, İKYS Sisteminde kaydı bulunmayan Personel
kbs_in_ikys_out = kbs_verisi[~kbs_verisi['TC Kimlik'].isin(ikys_verisi['TC Kimlik'])]
kbs_in_ikys_out.to_excel('./rapor/kbsde_olup_ikysde_olmayanlar.ods', index=False, header=True)

# İKS Sisteminde bilgisi bulunup, KBS Sisteminde kaydı bulunmayan Personel
ikys_in_kbs_out = ikys_verisi[~ikys_verisi['TC Kimlik'].isin(kbs_verisi['TC Kimlik'])]
ikys_in_kbs_out.to_excel('./rapor/ikysde_olup_kbsde_olmayanlar.ods', index=False, header=True)


ikys_kbs_esitle = ikys_verisi.loc[ikys_verisi['TC Kimlik'].isin(kbs_verisi['TC Kimlik'])]
ikys_kbs_esitle.to_excel('./rapor/ikys_personel_verileri.ods', index=False, header=True)

kbs_ikys_esitle = kbs_verisi.loc[kbs_verisi['TC Kimlik'].isin(ikys_verisi['TC Kimlik'])]
kbs_ikys_esitle.to_excel('./rapor/kbs_bordro_verileri.ods', index=False, header=True)

kbs_verisi = pd.DataFrame(pd.read_excel('./rapor/kbs_bordro_verileri.ods'))
ikys_verisi = pd.DataFrame(pd.read_excel('./rapor/ikys_personel_verileri.ods'))

if ikys_verisi.shape == kbs_verisi.shape:
    diff = ikys_verisi.compare(kbs_verisi, align_axis=1, keep_shape=False, keep_equal=True, result_names=('kbs', 'ikys'))
    diff.to_excel('./rapor/ikys_kbs_kontrol_raporu_1.ods')

    #### Raporlarma Versiyon - 2
    ikys_verisi.equals(kbs_verisi)
    comparison_values = ikys_verisi.values == kbs_verisi.values
    rows,cols=np.where(comparison_values==False)
    for item in zip(rows,cols):
        ikys_verisi.iloc[item[0], item[1]] = 'ikys {} --> kbs {}'.format(ikys_verisi.iloc[item[0], item[1]],kbs_verisi.iloc[item[0], item[1]])
    ikys_verisi.to_excel('./rapor/ikys_kbs_kontrol_raporu_2.ods')

else:
    print("rapor klasöründedeki kbs_bordro_verileri.ods dosyası ile ikys_personel_verileri.ods dosyasının satır ve sütunları uyuşmuyor.")


