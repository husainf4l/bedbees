# BedBees - Quick Reference Guide

## Database Seeding Commands

### Basic Seeding

```bash
# Seed all countries and attractions
python manage.py seed_database --countries-only
```

### Fresh Start

```bash
# Clear database and seed fresh data
python manage.py seed_database --countries-only --clear
```

### Production Setup

```bash
# Create admin user and seed data
python manage.py seed_database --countries-only --clear --create-admin
```

## AWS Deployment

### One-Command Deploy

```bash
./deploy_aws.sh
```

### Manual Steps

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Seed database
python manage.py seed_database --countries-only --create-admin

# 6. Test
python manage.py runserver
```

## Default Admin Credentials

```
Username: admin
Password: admin123
Email: admin@bedbees.com
```

**⚠️ Change password after first login!**

## Seeded Data Summary

- **16 Countries**: Jordan, Tunisia, Algeria, Turkey, Egypt, Morocco, UAE, Lebanon, Qatar, Saudi Arabia, Kuwait, Bahrain, Oman, Syria, Iraq, Yemen
- **262 Attractions**: Comprehensive details with photos, facts, visitor tips
- **Admin User**: Pre-configured for immediate access

## Test URLs

```
http://localhost:8000/admin/
http://localhost:8000/countries/jordan/
http://localhost:8000/countries/tunisia/attraction/carthage-archaeological-site/
http://localhost:8000/countries/algeria/attraction/algiers-casbah/
```

## Production Configuration

### Environment Variables (.env)

```env
DEBUG=False
SECRET_KEY=generate-new-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Gunicorn Start

```bash
gunicorn bedbees.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Nginx Reverse Proxy

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
}
```

## Common Issues

### Database Locked

```bash
# Stop Django server and try again
pkill -f runserver
python manage.py seed_database --countries-only
```

### Duplicate Countries

```bash
# Use --clear flag
python manage.py seed_database --countries-only --clear
```

### Permission Denied on deploy_aws.sh

```bash
chmod +x deploy_aws.sh
./deploy_aws.sh
```

## File Structure

```
bedbees/
├── core/
│   ├── management/
│   │   └── commands/
│   │       └── seed_database.py   # Seeding command
│   ├── models.py                   # Country model
│   └── views.py                    # Data source
├── deploy_aws.sh                   # AWS deployment script
├── DATABASE_SEEDING.md             # Full documentation
├── requirements.txt                # Python dependencies
└── manage.py                       # Django management
```

## Quick Links

- Full Documentation: `DATABASE_SEEDING.md`
- Admin Panel: http://localhost:8000/admin/
- Countries: http://localhost:8000/countries/
- Django Docs: https://docs.djangoproject.com/

---

**Need Help?** Check `DATABASE_SEEDING.md` for detailed documentation
