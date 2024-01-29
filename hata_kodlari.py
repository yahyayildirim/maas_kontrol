"""
Maaş Kontrol Programı tarafıdan üretilen kontrol raporunda alınan kırmızı renkli hatalar için bilgilendirici
ve hatanın giderilmesi için personele yol göstermek amaçlanmaktadır. Buraya eklenecek hatalar için türkçe dil
kurallarına azami derece uyulması gerekiyor. 
"""

ad_soyad_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personel isim/soyisim değişikliği yapmış olabilir. KBS/İKYS'den güncelleyiniz.
2- Personel evlenmiş/boşanmış olabilir. KBS/İKYS'den güncelleyiniz.
3- Personelin isminde/soyismin herhangi bir harf hatası olabilir. KBS/İKYS'den güncelleyiniz.
"""

sinif_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personelin hizmet sınıfı değişmiş ama KBS'den güncellenmemiş olabilir.
2- vb.
"""

unvan_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personel, unvan bilgisi KBS'ye hatalı işlenmiş olabilir.
2- Personel, unvan değişikliği yapmış ama KBS'den güncellenmemiş olabilir.
3- vb.
"""

derece_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personel, İKYS üzerinden derece terfi almış ama KBS'ye işlenmemiş olabilir.
2- vb.
"""

kademe_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personel, İKYS üzerinden kademe ilerlemesi almış ama KBS'ye işlenmemiş olabilir.
2- vb.
"""

gosterge_puani_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Gösterge Puanı derece/kademeye göre belirlenmektedir. Dereceyi/Kademeyi düzeltiniz.
2- vb.
"""

aylik_tutar_hata ="Gösterge Puanı hatalı olunca bu alanda hata vermektedir."

ek_gosterge_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personelin eğitim durumunu kontrol ediniz.
2- Personele İKYS üzerinden derece terfi yapılmış ama KBS sistemine işlenmemiş olabilir.
3- vb.
"""

ek_gos_ayligi_hata ="Ek Gösterge Puanı hatalı olunca bu alanda hata vermektedir."

yan_odeme_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Taşınır Kayıt Yetkilisine 575 puan mali sorumluluk puanı verilmektedir. Bu bir hata değildir. İKYS sisteminde bunu karşılaştıracağımız bir veri olmadığı için program hata olarak algılamaktadır.
2- Personel, unvan değişikliği yapmış olabilir.
3- VHKİ olarak görev yapmakta iken, ŞEF unvanına geçen biri, VHKİ görevini de yürütüyor ise 2250 puan alır. Bunu göz önünde bulundurunuz.
"""

yan_odeme_aylik_hata ="Yan Ödeme Puanı hatalı olunca bu alanda hata vermektedir."

ek_tazminat_puani_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personelin kariyer unvanına sahip olup olmadığını KBS/İKS'den kontrol ediniz.
"""

ozel_hiz_taz_puani_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Personelin derecesini ve eğitim durumunu kontrol ediniz.
2- Toplu Sözleşme ile bazı unvanlara ek özel hizmet tazminatı puanı verilmektedir. KBS üzerinden kontrol ediniz.
3- vb.
"""

ozel_hiz_taz_tutar_hata ="Özel Hizmet Tazminat Puanı hatalı olunca bu alanda hata vermektedir. ÖHT Puanını düzeltiniz."

khk_666_puani_hata ="""MUHTEMEL HATA SEBEPLERİ:
1- Toplu Sözleşme ile bazı unvanlara ek puanlar verilmektedir. KBS üzerinden kontrol ediniz.
2- KBS'den indirdiğimiz ve maas_kontrol/kbs/ klasörüne kopyaladığımız excel dosyasının son satırında bulunan personelin bilgileri eksik olduğu için bu hatayı vermiş olabilir. Bu durum sadece son satırdaki personel için geçerlidir ve hata olarak görmeyiniz.
3- vb.
"""

khk_666_tutar_hata ="666 Sayılı KHK ile personele verilen puanı kontrol ediniz. Puanı düzeltilise, bu alanda düzelecektir."

