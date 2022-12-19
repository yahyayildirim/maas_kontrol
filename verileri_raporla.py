#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import numpy as np
import pandas as pd

# KBS ve İKYS verilerini DataFrame ekliyoruz.
kbs_verisi = pd.DataFrame(pd.read_excel('./kbs/kbs_bordro_verileri.xlsx'))
ikys_verisi = pd.DataFrame(pd.read_excel('./ikys/ikys_personel_verileri.xlsx'))

# KBS Sisteminde bilgisi bulunup, İKYS Sisteminde kaydı bulunmayan Personel
kbs_in_ikys_out = kbs_verisi[~kbs_verisi['TC Kimlik'].isin(ikys_verisi['TC Kimlik'])]
kbs_in_ikys_out.to_excel('./rapor/kbsde_olup_ikysde_olmayanlar.xlsx', index=False, header=True, freeze_panes=(1,0))

# İKS Sisteminde bilgisi bulunup, KBS Sisteminde kaydı bulunmayan Personel
ikys_in_kbs_out = ikys_verisi[~ikys_verisi['TC Kimlik'].isin(kbs_verisi['TC Kimlik'])]
ikys_in_kbs_out.to_excel('./rapor/ikysde_olup_kbsde_olmayanlar.xlsx', index=False, header=True, freeze_panes=(1,0))

ikys_kbs_esitle = ikys_verisi.loc[ikys_verisi['TC Kimlik'].isin(kbs_verisi['TC Kimlik'])]
ikys_kbs_esitle.to_excel('./ikys/ikys_personel_verileri.xlsx', index=False, header=True, freeze_panes=(1,0))

kbs_ikys_esitle = kbs_verisi.loc[kbs_verisi['TC Kimlik'].isin(ikys_verisi['TC Kimlik'])]
kbs_ikys_esitle.to_excel('./kbs/kbs_bordro_verileri.xlsx', index=False, header=True, freeze_panes=(1,0))

print('4. KBS sisteminde bulunup, İKYS sisteminde olmayan personel raporu hazırlandı...')
print('5. İKYS sisteminde bulunup, KBS sisteminde olmayan personel raporu hazırlandı...')