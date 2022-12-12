# MAAŞ KONTROL PROGRAMI

```
Bu programın amacı, İKYS ve KBS Sisteminden aldığımız raporları karşılaştırarak hata olup
olmadığını kontrol etmek amacıyla yazılmıştır.

```

## 

# ÖN HAZIRLIK
1- Başta belirtmem gerikir ki Python versiyonunun 3.7 ve üzeri olması gerekiyor.

2- Masaüstündeyken sağ tık yaparak `Burada Uçbirim Aç`a tıklıyoruz.

3- Aşağıdaki kodu uçbirime kopyalayın ve enter yapın.
```
sudo apt install -yy git python3-pip
```
4- Aşağıdaki kodu uçbirime kopyalayın ve enter yapın.
```
sudo python3 -m pip install -U -r moduller.txt
```
5- Aşağıdaki kodu uçbirime kopyalayın ve enter yapın.
```
git clone https://gitlab.com/yahyayildirim/maas_kontrol.git
```
6- Şimdi Masaüstünde **maas_kontrol** adında bir klasör oluşmuş olması gerekiyor.

## 

# İKYS ÜZERİNDEN YAPILACAKLAR
Masaüstünde bulunan **maas_kontrol/izle** klasöründeki **ornek_ikys_personel_sorgulama.webm** videoyu izleyin.

## 

# KBS ÜZERİNDEN YAPILACAKLAR
Masaüstünde bulunan **maas_kontrol/izle** klasöründeki **ornek_kbs_raporlar.webm** videoyu izleyin.

## 

# PROGRAMIN ÇALIŞTIRILMASI
Programı iki yol ile çalıştırbiliriz.
* **1. YOL:** maas_kontrol klasöründe uçbirim açıp, `./Program_Calistir.py` komutunu çalıştırmak

* **2. YOL:** maas_kontrol klasöründe bulunan **Program_Calistir.py** dosyasına çift tıklayarak açılan menüden **Uçbirimde Çalıştır** butonuna tıklamak.
