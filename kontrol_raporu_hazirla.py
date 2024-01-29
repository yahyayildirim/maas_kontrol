#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

import numpy as np
import pandas as pd
import time
from datetime import datetime

bu_yil = datetime.now().year
bu_ay = datetime.now().strftime("%B")

# KBS ve İKYS verilerini DataFrame ekliyoruz.
kbs_verisi = pd.DataFrame(pd.read_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/kbs_bordro_verileri.xlsx'))
ikys_verisi = pd.DataFrame(pd.read_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/ikys_personel_verileri.xlsx'))

def kontrol_raporu_v1():
    if ikys_verisi.shape == kbs_verisi.shape:
        #### Raporlama Versiyon-1
        kbs = ikys_verisi[~ikys_verisi.apply(tuple, 1).isin(kbs_verisi.apply(tuple, 1))]
        ikys = kbs_verisi[~kbs_verisi.apply(tuple, 1).isin(ikys_verisi.apply(tuple, 1))]
        df_all = pd.concat([kbs.set_index('TC Kimlik'), ikys.set_index('TC Kimlik')], axis='columns', keys=['ikys verisi', 'kbs verisi'])
        df_final = df_all.swaplevel(axis='columns')[kbs_verisi.columns[1:]]
        def arkaplani_renklendir(data, color='red'):
            renk = 'background-color: {}'.format(color)
            veri = data.xs(key='ikys verisi', axis='columns', level=1)
            return pd.DataFrame(np.where(data.ne(veri, level=0), renk, ''), index=data.index, columns=data.columns)
        df_final.style.apply(arkaplani_renklendir, axis=None).to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/maas_kontrol_raporu_v1.xlsx', engine='openpyxl', freeze_panes=(2,1))
        print('%90')
    else:
        print('maas_kontrol_raporu_v1 hazırlanırken hata oluştu...\nLütfen telegramdan, yazılımcı ile iletişime geçin. @yahyayildirim')
        time.sleep(5)

def kontrol_raporu_v2():
    if ikys_verisi.shape == kbs_verisi.shape:
        #### Raporlama Versiyon-2
        #kbs_verisi.reset_index(drop=True, inplace=True)
        #ikys_verisi.reset_index(drop=True, inplace=True)
        if ikys_verisi['Adı Soyadı'].equals(kbs_verisi['Adı Soyadı']):
            kbs_verisi.set_index('Adı Soyadı', inplace=True)
            ikys_verisi.set_index('Adı Soyadı', inplace=True)
        else:
            kbs_verisi.set_index('TC Kimlik', inplace=True)
            ikys_verisi.set_index('TC Kimlik', inplace=True)

        #df_fark = kbs_verisi.compare(ikys_verisi, align_axis=1, keep_shape=False, keep_equal=True)
        df_fark = ikys_verisi.compare(kbs_verisi, align_axis=1, keep_shape=False, keep_equal=True).rename(columns={'self': 'ikys verisi', 'other': 'kbs verisi'}, level=-1)

        def arkaplani_renklendir(data, color='red'):
            renk = 'background-color: {}'.format(color)
            veri = data.xs(key='ikys verisi', axis='columns', level=1)
            df_rapor = pd.DataFrame(np.where(data.ne(veri, level=0), renk, ''), index=data.index, columns=data.columns)
            return df_rapor

        df_fark.style.apply(arkaplani_renklendir, axis=None).to_excel('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/maas_kontrol_raporu_v2.xlsx', engine='openpyxl', freeze_panes=(2,1))
        print('%95')

    else:
        print('maas_kontrol_raporu_v2 hazırlanırken hata oluştu...\nLütfen telegramdan, yazılımcı ile iletişime geçin. @yahyayildirim')
        time.sleep(5)

if __name__ == '__main__':
    kontrol_raporu_v1()
    kontrol_raporu_v2()