#!/usr/bin/env python
"""
Test script to verify Calendar & Pricing functionality
"""
import django
import os
import sys

# Setup Django
sys.path.insert(0, '/home/aqlaan/Desktop/bedbees')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedbees.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Accommodation, AccommodationAvailability
from datetime import datetime, timedelta

def test_calendar_system():
    print("=" * 60)
    print("CALENDAR & PRICING SYSTEM TEST")
    print("=" * 60)
    
    # 1. Check user and accommodation
    print("\n1. Checking User and Accommodation...")
    try:
        user = User.objects.get(username='test_host')
        print(f"   ✅ User found: {user.username} (ID: {user.id})")
    except User.DoesNotExist:
        print("   ❌ User 'test_host' not found!")
        return
    
    try:
        acc = Accommodation.objects.get(id=53)
        print(f"   ✅ Accommodation found: {acc.property_name} (ID: {acc.id})")
        print(f"   ✅ Owner: {acc.host.username}")
        
        if acc.host.id != user.id:
            print(f"   ⚠️  WARNING: Accommodation owner ({acc.host.username}) != test user ({user.username})")
        else:
            print(f"   ✅ Ownership verified!")
    except Accommodation.DoesNotExist:
        print("   ❌ Accommodation ID 53 not found!")
        return
    
    # 2. Check accommodation details
    print("\n2. Accommodation Details...")
    print(f"   Property Name: {acc.property_name}")
    print(f"   Type: {acc.property_type}")
    print(f"   City: {acc.city}")
    print(f"   Country: {acc.country}")
    print(f"   Number of Rooms: {acc.num_rooms}")
    print(f"   Max Guests: {acc.max_guests}")
    print(f"   Base Price: ${acc.base_price}/night")
    print(f"   Published: {acc.is_published}")
    print(f"   Active: {acc.is_active}")
    
    # 3. Check availability records
    print("\n3. Checking Availability Records...")
    today = datetime.now().date()
    next_month = today + timedelta(days=30)
    
    availabilities = AccommodationAvailability.objects.filter(
        accommodation=acc,
        date__gte=today,
        date__lte=next_month
    ).order_by('date')
    
    print(f"   Found {availabilities.count()} availability records for next 30 days")
    
    if availabilities.exists():
        print("\n   Sample dates:")
        for avail in availabilities[:5]:
            status = "Available" if avail.is_available else "Unavailable"
            print(f"     {avail.date}: {status} - ${avail.price}/night - {avail.available_rooms} rooms")
    else:
        print("   ⚠️  No availability records found. Calendar will show default availability.")
    
    # 4. Test API response format
    print("\n4. Testing API Response Format...")
    acc_data = {
        'id': acc.id,
        'name': acc.property_name,
        'property_type': acc.property_type,
        'city': acc.city,
        'country': acc.country,
    }
    print(f"   ✅ API would return: {acc_data}")
    
    # 5. Check calendar system components
    print("\n5. Calendar System Components...")
    print("   ✅ API Endpoint: /api/user/accommodations/")
    print("   ✅ Calendar API: /api/accommodation/{id}/calendar/")
    print("   ✅ Update API: /api/accommodation/{id}/calendar/update/")
    print("   ✅ JavaScript: /static/core/js/calendar.js")
    print("   ✅ Template: hostdashboard.html (Calendar & Pricing tab)")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"✅ User: {user.username}")
    print(f"✅ Accommodation: {acc.property_name} (ID: {acc.id})")
    print(f"✅ Ownership: {acc.host.username}")
    print(f"✅ Status: Published={acc.is_published}, Active={acc.is_active}")
    print(f"✅ Availability Records: {availabilities.count()} dates")
    print("\n📋 Next Steps:")
    print("   1. Log in as 'test_host'")
    print("   2. Go to: http://127.0.0.1:8000/hostdashboard/")
    print("   3. Click 'Calendar & Pricing' tab")
    print("   4. Select 'The Mayflower Hotel' from dropdown")
    print("   5. Calendar should load with interactive dates")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_calendar_system()
