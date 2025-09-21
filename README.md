# 🛍️ ResaleX - Premium Marketplace

> Современный маркетплейс для перепродажи товаров в стиле StockX

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Особенности

### 🎨 Дизайн
- **Темная тема** с современными черными цветами
- **Liquid Glass эффекты** для премиального вида
- **Адаптивный дизайн** для всех устройств
- **Мобильная навигация** в стиле приложения
- **Анимации и переходы** для лучшего UX

### 👥 Пользователи
- **Root** - полный контроль системы
- **Admin** - управление пользователями и товарами
- **Moderator** - модерация контента
- **Seller** - продажа товаров
- **User** - покупка товаров

### 🛒 Функции
- **Управление товарами** - добавление, редактирование, удаление
- **Система заказов** - отслеживание статусов
- **Чат** между покупателями и продавцами
- **Уведомления** в реальном времени
- **Платежи** через Stripe
- **Валюта** - Российские рубли (₽)

## 🚀 Быстрый старт

### Установка
```bash
# Клонируйте репозиторий
git clone https://github.com/YOUR_USERNAME/resale-marketplace.git
cd resale-marketplace

# Установите зависимости
pip install -r requirements.txt

# Запустите приложение
python run.py
```

### Первый вход
- **URL**: http://localhost:8000
- **Username**: `root`
- **Password**: `admin123`
- ⚠️ **Смените пароль после первого входа!**

## 📱 Скриншоты

### Главная страница
![Главная страница](screenshots/homepage.png)

### Дашборд пользователя
![Дашборд](screenshots/dashboard.png)

### Админ панель
![Админ панель](screenshots/admin.png)

## 🛠️ Технологии

### Backend
- **Flask** - веб-фреймворк
- **SQLAlchemy** - ORM для базы данных
- **Flask-Login** - аутентификация
- **Flask-WTF** - формы и CSRF защита
- **Werkzeug** - безопасность

### Frontend
- **Bootstrap 5** - CSS фреймворк
- **Font Awesome** - иконки
- **Google Fonts** - шрифты
- **JavaScript** - интерактивность

### Платежи
- **Stripe** - обработка платежей
- **SBP** - Система быстрых платежей

## 📁 Структура проекта

```
resale/
├── app.py                 # Основное приложение
├── run.py                 # Запуск сервера
├── config.py              # Конфигурация
├── requirements.txt       # Зависимости
├── templates/             # HTML шаблоны
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   └── ...
├── static/                # Статические файлы
│   ├── css/
│   ├── js/
│   └── images/
├── uploads/               # Загруженные файлы
└── instance/              # База данных
```

## 🔧 Настройка

### Переменные окружения
Создайте файл `.env`:
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
```

### База данных
SQLite база данных создается автоматически при первом запуске.

## 🌐 Деплой

### Railway (Рекомендуется)
1. Подключите GitHub репозиторий
2. Railway автоматически определит Python
3. Добавьте переменные окружения
4. Деплой произойдет автоматически

### Render
1. Создайте новый Web Service
2. Подключите репозиторий
3. Настройте переменные окружения
4. Деплой готов!

### Heroku
1. Установите Heroku CLI
2. Создайте приложение
3. Настройте переменные окружения
4. Деплой через Git

## 📖 Документация

- [FINAL_DEPLOY.md](FINAL_DEPLOY.md) - Подробная инструкция по деплою
- [deploy.sh](deploy.sh) - Скрипт быстрого деплоя

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

## 🆘 Поддержка

Если у вас возникли проблемы:

1. Проверьте [Issues](https://github.com/YOUR_USERNAME/resale-marketplace/issues)
2. Создайте новый Issue с описанием проблемы
3. Приложите логи и скриншоты

## 🎯 Roadmap

- [ ] Email уведомления
- [ ] Мобильное приложение
- [ ] API для мобильных приложений
- [ ] Система отзывов
- [ ] Аналитика продаж
- [ ] Многоязычность

## 👨‍💻 Автор

**ResaleX Team**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: contact@resalex.com

---

⭐ **Если проект вам понравился, поставьте звезду!**