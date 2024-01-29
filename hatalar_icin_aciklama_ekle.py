#!/usr/bin/env python3

import openpyxl
import os
import sys
from glob import glob
from openpyxl import load_workbook
from openpyxl.comments import Comment
from datetime import datetime
import hata_kodlari

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

bu_yil = datetime.now().year
bu_ay = datetime.now().strftime('%B')

bu_dizin = os.path.dirname(__file__) + '/rapor/'
excel_file =glob(bu_dizin.replace('./', '') + str(bu_yil) + '/' + str(bu_ay) + '/maas_kontrol_raporu_v2.xlsx')

wb = load_workbook(''.join(excel_file), data_only = True)
sh = wb.worksheets[0]

def _get_column_letter(col_idx):
    if not 1 <= col_idx <= 50:
        raise ValueError('Hatalı sütun numarası: {0}'.format(col_idx))
    letters = []
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx, 26)
        if remainder == 0:
            remainder = 26
            col_idx -= 1
        letters.append(chr(remainder+64))
    return ''.join(reversed(letters))

def aciklama_ekle():
    # satır ve sütunları tek tek kontrol et
    for i in range(1, sh.max_row+1):
        for j in range(1, sh.max_column+1):
            ## Arkaplanı kırmızı olan sütunları bul
            if sh.cell(row=i, column=j).fill.start_color.index != '00000000':
                #print(sh[f'{_get_column_letter(j-1)}1'], sh[f'{_get_column_letter(j-1)}1'].value)
                #print(sh[f'{_get_column_letter(i)}1'], sh[f'{_get_column_letter(i)}1'].value)
                if sh[f'{_get_column_letter(j-1)}1'].value == 'Adı Soyadı':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.ad_soyad_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Sınıf':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.sinif_hata}', '')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Unvan':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.unvan_hata}', '')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Derece':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.derece_hata}', '')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Kademe':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.kademe_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Gösterge Puanı':
                    sh.cell(row=i, column=j).comment =Comment(f'{hata_kodlari.gosterge_puani_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Aylık Tutar':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.aylik_tutar_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Ek Gösterge':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.ek_gosterge_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Ek Gös.Ay.':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.ek_gos_ayligi_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Yan Ödeme':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.yan_odeme_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Yan Ödeme Aylık':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.yan_odeme_aylik_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Ek Tazminat Puanı':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.ek_tazminat_puani_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Özel Hiz. Taz. Puanı':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.ozel_hiz_taz_puani_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Özel Hiz.Taz.':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.ozel_hiz_taz_tutar_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == '666 KHK Oranı':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.khk_666_puani_hata}','')

                if sh[f'{_get_column_letter(j-1)}1'].value == 'Ek Öde.(666 KHK':
                    sh.cell(row=i, column=j).comment = Comment(f'{hata_kodlari.khk_666_tutar_hata}','')

    wb.save('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/maas_kontrol_raporu_v3_test.xlsx')
    print('%100')
    x = input('İşleminiz başarılı bir şekilde tamamlanmıştır.\nPencereyi kapatmak için enter tuşa basın.')
    sys.exit(x)


if __name__ == '__main__':
    aciklama_ekle()