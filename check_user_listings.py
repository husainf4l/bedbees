#!/usr/bin/env python
"""
Debug script to check user's listings
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bedbees.settings")
django.setup()

from core.models import Accommodation, Tour
from django.contrib.auth.models import User

print("=" * 60)
print("🔍 USER LISTINGS DEBUG")
print("=" * 60)

# Show all users
users = User.objects.all()
print(f"\n👥 ALL USERS ({users.count()}):")
for user in users:
    acc_count = Accommodation.objects.filter(host=user).count()
    tour_count = Tour.objects.filter(host=user).count()
    if acc_count > 0 or tour_count > 0:
        print(f"  - {user.username} (ID: {user.id})")
        print(f"    Accommodations: {acc_count}")
        print(f"    Tours: {tour_count}")

# Show recent accommodations
print("\n🏠 RECENT ACCOMMODATIONS (Last 5):")
recent_accs = Accommodation.objects.all().order_by("-created_at")[:5]
for acc in recent_accs:
    print(f"\n  ID: {acc.id}")
    print(f"  Name: {acc.property_name}")
    print(f"  Host: {acc.host}")
    print(f"  Status: {acc.status}")
    print(f"  Published: {acc.is_published}")
    print(f"  Created: {acc.created_at}")

# Show recent tours
print("\n🗺️  RECENT TOURS (Last 5):")
recent_tours = Tour.objects.all().order_by("-created_at")[:5]
for tour in recent_tours:
    print(f"\n  ID: {tour.id}")
    print(f"  Name: {tour.tour_name}")
    print(f"  Host: {tour.host}")
    print(f"  Status: {tour.status}")
    print(f"  Published: {tour.is_published}")
    print(f"  Created: {tour.created_at}")

print("\n" + "=" * 60)
print("💡 TIP: Your 'new' listing is the most recent one above!")
print("=" * 60)
