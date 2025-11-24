from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .models import User, Property, Transaction, PriceHistory
from flask import jsonify

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('main.signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('main.login'))

    return render_template('signup.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))

        flash('Login failed.')
        return redirect(url_for('main.login'))

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@login_required
def dashboard():
    properties = Property.query.all()
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    portfolio = []
    existing_images = [] # Placeholder, need to implement image check logic or pass it

    for transaction in user_transactions:
        prop = Property.query.get(transaction.property_id)
        if prop:
            fractions_owned = transaction.fractions_bought
            equity = (fractions_owned / prop.total_fractions) * prop.total_value
            portfolio.append({
                'property_name': prop.name,
                'fractions_owned': fractions_owned,
                'equity': equity
            })

    return render_template('dashboard.html', properties=properties, portfolio=portfolio, existing_images=existing_images)

@main.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admins only.')
        return redirect(url_for('main.dashboard'))
    
    properties = Property.query.all()
    return render_template('admin_dashboard.html', properties=properties)

@main.route('/admin/add_property', methods=['POST'])
@login_required
def admin_add_property():
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('main.home'))
    
    name = request.form.get('name')
    total_value = float(request.form.get('total_value'))
    total_fractions = int(request.form.get('total_fractions'))
    description = request.form.get('description')
    location = request.form.get('location')
    image_url = request.form.get('image_url')

    new_property = Property(
        name=name,
        total_value=total_value,
        total_fractions=total_fractions,
        available_fractions=total_fractions,
        description=description,
        location=location,
        image_url=image_url
    )
    db.session.add(new_property)
    db.session.commit()
    flash('Property added successfully!')
    return redirect(url_for('main.admin_dashboard'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main.route('/add_funds', methods=['POST'])
@login_required
def add_funds():
    try:
        amount = float(request.form.get('amount'))
        if amount <= 0:
            flash('Amount must be positive.')
        else:
            current_user.balance += amount
            db.session.commit()
            flash(f'Successfully added ${amount:.2f}!')
    except (ValueError, TypeError):
        flash('Invalid amount.')
    
    return redirect(url_for('main.profile'))

@main.route('/property/<int:property_id>')
def property_details(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('property_details.html', property=property)

@main.route('/buy/<int:property_id>', methods=['GET', 'POST'])
@login_required
def buy(property_id):
    prop = Property.query.get_or_404(property_id)

    if request.method == 'POST':
        try:
            fractions = int(request.form.get('fractions'))
        except (TypeError, ValueError):
            flash('Invalid number.')
            return redirect(url_for('main.buy', property_id=property_id))

        if fractions > prop.available_fractions:
            flash('Not enough fractions.')
            return redirect(url_for('main.buy', property_id=property_id))

        price_per_fraction = prop.total_value / prop.total_fractions
        total_cost = fractions * price_per_fraction

        if current_user.balance < total_cost:
            flash('Insufficient balance.')
            return redirect(url_for('main.buy', property_id=property_id))

        current_user.balance -= total_cost
        prop.available_fractions -= fractions
        new_transaction = Transaction(
            user_id=current_user.id,
            property_id=prop.id,
            fractions_bought=fractions,
            price_per_fraction=price_per_fraction
        )
        db.session.add(new_transaction)
        db.session.commit()

        flash('Purchase successful!')
        return render_template('success.html', property_name=prop.name)

    return render_template('buy.html', property=prop)

@main.route('/api/history/<int:property_id>')
def get_price_history(property_id):
    history = PriceHistory.query.filter_by(property_id=property_id).order_by(PriceHistory.timestamp).all()
    data = [{'price': h.price, 'timestamp': h.timestamp.strftime('%Y-%m-%d %H:%M')} for h in history]
    return jsonify(data)
