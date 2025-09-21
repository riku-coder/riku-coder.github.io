#!/usr/bin/env python3
"""
ResaleX - Premium Marketplace
Запуск приложения
"""

import os
import sys
from app import app, db

def create_tables():
    """Создает таблицы базы данных"""
    with app.app_context():
        db.create_all()
        print("✅ Таблицы базы данных созданы")

def create_root_user():
    """Создает root пользователя если его нет"""
    from app import User
    
    with app.app_context():
        if not User.query.filter_by(username='root').first():
            root_user = User(
                username='root',
                email='admin@resalex.com',
                role='admin'
            )
            root_user.set_password('admin123')
            db.session.add(root_user)
            db.session.commit()
            print("✅ Root пользователь создан:")
            print("   Username: root")
            print("   Password: admin123")
            print("   ⚠️  ОБЯЗАТЕЛЬНО измените пароль после первого входа!")
        else:
            print("✅ Root пользователь уже существует")

def main():
    """Основная функция запуска"""
    print("🚀 Запуск ResaleX...")
    
    # Создаем папку для загрузок
    os.makedirs('static/uploads', exist_ok=True)
    print("✅ Папка для загрузок создана")
    
    # Создаем таблицы
    create_tables()
    
    # Создаем root пользователя
    create_root_user()
    
    print("\n🌐 Приложение запущено!")
    print("📍 URL: http://localhost:8000")
    print("\nНажмите Ctrl+C для остановки")
    
    # Запускаем приложение
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
