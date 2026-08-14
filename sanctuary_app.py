from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import os
from dotenv import load_dotenv
import logging
from functools import wraps

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# ============= SECURITY CONFIGURATION =============
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sanctuary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============= DATABASE MODELS =============
class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class ContactSubmission(db.Model):
    """Store contact form submissions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactSubmission {self.id}>'

# ============= FORMS =============
class LoginForm(FlaskForm):
    """Login form with CSRF protection"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    """Registration form with validation"""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class ContactForm(FlaskForm):
    """Secure contact form"""
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=120, message='Name must be between 2 and 120 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    phone = StringField('Phone', validators=[Length(max=20)])
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, max=2000, message='Message must be between 10 and 2000 characters')
    ])
    submit = SubmitField('Send Message')

# ============= USER LOADER =============
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for session management"""
    return User.query.get(int(user_id))

# ============= SECURITY HEADERS =============
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

# ============= ADMIN DECORATOR =============
def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first.', 'danger')
            return redirect(url_for('login', next=request.url))
        if not current_user.is_admin:
            logger.warning(f'Unauthorized admin access attempt by user: {current_user.username}')
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ============= APARTMENT UNITS DATA =============
UNITS_DATA = [
    {"id": 1, "number": "101", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Available", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 2, "number": "102", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Available", "description": "Spacious one-bedroom with separate living space."},
    {"id": 3, "number": "103", "type": "2 Bedroom", "bedrooms": 2, "bathrooms": 2, "price": 2000, "amenities": ["Kitchen", "2 Bedrooms", "Living Room", "Balcony", "Walk-in Closet"], "availability": "Occupied", "description": "Luxurious two-bedroom apartment with premium finishes."},
    {"id": 4, "number": "104", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Available", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 5, "number": "105", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Available", "description": "Spacious one-bedroom with separate living space."},
    {"id": 6, "number": "201", "type": "2 Bedroom", "bedrooms": 2, "bathrooms": 2, "price": 2000, "amenities": ["Kitchen", "2 Bedrooms", "Living Room", "Balcony", "Walk-in Closet"], "availability": "Available", "description": "Luxurious two-bedroom apartment with premium finishes."},
    {"id": 7, "number": "202", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Occupied", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 8, "number": "203", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Available", "description": "Spacious one-bedroom with separate living space."},
    {"id": 9, "number": "204", "type": "2 Bedroom", "bedrooms": 2, "bathrooms": 2, "price": 2000, "amenities": ["Kitchen", "2 Bedrooms", "Living Room", "Balcony", "Walk-in Closet"], "availability": "Available", "description": "Luxurious two-bedroom apartment with premium finishes."},
    {"id": 10, "number": "205", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Available", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 11, "number": "301", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Occupied", "description": "Spacious one-bedroom with separate living space."},
    {"id": 12, "number": "302", "type": "2 Bedroom", "bedrooms": 2, "bathrooms": 2, "price": 2000, "amenities": ["Kitchen", "2 Bedrooms", "Living Room", "Balcony", "Walk-in Closet"], "availability": "Available", "description": "Luxurious two-bedroom apartment with premium finishes."},
    {"id": 13, "number": "303", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Available", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 14, "number": "304", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Available", "description": "Spacious one-bedroom with separate living space."},
    {"id": 15, "number": "305", "type": "2 Bedroom", "bedrooms": 2, "bathrooms": 2, "price": 2000, "amenities": ["Kitchen", "2 Bedrooms", "Living Room", "Balcony", "Walk-in Closet"], "availability": "Available", "description": "Luxurious two-bedroom apartment with premium finishes."},
    {"id": 16, "number": "401", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Occupied", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 17, "number": "402", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Available", "description": "Spacious one-bedroom with separate living space."},
    {"id": 18, "number": "403", "type": "2 Bedroom", "bedrooms": 2, "bathrooms": 2, "price": 2000, "amenities": ["Kitchen", "2 Bedrooms", "Living Room", "Balcony", "Walk-in Closet"], "availability": "Available", "description": "Luxurious two-bedroom apartment with premium finishes."},
    {"id": 19, "number": "404", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Available", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 20, "number": "405", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Available", "description": "Spacious one-bedroom with separate living space."},
    {"id": 21, "number": "501", "type": "2 Bedroom", "bedrooms": 2, "bathrooms": 2, "price": 2000, "amenities": ["Kitchen", "2 Bedrooms", "Living Room", "Balcony", "Walk-in Closet"], "availability": "Available", "description": "Luxurious two-bedroom apartment with premium finishes."},
    {"id": 22, "number": "502", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Occupied", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 23, "number": "503", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Available", "description": "Spacious one-bedroom with separate living space."},
    {"id": 24, "number": "504", "type": "2 Bedroom", "bedrooms": 2, "bathrooms": 2, "price": 2000, "amenities": ["Kitchen", "2 Bedrooms", "Living Room", "Balcony", "Walk-in Closet"], "availability": "Available", "description": "Luxurious two-bedroom apartment with premium finishes."},
    {"id": 25, "number": "505", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Available", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 26, "number": "601", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Available", "description": "Spacious one-bedroom with separate living space."},
    {"id": 27, "number": "602", "type": "2 Bedroom", "bedrooms": 2, "bathrooms": 2, "price": 2000, "amenities": ["Kitchen", "2 Bedrooms", "Living Room", "Balcony", "Walk-in Closet"], "availability": "Occupied", "description": "Luxurious two-bedroom apartment with premium finishes."},
    {"id": 28, "number": "603", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Available", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 29, "number": "604", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Available", "description": "Spacious one-bedroom with separate living space."},
    {"id": 30, "number": "605", "type": "2 Bedroom", "bedrooms": 2, "bathrooms": 2, "price": 2000, "amenities": ["Kitchen", "2 Bedrooms", "Living Room", "Balcony", "Walk-in Closet"], "availability": "Available", "description": "Luxurious two-bedroom apartment with premium finishes."},
    {"id": 31, "number": "701", "type": "Studio", "bedrooms": 0, "bathrooms": 1, "price": 1200, "amenities": ["Kitchen", "Living Area", "Balcony"], "availability": "Occupied", "description": "Cozy studio with modern finishes and natural lighting."},
    {"id": 32, "number": "702", "type": "1 Bedroom", "bedrooms": 1, "bathrooms": 1, "price": 1500, "amenities": ["Kitchen", "Bedroom", "Living Room", "Balcony"], "availability": "Available", "description": "Spacious one-bedroom with separate living space."},
]

# ============= AUTHENTICATION ROUTES =============
@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def register():
    """User registration with rate limiting"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = User(username=secure_filename(form.username.data), email=form.email.data.lower())
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            logger.info(f'New user registered: {user.username}')
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logger.error(f'Registration error: {str(e)}')
            flash('An error occurred during registration. Please try again.', 'danger')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    """User login with rate limiting"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Your account has been deactivated.', 'danger')
                logger.warning(f'Login attempt by deactivated user: {user.username}')
                return redirect(url_for('login'))
            
            login_user(user, remember=True)
            logger.info(f'User logged in: {user.username}')
            next_page = request.args.get('next')
            if not next_page or url_has_allowed_host_and_scheme(next_page):
                next_page = url_for('dashboard')
            return redirect(next_page)
        else:
            logger.warning(f'Failed login attempt for username: {form.username.data}')
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    username = current_user.username
    logout_user()
    logger.info(f'User logged out: {username}')
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

# ============= ADMIN ROUTES =============
@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    """Admin dashboard"""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    total_contacts = ContactSubmission.query.count()
    recent_contacts = ContactSubmission.query.order_by(ContactSubmission.created_at.desc()).limit(10).all()
    
    stats = {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': total_users - active_users,
        'total_contacts': total_contacts,
        'admin_users': User.query.filter_by(is_admin=True).count()
    }
    
    return render_template('admin_dashboard.html', stats=stats, recent_contacts=recent_contacts, user=current_user)

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """Manage users - admin only"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('admin_users.html', users=users, user=current_user)

@app.route('/admin/contacts')
@login_required
@admin_required
def admin_contacts():
    """View all contact submissions - admin only"""
    page = request.args.get('page', 1, type=int)
    contacts = ContactSubmission.query.order_by(ContactSubmission.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin_contacts.html', contacts=contacts, user=current_user)

@app.route('/admin/user/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Toggle admin status for a user"""
    if user_id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot change your own admin status'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    try:
        user.is_admin = not user.is_admin
        db.session.commit()
        logger.info(f'Admin status toggled for user {user.username} by {current_user.username}')
        return jsonify({'success': True, 'message': f'User is now {"admin" if user.is_admin else "regular user"}', 'is_admin': user.is_admin})
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error toggling admin status: {str(e)}')
        return jsonify({'success': False, 'message': 'Error updating user'}), 500

@app.route('/admin/user/<int:user_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_active(user_id):
    """Toggle active status for a user"""
    if user_id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot deactivate your own account'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    try:
        user.is_active = not user.is_active
        db.session.commit()
        logger.info(f'Active status toggled for user {user.username} by {current_user.username}')
        return jsonify({'success': True, 'message': f'User is now {"active" if user.is_active else "deactivated"}', 'is_active': user.is_active})
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error toggling active status: {str(e)}')
        return jsonify({'success': False, 'message': 'Error updating user'}), 500

def url_has_allowed_host_and_scheme(url, allowed_hosts=None):
    """Prevent open redirect vulnerability"""
    from urllib.parse import urlparse
    if allowed_hosts is None:
        allowed_hosts = {app.config.get('SERVER_NAME', 'localhost')}
    parsed_url = urlparse(url)
    return not parsed_url.netloc or parsed_url.netloc in allowed_hosts

# ============= PROTECTED ROUTES =============
@app.route('/')
def index():
    """Landing page - redirect to dashboard if authenticated"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with apartment listings"""
    return render_template('dashboard.html', units=UNITS_DATA, user=current_user)

@app.route('/unit/<int:unit_id>')
@login_required
def unit_detail(unit_id):
    """View unit details - requires authentication"""
    unit = next((u for u in UNITS_DATA if u['id'] == unit_id), None)
    if not unit:
        flash('Unit not found.', 'warning')
        return redirect(url_for('dashboard'))
    return render_template('unit_detail.html', unit=unit)

# ============= API ROUTES (SECURED) =============
@app.route('/api/units', methods=['GET'])
@login_required
def get_units():
    """Get all units - requires authentication"""
    return jsonify(UNITS_DATA)

@app.route('/api/units/filter', methods=['POST'])
@login_required
def filter_units():
    """Filter units - requires authentication"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    
    filtered = UNITS_DATA
    
    # Validate and filter by type
    if 'type' in data and data['type'] in ['Studio', '1 Bedroom', '2 Bedroom']:
        filtered = [u for u in filtered if u['type'] == data['type']]
    
    # Validate and filter by price
    try:
        if 'price_min' in data and isinstance(data['price_min'], (int, float)):
            filtered = [u for u in filtered if u['price'] >= data['price_min']]
        
        if 'price_max' in data and isinstance(data['price_max'], (int, float)):
            filtered = [u for u in filtered if u['price'] <= data['price_max']]
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid price filter'}), 400
    
    # Validate and filter by availability
    if 'availability' in data and data['availability'] in ['Available', 'Occupied']:
        filtered = [u for u in filtered if u['availability'] == data['availability']]
    
    return jsonify(filtered)

@app.route('/api/contact', methods=['POST'])
@login_required
@limiter.limit("5 per hour")
def submit_contact():
    """Submit contact form - requires authentication and rate limiting"""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            contact = ContactSubmission(
                user_id=current_user.id,
                name=secure_filename(form.name.data),
                email=form.email.data.lower(),
                phone=form.phone.data if form.phone.data else None,
                message=form.message.data
            )
            db.session.add(contact)
            db.session.commit()
            logger.info(f'Contact form submitted by user: {current_user.username}')
            return jsonify({
                'success': True,
                'message': 'Thank you! We will contact you soon.'
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f'Contact submission error: {str(e)}')
            return jsonify({
                'success': False,
                'message': 'Error submitting form. Please try again.'
            }), 500
    else:
        return jsonify({
            'success': False,
            'errors': form.errors
        }), 400

# ============= ERROR HANDLERS =============
@app.errorhandler(403)
def forbidden(error):
    """Handle forbidden access"""
    return render_template('error.html', 
                         error_code=403, 
                         error_message='Access Forbidden'), 403

@app.errorhandler(404)
def not_found(error):
    """Handle page not found"""
    return render_template('error.html', 
                         error_code=404, 
                         error_message='Page Not Found'), 404

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded"""
    return render_template('error.html', 
                         error_code=429, 
                         error_message='Too many requests. Please try again later.'), 429

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server error"""
    db.session.rollback()
    logger.error(f'Internal server error: {str(error)}')
    return render_template('error.html', 
                         error_code=500, 
                         error_message='Internal Server Error'), 500

# ============= APPLICATION INITIALIZATION =============
def create_app():
    """Application factory"""
    with app.app_context():
        db.create_all()
        
        # Create default admin user if it doesn't exist
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@sanctuaryapartments.com',
                is_admin=True,
                is_active=True
            )
            admin_user.set_password('gordonramsey')
            db.session.add(admin_user)
            db.session.commit()
            logger.info('Admin user created: admin')
    
    return app

if __name__ == '__main__':
    create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'False').lower() == 'true')
