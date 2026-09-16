#  Internal Developer Portal (IDP) - Enterprise Backend & Management API

Bu proje, şirket içi servislerin, kullanıcıların, konfigürasyonların, sistem loglarının ve sunucu kaynak metriklerinin (CPU, RAM, Disk) tek bir merkezden güvenli bir şekilde yönetilmesini sağlayan, **FastAPI**, **SQLAlchemy** ve **Docker** destekli kurumsal bir **Internal Developer Portal (IDP)** backend servisidir.



## İçindekiler
1. [Proje Hakkında ve Mimari](#proje-hakkında-ve-mimari)
2. [Sistem Gereksinimleri](#sistem-gereksinimleri)
3. [Yerel Kurulum Adımları (Local Installation)](#yerel-kurulum-adımları-local-installation)
4. [Projeyi Çalıştırma (Development Mode)](#projeyi-çalıştırma-development-mode)
5. [PyInstaller ile Tek Dosya (.exe) Haline Getirme ve Çalıştırma](#pyinstaller-ile-tek-dosya-exe-haline-getirme-ve-çalıştırma)
6. [Docker ile Ayağa Kaldırma (Docker Compose)](#docker-ile-ayağa-kaldırma-docker-compose)
7. [API Uç Noktaları ve Dokümantasyon](#api-uç-noktaları-ve-dokümantasyon)



##  Proje Hakkında ve Mimari

Bu IDP backend servisi; modüler bir yapıda tasarlanmış olup, geliştiricilerin operasyonel süreçlerini hızlandırmayı amaçlar:
* **FastAPI:** Yüksek performanslı, Asenkron (Async) Python web framework'ü.
* **SQLAlchemy (ORM):** Güçlü ve esnek veritabanı yönetim katmanı (SQLite/PostgreSQL desteği).
* **JWT & Auth:** Güvenli kullanıcı kimlik doğrulama ve yetkilendirme mekanizması.
* **Psutil Entegrasyonu:** Gerçek zamanlı sunucu kaynak (CPU, RAM, Disk) takibi.
* **Dosya Yönetimi:** JSON ve YAML tabanlı konfigürasyon dosyalarını okuma ve güncelleme özellikleri.



##  Sistem Gereksinimleri

Projeyi kendi bilgisayarınızda kurup çalıştırmak için aşağıdaki araçların sisteminizde yüklü olması gerekmektedir:
* **Python** (Sürüm 3.10 veya üzeri / Docker imajında 3.13)
* **uv** (Hızlı Python paket ve bağımlılık yöneticisi)
* **PyInstaller** (Uygulamayı çalıştırılabilir `.exe` formatına paketlemek için)
* **Docker & Docker Compose** (Konteyner ortamında çalıştırmak için)



##  Yerel Kurulum Adımları (Local Installation)

Projeyi bilgisayarınıza klonladıktan sonra terminal üzerinden backend ana dizinine gelin ve bağımlılıkları senkronize edin:

uv sync

(Not: sqlalchemy ve diğer tüm gereksinimli kütüphaneler uv sync komutu ile otomatik olarak eksiksiz bir şekilde kurulacaktır).

##   Projeyi Çalıştırma (Development Mode)
Geliştirme ortamında FastAPI sunucusunu canlı yeniden başlatma (--reload) özelliğiyle ve tüm ağ arayüzlerinden erişilebilir şekilde ayağa kaldırmak için şu komutu çalıştırın:


uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Sunucu başarıyla ayağa kalktıktan sonra tarayıcınızdan http://127.0.0.1:8000 adresine giderek sistemin aktif olduğunu doğrulayabilirsiniz.

##  PyInstaller ile Tek Dosya (.exe) Haline Getirme ve Çalıştırma
Python ortamının bulunmadığı veya bağımsız bir çalıştırılabilir dosya olarak test etmek istediğiniz senaryolar için uygulamayı PyInstaller ile paketleyebilirsiniz:

Projeyi tek bir çalıştırılabilir dosya (--onefile) olarak derlemek için terminalde şu komutu çalıştırın:


uv run pyinstaller --onefile app/main.py
Derleme işlemi tamamlandığında projenin kök dizininde veya dist klasörü içerisinde main.exe dosyası oluşacaktır.

Oluşan bu .exe dosyasını kendi backend dizininizde çalıştırarak (çift tıklayarak veya terminalden çağırarak) harici bir Python bağımlılığına gerek kalmadan sunucuyu test edebilirsiniz.

##  Docker ile Ayağa Kaldırma (Docker Compose)
Projeyi tamamen izole bir konteyner ortamında çalıştırmak için proje ana dizininde aşağıdaki komutu çalıştırabilirsiniz:


docker compose up --build
Bu komut, Dockerfile ve `docker-compose.yml` yapılandırmanızı kullanarak Python 3.13 ortamını hazırlar, bağımlılıkları kurar ve uygulamayı `http://localhost:8000` adresinde ayağa kaldırır.

## API Uç Noktaları ve Dokümantasyon

Proje çalışırken tüm API endpoint'lerini interaktif olarak test etmek ve incelemek için Swagger UI veya ReDoc arayüzlerini kullanabilirsiniz:

  **Kendi Bilgisayarınızdan (Local):**
  **Swagger UI:** `http://127.0.0.1:8000/docs` veya `http://localhost:8000/docs`
  **ReDoc:** `http://127.0.0.1:8000/redoc`
  **Sağlık Durumu (Health Check):** `http://127.0.0.1:8000/health`

  **Aynı Ağdaki Başka Bir Bilgisayardan (Network / IP ile):**
  **Swagger UI:** `http://192.168.1.120:8000/docs`
  **ReDoc:** `http://192.168.1.120:8000/redoc`
  **Sağlık Durumu (Health Check):** `http://192.168.1.120:8000/health`