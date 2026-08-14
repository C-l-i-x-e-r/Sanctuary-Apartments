# Setup Guide - Sanctuary Apartments Secure Web Application

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Windows PowerShell or Command Prompt

### Installation Steps

1. **Navigate to project directory**:
```powershell
cd "c:\Users\HomePC\Desktop\VISUAL STUDIO"
```

2. **Install dependencies**:
```powershell
python -m pip install -r requirements.txt
```

3. **Update environment configuration** (`.env`):
```
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<generate-a-random-key-below>
SQLALCHEMY_DATABASE_URI=sqlite:///sanctuary.db
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

   **Generate a secure SECRET_KEY**:
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output and paste it as the value for `SECRET_KEY` in `.env`

4. **Run the application**:
```powershell
python sanctuary_app.py
```

5. **Access the application**:
   - Open browser to: `http://localhost:5000`
   - You will be redirected to login page

## Default Admin Account

### Initial Login
- **Username**: `admin`
- **Password**: `gordonramsey`

The admin account is automatically created when the application starts for the first time.

### First Admin Login
1. Go to http://localhost:5000/login
2. Enter username: `admin`
3. Enter password: `gordonramsey`
4. Click Login
5. You'll be redirected to the admin panel

### Change Admin Password (Recommended)
After first login, change the admin password:
1. Log out
2. Create a new admin account with strong password
3. Promote the new account to admin
4. Delete or deactivate the default admin account

## User Registration

Users can create accounts by:
1. Going to http://localhost:5000/login
2. Clicking "Register here" link
3. Filling in username, email, and password
4. Submitting registration form

**Password Requirements**:
- Minimum 8 characters
- Mix of uppercase and lowercase
- Must match confirmation field

## Features Overview

### For Regular Users
- ✅ Create secure account
- ✅ Browse 32 apartment units
- ✅ Filter apartments by type, availability, price
- ✅ View unit details
- ✅ Submit contact form
- ✅ Secure logout

### For Administrators
- ✅ Admin dashboard with statistics
- ✅ User management (make admin, activate/deactivate)
- ✅ View all contact submissions
- ✅ Audit logging
- ✅ Rate limiting management

## Project Structure

```
sanctuary-apartments/
├── sanctuary_app.py          # Main Flask application
├── requirements.txt          # Python dependencies
├── .env                      # Environment configuration
├── README.md                 # Main documentation
├── SECURITY.md              # Security documentation
├── ADMIN_GUIDE.md           # Admin user guide
├── SETUP_GUIDE.md           # This file
├── templates/               # HTML templates
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard.html       # Main dashboard (authenticated)
│   ├── unit_detail.html     # Unit detail page
│   ├── admin_dashboard.html # Admin dashboard
│   ├── admin_users.html     # User management
│   ├── admin_contacts.html  # Contact submissions
│   └── error.html           # Error pages
├── static/                  # Static assets
│   └── style.css            # Stylesheet
└── sanctuary.db             # SQLite database (created on first run)
```

## URL Routes

### Public (No Authentication Required)
- `GET /login` - Login page
- `GET /register` - Registration page
- `POST /register` - Submit registration

### Authenticated User Routes
- `GET /` - Redirect to dashboard
- `GET /dashboard` - Main apartment listings
- `GET /unit/<id>` - Unit detail page
- `POST /logout` - Logout user
- `GET /api/units` - Get all units (JSON)
- `POST /api/units/filter` - Filter units (JSON)
- `POST /api/contact` - Submit contact form (JSON)

### Admin Routes (Authentication + Admin Role Required)
- `GET /admin` - Admin dashboard
- `GET /admin/users` - User management
- `GET /admin/contacts` - Contact submissions
- `POST /admin/user/<id>/toggle-admin` - Toggle admin status
- `POST /admin/user/<id>/toggle-active` - Toggle active status

## Security Features Implemented

✅ **Authentication**
- User registration with validation
- Bcrypt password hashing
- Session management with timeout

✅ **Authorization**
- Login required for apartment access
- Admin role verification
- Rate limiting on sensitive endpoints

✅ **Protection**
- CSRF tokens on all forms
- SQL Injection prevention
- XSS prevention
- Security headers
- Input validation and sanitization

✅ **Monitoring**
- Activity logging
- Failed login tracking
- Admin action logging

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```powershell
# Kill the process using port 5000
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

Or change the port in `sanctuary_app.py`:
```python
app.run(port=5001)  # Use different port
```

### Database Errors
If database is corrupted:
```powershell
# Delete the database file
Remove-Item sanctuary.db
# Restart the app - database will be recreated
python sanctuary_app.py
```

### Forgot Admin Password
```powershell
# Delete database
Remove-Item sanctuary.db
# Restart app - default admin account will be recreated
python sanctuary_app.py
```

### Dependencies Not Installing
```powershell
# Upgrade pip first
python -m pip install --upgrade pip
# Then install requirements
python -m pip install -r requirements.txt
```

## Production Deployment

### Before Deploying to Production

1. **Change Secret Key**:
   - Generate a new secure key
   - Update `.env` with new key

2. **Change Admin Password**:
   - Create new admin account
   - Delete default admin account

3. **Update Configuration**:
   ```
   FLASK_ENV=production
   DEBUG=False
   ```

4. **Enable HTTPS**:
   - Obtain SSL/TLS certificate
   - Configure with reverse proxy (nginx/Apache)

5. **Use Production Database**:
   - Replace SQLite with PostgreSQL
   - Configure connection string in `.env`

6. **Set Up Monitoring**:
   - Enable access logging
   - Configure error alerts
   - Monitor failed login attempts

### Deployment Options

**Option 1: Gunicorn (Recommended)**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 sanctuary_app:app
```

**Option 2: Docker**
Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "sanctuary_app:app"]
```

**Option 3: Cloud Platforms**
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service

## Testing

### Test Admin Account
```
Username: admin
Password: gordonramsey
Role: Admin
```

### Test Regular User Account
```
Username: testuser
Email: test@example.com
Password: TestPassword123!
Role: User
```

## Support & Documentation

- **Main README**: [README.md](README.md)
- **Security Guide**: [SECURITY.md](SECURITY.md)
- **Admin Guide**: [ADMIN_GUIDE.md](ADMIN_GUIDE.md)
- **This Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md)

## Performance Tips

1. **Enable Caching**:
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

2. **Database Optimization**:
   - Add indexes to frequently searched columns
   - Archive old contact submissions
   - Regular database maintenance

3. **Static File Optimization**:
   - Minify CSS
   - Compress images
   - Use CDN for assets

4. **Load Balancing**:
   - Use multiple Gunicorn workers
   - Deploy behind nginx reverse proxy
   - Enable connection pooling

## Next Steps

1. ✅ Run the application
2. ✅ Test login with admin account
3. ✅ Create test user account
4. ✅ Explore admin features
5. ✅ Review security documentation
6. ✅ Plan production deployment
7. ✅ Update default credentials
8. ✅ Set up monitoring and backups
9. ✅ Configure HTTPS
10. ✅ Go live!

---

**Version**: 2.0
**Last Updated**: 2024
**Status**: Production Ready
**Support**: admin@sanctuaryapartments.com
