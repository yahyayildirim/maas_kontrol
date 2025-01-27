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
* 97-İlave Ödeme (375 KHK Ek M.40)

* Beta/deneme/test amaçlı olarak rapor klasöründe ilgili yıl ve ayın içinde emsan veri için txt oluşturma eklenmiştir. Lütfen bu listeleri baz alarak emsan veri göndermeyin sadece test amaçlı üretilmektedir.

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

6- Aşağıdaki kodu uçbirime yazın/kopyalayın ve enter yapın. Bu aşama bilgisayar özelliklerine göre uzun sürebilir, sabredip bitmesini bekleyin.

Python versiyonunuz 3.10'nun altında ise `--break-system-packages` ibaresini aşağıdaki koddan çıkartmayı unutmayın.
```
for i in $(cat moduller.txt);do sudo python3 -m pip install --break-system-packages --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -U $i;done
```
**Önemli Not-1: _Domain kullanıcılarında 6. madde hata verecektir. Bu sebeple harici bir internet ile işlem yapmanız gerekmektedir._**

**Önemli Not-2: _Domain kullanıcıları harici internete bağlandıkları halde gitlab'a bağlanamıyorlarsa /etc/resolv.conf dosyasını açıp nameserver 8.8.8.8 olarak düzenleme yapmaları gerekmektedir._**

## 

# İKYS ÜZERİNDEN YAPILACAKLAR
**[Buradan](https://gitlab.com/yahyayildirim/test/-/raw/main/video_and_picture/maas_kontrol/ornek_ikys_personel_sorgulama.webm)** videoyu izleyerek raporu Masaüstünde bulunan **maas_kontrol/ikys** klasörüne kopyalayın.

**ÖNEMLİ NOT:** İndirdiğiniz dosyayı hiç açmayın, olduğu gibi ikys klasörüne taşıyın/kopyalayın. Eğer dosyanın ismi sadece **Personel** ise **Personel Rapor.xls** olarak değiştirin, bunun dışında hiçbir şekilde ismini veya dosya uzantısını değiştirmeyin.


## 

# KBS ÜZERİNDEN YAPILACAKLAR
**[Buradan](https://gitlab.com/yahyayildirim/test/-/raw/main/video_and_picture/maas_kontrol/ornek_kbs_raporlar.webm)** videoyu izleyerek raporu Masaüstünde bulunan **maas_kontrol/kbs** klasörüne kopyalayın.

**ÖNEMLİ NOT:** Dosya ismini değiştirmenize gerek yoktur. Burada dikkat etmeniz gereken, kbs klasörüne en son indirdiğiniz rapor tek kalsın.

## 

# PROGRAMIN ÇALIŞTIRILMASI
Programı iki yol ile çalıştırbiliriz.
* **1. YOL:** maas_kontrol klasöründe bulunan **calistir.py** dosyasına çift tıklayarak açılan menüden **Uçbirimde Çalıştır** butonuna tıklamak.

* **2. YOL:** maas_kontrol klasöründe uçbirim açıp, `./calistir.py` komutunu çalıştırmak

##

# GÜNCELLEME
* Programı devamlı güncelliyorum. Onun için programı çalıştırmadan önce mutlaka **maas_kontrol** klasörünün içindeyken, sağ tıklayıp burada uç birim aç deyin ve **git pull** ile güncelleme yapın.

##

# SSS
<p>
<details>
<summary><strong>1. Sık sorulan sorular buraya eklenecektir.</strong></summary>

<strong>Cevap:</strong> <em>Bu alanda</em> <strong>görünecek</strong> şekilde yazılacaktır.

<pre><code>Eğer kod var ise burada görünecektir.</code></pre>

</details>
</p>
<p>
<details>
<summary><strong>Banka Listesi Hakkında</strong></summary>

<strong>Cevap:</strong> <em>Bankaların çoğu KBS üzerinden listeyi direk bankaya aktarıyor. Ancak, şu anda sadece <strong>ALBARAKA</strong> bankası için banka listesi oluşturulabilmektedir.</em>
`Eğer sizin çalıştığınız bankada internet üzerinden manuel olarak sisteme eklemenizi istiyor ise bana ilgili excel dosyasını gönderirseniz, ekleme yapmaya çalışırım.`

</details>
</p>
