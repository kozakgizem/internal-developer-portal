import logging
import sys

# Log formatını ve seviyesini ayarlıyoruz
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        # Logları terminale (konsola) yazdırır
        logging.StreamHandler(sys.stdout),
        # Logları aynı zamanda proje ana dizininde 'app.log' adında bir dosyaya kaydeder
        logging.FileHandler("app.log", encoding="utf-8")
    ],
)

def get_logger(name: str):
    """Her modül için özelleştirilmiş logger döndürür."""
    return logging.getLogger(name)