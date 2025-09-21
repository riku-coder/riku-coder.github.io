# 🚀 Финальный деплой ResaleX на GitHub

## 📋 Полная инструкция для деплоя

### 1. Подготовка проекта

```bash
# Перейдите в папку проекта
cd /private/var/Riku/Documents/resale

# Убедитесь, что все файлы на месте
ls -la
```

### 2. Создание репозитория на GitHub

1. **Перейдите на [GitHub.com](https://github.com)**
2. **Нажмите "New repository"**
3. **Заполните:**
   - Repository name: `resalex-marketplace`
   - Description: `Premium marketplace for reselling exclusive items - ResaleX`
   - Выберите "Public"
   - НЕ добавляйте README, .gitignore, license (уже есть)
4. **Нажмите "Create repository"**

### 3. Инициализация Git и загрузка

```bash
# Инициализируйте git
git init

# Добавьте все файлы
git add .

# Сделайте первый коммит
git commit -m "Initial commit: ResaleX marketplace with dark theme and ruble currency"

# Добавьте удаленный репозиторий (замените YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/resalex-marketplace.git

# Загрузите на GitHub
git push -u origin main
```

### 4. Настройка для деплоя на Heroku

#### 4.1 Установка Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Или скачайте с https://devcenter.heroku.com/articles/heroku-cli
```

#### 4.2 Вход и создание приложения
```bash
# Войдите в Heroku
heroku login

# Создайте приложение
heroku create resalex-marketplace

# Добавьте переменные окружения
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
heroku config:set STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
heroku config:set FLASK_ENV=production
```

#### 4.3 Деплой на Heroku
```bash
# Добавьте Heroku как удаленный репозиторий
git remote add heroku https://git.heroku.com/resalex-marketplace.git

# Деплой
git push heroku main

# Откройте приложение
heroku open
```

### 5. Альтернатива: Деплой на Railway

1. **Перейдите на [Railway.app](https://railway.app)**
2. **Войдите через GitHub**
3. **Нажмите "New Project" → "Deploy from GitHub repo"**
4. **Выберите ваш репозиторий `resalex-marketplace`**
5. **Railway автоматически определит Python и установит зависимости**
6. **Добавьте переменные окружения в настройках проекта**

### 6. Альтернатива: Деплой на Render

1. **Перейдите на [Render.com](https://render.com)**
2. **Войдите через GitHub**
3. **Нажмите "New" → "Web Service"**
4. **Выберите ваш репозиторий**
5. **Настройки:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`
   - **Environment:** Python 3
6. **Добавьте переменные окружения**

### 7. Настройка переменных окружения

На любом хостинге добавьте:

```bash
SECRET_KEY=your-secret-key-here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
FLASK_ENV=production
```

### 8. Создание root аккаунта

После деплоя:
1. Откройте ваше приложение
2. Перейдите на `/login`
3. Войдите с данными: `root` / `admin123`
4. Смените пароль в настройках

### 9. Настройка СБП (для продакшена)

Для интеграции с СБП замените Stripe на:

```python
# В app.py замените Stripe на СБП
# Используйте API СБП для обработки платежей
# Или интегрируйте через ЮKassa, Тинькофф и т.д.
```

### 10. Обновление проекта

```bash
# Внесите изменения в код
# Добавьте изменения
git add .

# Сделайте коммит
git commit -m "Update: описание изменений"

# Загрузите на GitHub
git push origin main

# Обновите на хостинге
git push heroku main  # для Heroku
# или автоматически для Railway/Render
```

## 🔧 Полезные команды

### Git
```bash
# Статус файлов
git status

# Просмотр изменений
git diff

# Отмена изменений
git checkout -- filename

# Создание ветки
git checkout -b feature-name
```

### Heroku
```bash
# Просмотр логов
heroku logs --tail

# Открыть приложение
heroku open

# Перезапуск
heroku restart

# Просмотр переменных
heroku config
```

## 📱 Особенности проекта

### ✨ Что включено:
- **Темная тема** - современный черный дизайн
- **Валюты в рублях** - все цены в ₽
- **Favicon** - аватарка сайта в браузере
- **Liquid Glass эффекты** - премиальный дизайн
- **Адаптивность** - работает на всех устройствах
- **Система ролей** - Root, Admin, Moderator, Seller, User
- **Управление товарами** - полный функционал
- **Отслеживание заказов** - статусы и история

### 🎨 Дизайн:
- **Цветовая схема:** Черный (#0a0a0a) + голубые акценты (#00d4ff)
- **Типографика:** Inter font
- **Эффекты:** Backdrop blur, градиенты, тени
- **Анимации:** Плавные переходы и hover эффекты

### 💰 Валюты:
- **Основная валюта:** Российский рубль (₽)
- **Формат цен:** Без копеек (целые числа)
- **Готовность к СБП:** Структура для интеграции

## ⚠️ Важные моменты

1. **GitHub Pages не поддерживает Flask** - нужен сервер
2. **Используйте Heroku/Railway/Render** для полного функционала
3. **Настройте переменные окружения** на хостинге
4. **Смените пароль root** после деплоя
5. **Настройте СБП** для продакшена

## 🆘 Если что-то не работает

1. **Проверьте логи:** `heroku logs --tail`
2. **Проверьте переменные окружения**
3. **Убедитесь, что все зависимости установлены**
4. **Проверьте, что порт настроен правильно**

---

**🎉 Готово! Ваш ResaleX теперь доступен в интернете!**

**URL:** https://resalex-marketplace.herokuapp.com (или ваш хостинг)

**Root аккаунт:** root / admin123 (смените пароль!)
