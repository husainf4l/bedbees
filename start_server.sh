#!/bin/bash
# Bedbees Django Development Server Startup Script

echo "🚀 Starting Bedbees Django Server..."

# Activate virtual environment
source venv/bin/activate

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Set Django settings module if not already set
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-bedbees.settings}

echo "📋 Django Settings Module: $DJANGO_SETTINGS_MODULE"
echo "🌐 Server will be available at: http://localhost:8000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "═══════════════════════════════════════════════════════════════"

# Start the server
python manage.py runserver
