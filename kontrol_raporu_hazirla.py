#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import numpy as np
import pandas as pd
import time

# KBS ve İKYS verilerini DataFrame ekliyoruz.
kbs_verisi = pd.DataFrame(pd.read_excel('./kbs/kbs_bordro_verileri.xlsx'))
ikys_verisi = pd.DataFrame(pd.read_excel('./ikys/ikys_personel_verileri.xlsx'))

if ikys_verisi.shape == kbs_verisi.shape:
    #### Raporlama Versiyon-3

    kbs = ikys_verisi[~ikys_verisi.apply(tuple, 1).isin(kbs_verisi.apply(tuple, 1))]
    ikys = kbs_verisi[~kbs_verisi.apply(tuple, 1).isin(ikys_verisi.apply(tuple, 1))]

    df_all = pd.concat([kbs.set_index('TC Kimlik'), ikys.set_index('TC Kimlik')], axis='columns', keys=['ikys verisi', 'kbs verisi'])
    df_final = df_all.swaplevel(axis='columns')[kbs_verisi.columns[1:]]

    def arkaplani_renklendir(data, color='red'):
        renk = 'background-color: {}'.format(color)
        veri = data.xs(key='ikys verisi', axis='columns', level=1)
        return pd.DataFrame(np.where(data.ne(veri, level=0), renk, ''), index=data.index, columns=data.columns)
    df_final.style.apply(arkaplani_renklendir, axis=None).to_excel('./rapor/maas_kontrol_raporu.xlsx', engine='openpyxl', freeze_panes=(2,2))
    print('5. Maaş Kontrol Raporu başarılı bir şekilde hazırlandı...')
    print('Artık uçbirimi kapatıp, /rapor/ klasörüne bakabilirsiniz...')
    time.sleep(20)
else:
    print('Birşeyler ters gitti... Lütfen telegramdan, yazılımcı ile iletişime geçin. @yahyayildirim')
    time.sleep(60)