# MAAŞ KONTROL PROGRAMI

```
Bu programın amacı, İKYS ve KBS Sisteminden aldığımız raporları karşılaştırarak hata olup
olmadığını kontrol etmek amacıyla yazılmıştır.

```
Bu program ile; İKYS ve KBS sistemlerinde bulunan aşağıdaki veriler karşılaştırılır.
* T.C. Kimlik No
* Adı ve Soyad
* Unvan
* Hizmet Sınıfı
* Derece
* Kademe
* Yan Ödeme	Puanı
* Aylık Tutar
* Ek Gösterge
* Ek Gösterge Tutarı
* Gösterge Puanı (İş güç., teminde güç., mali sorum. vs.)
* Gösterge Tutarı
* Ek Tazminat Puanı
* Özel Hizmet Tazminatı Puanı
* Özel Hizmet Tazminatı Tutarı
* 666 KHK Puanı
* 666 KHK Tutarı

Şimdilik bunlar, Kıdem Yılını ve buna bağlı olarak ödenen Kıdem Aylık Tutarını maalesef ekleyemiyorum. Çünkü; İKYS ve KBS'deki hizmet süreleri bir birini tutmuyor. Diyanete Başlama Tarihi ve İlk Göreve Başlama Tarihlerini ayrı ayrı denememe rağmen, olumlu sonuç alamadım.

## 

# ÖN HAZIRLIK
1- Başta belirtmem gerikir ki bu programın sağlıklı çalışabilmesi için Python versiyonunun 3.7 ve üzeri olması gerekiyor.

2- Masaüstündeyken sağ tık yaparak `Burada Uçbirim Aç`a tıklıyoruz.

3- Aşağıdaki kodu uçbirime kopyalayın ve enter yapın.
```
sudo apt install -yy git python3-pip
```
4- Aşağıdaki kodu uçbirime kopyalayın ve enter yapın.
```
git clone https://gitlab.com/yahyayildirim/maas_kontrol.git
```
5- Şimdi Masaüstünde **maas_kontrol** adında bir klasör oluşmuş olması gerekiyor. `cd maas_kontrol` komutu ile klasöre geçiş yapın.

6- Aşağıdaki kodu uçbirime yazın/kopyalayın ve enter yapın.
```
sudo python3 -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -U -r moduller.txt
```
**Önemli Not: _Domain kullanıcılarında 6. madde hata verir ise harici bir internet ile işlem yapmaları gerekiyor._**

## 

# İKYS ÜZERİNDEN YAPILACAKLAR
Masaüstünde bulunan **maas_kontrol/izle** klasöründeki **ornek_ikys_personel_sorgulama.webm** videoyu izleyin.
* **ÖNEMLİ NOT:** İndirdiğiniz dosyayı hiç açmayın, olduğu gibi ikys klasörüne taşıyın/kopyalayın. Hiçbir şekilde ismini veya dosya uzantısını değiştirmeyin.


## 

# KBS ÜZERİNDEN YAPILACAKLAR
Masaüstünde bulunan **maas_kontrol/izle** klasöründeki **ornek_kbs_raporlar.webm** videoyu izleyin.
* **ÖNEMLİ NOT:** Dosya ismini değiştirmenize gerek yoktur. Burada dikkat etmeniz gereken, kbs klasörüne indirdiğiniz dosyaların ilk indirileni baz alınır. Onun için gereksiz olan veya güncel olmayanı silin. En son indirdiğiniz tek kalsın.

## 

# PROGRAMIN ÇALIŞTIRILMASI
Programı iki yol ile çalıştırbiliriz.
* **1. YOL:** maas_kontrol klasöründe uçbirim açıp, `./calistir.py` komutunu çalıştırmak

* **2. YOL:** maas_kontrol klasöründe bulunan **calistir.py** dosyasına çift tıklayarak açılan menüden **Uçbirimde Çalıştır** butonuna tıklamak.

##

# GÜNCELLEME
* Programı devamlı güncelliyorum. Onun için programı çalıştırmadan önce mutlaka **maas_kontrol** klasörünün içinde uç birim açıp **git pull** ile güncelleme yapın.

##

# SSS
<p>
<details>
<summary><strong>1. Sık sorulan sorular buraya eklenecektir.</strong></summary>

Cevap: <em>Bu alanda</em> <strong>görünecek</strong> şekilde yazılacaktır.

<pre><code>Eğer kod var ise burada görünecektir.</code></pre>

</details>
</p>
