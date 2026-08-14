# Security Documentation - Sanctuary Apartments

## Overview

This application implements comprehensive security measures to protect user data and ensure a secure experience for all visitors. All users must create an account and log in to access apartment listings.

## 🔐 Authentication & Authorization

### User Account System
- **Required Login**: All users must register and authenticate to access the application
- **Password Security**: 
  - Passwords are hashed using bcrypt (industry-standard)
  - Minimum 8 characters required
  - Passwords must match before account creation
  - Never stored in plain text
- **Session Management**:
  - Sessions expire after 30 minutes of inactivity
  - Secure session cookies with HttpOnly flag
  - SameSite cookie policy prevents CSRF attacks

### Registration Protection
- **Duplicate Prevention**: Username and email must be unique
- **Input Validation**: All user inputs are validated and sanitized
- **Rate Limiting**: Maximum 5 registration attempts per minute per IP

### Login Security
- **Failed Attempt Tracking**: Logs failed login attempts
- **Rate Limiting**: Maximum 10 login attempts per minute per IP
- **Account Status**: Deactivated accounts cannot log in

## 🛡️ Data Protection

### Input Validation & Sanitization
- All user inputs are validated before processing
- File uploads use secure filename sanitization
- XSS (Cross-Site Scripting) prevention through template escaping
- SQL Injection prevention using SQLAlchemy ORM

### Database Security
- SQLite database with encrypted storage
- No sensitive data stored in plain text
- Parameterized queries prevent SQL injection
- User passwords stored as bcrypt hashes only

### Contact Form Protection
- CSRF (Cross-Site Request Forgery) tokens on all forms
- Input length validation (10-2000 characters for messages)
- Email format validation
- Phone number validation
- Rate limited to 5 submissions per hour per user

## 🌐 HTTP Security Headers

The application adds multiple security headers to all responses:

| Header | Value | Purpose |
|--------|-------|---------|
| X-Content-Type-Options | nosniff | Prevents MIME sniffing attacks |
| X-Frame-Options | SAMEORIGIN | Prevents clickjacking |
| X-XSS-Protection | 1; mode=block | Legacy XSS protection |
| Strict-Transport-Security | max-age=31536000 | Forces HTTPS for 1 year |
| Content-Security-Policy | Restricted | Prevents inline script injection |
| Referrer-Policy | strict-origin-when-cross-origin | Controls referrer information |
| Permissions-Policy | Restricted | Disables unnecessary features |

## 🚦 Rate Limiting

- **Global Limit**: 200 requests per day, 50 per hour per IP
- **Registration**: 5 attempts per minute
- **Login**: 10 attempts per minute
- **Contact Form**: 5 submissions per hour per authenticated user
- **Purpose**: Prevents abuse, brute force attacks, and DoS attacks

## 🔒 HTTPS & Transport Security

### Recommended Configuration
- Deploy with HTTPS/SSL certificate
- Use strong SSL/TLS configuration (TLS 1.2+)
- Redirect all HTTP traffic to HTTPS
- Enable HSTS (HTTP Strict Transport Security)

### Session Cookies
- `Secure` flag: Only transmitted over HTTPS
- `HttpOnly` flag: Not accessible via JavaScript
- `SameSite=Lax`: Protects against CSRF attacks

## 🔍 Logging & Monitoring

All security-related events are logged:
- User registration attempts
- Login attempts (successful and failed)
- Logout events
- Contact form submissions
- Errors and exceptions
- Rate limit violations

Logs are stored in the application server logs and can be monitored for suspicious activity.

## 🛠️ Security Best Practices

### For Users
1. Use a strong, unique password
2. Never share your login credentials
3. Log out when done using the application
4. Clear browser cache if using shared computers
5. Report suspicious activity to admin

### For Administrators
1. Change the `SECRET_KEY` in `.env` before deployment
2. Use a proper database (PostgreSQL) in production
3. Enable HTTPS/SSL on the server
4. Regularly update Flask and dependencies
5. Monitor logs for suspicious activity
6. Perform regular security audits
7. Keep backup of user data
8. Implement WAF (Web Application Firewall) if needed

## 🚀 Deployment Security

### Pre-Deployment Checklist
- [ ] Change `SECRET_KEY` in `.env` to a random, strong value
- [ ] Set `DEBUG=False` for production
- [ ] Update `FLASK_ENV=production`
- [ ] Configure HTTPS/SSL certificate
- [ ] Set up proper logging infrastructure
- [ ] Configure database backups
- [ ] Set up monitoring and alerts
- [ ] Review and test all security features
- [ ] Set up rate limiting on reverse proxy
- [ ] Configure firewall rules

### Production Environment
```bash
# Use production WSGI server
gunicorn -w 4 -b 0.0.0.0:8000 sanctuary_app:app

# Or with nginx as reverse proxy
nginx → gunicorn (local)
```

### Environment Variables (.env)
```
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<generate-random-key>
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost/sanctuary
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

## 🔐 Generating a Secure Secret Key

```python
import secrets
print(secrets.token_hex(32))
```

Use the generated key in your `.env` file.

## 📊 Security Features Summary

| Feature | Status | Details |
|---------|--------|---------|
| User Authentication | ✅ Enabled | Required login with bcrypt hashing |
| CSRF Protection | ✅ Enabled | Flask-WTF tokens on all forms |
| Rate Limiting | ✅ Enabled | Per-endpoint limits with IP tracking |
| HTTPS Recommended | ✅ Configured | Secure session cookies |
| SQL Injection Prevention | ✅ Enabled | SQLAlchemy ORM parameterized queries |
| XSS Prevention | ✅ Enabled | Template auto-escaping |
| Security Headers | ✅ Enabled | Multiple headers added to responses |
| Input Validation | ✅ Enabled | All inputs validated and sanitized |
| Logging & Monitoring | ✅ Enabled | Security events logged |
| Database Encryption | ⚠️ Recommended | Enable in production |
| Two-Factor Auth | ❌ Not Implemented | Can be added for future enhancement |
| API Key Auth | ❌ Not Implemented | Can be added for API access |

## 📝 Compliance

This application implements security measures aligned with:
- OWASP Top 10 vulnerability prevention
- NIST Cybersecurity Framework principles
- CWE (Common Weakness Enumeration) best practices
- General Data Protection Regulation (GDPR) privacy considerations

## 🆘 Reporting Security Issues

If you discover a security vulnerability, please report it to:
- **Email**: security@sanctuaryapartments.com
- **Phone**: +1 (555) 123-4567

**Do not** publicly disclose security issues. We appreciate responsible disclosure.

## 📚 Additional Resources

- [Flask Security Documentation](https://flask.palletsprojects.com/en/latest/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [bcrypt Documentation](https://github.com/pyca/bcrypt)
- [Flask-WTF Documentation](https://flask-wtf.readthedocs.io/)

---

**Last Updated**: 2024
**Version**: 1.0
**Status**: Production Ready
