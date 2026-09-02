import json
import yaml
from pathlib import Path

# Proje kök dizinini dinamik olarak buluyoruz
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
CONFIG_JSON_PATH = ROOT_DIR / "portal_config.json"
SERVICES_YAML_PATH = ROOT_DIR / "services.yaml"

def read_json_config():
    """Portal JSON konfigürasyon dosyasını okur (Dosya işlemleri)."""
    if CONFIG_JSON_PATH.exists():
        with open(CONFIG_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "portal_config.json bulunamadı."}

def update_json_config(new_data: dict):
    """Portal JSON konfigürasyon dosyasını günceller (Dosya yazma işlemi)."""
    with open(CONFIG_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    return read_json_config()

def read_yaml_services():
    """Servislerin YAML konfigürasyon dosyasını okur."""
    if SERVICES_YAML_PATH.exists():
        with open(SERVICES_YAML_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {"error": "services.yaml bulunamadı."}