import tkinter as tk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageTk
import threading
import time
import pandas as pd
import re
import os
import requests

class HepsiburadaYorumCekici:
    def __init__(self, root):
        self.root = root
        self.root.title("T-Rax Team Hepsiburada Yorum Çekici Sistemi")
        self.root.resizable(width=False, height=False)

        # Arka plan ve logo resimleri
        background_image = Image.open("C:/Users/slmbn/OneDrive/Desktop/T-RAX TEAM  HEPSİBURADA/Image/arka_plan.png")   #Benim Bilgisayarımda Bu Dizinde Çekmektedir Bu Kodu Kendi Bilgisayarınıza Göre Uygulayınız.
        background_image = background_image.resize((1020, 1020), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)
        self.background_label = tk.Label(root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        logo_image = Image.open("C:/Users/slmbn/OneDrive/Desktop/T-RAX TEAM  HEPSİBURADA/Image/logo.png")  #Benim Bilgisayarımda Bu Dizinde Çekmektedir Bu Kodu Kendi Bilgisayarınıza Göre Uygulayınız.
        logo_image = logo_image.resize((200, 200), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(logo_image)
        self.logo_label = tk.Label(root, image=self.logo, bg='white')
        self.logo_label.pack(pady=20)

        # UI bileşenleri
        self.frame = tk.Frame(root, bg='orange', padx=10, pady=10)
        self.frame.pack(padx=10, pady=10)

        self.url_label = tk.Label(self.frame, text="Hepsiburada ürününün linkini giriniz:", bg='orange')
        self.url_label.pack(pady=50)

        self.url_entry = tk.Entry(self.frame, width=100)
        self.url_entry.pack(pady=10)

        self.yorum_sayaci = 0
        self.yorum_sayac_label = tk.Label(self.frame, text=f"Toplam Yorum Sayısı: {self.yorum_sayaci}", bg='orange')
        self.yorum_sayac_label.pack(pady=20)

        self.baslat_button = tk.Button(self.frame, text="Yorumları Çek", command=self.baslat)
        self.baslat_button.pack(pady=20)

        self.durdur_button = tk.Button(self.frame, text="Yorumları Durdur", command=self.durdur, state=tk.DISABLED)
        self.durdur_button.pack(pady=20)

        self.bilgi = tk.Label(self.frame, text="Lütfen Açılan Sayfayı Kapatmayınız:", bg='orange')
        self.bilgi.pack(pady=50)

        self.bilgi2 = tk.Label(self.frame, text="T-RAX TEAM SYSTEM 2024", bg='orange')
        self.bilgi2.pack(pady=30)

        self.surucu = None
        self.islem_durdur_event = threading.Event()
        self.islem_devam_event = threading.Event()
        self.lock = threading.Lock()

        self.geckodriver_kur()

    def geckodriver_kur(self):
        if not self.is_firefox_driver_installed():
            firefox_url = "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US"
            firefox_path = "firefox_installer.exe"

            if not self.is_firefox_installed():
                print("Firefox bulunamadı. İndiriliyor...")
                self.download_file(firefox_url, firefox_path)
                print("Firefox indirildi. Kuruluyor...")
                self.install_firefox(firefox_path)
                print("Firefox kuruldu.")
            else:
                print("Firefox zaten yüklü.")

            try:
                self.surucu = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=self.setup_firefox_options())
            except Exception as e:
                print(f"Firefox başlatılırken hata oluştu: {str(e)}")
        else:
            print("Geckodriver zaten yüklü. Firefox başlatılıyor...")
            self.surucu = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=self.setup_firefox_options())

    def is_firefox_installed(self):
        firefox_paths = [
            "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
        ]
        return any(os.path.exists(path) for path in firefox_paths)

    def is_firefox_driver_installed(self):
        gecko_driver_path = GeckoDriverManager().install()
        return os.path.exists(gecko_driver_path)

    def download_file(self, url, local_filename):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def install_firefox(self, installer_path):
        os.system(f"{installer_path} /S")

    def setup_firefox_options(self):
        options = Options()
        firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
        if os.path.exists(firefox_binary_path):
            options.binary_location = firefox_binary_path
        else:
            print("Firefox yürütülebilir dosyası bulunamadı. Lütfen yolu kontrol edin.")
        options.headless = True  # Tarayıcıyı arka planda çalıştır
        return options

    def baslat(self):
        urun_url = self.url_entry.get()
        if not urun_url.endswith("-yorumlari"):
            urun_url += "-yorumlari"

        messagebox.showinfo("Başlatılıyor", "Yorum çekme işlemi başlatıldı. Lütfen bekleyiniz...")
        self.durdur_button.config(state=tk.NORMAL)  # Durdur butonunu aktif et
        self.islem_durdur_event.clear()  # Durdur olayını temizle
        self.islem_devam_event.set()  # İşlemi devam ettir

        threading.Thread(target=self.hepsiburada_yorum_cek, args=(urun_url,)).start()

    def durdur(self):
        self.islem_durdur_event.set()  # Durdur olayını ayarla
        messagebox.showinfo("Durduruldu", "Yorum çekme işlemi durduruldu.")

    def hepsiburada_yorum_cek(self, url):
        genel_bekleme_suresi = 0.5
        yorumlar = []

        try:
            self.surucu.get(url)
            time.sleep(5)
            print('Ürünün yorum sayfasına gidildi')
            sayfa_sayisi = 1
            yorum_numarasi = 1

            while True:
                if self.islem_durdur_event.is_set():
                    break

                time.sleep(3)

                try:
                    sayfalama_eleman = WebDriverWait(self.surucu, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/main/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div[6]/div[3]/div[2]/div/ul'))
                    )
                    sayfa_elementleri = sayfalama_eleman.find_elements(By.TAG_NAME, 'li')
                    toplam_sayfa = int(sayfa_elementleri[-1].find_element(By.TAG_NAME, 'span').text)
                    print(f'Toplam Sayfa: {toplam_sayfa}')
                except Exception as e:
                    print(f'Sayfa sayısı tespit edilirken hata oluştu: {str(e)}')
                    break

                print(f'Botun Şu anki sayfası: {sayfa_sayisi}, Toplam Tespit Edilen sayfa: {toplam_sayfa}')

                for i in range(1, 11):
                    if self.islem_durdur_event.is_set():
                        break
                    try:
                        yorum = self.surucu.find_element(By.XPATH, f'/html/body/div[2]/main/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div[6]/div[3]/div[1]/div[{i}]/div[2]/div[2]/span').text
                        print(f'Yorum {yorum_numarasi}: {yorum}')
                        yorum = self.remove_emojis(yorum)  # Emojileri temizle
                        yorumlar.append([yorum_numarasi, yorum])
                        yorum_numarasi += 1
                        self.yorum_sayaci += 1
                        # Yorum sayacını güncelle ve ekranda göster
                        with self.lock:
                            self.yorum_sayac_label.config(text=f"Toplam Yorum Sayısı: {self.yorum_sayaci}")

                        time.sleep(genel_bekleme_suresi)
                    except Exception as e:
                        print(f'Yorum çekilirken hata oluştu: {str(e)}')
                        continue

                sayfa_sayisi += 1

                try:
                    # Modalları kapatmayı deneyin
                    self.close_modal()

                    # Sayfa geçişi için "Sonraki" butonuna tıklayın
                    sonraki_button = WebDriverWait(self.surucu, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/main/div[2]/div/div/div/div/div/div/div[1]/div[2]/div[2]/div[6]/div[3]/div[2]/div/ul/li[last()]/a'))
                    )
                    sonraki_button.click()
                    time.sleep(genel_bekleme_suresi)
                except Exception as e:
                    print(f'Sayfa geçişi yapılırken hata oluştu: {str(e)}')
                    break

        except Exception as e:
            print(f'Yorum çekme işlemi sırasında hata oluştu: {str(e)}')

        finally:
            # Sonuçları bir dosyaya kaydedin
            self.save_comments_to_csv(yorumlar)
            self.surucu.quit()

    def remove_emojis(self, text):
        return re.sub(r'[^\w\s]', '', text)  # Emojileri temizler

    def save_comments_to_csv(self, comments):
        df = pd.DataFrame(comments, columns=["Yorum Numarası", "Yorum"])
        df.to_csv("yorumlar.csv", index=False, encoding='utf-8')
        print("Yorumlar 'yorumlar.csv' dosyasına kaydedildi.")

    def close_modal(self):
        try:
            modals = self.surucu.find_elements(By.CLASS_NAME, 'modal')
            for modal in modals:
                close_button = modal.find_element(By.XPATH, './/button[contains(@class, "close")]')
                close_button.click()
                print('Modal kapatıldı.')
        except Exception as e:
            print(f'Modal kapatılırken hata oluştu: {str(e)}')

if __name__ == "__main__":
    root = tk.Tk()
    app = HepsiburadaYorumCekici(root)
    root.mainloop()
