#!/usr/bin/env python3
"""
ResaleX - Демонстрационные данные
Создает тестовые данные для демонстрации функционала
"""

from app import app, db, User, Product, Order
from datetime import datetime, timedelta
import random

def create_demo_users():
    """Создает демонстрационных пользователей"""
    users_data = [
        {'username': 'admin', 'email': 'admin@resalex.com', 'role': 'admin'},
        {'username': 'moderator1', 'email': 'moderator@resalex.com', 'role': 'moderator'},
        {'username': 'seller1', 'email': 'seller1@resalex.com', 'role': 'seller'},
        {'username': 'seller2', 'email': 'seller2@resalex.com', 'role': 'seller'},
        {'username': 'buyer1', 'email': 'buyer1@resalex.com', 'role': 'user'},
        {'username': 'buyer2', 'email': 'buyer2@resalex.com', 'role': 'user'},
    ]
    
    for user_data in users_data:
        if not User.query.filter_by(username=user_data['username']).first():
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                role=user_data['role']
            )
            user.set_password('password123')
            db.session.add(user)
    
    db.session.commit()
    print("✅ Демонстрационные пользователи созданы")

def create_demo_products():
    """Создает демонстрационные товары"""
    sellers = User.query.filter_by(role='seller').all()
    if not sellers:
        print("❌ Нет продавцов для создания товаров")
        return
    
    products_data = [
        {
            'name': 'Air Jordan 1 Retro High OG',
            'brand': 'Nike',
            'category': 'sneakers',
            'condition': 'new',
            'size': 'US 9',
            'price': 180.00,
            'description': 'Классические Air Jordan 1 в оригинальной цветовой схеме. Новые, с бирками.'
        },
        {
            'name': 'Yeezy Boost 350 V2',
            'brand': 'Adidas',
            'category': 'sneakers',
            'condition': 'like_new',
            'size': 'US 10',
            'price': 220.00,
            'description': 'Популярная модель Yeezy в отличном состоянии. Носили всего несколько раз.'
        },
        {
            'name': 'Supreme Box Logo Hoodie',
            'brand': 'Supreme',
            'category': 'clothing',
            'condition': 'good',
            'size': 'L',
            'price': 450.00,
            'description': 'Культовая толстовка Supreme с бокс-логотипом. В хорошем состоянии.'
        },
        {
            'name': 'Off-White x Nike Air Presto',
            'brand': 'Nike',
            'category': 'sneakers',
            'condition': 'new',
            'size': 'US 8.5',
            'price': 320.00,
            'description': 'Коллаборация Off-White и Nike. Новые, в оригинальной упаковке.'
        },
        {
            'name': 'Travis Scott x Air Jordan 1',
            'brand': 'Nike',
            'category': 'sneakers',
            'condition': 'like_new',
            'size': 'US 9.5',
            'price': 1200.00,
            'description': 'Эксклюзивная коллаборация с Travis Scott. Очень редкие.'
        },
        {
            'name': 'Balenciaga Triple S',
            'brand': 'Balenciaga',
            'category': 'sneakers',
            'condition': 'good',
            'size': 'US 10.5',
            'price': 280.00,
            'description': 'Стильные кроссовки Balenciaga. В хорошем состоянии.'
        },
        {
            'name': 'Gucci GG Marmont Bag',
            'brand': 'Gucci',
            'category': 'accessories',
            'condition': 'like_new',
            'size': 'One Size',
            'price': 890.00,
            'description': 'Элегантная сумка Gucci. Носили аккуратно, в отличном состоянии.'
        },
        {
            'name': 'iPhone 14 Pro Max',
            'brand': 'Apple',
            'category': 'electronics',
            'condition': 'new',
            'size': '256GB',
            'price': 1100.00,
            'description': 'Новый iPhone 14 Pro Max в оригинальной упаковке. Запечатан.'
        }
    ]
    
    for product_data in products_data:
        if not Product.query.filter_by(name=product_data['name']).first():
            product = Product(
                name=product_data['name'],
                brand=product_data['brand'],
                category=product_data['category'],
                condition=product_data['condition'],
                size=product_data['size'],
                price=product_data['price'],
                description=product_data['description'],
                seller_id=random.choice(sellers).id,
                status='approved'  # Автоматически одобряем для демо
            )
            db.session.add(product)
    
    db.session.commit()
    print("✅ Демонстрационные товары созданы")

def create_demo_orders():
    """Создает демонстрационные заказы"""
    buyers = User.query.filter_by(role='user').all()
    products = Product.query.filter_by(status='approved').all()
    
    if not buyers or not products:
        print("❌ Нет покупателей или товаров для создания заказов")
        return
    
    orders_data = [
        {'status': 'delivered', 'days_ago': 5},
        {'status': 'shipped', 'days_ago': 2},
        {'status': 'paid', 'days_ago': 1},
        {'status': 'pending', 'days_ago': 0},
    ]
    
    for order_data in orders_data:
        product = random.choice(products)
        buyer = random.choice(buyers)
        
        # Проверяем, что покупатель не является продавцом этого товара
        if buyer.id != product.seller_id:
            order = Order(
                buyer_id=buyer.id,
                product_id=product.id,
                total_amount=product.price,
                status=order_data['status'],
                created_at=datetime.utcnow() - timedelta(days=order_data['days_ago'])
            )
            
            if order_data['status'] == 'shipped':
                order.tracking_number = f"TR{random.randint(100000, 999999)}"
            
            db.session.add(order)
    
    db.session.commit()
    print("✅ Демонстрационные заказы созданы")

def main():
    """Основная функция создания демо данных"""
    print("🎭 Создание демонстрационных данных для ResaleX...")
    
    with app.app_context():
        # Создаем пользователей
        create_demo_users()
        
        # Создаем товары
        create_demo_products()
        
        # Создаем заказы
        create_demo_orders()
        
        print("\n🎉 Демонстрационные данные успешно созданы!")
        print("\n📋 Созданные аккаунты:")
        print("   Root: root / admin123")
        print("   Admin: admin / password123")
        print("   Moderator: moderator1 / password123")
        print("   Seller: seller1 / password123")
        print("   Buyer: buyer1 / password123")
        print("\n🚀 Теперь вы можете протестировать все функции!")

if __name__ == '__main__':
    main()
