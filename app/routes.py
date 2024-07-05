from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Order
from app.forms import RegistrationForm, LoginForm, OrderForm, AddressEmailForm
from sqlalchemy import or_

bp = Blueprint('routes', __name__)
@bp.route("/")
@bp.route("/home")
def home():
    return render_template('home.html')

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password_hash=hashed_password, user_type=form.user_type.data, phone_no = form.phone_no.data)
        global temp_user_id
        
        db.session.add(user)
        temp_user_id = user.id
        db.session.commit()
        if user.user_type != 'delivery':
            return redirect(url_for('routes.address_redirect', user_id = user.id))
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('routes.login'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)

@bp.route("/address_redirect/<int:user_id>", methods=['GET', 'POST'])
def address_redirect(user_id):
    form = AddressEmailForm()
    user = User.query.get(user_id)
    if not user:
        redirect(url_for('routes.register'))
    if form.validate_on_submit():
        user.email = form.email.data
        user.address = form.address.data
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('routes.login'))
    else:
        print(form.errors)
    return render_template('address_redirect.html', form=form, user_id = user_id)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('routes.dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    else:
        print(form.errors)
    return render_template('login.html', title='Login', form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@bp.route("/dashboard")
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('routes.login'))
    elif current_user.username == 'dev':
        return redirect(url_for('routes.dev_page'))
    elif current_user.user_type == 'hospital':
        return redirect(url_for('routes.hospital_dashboard'))
    elif current_user.user_type == 'vendor':
        return redirect(url_for('routes.vendor_dashboard'))
    elif current_user.user_type == 'delivery':
        return redirect(url_for('routes.delivery_dashboard'))

@bp.route("/hospital_dashboard", methods=['GET', 'POST'])
def hospital_dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('routes.login'))
    if current_user.user_type != 'hospital':
        return redirect(url_for('routes.access_denied'))
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(item=form.item.data, amount=form.amount.data, hospital_username=current_user.username, urgency=form.urgency.data)
        db.session.add(order)
        db.session.commit()
        flash('Your order has been placed!', 'success')
        return redirect(url_for('routes.hospital_dashboard'))
    past_orders = Order.query.filter_by(hospital_username=current_user.username).filter(Order.status == 'received').all()
    current_orders = Order.query.filter_by(hospital_username=current_user.username).filter(or_( Order.status == 'current', Order.status == 'out_for_delivery', Order.status == 'delivered')).all()
    return render_template('hospital_dashboard.html', title='Hospital Dashboard', form=form, past_orders=past_orders, current_orders=current_orders)

@bp.route("/call_del_order/<int:order_id>")
def call_del_order(order_id):
    del_order(order_id)
    return redirect(url_for('routes.hospital_dashboard'))

def del_order(order_id :int):
    order = Order.query.get(order_id)
    if order:
        order.status = 'removed'
        db.session.commit()
    

@bp.route("/vendor_dashboard")
def vendor_dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('routes.login'))
    if current_user.user_type != 'vendor':
        return redirect(url_for('routes.access_denied'))
    orders = Order.query.filter_by(status='current').all()
    i = 4
    for order in orders:
        order.distance = i
        i = i-1

    orders = Order.query.filter_by(status='current').order_by(Order.distance).all()    
    return render_template('vendor_dashboard.html', title='Vendor Dashboard', orders=orders)

@bp.route("/delivery_dashboard")
def delivery_dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('routes.login'))
    if current_user.user_type != 'delivery':
        return redirect(url_for('routes.access_denied'))
    orders = Order.query.filter_by(status='out_for_delivery').all()
    return render_template('delivery_dashboard.html', title='Delivery Dashboard', orders=orders)

@bp.route("/checkout_order/<int:order_id>", methods=['POST'])
def checkout_order(order_id):
    if not current_user.is_authenticated:
        return redirect(url_for('routes.login'))
    if current_user.user_type != 'vendor':
        return redirect(url_for('routes.access_denied'))
    order = Order.query.get_or_404(order_id)
    order.status = 'out_for_delivery'
    order.vendor = current_user.username
    order.phone_no = current_user.phone_no
    db.session.commit()
    flash('Order checked out for delivery', 'success')
    return redirect(url_for('routes.vendor_dashboard'))

@bp.route("/deliver_order/<int:order_id>", methods=['POST'])
def deliver_order(order_id):
    if not current_user.is_authenticated:
        return redirect(url_for('routes.login'))
    if current_user.user_type != 'delivery':
        return redirect(url_for('routes.access_denied'))
    order = Order.query.get_or_404(order_id)
    order.status = 'delivered'
    db.session.commit()
    flash('Order delivered', 'success')
    return redirect(url_for('routes.delivery_dashboard'))

@bp.route("/order_received/<int:order_id>", methods=['POST'])
def order_received(order_id):
    if not current_user.is_authenticated:
        return redirect(url_for('routes.login'))
    if current_user.user_type != 'hospital':
        return redirect(url_for('routes.access_denied'))
    order = Order.query.get_or_404(order_id)
    order.status = 'received'
    db.session.commit()
    Order.update_csv()  
    flash('Order received', 'success')
    return redirect(url_for('routes.hospital_dashboard'))

@bp.route("/access_denied")
def access_denied():
    return render_template('access_denied.html')

@bp.route("/dev_page")
def dev_page():
    if not current_user.is_authenticated:
        return redirect(url_for('routes.login'))
    if  current_user.username != 'dev':
        return redirect(url_for('routes.access_denied'))
    
    all_users = User.query.all()
    all_orders = Order.query.all()
    return render_template('dev_page.html', all_users = all_users, all_orders = all_orders)

@bp.route("/dev_order_delete/<int:order_id>")
def dev_order_delete(order_id):
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for('routes.dev_page'))

@bp.route("/dev_user_delete/<int:user_id>")
def dev_user_delete(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('routes.dev_page'))
