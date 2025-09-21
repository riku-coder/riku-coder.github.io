#!/bin/bash

# ResaleX - Скрипт быстрого деплоя на GitHub
echo "🚀 ResaleX - Быстрый деплой на GitHub"
echo "======================================"

# Проверяем, что мы в правильной директории
if [ ! -f "app.py" ]; then
    echo "❌ Ошибка: Запустите скрипт из папки resale"
    exit 1
fi

# Проверяем, что Git инициализирован
if [ ! -d ".git" ]; then
    echo "📦 Инициализация Git репозитория..."
    git init
fi

# Добавляем все файлы
echo "📁 Добавление файлов в Git..."
git add .

# Создаем коммит
echo "💾 Создание коммита..."
git commit -m "ResaleX: Premium marketplace ready for deployment

✅ Features:
- Dark theme with liquid glass effects
- User management system
- Product management
- Chat system between buyers and sellers
- Notification system
- Payment integration with Stripe
- Russian Rubles currency
- Responsive design
- Admin panel with full control

🎨 Design:
- Modern black colors
- Mobile-friendly navigation
- Premium UI/UX
- Animated backgrounds
- Custom scrollbar

🔧 Technical:
- Flask backend
- SQLite database
- Bootstrap 5 frontend
- Font Awesome icons
- Google Fonts (Inter)

Ready for production deployment!"

# Показываем статус
echo "📊 Статус Git:"
git status

echo ""
echo "✅ Готово! Теперь выполните следующие команды:"
echo ""
echo "1. Создайте репозиторий на GitHub.com"
echo "2. Подключите репозиторий:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/resale-marketplace.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Деплой на хостинг:"
echo "   - Railway: https://railway.app"
echo "   - Render: https://render.com"
echo "   - Heroku: https://heroku.com"
echo ""
echo "📖 Подробная инструкция в файле FINAL_DEPLOY.md"
echo ""
echo "🎉 Удачи с деплоем!"
