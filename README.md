# Sanctuary Apartments - Web Application

A secure, modern web application showcasing 32 luxury apartment units with user authentication, detailed information, filtering capabilities, and contact management.

## 🔐 Security Features

✅ **User Authentication** - All users must create an account and log in
✅ **Password Security** - Bcrypt hashing with minimum 8 characters
✅ **CSRF Protection** - CSRF tokens on all forms
✅ **Rate Limiting** - Per-endpoint rate limits to prevent abuse
✅ **Security Headers** - Comprehensive HTTP security headers
✅ **Input Validation** - All inputs validated and sanitized
✅ **HTTPS Ready** - Secure session cookies and HSTS support
✅ **SQL Injection Prevention** - SQLAlchemy ORM prevents injection attacks
✅ **Logging & Monitoring** - Security events logged for audit

See [SECURITY.md](SECURITY.md) for comprehensive security documentation.

## Features

- **User Accounts**: Secure registration and login system
- **32 Premium Units**: Browse all available apartment units with detailed information
- **Unit Filtering**: Filter units by type, availability status, and price range
- **Unit Details**: View comprehensive information about each unit
- **Secure Contact Form**: Get in touch with the leasing team (authenticated users only)
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Session Management**: Secure sessions with 30-minute timeout

## Project Structure

```
sanctuary-apartments/
├── sanctuary_app.py          # Main Flask application
├── requirements.txt          # Python dependencies
├── .env                      # Environment configuration (change SECRET_KEY!)
├── SECURITY.md              # Security documentation
├── README.md                # This file
├── templates/
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── dashboard.html       # Main apartment listings (authenticated)
│   ├── unit_detail.html     # Individual unit detail page
│   └── error.html           # Error page
└── static/
    └── style.css            # Stylesheet
```

## User Roles

- **Visitor**: Can only access login/registration pages
- **Authenticated User**: Can view apartments, filter listings, and submit contact forms
- **Administrator**: Can manage users, view contact submissions, and access admin panel

## 👨‍💼 Admin Access

**Admin Credentials** (Default):
- Username: `admin`
- Password: `gordonramsey`

⚠️ **IMPORTANT**: Change the admin password immediately in production!

**Admin Features**:
- User management (make users admin, activate/deactivate accounts)
- View contact submissions
- System statistics and monitoring
- Access to `/admin` panel

See [ADMIN_GUIDE.md](ADMIN_GUIDE.md) for complete admin documentation.

## Unit Types Available

- **Studio**: $1,200/month - Compact living spaces with modern finishes
- **1 Bedroom**: $1,500/month - Spacious units with separate bedroom and living area
- **2 Bedroom**: $2,000/month - Luxury apartments with premium finishes

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Navigate to the project directory:
```bash
cd "c:\Users\HomePC\Desktop\VISUAL STUDIO"
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Update the `.env` file with a secure secret key:
```bash
# Generate a secure key
python -c "import secrets; print(secrets.token_hex(32))"

# Update .env with the generated key
# Change: SECRET_KEY=your-generated-key-here
```

### Running the Application

1. Start the Flask development server:
```bash
python sanctuary_app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

The application will redirect you to the login page.

### Test Account (Development Only)

For development, register a new account:
- Username: `testuser`
- Email: `test@example.com`
- Password: `TestPassword123!`

## API Endpoints

All API endpoints require authentication (login).

### Authentication
- `GET/POST /login` - Login with username and password
- `GET/POST /register` - Create new account
- `GET /logout` - Logout current user

### Protected Routes
- `GET /dashboard` - Main page with apartment listings
- `GET /unit/<id>` - View specific unit details

### API Routes (JSON)
- `GET /api/units` - Get all units
- `POST /api/units/filter` - Filter units by criteria
- `POST /api/contact` - Submit contact form

#### Filter Request Format
```json
{
  "type": "Studio|1 Bedroom|2 Bedroom",
  "availability": "Available|Occupied",
  "price_min": number,
  "price_max": number
}
```

#### Contact Form Request
```json
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "message": "string"
}
```

## Unit Information Included

Each unit includes:
- Unit number
- Apartment type (Studio, 1BR, or 2BR)
- Number of bedrooms and bathrooms
- Monthly rent price
- List of amenities
- Availability status (Available/Occupied)
- Detailed description

## Contact Information

**Sanctuary Apartments**
- Address: 123 Sanctuary Lane, City, State 12345
- Phone: +1 (555) 123-4567
- Email: info@sanctuaryapartments.com
- Hours: Mon-Fri: 9AM-6PM, Sat-Sun: 10AM-4PM

## Security Highlights

### Authentication
- Bcrypt password hashing
- Minimum 8-character passwords required
- Session timeout after 30 minutes
- Account deactivation support

### Protection Against Common Attacks
- CSRF (Cross-Site Request Forgery) tokens
- XSS (Cross-Site Scripting) prevention
- SQL Injection prevention
- Rate limiting on login/registration
- Security headers on all responses

### Rate Limiting
- Global: 200 requests/day, 50/hour per IP
- Registration: 5 attempts/minute
- Login: 10 attempts/minute
- Contact Form: 5 submissions/hour per user

## Configuration

Key settings in `.env`:
```
FLASK_ENV=production          # Set to development for debugging
DEBUG=False                   # Set to False in production
SECRET_KEY=<change-me>        # Generate a secure random key
SESSION_COOKIE_SECURE=True    # Only send over HTTPS
SESSION_COOKIE_HTTPONLY=True  # Not accessible via JavaScript
```

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (development) / PostgreSQL (production recommended)
- **Authentication**: Flask-Login, bcrypt
- **Validation**: WTForms with validation
- **CSRF Protection**: Flask-WTF
- **Rate Limiting**: Flask-Limiter
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## Future Enhancements

- [ ] Two-factor authentication (2FA)
- [ ] Unit images and photo galleries
- [ ] Virtual tours
- [ ] Online application form
- [ ] Database integration for persistent data
- [ ] Email notifications for inquiries
- [ ] User favorites/wishlist
- [ ] API token authentication
- [ ] Advanced analytics
- [ ] Mobile app

## Production Deployment

### Important Pre-Deployment Steps

1. **Change Secret Key**:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Update in `.env`

2. **Set Production Environment**:
   ```
   FLASK_ENV=production
   DEBUG=False
   ```

3. **Use WSGI Server** (not Flask dev server):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 sanctuary_app:app
   ```

4. **Enable HTTPS**:
   - Obtain SSL/TLS certificate
   - Configure with reverse proxy (nginx/Apache)

5. **Set Up Database**:
   - Use PostgreSQL instead of SQLite
   - Configure backups

6. **Security Monitoring**:
   - Enable logging
   - Set up alerts
   - Monitor failed login attempts

See [SECURITY.md](SECURITY.md) for complete security guidelines.

## Troubleshooting

### Database Reset
```bash
# Delete the database file to reset
rm sanctuary.db

# Restart the application - database will be recreated
```

### Clear Sessions
- Sessions are stored in-memory and cleared on server restart

### Forgot Password
- Currently not implemented
- Users must create a new account or contact admin

## Support & Issues

For issues or questions:
- Email: support@sanctuaryapartments.com
- Phone: +1 (555) 123-4567
- Security issues: security@sanctuaryapartments.com

## License

© 2024 Sanctuary Apartments. All rights reserved.

## Version

- **Version**: 2.0 (Secure Edition)
- **Status**: Production Ready
- **Last Updated**: 2024

