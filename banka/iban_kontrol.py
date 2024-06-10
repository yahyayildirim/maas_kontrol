#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True

from colors import red, green, yellow # pip install ansicolors
import os

import locale
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

def country_detect (raw_1):
    global max_leng
    global account_control
    global bank_branch
    global status_sepa
    try:
        country_number = raw_1[0] + raw_1[1]
        country_number = country_number.upper()
    except Exception:
        print(red(f"Eksik veri.!"))
        return exit(1)

    if country_number == "TR":
        country = "Turkey"
        max_leng = 26
        status_sepa = False
        account_control = False
        bank_branch = True 
    else :
        country = "Not detected...!"
        error_satut = True

    return country , max_leng , status_sepa , account_control , bank_branch , country_number
    

def iban_parametres(iban_1):
    global control_number_global 
    global bank_code_local
    global rezerve_code  
    if country_detect(iban_1)[0] == "Turkey":
        try:
            control_number_global = iban_1[2] + iban_1[3]
            bank_code_local = iban_1[4] + iban_1[5] + iban_1[6] + iban_1[7] + iban_1[8]
            rezerve_code = iban_1[9]
            account_number = iban_1[10:26]
            sube_kodu = iban_1[10:14]
            musteri_no = iban_1[13:22]
            hesap_ek_no = iban_1[22:]

        except Exception:
            print(red(f"Eksik veri.!"))
            return exit(1)

        if bank_code_local == "00001":
            bank_name = "TC Merkez Bankası"

        elif bank_code_local == "00004":
            bank_name = "İller Bankası"

        elif bank_code_local == "00010":
            bank_name = "Ziraat Bankası"
            musteri_no = iban_1[15:22]

        elif bank_code_local == "00012":
            bank_name = "Halkbank"
            musteri_no = iban_1[18:26]

        elif bank_code_local == "00015":
            bank_name = "Vakıflar Bankası"
            musteri_no = iban_1[10:26]
            sube_kodu = ""
            hesap_ek_no = ""

        elif bank_code_local == "00017":
            bank_name = "Kalkınma Bankası"

        elif bank_code_local == "00029":
            bank_name = "Birleşik Fon Bankası"

        elif bank_code_local == "00032":
            bank_name = "Türk Ekonomi Bankası"

        elif bank_code_local == "00046":
            bank_name = "Akbank"
            musteri_no = iban_1[18:26]

        elif bank_code_local == "00059":
            bank_name = "Şekerbank"

        elif bank_code_local == "00062":
            bank_name = "Garanti Bankası"
            musteri_no = iban_1[18:26]

        elif bank_code_local == "00064":
            bank_name = "İş Bankası"
            musteri_no = iban_1[18:26]

        elif bank_code_local == "00067":
            bank_name = "Yapı ve Kredi Bankası"
            musteri_no = iban_1[18:26]

        elif bank_code_local == "00099":
            bank_name = "ING Bank"

        elif bank_code_local == "00100":
            bank_name = "Adabank"

        elif bank_code_local == "00111":
            bank_name = "Finansbank"

        elif bank_code_local == "00123":
            bank_name = "HSBC"

        elif bank_code_local == "00132":
            bank_name = "Takasbank"

        elif bank_code_local == "00134":
            bank_name = "Denizbank"

        elif bank_code_local == "00135":
            bank_name = "Anadolu Bank"

        elif bank_code_local == "00137":
            bank_name = "Rabobank"

        elif bank_code_local == "00138":
            bank_name = "Dilerbank"

        elif bank_code_local == "00139":
            bank_name = "GSD Bank"

        elif bank_code_local == "00141":
            bank_name = "Nurol Yatırım Bankası"

        elif bank_code_local == "00142":
            bank_name = "Bankpozitif Kredi ve Kalkınma Bankası"

        elif bank_code_local == "00143":
            bank_name = "Aktif Yatırım Bankası"

        elif bank_code_local == "00146":
            bank_name = "Odea Bank"

        elif bank_code_local == "00147":
            bank_name = "Bank of Tokyo-Mitsubishi UFJ Turkey"

        elif bank_code_local == "00203":
            bank_name = "Albaraka Türk Katılım Bankası"
            musteri_no = iban_1[13:20]

        elif bank_code_local == "00205":
            bank_name = "Kuveyt Türk Katılım Bankası"
            musteri_no = iban_1[13:20]

        elif bank_code_local == "00206":
            bank_name = "Türkiye Finans Katılım Bankası"
            musteri_no = iban_1[13:20]

        elif bank_code_local == "00209":
            bank_name = "Ziraat Katılım Bankası"
            musteri_no = iban_1[13:20]

        elif bank_code_local == "00210":
            bank_name = "Vakıf Katılım Bankası"
            musteri_no = iban_1[13:20]

        elif bank_code_local == "00806":
            bank_name = "Merkezi Kayıt Kuruluşu"
            
        elif bank_code_local == "00109":
            bank_name = "ICBC Turkey Bank"
        else:
            else_proc = "0"
            return else_proc
        #16
    else:
        control_number_global = "DESTEKLENMİYOR"
        bank_code_local =  "DESTEKLENMİYOR"
        rezerve_code = "DESTEKLENMİYOR"
        account_number =  "DESTEKLENMİYOR"
        sube_kodu = "DESTEKLENMİYOR"
        musteri_no = "DESTEKLENMİYOR"
        hesap_ek_no = "DESTEKLENMİYOR"
        bank_name = "DESTEKLENMİYOR"

    return control_number_global, bank_code_local, rezerve_code, account_number, bank_name, sube_kodu, musteri_no, hesap_ek_no

def banka_adi(iban_1):
    return iban_parametres(iban_1)[4]

def sube_kodu(iban_1):
    return iban_parametres(iban_1)[5]

def musteri_no(iban_1):
    return iban_parametres(iban_1)[6]

def hesap_ek_no(iban_1):
    return iban_parametres(iban_1)[7]
