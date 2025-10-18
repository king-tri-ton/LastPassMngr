import os
import json
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class PasswordStorage:
    def __init__(self, master_password):
        """
        Инициализация хранилища паролей с шифрованием
        
        Args:
            master_password (str): Мастер-пароль для шифрования
        """
        # Путь к хранилищу
        self.storage_dir = Path.home() / "Documents" / "LastPassMngr"
        self.storage_file = self.storage_dir / "passwords.enc"
        self.salt_file = self.storage_dir / ".salt"
        self.verify_file = self.storage_dir / ".verify"
        
        # Создаем директорию если не существует
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Генерируем или загружаем ключ шифрования
        self.cipher = self._init_cipher(master_password)
        
    def _init_cipher(self, master_password):
        """Инициализирует шифрование"""
        # Если есть сохраненная соль, используем её
        if self.salt_file.exists():
            with open(self.salt_file, 'rb') as f:
                salt = f.read()
        else:
            # Генерируем новую соль
            salt = os.urandom(32)
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
        
        # Создаем ключ из мастер-пароля
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return Fernet(key)
    
    def verify_master_password(self):
        """
        Проверяет правильность мастер-пароля
        
        Returns:
            bool: True если пароль правильный
        """
        # Если это первый запуск
        if not self.verify_file.exists():
            # Создаем контрольный файл
            try:
                verify_data = "PASSWORD_CORRECT"
                encrypted = self.cipher.encrypt(verify_data.encode())
                with open(self.verify_file, 'wb') as f:
                    f.write(encrypted)
                return True
            except:
                return False
        
        # Проверяем существующий пароль
        try:
            with open(self.verify_file, 'rb') as f:
                encrypted = f.read()
            decrypted = self.cipher.decrypt(encrypted)
            return decrypted.decode() == "PASSWORD_CORRECT"
        except:
            return False
    
    def is_first_run(self):
        """Проверяет, первый ли это запуск"""
        return not self.storage_file.exists()
    
    def save_password(self, site, login, password):
        """
        Сохраняет пароль для сайта
        
        Args:
            site (str): Название сайта
            login (str): Логин
            password (str): Пароль
        """
        # Загружаем существующие данные
        data = self._load_data()
        
        # Добавляем новую запись
        if site not in data:
            data[site] = []
        
        data[site].append({
            'login': login,
            'password': password
        })
        
        # Сохраняем данные
        self._save_data(data)
    
    def get_passwords(self, site=None):
        """
        Получает сохраненные пароли
        
        Args:
            site (str, optional): Название сайта для фильтрации
        
        Returns:
            dict or list: Все пароли или пароли для конкретного сайта
        """
        data = self._load_data()
        
        if site:
            return data.get(site, [])
        return data
    
    def delete_password(self, site, login):
        """
        Удаляет пароль
        
        Args:
            site (str): Название сайта
            login (str): Логин
        """
        data = self._load_data()
        
        if site in data:
            data[site] = [item for item in data[site] if item['login'] != login]
            if not data[site]:
                del data[site]
            self._save_data(data)
    
    def change_master_password(self, old_password, new_password):
        """
        Меняет мастер-пароль
        
        Args:
            old_password (str): Старый мастер-пароль
            new_password (str): Новый мастер-пароль
        
        Returns:
            bool: True если успешно
        """
        try:
            # Загружаем данные со старым паролем
            data = self._load_data()
            
            # Создаем новый шифр с новым паролем
            old_cipher = self.cipher
            self.cipher = self._init_cipher(new_password)
            
            # Пересохраняем данные с новым паролем
            self._save_data(data)
            
            # Обновляем verify файл
            verify_data = "PASSWORD_CORRECT"
            encrypted = self.cipher.encrypt(verify_data.encode())
            with open(self.verify_file, 'wb') as f:
                f.write(encrypted)
            
            return True
        except:
            self.cipher = old_cipher
            return False
    
    def _load_data(self):
        """Загружает и расшифровывает данные"""
        if not self.storage_file.exists():
            return {}
        
        try:
            with open(self.storage_file, 'rb') as f:
                encrypted_data = f.read()
            
            if not encrypted_data:
                return {}
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}
    
    def _save_data(self, data):
        """Шифрует и сохраняет данные"""
        try:
            json_data = json.dumps(data, ensure_ascii=False, indent=2)
            encrypted_data = self.cipher.encrypt(json_data.encode())
            
            with open(self.storage_file, 'wb') as f:
                f.write(encrypted_data)
        except Exception as e:
            print(f"Error saving data: {e}")