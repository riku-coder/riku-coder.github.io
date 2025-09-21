# 🚀 Быстрый деплой ResaleX

## 1. GitHub (2 минуты)

```bash
# В папке проекта
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/resalex-marketplace.git
git push -u origin main
```

## 2. Heroku (5 минут)

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

# Откройте
heroku open
```

## 3. Railway (3 минуты)

1. Перейдите на [Railway.app](https://railway.app)
2. Войдите через GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Выберите репозиторий
5. Готово!

## 4. Render (3 минуты)

1. Перейдите на [Render.com](https://render.com)
2. Войдите через GitHub
3. "New" → "Web Service"
4. Выберите репозиторий
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `python run.py`

## ⚠️ Важно

- Замените `YOUR_USERNAME` на ваш GitHub username
- Получите ключи Stripe на [stripe.com](https://stripe.com)
- Создайте `.env` файл с переменными окружения

---

**Готово! Ваш ResaleX в интернете!** 🎉
