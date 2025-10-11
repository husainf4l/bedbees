#!/usr/bin/env python
"""
Debug script to test the publishing system
Run with: python test_publishing.py
"""

import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bedbees.settings")
django.setup()

from core.models import Accommodation, Tour, RentalCar
from django.contrib.auth.models import User

print("=" * 60)
print("🔍 PUBLISHING SYSTEM DEBUG REPORT")
print("=" * 60)

# Check if there are any listings
print("\n📊 LISTING INVENTORY:")
print(f"  Accommodations: {Accommodation.objects.count()}")
print(f"  Tours: {Tour.objects.count()}")
print(f"  Rental Cars: {RentalCar.objects.count()}")

# Check accommodations status
accommodations = Accommodation.objects.all()[:5]
if accommodations:
    print("\n🏠 SAMPLE ACCOMMODATIONS:")
    for acc in accommodations:
        print(f"\n  ID: {acc.id}")
        print(f"  Name: {acc.property_name}")
        print(f"  Status: {acc.status}")
        print(f"  Published: {acc.is_published}")
        print(f"  Active: {acc.is_active}")
        print(f"  Location: {acc.city}, {acc.country}")
        print(f"  Host: {acc.host}")
else:
    print("\n⚠️  No accommodations found!")

# Check tours status
tours = Tour.objects.all()[:5]
if tours:
    print("\n🗺️  SAMPLE TOURS:")
    for tour in tours:
        print(f"\n  ID: {tour.id}")
        print(f"  Name: {tour.tour_name}")
        print(f"  Status: {tour.status}")
        print(f"  Published: {tour.is_published}")
        print(f"  Active: {tour.is_active}")
        print(f"  Location: {tour.city}, {tour.country}")
        print(f"  Host: {tour.host}")
else:
    print("\n⚠️  No tours found!")

# Check users
users = User.objects.all()
print(f"\n👥 USERS: {users.count()} total")
for user in users:
    print(f"  - {user.username} (ID: {user.id})")

# Test publishing function
print("\n" + "=" * 60)
print("🧪 TEST PUBLISHING FUNCTION")
print("=" * 60)

if accommodations:
    test_acc = accommodations.first()
    print(f"\n✅ Testing with: {test_acc.property_name} (ID: {test_acc.id})")
    print(f"   Before: status={test_acc.status}, published={test_acc.is_published}")

    # Try the publish method
    try:
        test_acc.publish()
        test_acc.refresh_from_db()
        print(f"   After:  status={test_acc.status}, published={test_acc.is_published}")
        print("   ✅ Publish method works!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
else:
    print("\n⚠️  Cannot test - no accommodations available")

print("\n" + "=" * 60)
print("📋 NEXT STEPS:")
print("=" * 60)
print(
    """
1. Make sure you have at least one accommodation or tour created
2. Note the ID of the listing you want to publish
3. Use this URL pattern:
   - Accommodation: http://127.0.0.1:8000/accommodation/{id}/publish/
   - Tour: http://127.0.0.1:8000/tour/{id}/publish/
4. Make sure you're logged in as the host who owns the listing
5. The publish action requires a POST request (use a form or button)
"""
)

print("=" * 60)
