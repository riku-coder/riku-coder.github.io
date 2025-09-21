
# 🚀 Деплой ResaleX на GitHub и хостинг

## 📋 Быстрая инструкция

### 1. Создание репозитория на GitHub

1. **Перейдите на [GitHub.com](https://github.com)**
2. **Нажмите "New repository"**
3. **Заполните:**
   - Repository name: `resalex-marketplace`
   - Description: `Premium marketplace for reselling exclusive items`
   - Выберите "Public" или "Private"
   - НЕ добавляйте README, .gitignore, license (уже есть)
4. **Нажмите "Create repository"**

### 2. Загрузка проекта на GitHub

```bash
# Перейдите в папку проекта
cd /private/var/Riku/Documents/resale

# Инициализируйте git
git init

# Добавьте все файлы
git add .

# Сделайте первый коммит
git commit -m "Initial commit: ResaleX marketplace"

# Добавьте удаленный репозиторий (замените YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/resalex-marketplace.git

# Загрузите на GitHub
git push -u origin main
```

### 3. Деплой на Heroku (рекомендуется)

#### 3.1 Установка Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Или скачайте с https://devcenter.heroku.com/articles/heroku-cli
```

#### 3.2 Вход в Heroku
```bash
heroku login
```

#### 3.3 Создание приложения
```bash
# В папке проекта
heroku create resalex-marketplace

# Добавьте переменные окружения
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set STRIPE_PUBLISHABLE_KEY=pk_test_...
heroku config:set STRIPE_SECRET_KEY=sk_test_...
```

#### 3.4 Деплой
```bash
git push heroku main
```

#### 3.5 Откройте приложение
```bash
heroku open
```

### 4. Деплой на Railway

#### 4.1 Перейдите на [Railway.app](https://railway.app)
#### 4.2 Войдите через GitHub
#### 4.3 Нажмите "New Project" → "Deploy from GitHub repo"
#### 4.4 Выберите ваш репозиторий
#### 4.5 Railway автоматически определит Python и установит зависимости

### 5. Деплой на Render

#### 5.1 Перейдите на [Render.com](https://render.com)
#### 5.2 Войдите через GitHub
#### 5.3 Нажмите "New" → "Web Service"
#### 5.4 Выберите ваш репозиторий
#### 5.5 Настройки:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python run.py`
   - **Environment:** Python 3

### 6. Настройка переменных окружения

На любом хостинге добавьте переменные:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### 7. Создание root аккаунта

После деплоя:
1. Откройте ваше приложение
2. Перейдите на `/login`
3. Войдите с данными: `root` / `admin123`
4. Смените пароль в настройках

### 8. Обновление проекта

```bash
# Внесите изменения в код
# Добавьте изменения
git add .

# Сделайте коммит
git commit -m "Update: описание изменений"

# Загрузите на GitHub
git push origin main

# Обновите на хостинге (Heroku)
git push heroku main
```

## 🔧 Полезные команды

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

## ⚠️ Важные моменты

1. **Никогда не коммитьте секретные ключи**
2. **Используйте переменные окружения для конфиденциальных данных**
3. **Регулярно делайте бэкапы базы данных**
4. **Тестируйте на staging окружении перед продакшеном**

## 🆘 Если что-то не работает

1. **Проверьте логи:** `heroku logs --tail`
2. **Проверьте переменные окружения**
3. **Убедитесь, что все зависимости установлены**
4. **Проверьте, что порт настроен правильно**

---

**🎉 Готово! Ваш ResaleX теперь доступен в интернете!**
