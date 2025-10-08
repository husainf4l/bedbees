# BedBees Database Seeding Documentation

## Overview

The BedBees application includes a powerful database seeding system that populates your database with countries, attractions, and comprehensive travel data directly from the `views.py` file.

## Features

✅ **Automated Data Extraction**: Reads `countries_data` and `demo_attractions` directly from `views.py`  
✅ **Comprehensive Seeding**: Seeds 16+ countries with 260+ detailed attractions  
✅ **AWS Ready**: Includes AWS deployment preparation  
✅ **Admin User Creation**: Automatically creates admin user for production  
✅ **Idempotent**: Can be run multiple times safely  
✅ **Transaction Safe**: All operations wrapped in database transactions

## Quick Start

### Seed Database

```bash
# Seed countries and attractions only
python manage.py seed_database --countries-only

# Clear existing data and seed fresh
python manage.py seed_database --countries-only --clear

# Create admin user and seed database
python manage.py seed_database --countries-only --create-admin

# All options combined
python manage.py seed_database --countries-only --clear --create-admin
```

### AWS Deployment

```bash
# Make deployment script executable
chmod +x deploy_aws.sh

# Run deployment script
./deploy_aws.sh
```

## Command Options

### `seed_database` Management Command

| Option             | Description                                                     |
| ------------------ | --------------------------------------------------------------- |
| `--clear`          | Clear existing data before seeding                              |
| `--countries-only` | Seed only countries and attractions (recommended)               |
| `--create-admin`   | Create default admin user (username: admin, password: admin123) |

## What Gets Seeded

### Countries (16 Total)

- Jordan
- Tunisia
- Algeria
- Turkey
- Egypt
- Morocco
- United Arab Emirates
- Lebanon
- Qatar
- Saudi Arabia
- Kuwait
- Bahrain
- Oman
- Syria
- Iraq
- Yemen

### Attractions (262 Total)

Each country includes 12-24 detailed attractions with:

- **Basic Information**: Name, location, description
- **Rich Content**: Historical significance, cultural impact, architecture details
- **Visitor Information**: Best time to visit, how to get there, entrance fees, opening hours
- **Practical Details**: What to wear, health & safety, guided tours information
- **Engaging Content**: 5-8 facts, 5-8 visitor tips, nearby attractions
- **Media**: Photo galleries (8-10 images per attraction)
- **Metadata**: GPS coordinates, annual visitor numbers, UNESCO status

### Example Attraction Data Structure

```python
{
    'id': 'petra',
    'slug': 'petra',
    'name': 'Petra',
    'location': 'Ma\'an Governorate, Jordan',
    'description': 'Ancient rock-cut city and UNESCO World Heritage Site',
    'long_description': '...',
    'historical_significance': '...',
    'cultural_impact': '...',
    'discovery': '...',
    'architecture': '...',
    'water_system': '...',
    'best_time_to_visit': '...',
    'how_to_get_there': '...',
    'entrance_fees': '...',
    'opening_hours': '...',
    'what_to_wear': '...',
    'health_safety': '...',
    'guided_tours': '...',
    'conservation': '...',
    'facts': [...],
    'visitor_tips': [...],
    'key_sites': [...],
    'nearby_attractions': [...],
    'photos': [...],
    'coordinates': {'lat': 30.3285, 'lng': 35.4444},
    'annual_visitors': 1000000,
    'unesco_site': True,
    'climate': '...'
}
```

## Database Schema

### Country Model

```python
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.URLField()
    accommodations_count = models.IntegerField(default=0)
    tours_count = models.IntegerField(default=0)
    attractions = models.JSONField()  # Stores attraction array
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## AWS Deployment Guide

### 1. Prepare Environment

```bash
# Run deployment script
./deploy_aws.sh
```

This script will:

- Create/activate virtual environment
- Install dependencies
- Run migrations
- Collect static files
- Seed database
- Create admin user
- Generate .env template

### 2. EC2 Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3-pip python3-venv nginx -y

# Clone your repository
git clone <your-repo-url> /var/www/bedbees
cd /var/www/bedbees

# Run deployment script
chmod +x deploy_aws.sh
./deploy_aws.sh

# Install gunicorn
pip install gunicorn

# Test gunicorn
gunicorn bedbees.wsgi:application --bind 0.0.0.0:8000
```

### 3. Nginx Configuration

Create `/etc/nginx/sites-available/bedbees`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /var/www/bedbees;
    }

    location /media/ {
        root /var/www/bedbees;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/bedbees /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. Systemd Service

Create `/etc/systemd/system/bedbees.service`:

```ini
[Unit]
Description=BedBees Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/bedbees
Environment="PATH=/var/www/bedbees/venv/bin"
ExecStart=/var/www/bedbees/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          bedbees.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl start bedbees
sudo systemctl enable bedbees
sudo systemctl status bedbees
```

### 5. Environment Variables (.env)

```env
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# PostgreSQL (optional)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=bedbees_db
DB_USER=bedbees_user
DB_PASSWORD=strong_password_here
DB_HOST=your-rds-endpoint.amazonaws.com
DB_PORT=5432

# AWS S3 (optional)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_STORAGE_BUCKET_NAME=bedbees-media
AWS_S3_REGION_NAME=us-east-1

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

## Troubleshooting

### Issue: "UNIQUE constraint failed: core_country.name"

**Solution**: Run with `--clear` flag to remove duplicates:

```bash
python manage.py seed_database --countries-only --clear
```

### Issue: "cannot import name 'countries_data'"

**Solution**: The command reads directly from `views.py`. Ensure the file exists and contains the dictionaries.

### Issue: Missing attractions data

**Solution**: Check that both `countries_data` and `demo_attractions` are properly defined in `views.py`.

## Testing

### Test URLs

After seeding, test these URLs:

```bash
# Country pages
http://localhost:8000/countries/jordan/
http://localhost:8000/countries/tunisia/
http://localhost:8000/countries/algeria/

# Attraction pages
http://localhost:8000/countries/jordan/attraction/petra/
http://localhost:8000/countries/tunisia/attraction/carthage-archaeological-site/
http://localhost:8000/countries/algeria/attraction/algiers-casbah/
```

### Verification Script

```python
# Test all seeded countries
python -c "
from core.models import Country
countries = Country.objects.all()
print(f'Total countries: {countries.count()}')
for country in countries:
    print(f'  {country.name}: {len(country.attractions or [])} attractions')
"
```

## Production Checklist

- [ ] Update `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static: `python manage.py collectstatic`
- [ ] Seed database: `python manage.py seed_database --countries-only --create-admin`
- [ ] Change admin password
- [ ] Set up SSL certificate
- [ ] Configure backups
- [ ] Set up monitoring
- [ ] Test all critical URLs

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review Django logs: `tail -f /var/log/nginx/error.log`
3. Check application logs: `journalctl -u bedbees -f`

## License

This seeding system is part of the BedBees project.

---

**Last Updated**: October 8, 2025  
**Version**: 1.0.0
