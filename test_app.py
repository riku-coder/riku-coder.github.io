#!/usr/bin/env python3
"""
ResaleX - Тестирование приложения
Проверяет основные функции системы
"""

import requests
import time
import sys
from urllib.parse import urljoin

BASE_URL = "http://localhost:5000"

def test_connection():
    """Тестирует подключение к приложению"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Приложение запущено и доступно")
            return True
        else:
            print(f"❌ Приложение отвечает с кодом {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Не удается подключиться к приложению: {e}")
        return False

def test_pages():
    """Тестирует доступность основных страниц"""
    pages = [
        ("/", "Главная страница"),
        ("/login", "Страница входа"),
        ("/products", "Каталог товаров"),
    ]
    
    print("\n🔍 Тестирование страниц:")
    for url, name in pages:
        try:
            response = requests.get(urljoin(BASE_URL, url), timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: OK")
            else:
                print(f"❌ {name}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {name}: {e}")

def test_login():
    """Тестирует вход в систему"""
    print("\n🔐 Тестирование входа:")
    
    # Тест с правильными данными
    login_data = {
        'username': 'root',
        'password': 'admin123'
    }
    
    try:
        session = requests.Session()
        
        # Получаем страницу входа
        login_page = session.get(urljoin(BASE_URL, '/login'))
        if login_page.status_code != 200:
            print("❌ Не удается загрузить страницу входа")
            return False
        
        # Отправляем данные для входа
        response = session.post(urljoin(BASE_URL, '/login'), data=login_data, allow_redirects=False)
        
        if response.status_code == 302:  # Редирект после успешного входа
            print("✅ Вход root пользователя: OK")
            
            # Проверяем доступ к дашборду
            dashboard = session.get(urljoin(BASE_URL, '/dashboard'))
            if dashboard.status_code == 200:
                print("✅ Доступ к дашборду: OK")
                return True
            else:
                print("❌ Доступ к дашборду: FAILED")
                return False
        else:
            print("❌ Вход root пользователя: FAILED")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при тестировании входа: {e}")
        return False

def test_database():
    """Тестирует работу с базой данных"""
    print("\n🗄️ Тестирование базы данных:")
    
    try:
        from app import app, db, User
        with app.app_context():
            # Проверяем подключение к БД
            user_count = User.query.count()
            print(f"✅ Подключение к БД: OK (пользователей: {user_count})")
            
            # Проверяем root пользователя
            root_user = User.query.filter_by(username='root').first()
            if root_user:
                print("✅ Root пользователь найден: OK")
            else:
                print("❌ Root пользователь не найден")
                return False
                
            return True
            
    except Exception as e:
        print(f"❌ Ошибка БД: {e}")
        return False

def test_stripe_config():
    """Тестирует конфигурацию Stripe"""
    print("\n💳 Тестирование Stripe:")
    
    try:
        from app import app
        with app.app_context():
            stripe_key = app.config.get('STRIPE_SECRET_KEY')
            if stripe_key and stripe_key != 'sk_test_your_stripe_key':
                print("✅ Stripe ключ настроен: OK")
                return True
            else:
                print("⚠️ Stripe ключ не настроен (используйте тестовые ключи)")
                return False
    except Exception as e:
        print(f"❌ Ошибка конфигурации Stripe: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование ResaleX...")
    print("=" * 50)
    
    # Тест подключения
    if not test_connection():
        print("\n❌ Приложение не запущено!")
        print("Запустите: python run.py")
        sys.exit(1)
    
    # Тест страниц
    test_pages()
    
    # Тест базы данных
    if not test_database():
        print("\n❌ Проблемы с базой данных!")
        sys.exit(1)
    
    # Тест входа
    if not test_login():
        print("\n❌ Проблемы с аутентификацией!")
        sys.exit(1)
    
    # Тест Stripe
    test_stripe_config()
    
    print("\n" + "=" * 50)
    print("🎉 Все основные тесты пройдены!")
    print("\n📋 Следующие шаги:")
    print("1. Откройте http://localhost:5000 в браузере")
    print("2. Войдите как root (root / admin123)")
    print("3. Создайте пользователей разных ролей")
    print("4. Добавьте товары и протестируйте покупки")
    print("\n🚀 ResaleX готов к использованию!")

if __name__ == '__main__':
    main()
