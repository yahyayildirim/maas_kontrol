# MAAŞ KONTROL PROGRAMI

```
Bu programın amacı, İKYS ve KBS Sisteminden aldığımız raporlaro karşılaştırarak hata olup olmadığını kontrol etmek amacıyla yazılmıştır.

```


# ÖN HAZIRLIK
* Başta belirtmem gerikir ki Python versiyonunun 3.7 ve üzeri olması gerekiyor.
* Masaüstündeyken sağ tık yaparak `Burada Uçbirim Aç`a tıklıyoruz.
* 
```
sudo apt install -yy git python3-pip
```
yazıp enter yapın.
* 
```
sudo python3 -m pip install -U -r moduller.txt
```
komutu ile gerekli olan kütüphanleri kuruyoruz.
* `git clone https://gitlab.com/yahyayildirim/maas_kontrol.git` ile programı indiriyoruz.
* Şimdi Masaüstünde maas_kontrol adında bir klasör oluşmuş olması gerekiyor.


# İKYS ÜZERİNDEN YAPILACAKLAR
* Masaüstünde bulunan **maas_kontrol/izle** klasöründeki **ornek_ikys_personel_sorgulama.webm** videoyu izleyin.


# KBS ÜZERİNDEN YAPILACAKLAR
* Masaüstünde bulunan **maas_kontrol/izle** klasöründeki **ornek_kbs_raporlar.webm** videoyu izleyin.


# PROGRAMIN ÇALIŞTIRILMASI
* Programı iki yol ile çalıştırbiliriz.
### 1. YOL:
* **maas_kontrol** klasöründe uçbirim açıp, `./Program_Calistir.py` komutunu çalıştırmak

### 2. YOL:
* **maas_kontrol** klasöründe bulunan **Program_Calistir.py** dosyasına çift tıklayarak açılan menüden **Uçbirimde Çalıştır** butonuna tıklamak.
