#!/bin/bash
# AWS Deployment Script for BedBees Django Application
# This script prepares the application for AWS deployment

set -e  # Exit on any error

echo "========================================="
echo "BedBees AWS Deployment Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found!"
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Install/Update dependencies
print_info "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencies installed"

# Collect static files
print_info "Collecting static files..."
python manage.py collectstatic --noinput
print_success "Static files collected"

# Run migrations
print_info "Running database migrations..."
python manage.py migrate --noinput
print_success "Migrations completed"

# Seed database
print_info "Seeding database with countries and attractions..."
python manage.py seed_database --countries-only --create-admin
print_success "Database seeded successfully"

# Create superuser prompt
echo ""
print_info "Default admin user created:"
echo "  Username: admin"
echo "  Password: admin123"
echo "  Email: admin@bedbees.com"
echo ""
print_warning "⚠️  IMPORTANT: Change the admin password after first login!"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    print_warning ".env file not found!"
    print_info "Creating .env template..."
    cat > .env << 'EOF'
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database Settings (if using PostgreSQL on AWS RDS)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=bedbees_db
# DB_USER=bedbees_user
# DB_PASSWORD=your_password_here
# DB_HOST=your-rds-endpoint.region.rds.amazonaws.com
# DB_PORT=5432

# AWS S3 Settings (for media files)
# AWS_ACCESS_KEY_ID=your_access_key
# AWS_SECRET_ACCESS_KEY=your_secret_key
# AWS_STORAGE_BUCKET_NAME=bedbees-media
# AWS_S3_REGION_NAME=us-east-1

# Email Settings
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password

# Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True
EOF
    print_success ".env template created"
    print_warning "Please edit .env and add your production settings!"
else
    print_success ".env file found"
fi

# Test the application
print_info "Running Django checks..."
python manage.py check
print_success "Django checks passed"

# Display next steps
echo ""
echo "========================================="
print_success "Deployment preparation complete!"
echo "========================================="
echo ""
print_info "Next steps for AWS deployment:"
echo ""
echo "1. EC2 Deployment:"
echo "   - Launch an EC2 instance (Ubuntu 22.04 recommended)"
echo "   - Install nginx: sudo apt install nginx"
echo "   - Install gunicorn: pip install gunicorn"
echo "   - Configure nginx as reverse proxy"
echo "   - Set up systemd service for gunicorn"
echo ""
echo "2. Database (Optional - AWS RDS):"
echo "   - Create PostgreSQL RDS instance"
echo "   - Update .env with RDS credentials"
echo "   - Run migrations: python manage.py migrate"
echo ""
echo "3. Static/Media Files (Optional - AWS S3):"
echo "   - Create S3 bucket for media files"
echo "   - Install boto3 and django-storages"
echo "   - Update .env with S3 credentials"
echo ""
echo "4. Security:"
echo "   - Update SECRET_KEY in .env"
echo "   - Set DEBUG=False"
echo "   - Configure ALLOWED_HOSTS"
echo "   - Change admin password"
echo "   - Set up SSL certificate (Let's Encrypt)"
echo ""
echo "5. Start the server:"
echo "   - Development: python manage.py runserver"
echo "   - Production: gunicorn bedbees.wsgi:application --bind 0.0.0.0:8000"
echo ""
print_success "Happy deploying! 🚀"
echo ""
