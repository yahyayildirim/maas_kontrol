"""
Maaş Kontrol Programı tarafıdan üretilen kontrol raporunda alınan kırmızı renkli hatalar için bilgilendirici
ve hatanın giderilmesi için personele yol göstermek amaçlanmaktadır. Buraya eklenecek hatalar için türkçe dil
kurallarına azami derece uyulması gerekiyor. 
"""

ad_soyad_hata = [
   "Personel isim/soyisim değişikliği yapmış olabilir. KBS/İKYS'den güncelleyiniz.",
   "Personel evlenmiş/boşanmış olabilir. KBS/İKYS'den güncelleyiniz.",
   "Personelin isim veya soyisminde herhangi bir harf hatası olabilir. KBS/İKYS'den güncelleyiniz.",
]

sinif_hata = [
   "Personelin hizmet sınıfı değişmiş ama KBS'den güncellenmemiş olabilir.",
]

unvan_hata = [
   "Personelin unvan bilgisi KBS'ye hatalı işlenmiş olabilir.",
   "Personel, unvan değişikliği yapmış ama KBS'den güncellenmemiş olabilir.",
   "Personel vekil ise hata verebilir, dikkate almayınız."
]

derece_kademe_hata = [
   "Personel, İKYS üzerinden derece/kademe terfi almış ama KBS'ye işlenmemiş olabilir.",
   "Personelin terfisi yapılmış, ancak terfi tarihi henüz gelmediği için sisteme yansımamış olabilir.",
   "Terfi tarihini kontrol ediniz, terfi tarihi bir sonraki maaş dönemi olabilir.", 
   "Örnek: 15.01.2024 terfi tarihi olan bir personelin terfisi, Şubat maaşında KBS'ye işlenir.",
]

gosterge_puani_hata = [
   "Gösterge Puanı derece/kademeye göre belirlenmektedir. Dereceyi/Kademeyi kontrol ediniz, eğer hata var ise düzeltiniz.",
   "Hata terfiden kaynaklanıyor ise Terfi menüsüne girerek düzeltiniz.",
   "Hatanın terfi menüsünden düzeltme imkanı yok ise ön yüzden düzeltiniz.",
]

aylik_tutar_hata = [
   "Gösterge Puanı hatalı olunca bu alanda hata vermektedir. Puanı düzeltirseniz, bu alanda düzelecektir.",
]

ek_gosterge_hata = [
   "Personele İKYS üzerinden derece terfi yapılmış ama KBS sistemine işlenmemiş olabilir.",
   "Maaş döneminden sonra diploma İKYS'ye işlenmiş olabilir, kontrol ediniz.",
   "Bu alandaki hata, emekli keseneklerini etkilediği için dikkatli ve titizlikle inceleme yapılmalıdır.",
   "Hatanın sebebi tam olarak tespit edilmeden işlem yapılmamalıdır.",
   "Personelin istisnai bir durumu olabilir. (İl Müftülüğü Terfi Bürosu ile iletişime geçin)",
]

ek_gos_ayligi_hata = [
   "Ek Gösterge Puanı hatalı olunca bu alanda hata vermektedir. Ek göstergeyi düzeltirseniz, bu alanda düzelecektir.",
]

yan_odeme_hata = [
   "Taşınır Kayıt Yetkilisine 575 puan mali sorumluluk puanı verilmektedir. Bu bir hata değildir. İKYS sisteminde bunu karşılaştıracağımız bir veri olmadığı için program hata olarak algılamaktadır.",
   "Personel, unvan değişikliği yapmış olabilir.",
   "Personel ay içerisinde rapor almış olabilir, kontrol ediniz.",
   "VHKİ olarak görev yapmakta iken, ŞEF unvanına geçen biri, VHKİ görevini de yürütüyor ise 2250 puan alır. Bunu göz önünde bulundurunuz.",
   "Diğer durumlarda Yan Ödeme Kararnamesine bakarak ilgili personelin alması gerektiği tazminat oranını kontrol ediniz.\nhttps://www.resmigazete.gov.tr/eskiler/2006/05/20060505-1.htm",
   "Tekniker ve Teknisyen unvanlarında sadece MYO olarak sorgulama yapılmaktadır. Personeliniz Meslek lisesi mezunu ise kontrolünü tazminat cetveline göre yapınız.",
]

yan_odeme_aylik_hata = [
   "Yan Ödeme Puanı hatalı olunca bu alanda hata vermektedir. Puanı düzeltirseniz, bu alanda düzelecektir.",
]

ek_tazminat_puani_hata = [
   "Personelin kariyer unvanına sahip olup olmadığını KBS/İKS'den kontrol ediniz.",
   "Baş ve Uzman unvanlı personelin ek tazminat oranaları, ilgili tazminat kararnamesi ve Toplu Sözleşmeye göre belirlenmektedir.",
   "KBS üzerinden Diğer Tazminat alanında giriş yapılması gerekmektedir. Kontrol ediniz.",
"""
2026 Yılı için;
Baş Vaiz, Baş İ.H, K.K. Baş Öğreticisi
1-2 Derecede olanlar : 55
Diğerleri            : 45

Uzman Vaiz, Uzman İ.H, K.K uzman Öğreticisi, Baş Müezzin
1-2 Derecede olanlar : 30
Diğerleri            : 25
"""
]

ozel_hiz_taz_puani_hata = [
   "Personelin derecesini ve eğitim durumunu kontrol ediniz.",
   "Personel ay içerisinde rapor almış olabilir, kontrol ediniz.",
   "Toplu Sözleşme ile bazı unvanlara ek özel hizmet tazminatı puanı verilmektedir. İlgili dönem toplu sözleşmeye göre verilen puanlar KBS'ye merkez tarafından yüklenmektedir. Buna göre bu oranı KBS üzerinden kontrol ediniz.",
   "Bu tutar 5510'a tabi personelin emekli keseneğini etkilediği için titizlikle kontrol edilmelidir.",
   "Diğer durumlarda aşağıdaki linklerden kontrol sağlayınız.",
   "Devlet Memurlarına Ödenecek Zam ve Tazminatlara İlişkin Kararlar:\nhttps://www.hmb.gov.tr/bumko-kamu-personel-mevzuati",
   "Kamu Görevlilerinin Geneline ve Hizmet Kollarına Yönelik Mali ve Sosyal Haklara İlişkin Toplu Sözleşmeler:\nhttps://pdb.ibu.edu.tr/tr/page/toplu-sozlesmeler/9624"
]

ozel_hiz_taz_tutar_hata = [
   "Özel Hizmet Tazminat Puanı hatalı olunca bu alanda hata vermektedir. Puanı düzeltirseniz, bu alanda düzelecektir.",
]

khk_666_puani_hata = [
   "KBS'den indirdiğimiz ve excel dosyasının son satırında bulunan personelin bilgileri eksik olduğu için bu hatayı vermiş olabilir. Bu durum sadece (bordronun) son satırdaki personel için geçerlidir ve hata olarak görmeyiniz.",
   "Toplu Sözleşme ile bazı unvanlara ek puanlar verilmektedir.İlgili dönem toplu sözleşmeye göre verilen puanlar KBS'ye merkez tarafından yüklenmektedir. Buna göre bu oranı KBS üzerinden kontrol ediniz.",
   "KBS, naklen gelen personelin Ek 666 KHK tazminatını silmektedir. Naklen gelen personelde bu özellikle kontrol edilmelidir. kontrol edilmesi için KBS ön yüzden Diğer Tazminatlar menüsüne bakılmalıdır, eğer bu menü boş ise KBS ön yüzden bütün veriler seçilerek ön yüzden kaydet yapılmalıdır.",
   "Diğer durumlarda 375 Sayılı Kararnameye bakarak ilgili unvanın alması gerektiği tazminat oranını kontrol ediniz.\nhttps://www.mevzuat.gov.tr/mevzuat?MevzuatNo=375&amp;MevzuatTur=4&amp;MevzuatTertip=5",
]

khk_666_tutar_hata = [
   "KBS'den indirdiğimiz ve excel dosyasının son satırında bulunan personelin bilgileri eksik olduğu için bu hatayı vermiş olabilir. Bu durum sadece (bordronun) son satırdaki personel için geçerlidir ve hata olarak görmeyiniz.",
   "666 Sayılı KHK ile personele verilen puan hatalı olunca bu alanda hata vermektedir. Puanı düzeltirseniz, bu alanda düzelecektir.",
]

ilave_odeme_hata = [
   "KBS'den indirdiğimiz ve excel dosyasının son satırında bulunan personelin bilgileri eksik olduğu için bu hatayı vermiş olabilir. Bu durum sadece (bordronun) son satırdaki personel için geçerlidir ve hata olarak görmeyiniz.",
   'Herhangi bir nedenle 97-İlave Ödeme (375 KHK Ek M.40) kodlu tazminat yüklenmemiş olanlar için; mutemetlerce maaş/ücret bilgi girişi ekranından ilgili kişinin bilgileri ekrana getirilerek Diğer Tazminat ekranından "97-İlave Ödeme (375 KHK Ek M.40)" tazminat kodunun eklenmesi gerekmektedir.',
   '7456 sayılı Kanunun 28 inci Maddesi ile 375 sayılı Kanun Hükmünde Kararnameye eklenen Ek 40 ıncı maddede sayılmaması nedeniyle ilave ödemeden yararlandırılmayacak personelin bilgileri mutemetlerce maaş/ücret bilgi girişi ekranından ekrana getirilerek Diğer Tazminat ekranından "97-İlave Ödeme (375 KHK Ek M.40)" tazminat kodunun silinmesi gerekmektedir.',
]