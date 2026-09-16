import sys
import os

# 'src' klasörünü Python arama yoluna ekliyoruz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/internal_developer_portal')))

# Örnek birim testi: Projedeki Pydantic şemalarının veya yardımcı bir fonksiyonun 
# veriyi doğru doğrulayıp doğrulamadığını (harici servis/DB olmadan) test ediyoruz.
from app.schemas.user_schema import UserBase

def test_user_base_schema_unit():
    """
    Unit Test: UserBase Pydantic şemasının veri doğrulama (validation) 
    mantığını izole bir şekilde test eder. Veritabanı veya HTTP sunucusu gerektirmez.
    """
    # Geçerli bir kullanıcı verisi oluşturalım
    user_data = {"username": "testuser", "email": "test@example.com"}
    
    # Şemayı bu verilerle başlatalım
    user = UserBase(**user_data)
    
    # Alanların doğru set edilip edilmediğini birim test ile kontrol edelim
    assert user.username == "testuser"
    assert user.email == "test@example.com"