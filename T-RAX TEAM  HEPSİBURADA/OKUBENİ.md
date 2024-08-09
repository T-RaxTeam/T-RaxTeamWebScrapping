T-Rax Team Hepsiburada Yorum Çekici Sistemi
Programın Amacı:
T-Rax Team Hepsiburada Yorum Çekici Sistemi, Hepsiburada üzerindeki ürünlerin kullanıcı yorumlarını otomatik olarak çekmek ve bu yorumları nlpye uygun sunmak amacıyla geliştirilmiş bir programdır.

Kullanılan Kütüphaneler:
tkinter: Kullanıcı arayüzünü oluşturmak için kullanıldı.
selenium: Hepsiburada web sitesine bağlanıp, yorumları çekmek için kullanıldı.
webdriver_manager: ChromeDriver'ı otomatik olarak indirmek ve yönetmek için kullanıldı.
Pillow: Arka plan ve logo resimlerini işlemek için kullanıldı.
transformers ve torch: Yorumların duygu analizini yapmak için kullanılan NLP kütüphaneleri.

Kullanıcı Arayüzü:
Kullanıcı, Hepsiburada ürün linkini girebileceği bir alan ile karşılaşır.
Programın arka planı ve logosu görüntülenir.
Kullanıcı, yorumları çekmek için bir butona basar.
Kullanım Talimatları:
Kurulum ----------------------------
pip install -r requirements.txt







-------------------------------------
Programı başlatın.
Hepsiburada ürün linkini ilgili alana girin.
"Yorumları Çek" butonuna tıklayın.
Program, yorumları çekmeye başlayacak ve süreç boyunca sizi bilgilendirecektir.
İşlem tamamlandığında, tüm yorumlar ve analizleri "yorumlar.csv" dosyasına kaydedilecektir.
Sonuç:
Bu program, kullanıcıların Hepsiburada ürünleri hakkındaki yorumları hızlı ve etkili bir şekilde toplamalarını ve bu yorumların duygu analizini yapmalarını sağlar. Kullanıcı dostu arayüzü ve otomatik işlevselliği sayesinde zaman kazandırır ve değerli içgörüler sunar.
