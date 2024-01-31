"""
Maaş Kontrol Programı tarafıdan üretilen kontrol raporunda alınan kırmızı renkli hatalar için bilgilendirici
ve hatanın giderilmesi için personele yol göstermek amaçlanmaktadır. Buraya eklenecek hatalar için türkçe dil
kurallarına azami derece uyulması gerekiyor. 
"""

ad_soyad_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personel isim/soyisim değişikliği yapmış olabilir. KBS/İKYS'den güncelleyiniz.
2- Personel evlenmiş/boşanmış olabilir. KBS/İKYS'den güncelleyiniz.
3- Personelin isim veya soyisminde herhangi bir harf hatası olabilir. KBS/İKYS'den güncelleyiniz.
"""

sinif_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personelin hizmet sınıfı değişmiş ama KBS'den güncellenmemiş olabilir.
2- vb.
"""

unvan_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personelin unvan bilgisi KBS'ye hatalı işlenmiş olabilir.
2- Personel, unvan değişikliği yapmış ama KBS'den güncellenmemiş olabilir.
3- vb.
"""

derece_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personel, İKYS üzerinden derece terfi almış ama KBS'ye işlenmemiş olabilir.
2- Terfi tarihini kontrol ediniz, terfi tarihi bir sonraki maaş dönemi olabilir, 
   Örnek: 15.01.2024 terfi tarihi olan bir personelin terfisi, Şubat maaşında KBS'ye işlenir.
"""

kademe_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personel, İKYS üzerinden derece terfi almış ama KBS'ye işlenmemiş olabilir.
2- Terfi tarihini kontrol ediniz, terfi tarihi bir sonraki maaş dönemi olabilir, 
   Örnek: 15.01.2024 terfi tarihi olan bir personelin terfisi, Şubat maaşında KBS'ye işlenir.
"""

gosterge_puani_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Gösterge Puanı derece/kademeye göre belirlenmektedir. Dereceyi/Kademeyi kontrol ediniz, eğer hata var ise düzeltiniz.
2- Hata terfiden kaynaklanıyor ise Terfi menüsüne girerek düzeltiniz.
3- Hatanın terfi menüsünden düzeltme imkanı yok ise ön yüzden düzeltiniz.
"""

aylik_tutar_hata ="Gösterge Puanı hatalı olunca bu alanda hata vermektedir. Puanı düzeltirseniz, bu alanda düzelecektir."

ek_gosterge_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personele İKYS üzerinden derece terfi yapılmış ama KBS sistemine işlenmemiş olabilir.
2- Maaş döneminden sonra diploma İKYS'ye işlenmiş olabilir, kontrol ediniz.
3- Bu alandaki hata, emekli keseneklerini etkilediği için dikkatli ve titizlikle inceleme yapılmalıdır.
4- Hatanın sebebi tam olarak tespit edilmeden işlem yapılmamalıdır.
5- Personelin istisnai bir durumu olabilir. (İl Müftülüğü Terfi Bürosu ile iletişime geçin)
"""

ek_gos_ayligi_hata ="Ek Gösterge Puanı hatalı olunca bu alanda hata vermektedir. Ek göstergeyi düzeltirseniz, bu alanda düzelecektir."

yan_odeme_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Taşınır Kayıt Yetkilisine 575 puan mali sorumluluk puanı verilmektedir. Bu bir hata değildir. İKYS sisteminde bunu karşılaştıracağımız bir veri olmadığı için program hata olarak algılamaktadır.
2- Personel, unvan değişikliği yapmış olabilir.
3- VHKİ olarak görev yapmakta iken, ŞEF unvanına geçen biri, VHKİ görevini de yürütüyor ise 2250 puan alır. Bunu göz önünde bulundurunuz.
4- Diğer durumlarda Yan Ödeme Kararnamesine bakarak ilgili personelin alması gerektiği tazminat oranını kontrol ediniz.
   https://www.resmigazete.gov.tr/eskiler/2006/05/20060505-1.htm
"""

yan_odeme_aylik_hata ="Yan Ödeme Puanı hatalı olunca bu alanda hata vermektedir. Puanı düzeltirseniz, bu alanda düzelecektir."

ek_tazminat_puani_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personelin kariyer unvanına sahip olup olmadığını KBS/İKS'den kontrol ediniz.
2- Uzman veya Baş unvanlı personelin ek tazmnat oranaları, ilgili tazminat kararnamesi ve Toplu Sözleşmeye göre belirlenmektedir.

2024 Yılı için;
Uzman Vaiz, Uzman İ.H, K.K uzman Öğreticisi, Baş Müezzin
1-2 Derecede olanlar : 25
Diğerleri            : 20

Baş Vaiz, Baş İ.H, K.K. Baş Öğreticisi
1-2 Derecede olanlar : 50
Diğerleri            : 40
"""

ozel_hiz_taz_puani_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personelin derecesini ve eğitim durumunu kontrol ediniz.
2- Toplu Sözleşme ile bazı unvanlara ek özel hizmet tazminatı puanı verilmektedir. İlgili dönem toplu sözleşmeye göre verilen puanlar KBS'ye merkez tarafından yüklenmektedir. Buna göre bu oranı KBS üzerinden kontrol ediniz.
3- Bu tutar 5510'a tabi personelin emekli keseneğini etkilediği için titizlikle kontrol edilmelidir.
"""

ozel_hiz_taz_tutar_hata ="Özel Hizmet Tazminat Puanı hatalı olunca bu alanda hata vermektedir. Puanı düzeltirseniz, bu alanda düzelecektir."

khk_666_puani_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Toplu Sözleşme ile bazı unvanlara ek puanlar verilmektedir.İlgili dönem toplu sözleşmeye göre verilen puanlar KBS'ye merkez tarafından yüklenmektedir. Buna göre bu oranı KBS üzerinden kontrol ediniz.
2- KBS'den indirdiğimiz ve maas_kontrol/kbs/ klasörüne kopyaladığımız excel dosyasının son satırında bulunan personelin bilgileri eksik olduğu için bu hatayı vermiş olabilir. Bu durum sadece (bordronun) son satırdaki personel için geçerlidir ve hata olarak görmeyiniz.
3- KBS, naklen gelen personelin Ek 666 KHK tazminatını silmektedir. Naklen gelen personelde bu özellikle kontrol edilmelidir. kontrol edilmesi için KBS ön yüzden Diğer Tazminatlar menüsüne bakılmalıdır, eğer bu menü boş ise KBS ön yüzden bütün veriler seçilerek ön yüzden kaydet yapılmalıdır.
"""

khk_666_tutar_hata ="666 Sayılı KHK ile personele verilen puan hatalı olunca bu alanda hata vermektedir. Puanı düzeltirseniz, bu alanda düzelecektir."
