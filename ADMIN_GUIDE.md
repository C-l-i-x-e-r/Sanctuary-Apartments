# Admin Guide - Sanctuary Apartments

## Admin Access

### Default Admin Credentials
- **Username**: `admin`
- **Password**: `gordonramsey`

⚠️ **IMPORTANT**: Change this password immediately after first login in production!

## Admin Features

### 1. Admin Dashboard (`/admin`)
The main admin panel showing:
- **Statistics Overview**:
  - Total Users
  - Active Users
  - Inactive Users
  - Admin Users
  - Total Contact Submissions

- **Recent Contact Submissions**:
  - View latest 10 contact submissions
  - See submitter name, email, phone, date, and message preview
  - Quick link to view all submissions

### 2. User Management (`/admin/users`)
Complete user management system:

**View User List**:
- Username
- Email address
- Role (Admin/User)
- Account status (Active/Inactive)
- Join date
- Action buttons

**User Actions**:
- **Toggle Admin Status**: Make regular users administrators or remove admin privileges
- **Toggle Active Status**: Activate or deactivate user accounts
- **Pagination**: Browse through users (20 per page)

**Restrictions**:
- Cannot modify your own account
- Cannot deactivate your own account
- Deactivated users cannot log in

### 3. Contact Submissions (`/admin/contacts`)
View all contact form submissions:

**Contact Information Display**:
- Submitter name
- Email (clickable mailto link)
- Phone number (clickable tel link)
- Full message content
- Submitter username
- Submission date and time
- Pagination support

**Features**:
- Cards layout for easy reading
- Color-coded borders
- Hover effects for better UX
- Sortable by date (newest first)
- Page navigation (20 per page)

## Admin Privileges

Only admin users can access:
1. `/admin` - Admin Dashboard
2. `/admin/users` - User Management
3. `/admin/contacts` - Contact Submissions
4. Toggle admin status on users
5. Toggle active status on users

Regular users cannot access these routes and will be redirected to the main dashboard.

## Security Features

### Admin Protection
- ✅ Admin routes require login
- ✅ Admin routes require admin role
- ✅ All admin actions are logged
- ✅ Cannot modify your own account (prevents accidental lockout)
- ✅ Unauthorized access attempts are logged

### Audit Trail
All admin activities are logged, including:
- Admin status changes
- User activation/deactivation
- Login/logout events
- Failed access attempts

## Common Admin Tasks

### Making a User an Admin
1. Go to `/admin/users`
2. Find the user in the list
3. Click "Make Admin" button
4. Confirm the action
5. User will now have admin access

### Deactivating a User
1. Go to `/admin/users`
2. Find the user in the list
3. Click "Deactivate" button
4. Confirm the action
5. User cannot log in anymore (but account data is preserved)

### Reactivating a User
1. Go to `/admin/users`
2. Find the deactivated user (marked as inactive)
3. Click "Activate" button
4. Confirm the action
5. User can log in again

### Viewing Contact Submissions
1. Go to `/admin/contacts`
2. Browse through submissions
3. Click on email to send reply
4. Click on phone to call (if available)
5. Use pagination to view older submissions

## Database Structure

### User Model
```
User:
  - id: Integer (Primary Key)
  - username: String (Unique)
  - email: String (Unique)
  - password_hash: String
  - created_at: DateTime
  - is_active: Boolean (default: True)
  - is_admin: Boolean (default: False)
```

### ContactSubmission Model
```
ContactSubmission:
  - id: Integer (Primary Key)
  - user_id: Integer (Foreign Key to User)
  - name: String
  - email: String
  - phone: String (Optional)
  - message: Text
  - created_at: DateTime
```

## Troubleshooting

### Forgot Admin Password
1. Delete the database file (`sanctuary.db`)
2. Restart the application
3. Default admin account will be recreated with password `gordonramsey`
4. Update `.gitignore` to include `*.db` files

### Cannot Log In as Admin
- Verify username is `admin` (case-sensitive)
- Verify password is `gordonramsey`
- Check that your account is active (not deactivated)
- Clear browser cookies and try again

### Admin Panel Not Showing
- Verify you are logged in
- Verify your account has admin privileges
- Check browser console for errors
- Try logging out and logging back in

### Missing Contact Submissions
- Verify users are logged in (only authenticated users can submit)
- Check the `/api/contact` endpoint is working
- Verify database file exists and is readable

## Best Practices

1. **Change Default Password**: Always change the default admin password in production
2. **Create Multiple Admins**: Have backup admin accounts in case of lockout
3. **Regular Backups**: Backup the database regularly
4. **Monitor Logs**: Check logs for suspicious activity
5. **Update Regularly**: Keep Flask and dependencies updated
6. **Secure Database**: Store `sanctuary.db` securely with proper file permissions
7. **Use HTTPS**: Always use HTTPS in production
8. **Strong Passwords**: Enforce strong passwords for all users
9. **Review Users**: Regularly review user list for suspicious accounts
10. **Test Security**: Periodically test security features

## Production Deployment

### Pre-Deployment
- [ ] Change admin password
- [ ] Verify is_admin field exists in database
- [ ] Test admin routes thoroughly
- [ ] Backup database
- [ ] Enable HTTPS/SSL
- [ ] Set DEBUG=False

### After Deployment
- [ ] Test admin login
- [ ] Test user management
- [ ] Test contact submission viewing
- [ ] Monitor access logs
- [ ] Document admin procedures

## API Admin Endpoints

### User Management
- `POST /admin/user/<user_id>/toggle-admin` - Toggle admin status
- `POST /admin/user/<user_id>/toggle-active` - Toggle active status

Both require:
- User to be authenticated
- User to be admin
- JSON response with success/message

## Support

For admin support or issues:
- Email: admin@sanctuaryapartments.com
- Phone: +1 (555) 123-4567
- Security Issues: security@sanctuaryapartments.com

---

**Version**: 2.0
**Last Updated**: 2024
**Status**: Production Ready
