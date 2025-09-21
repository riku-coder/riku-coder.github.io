# 🚀 Деплой ResaleX на GitHub Pages

## 📋 Быстрая инструкция

### 1. Создание репозитория на GitHub

1. **Перейдите на [GitHub.com](https://github.com)**
2. **Нажмите "New repository"**
3. **Заполните:**
   - Repository name: `resalex-marketplace`
   - Description: `Premium marketplace for reselling exclusive items`
   - Выберите "Public"
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

### 3. Настройка GitHub Pages

1. **Перейдите в настройки репозитория**
2. **Найдите раздел "Pages" в левом меню**
3. **В разделе "Source" выберите "Deploy from a branch"**
4. **Выберите ветку "main" и папку "/ (root)"**
5. **Нажмите "Save"**

### 4. Настройка для статического хостинга

Поскольку это Flask приложение, нужно настроить его для статического хостинга:

#### 4.1 Создайте файл `index.html` в корне
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ResaleX - Premium Marketplace</title>
    <meta http-equiv="refresh" content="0; url=https://your-heroku-app.herokuapp.com">
</head>
<body>
    <p>Перенаправление на <a href="https://your-heroku-app.herokuapp.com">ResaleX</a>...</p>
</body>
</html>
```

#### 4.2 Или используйте GitHub Actions для автоматического деплоя

Создайте файл `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Heroku

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

### 5. Альтернатива: Деплой на Heroku + GitHub Pages редирект

#### 5.1 Деплой на Heroku
```bash
# Установите Heroku CLI
brew install heroku/brew/heroku

# Войдите
heroku login

# Создайте приложение
heroku create resalex-marketplace

# Добавьте переменные
heroku config:set SECRET_KEY=your-secret-key
heroku config:set STRIPE_PUBLISHABLE_KEY=pk_test_...
heroku config:set STRIPE_SECRET_KEY=sk_test_...

# Деплой
git push heroku main
```

#### 5.2 Создайте редирект на GitHub Pages
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ResaleX - Premium Marketplace</title>
    <meta http-equiv="refresh" content="0; url=https://resalex-marketplace.herokuapp.com">
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        .logo {
            font-size: 3rem;
            margin-bottom: 20px;
        }
        .loading {
            font-size: 1.2rem;
            margin: 20px 0;
        }
        .link {
            color: #ffc107;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">💎 ResaleX</div>
        <div class="loading">Перенаправление на приложение...</div>
        <p>Если перенаправление не произошло автоматически, <a href="https://resalex-marketplace.herokuapp.com" class="link">нажмите здесь</a></p>
    </div>
</body>
</html>
```

### 6. Обновление проекта

```bash
# Внесите изменения в код
# Добавьте изменения
git add .

# Сделайте коммит
git commit -m "Update: описание изменений"

# Загрузите на GitHub
git push origin main

# Обновите на Heroku (если используете)
git push heroku main
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

## ⚠️ Важные моменты

1. **GitHub Pages поддерживает только статические сайты**
2. **Для Flask приложений нужен сервер (Heroku, Railway, Render)**
3. **GitHub Pages можно использовать для редиректа**
4. **Или для документации проекта**

## 🆘 Если что-то не работает

1. **Проверьте настройки Pages в GitHub**
2. **Убедитесь, что репозиторий публичный**
3. **Проверьте, что файл index.html в корне**
4. **Подождите несколько минут для обновления**

---

**🎉 Готово! Ваш ResaleX доступен по адресу:**
**https://YOUR_USERNAME.github.io/resalex-marketplace**
