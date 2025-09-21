# 🚀 ResaleX - Финальный деплой на GitHub

## ✅ Что исправлено

### 1. Кнопки чата для пользователей
- ✅ Добавлены кнопки чата в пользовательский дашборд
- ✅ Пользователи могут общаться с продавцами по заказам

### 2. Система уведомлений
- ✅ Добавлена иконка уведомлений в навигацию
- ✅ API для получения уведомлений
- ✅ Автоматическая проверка новых уведомлений каждые 30 секунд
- ✅ Уведомления о новых заказах для продавцов
- ✅ Уведомления об обновлении статуса для покупателей

### 3. Все предыдущие исправления
- ✅ Темная тема с современными черными цветами
- ✅ Валюта в рублях (₽)
- ✅ Кнопки админ панели работают
- ✅ Редактирование и удаление товаров
- ✅ Система чата между покупателями и продавцами
- ✅ Управление пользователями (блокировка/удаление)

## 🚀 Быстрый деплой на GitHub

### Шаг 1: Создание репозитория на GitHub
1. Перейдите на [GitHub.com](https://github.com)
2. Нажмите "New repository"
3. Название: `resale-marketplace`
4. Описание: `Premium resale marketplace like StockX`
5. Выберите "Public"
6. НЕ добавляйте README, .gitignore или лицензию (у нас уже есть)
7. Нажмите "Create repository"

### Шаг 2: Инициализация Git в проекте
```bash
cd /private/var/Riku/Documents/resale
git init
git add .
git commit -m "Initial commit: ResaleX marketplace"
```

### Шаг 3: Подключение к GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/resale-marketplace.git
git branch -M main
git push -u origin main
```

### Шаг 4: Настройка для деплоя
Создайте файл `.env` в корне проекта:
```bash
echo "FLASK_ENV=production" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env
echo "STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here" >> .env
echo "STRIPE_SECRET_KEY=sk_test_your_key_here" >> .env
```

## 🌐 Деплой на хостинг

### Вариант 1: Railway (Рекомендуется)
1. Перейдите на [Railway.app](https://railway.app)
2. Войдите через GitHub
3. Нажмите "New Project" → "Deploy from GitHub repo"
4. Выберите ваш репозиторий `resale-marketplace`
5. Railway автоматически определит Python и установит зависимости
6. Добавьте переменные окружения в настройках проекта:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key-here`
   - `STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here`
   - `STRIPE_SECRET_KEY=sk_test_your_key_here`
7. Деплой произойдет автоматически

### Вариант 2: Render
1. Перейдите на [Render.com](https://render.com)
2. Войдите через GitHub
3. Нажмите "New" → "Web Service"
4. Подключите ваш репозиторий
5. Настройки:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`
   - **Environment**: Python 3
6. Добавьте переменные окружения
7. Нажмите "Create Web Service"

### Вариант 3: Heroku
1. Установите [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Войдите в Heroku: `heroku login`
3. Создайте приложение: `heroku create resale-marketplace`
4. Добавьте переменные окружения:
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
   heroku config:set STRIPE_SECRET_KEY=sk_test_your_key_here
   ```
5. Деплой: `git push heroku main`

## 🔧 Настройка Stripe для продакшена

### 1. Получите ключи Stripe
1. Войдите в [Stripe Dashboard](https://dashboard.stripe.com)
2. Перейдите в "Developers" → "API keys"
3. Скопируйте:
   - **Publishable key** (начинается с `pk_live_`)
   - **Secret key** (начинается с `sk_live_`)

### 2. Обновите переменные окружения
Замените тестовые ключи на продакшн ключи в настройках хостинга.

## 📱 Функции сайта

### Для покупателей:
- ✅ Регистрация и авторизация
- ✅ Просмотр товаров с фильтрацией
- ✅ Покупка товаров
- ✅ Отслеживание заказов
- ✅ Чат с продавцами
- ✅ Уведомления о статусе заказов
- ✅ Профиль с историей покупок

### Для продавцов:
- ✅ Добавление товаров
- ✅ Редактирование и удаление товаров
- ✅ Управление заказами
- ✅ Чат с покупателями
- ✅ Уведомления о новых заказах
- ✅ Статистика продаж

### Для администраторов:
- ✅ Управление пользователями
- ✅ Модерация товаров
- ✅ Просмотр всех заказов
- ✅ Блокировка/разблокировка пользователей
- ✅ Удаление пользователей

## 🎨 Дизайн
- ✅ Современная темная тема
- ✅ Liquid Glass эффекты
- ✅ Адаптивный дизайн
- ✅ Мобильная навигация
- ✅ Анимации и переходы
- ✅ Премиальный внешний вид

## 💰 Платежи
- ✅ Интеграция со Stripe
- ✅ Валюта: Российские рубли (₽)
- ✅ Безопасные платежи

## 🔒 Безопасность
- ✅ Хеширование паролей
- ✅ CSRF защита
- ✅ Валидация форм
- ✅ Безопасная загрузка файлов
- ✅ Контроль доступа по ролям

## 📞 Поддержка
Если возникли проблемы с деплоем:
1. Проверьте логи в панели хостинга
2. Убедитесь, что все переменные окружения установлены
3. Проверьте, что база данных создается корректно
4. Убедитесь, что порт настроен правильно

## 🎉 Готово!
Ваш премиальный маркетплейс ResaleX готов к использованию!

**URL после деплоя**: `https://your-app-name.railway.app` (или другой хостинг)

**Root аккаунт**:
- Username: `root`
- Password: `admin123`
- ⚠️ **ОБЯЗАТЕЛЬНО смените пароль после первого входа!**
