import json
import os
import hashlib

ACCOUNTS_FILE = "accounts.json"


class GameManager:
    def __init__(self):
        # проверяем наличие файла аккаунтов, если нет, то создаём пустой файл
        if not os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _load_accounts(self):
        # загружаем список аккаунтов из JSON-файла
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_accounts(self, data):
        # сохраняем обновленный список аккаунтов обратно в JSON-файл
        with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _hash_password(self, password: str) -> str:
        # создаём хэш пароля
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def account_exists(self, name: str) -> bool:
        # проверяем существование аккаунта по имени
        accounts = self._load_accounts()
        return name in accounts

    def create_account(self, name: str, password: str) -> bool:
        # регистрация нового аккаунта
        accounts = self._load_accounts()
        if name in accounts:
            return False  # аккаунт уже существует

        # добавляем аккаунт с зашифрованным паролем
        accounts[name] = {"password": self._hash_password(password)}
        self._save_accounts(accounts)
        return True

    def login(self, name: str, password: str) -> bool:
        # авторизация пользователя
        accounts = self._load_accounts()
        if name not in accounts:
            return False  # учётная запись не найдена

        # сравниваем введённый пароль с сохранённым хэшем
        return accounts[name]["password"] == self._hash_password(password)
