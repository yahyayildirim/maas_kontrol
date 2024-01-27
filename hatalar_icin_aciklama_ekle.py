#!/usr/bin/env python3

import openpyxl
from openpyxl import load_workbook
from openpyxl.comments import Comment
from datetime import datetime

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

bu_yil = datetime.now().year
bu_ay = datetime.now().strftime("%B")

excel_file = './rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/maas_kontrol_raporu_v2.xlsx' 
wb = load_workbook(excel_file, data_only = True)
sh = wb.worksheets[0]

def _get_column_letter(col_idx):
    if not 1 <= col_idx <= 18278:
        raise ValueError("Hatalı sütun numarası: {0}".format(col_idx))
    letters = []
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx, 26)
        if remainder == 0:
            remainder = 26
            col_idx -= 1
        letters.append(chr(remainder+64))
    return ''.join(reversed(letters))

# satır ve sütunları tek tek kontrol et
for i in range(1, sh.max_row+1):
    for j in range(1, sh.max_column+1):
        ## Arkaplanı kırmızı olan sütunları bul
        if sh.cell(row=i, column=j).fill.start_color.index == 'FFFF0000':
            if sh[f'{_get_column_letter(j-1)}1'].value == "Ek Gösterge":
            #print(sh[f'{_get_column_letter(j-1)}1'], sh[f'{_get_column_letter(j-1)}1'].value)
            #print(sh[f'{_get_column_letter(i)}1'], sh[f'{_get_column_letter(i)}1'].value)
                sh.cell(row=i, column=j).comment = Comment("Personelin ek göstergesi hatalıdır.","")

            if sh[f'{_get_column_letter(j-1)}1'].value == "Gösterge Puanı":
                sh.cell(row=i, column=j).comment = Comment("Personelin; iş güçlüğü, iş riski, teminde güçlük, mali sorumluluk vs. puanında hata var.\n\nEğer ilgili personel taşınır kayıt yetkilisi ise 575 puan fazladan aldığı için hatayı dikkate almayın.","Yahya YILDIRIM")



wb.save('./rapor/' + str(bu_yil) + '/' + str(bu_ay) + '/maas_kontrol_raporu_v3.xlsx')

