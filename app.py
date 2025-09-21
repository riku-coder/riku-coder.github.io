from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DecimalField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import stripe
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])

# Stripe configuration (для тестирования, в продакшене заменить на СБП)
stripe.api_key = app.config['STRIPE_SECRET_KEY']

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, seller, moderator, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    avatar_url = db.Column(db.String(120), nullable=True)
    email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(120), nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    brand = db.Column(db.String(100))
    category = db.Column(db.String(50))
    size = db.Column(db.String(20))
    condition = db.Column(db.String(50))  # New, Like New, Good, Fair, Poor
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, sold
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    seller = db.relationship('User', backref='products')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, shipped, delivered, cancelled
    payment_intent_id = db.Column(db.String(200))
    tracking_number = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    buyer = db.relationship('User', foreign_keys=[buyer_id], backref='orders')
    product = db.relationship('Product', backref='orders')

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    order = db.relationship('Order', backref='messages')

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=1, max=200)])
    description = TextAreaField('Description')
    brand = StringField('Brand', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('sneakers', 'Sneakers'),
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('electronics', 'Electronics'),
        ('collectibles', 'Collectibles')
    ])
    size = StringField('Size')
    condition = SelectField('Condition', choices=[
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    image = FileField('Product Image')
    submit = SubmitField('Add Product')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[
        ('user', 'User'),
        ('seller', 'Seller'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    ])
    submit = SubmitField('Create User')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    products = Product.query.filter_by(status='approved').order_by(Product.created_at.desc()).limit(12).all()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Пользователь с таким именем уже существует', 'error')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Пользователь с таким email уже существует', 'error')
            return render_template('register.html', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role='user'  # Все регистрирующиеся пользователи - покупатели
        )
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно! Теперь вы можете войти в систему', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        users = User.query.all()
        products = Product.query.all()
        orders = Order.query.all()
        return render_template('admin_dashboard.html', users=users, products=products, orders=orders)
    elif current_user.role == 'moderator':
        products = Product.query.filter_by(status='pending').all()
        orders = Order.query.all()
        return render_template('moderator_dashboard.html', products=products, orders=orders)
    elif current_user.role == 'seller':
        products = Product.query.filter_by(seller_id=current_user.id).all()
        orders = Order.query.join(Product).filter(Product.seller_id == current_user.id).all()
        return render_template('seller_dashboard.html', products=products, orders=orders)
    else:
        orders = Order.query.filter_by(buyer_id=current_user.id).all()
        return render_template('user_dashboard.html', orders=orders)

@app.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.role not in ['root', 'admin']:
        flash('У вас нет прав для создания пользователей', 'error')
        return redirect(url_for('dashboard'))
    
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return render_template('create_user.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'error')
            return render_template('create_user.html', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_user.html', form=form)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role not in ['seller', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            brand=form.brand.data,
            category=form.category.data,
            size=form.size.data,
            condition=form.condition.data,
            price=form.price.data,
            seller_id=current_user.id
        )
        
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            if filename:
                form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                product.image_url = f'/static/uploads/{filename}'
        
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_product.html', form=form)

@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(status='approved')
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Product.name.contains(search) | Product.brand.contains(search))
    
    products = query.paginate(page=page, per_page=12, error_out=False)
    
    return render_template('products.html', products=products, category=category, search=search)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/buy/<int:product_id>', methods=['POST'])
@login_required
def buy_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if product.seller_id == current_user.id:
        flash('You cannot buy your own product', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    if product.status != 'approved':
        flash('Product is not available for purchase', 'error')
        return redirect(url_for('product_detail', product_id=product_id))
    
    # Create order
    order = Order(
        buyer_id=current_user.id,
        product_id=product.id,
        total_amount=product.price,
        status='pending'
    )
    
    db.session.add(order)
    db.session.commit()
    
    # Create Stripe payment intent
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(product.price * 100),  # Convert to cents
            currency='usd',
            metadata={'order_id': order.id}
        )
        order.payment_intent_id = intent.id
        db.session.commit()
        
        return render_template('payment.html', order=order, client_secret=intent.client_secret)
    except Exception as e:
        flash('Payment processing error', 'error')
        return redirect(url_for('product_detail', product_id=product_id))

@app.route('/update_order_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check permissions
    can_update = (
        current_user.role in ['admin', 'moderator'] or
        (current_user.role == 'seller' and order.product.seller_id == current_user.id)
    )
    
    if not can_update:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    new_status = request.form.get('status')
    tracking_number = request.form.get('tracking_number', '')
    
    if new_status in ['shipped', 'delivered', 'cancelled']:
        order.status = new_status
        if tracking_number:
            order.tracking_number = tracking_number
        db.session.commit()
        flash('Order status updated successfully', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/update_product_status/<int:product_id>', methods=['POST'])
@login_required
def update_product_status(product_id):
    if current_user.role not in ['admin', 'moderator']:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    product = Product.query.get_or_404(product_id)
    new_status = request.form.get('status')
    
    if new_status in ['approved', 'rejected']:
        product.status = new_status
        db.session.commit()
        flash('Product status updated successfully', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Проверяем права доступа
    if current_user.role not in ['admin', 'moderator'] and product.seller_id != current_user.id:
        flash('У вас нет прав для редактирования этого товара', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.brand = request.form.get('brand')
        product.category = request.form.get('category')
        product.condition = request.form.get('condition')
        product.size = request.form.get('size')
        
        # Обработка загрузки нового изображения
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                if filename:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    product.image_url = filename
        
        # Если редактирует продавец, товар требует повторного одобрения
        if current_user.role not in ['admin', 'moderator']:
            product.status = 'pending'
            flash('Товар обновлен и отправлен на модерацию', 'success')
        else:
            flash('Товар успешно обновлен', 'success')
        
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Проверяем права доступа
    if current_user.role not in ['admin', 'moderator'] and product.seller_id != current_user.id:
        flash('У вас нет прав для удаления этого товара', 'error')
        return redirect(url_for('dashboard'))
    
    # Удаляем изображение если есть
    if product.image_url:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image_url)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(product)
    db.session.commit()
    flash('Товар успешно удален', 'success')
    return redirect(url_for('dashboard'))

@app.route('/profile')
@login_required
def profile():
    # Получаем статистику пользователя
    orders = Order.query.filter_by(buyer_id=current_user.id).all()
    products = Product.query.filter_by(seller_id=current_user.id).all() if current_user.role in ['seller', 'admin', 'moderator'] else []
    
    total_spent = sum(order.total_amount for order in orders)
    total_earned = sum(order.total_amount for order in Order.query.join(Product).filter(Product.seller_id == current_user.id).all()) if current_user.role in ['seller', 'admin', 'moderator'] else 0
    
    return render_template('profile.html', 
                         orders=orders, 
                         products=products,
                         total_spent=total_spent,
                         total_earned=total_earned)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Обновляем данные пользователя
        current_user.username = request.form.get('username', current_user.username)
        current_user.email = request.form.get('email', current_user.email)
        
        # Обновляем пароль если указан новый
        new_password = request.form.get('password')
        if new_password:
            current_user.password_hash = generate_password_hash(new_password)
        
        # Обработка загрузки аватара
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename:
                filename = secure_filename(file.filename)
                if filename:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    current_user.avatar_url = filename
        
        db.session.commit()
        flash('Профиль успешно обновлен', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html')

@app.route('/admin/user/<int:user_id>/toggle_status', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    if current_user.role not in ['admin', 'moderator']:
        flash('У вас нет прав для выполнения этого действия', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'активирован' if user.is_active else 'заблокирован'
    flash(f'Пользователь {user.username} {status}', 'success')
    return redirect(url_for('dashboard'))

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role not in ['admin', 'moderator']:
        flash('У вас нет прав для выполнения этого действия', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Нельзя удалить root пользователя
    if user.role == 'root':
        flash('Нельзя удалить root пользователя', 'error')
        return redirect(url_for('dashboard'))
    
    # Нельзя удалить самого себя
    if user.id == current_user.id:
        flash('Нельзя удалить самого себя', 'error')
        return redirect(url_for('dashboard'))
    
    db.session.delete(user)
    db.session.commit()
    flash(f'Пользователь {user.username} удален', 'success')
    return redirect(url_for('dashboard'))

@app.route('/chat/<int:order_id>')
@login_required
def chat(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Проверяем права доступа к чату
    if current_user.id not in [order.buyer_id, order.product.seller_id] and current_user.role not in ['admin', 'moderator']:
        flash('У вас нет прав для просмотра этого чата', 'error')
        return redirect(url_for('dashboard'))
    
    messages = ChatMessage.query.filter_by(order_id=order_id).order_by(ChatMessage.created_at.asc()).all()
    
    # Помечаем сообщения как прочитанные
    for message in messages:
        if message.receiver_id == current_user.id:
            message.is_read = True
    db.session.commit()
    
    return render_template('chat.html', order=order, messages=messages)

@app.route('/chat/<int:order_id>/send', methods=['POST'])
@login_required
def send_message(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Проверяем права доступа к чату
    if current_user.id not in [order.buyer_id, order.product.seller_id] and current_user.role not in ['admin', 'moderator']:
        flash('У вас нет прав для отправки сообщений в этот чат', 'error')
        return redirect(url_for('dashboard'))
    
    message_text = request.form.get('message')
    if not message_text:
        flash('Сообщение не может быть пустым', 'error')
        return redirect(url_for('chat', order_id=order_id))
    
    # Определяем получателя
    receiver_id = order.buyer_id if current_user.id == order.product.seller_id else order.product.seller_id
    
    message = ChatMessage(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        order_id=order_id,
        message=message_text
    )
    
    db.session.add(message)
    db.session.commit()
    
    flash('Сообщение отправлено', 'success')
    return redirect(url_for('chat', order_id=order_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create root admin user if it doesn't exist
        if not User.query.filter_by(username='root').first():
            root_user = User(
                username='root',
                email='admin@resale.com',
                role='admin'
            )
            root_user.set_password('admin123')  # User should change this
            db.session.add(root_user)
            db.session.commit()
            print("Root admin created with username: root, password: admin123")

# API для уведомлений
@app.route('/api/notifications')
@login_required
def get_notifications():
    # Получаем последние 10 уведомлений для пользователя
    notifications = []
    
    # Уведомления о новых заказах (для продавцов)
    if current_user.role in ['seller', 'admin']:
        recent_orders = Order.query.filter(
            Order.product.has(seller_id=current_user.id),
            Order.created_at >= datetime.utcnow() - timedelta(days=7)
        ).order_by(Order.created_at.desc()).limit(5).all()
        
        for order in recent_orders:
            notifications.append({
                'id': order.id,
                'title': 'Новый заказ',
                'message': f'Заказ #{order.id} на {order.product.name}',
                'created_at': order.created_at.isoformat(),
                'is_read': False
            })
    
    # Уведомления о статусе заказов (для покупателей)
    if current_user.role == 'user':
        recent_orders = Order.query.filter(
            Order.buyer_id == current_user.id,
            Order.created_at >= datetime.utcnow() - timedelta(days=7)
        ).order_by(Order.created_at.desc()).limit(5).all()
        
        for order in recent_orders:
            if order.status in ['shipped', 'delivered']:
                notifications.append({
                    'id': order.id,
                    'title': 'Обновление заказа',
                    'message': f'Заказ #{order.id} - статус: {order.status}',
                    'created_at': order.created_at.isoformat(),
                    'is_read': False
                })
    
    return jsonify({'notifications': notifications})

@app.route('/api/notifications/unread')
@login_required
def get_unread_notifications_count():
    count = 0
    
    # Подсчитываем непрочитанные уведомления
    if current_user.role in ['seller', 'admin']:
        count = Order.query.filter(
            Order.product.has(seller_id=current_user.id),
            Order.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
    elif current_user.role == 'user':
        count = Order.query.filter(
            Order.buyer_id == current_user.id,
            Order.status.in_(['shipped', 'delivered']),
            Order.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
    
    return jsonify({'count': count})

if __name__ == '__main__':
    app.run(debug=True)
