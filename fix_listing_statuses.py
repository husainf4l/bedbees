#!/usr/bin/env python
"""
Fix existing listings to have correct status
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bedbees.settings")
django.setup()

from core.models import Accommodation, Tour, RentalCar

print("🔧 FIXING LISTING STATUSES")
print("=" * 60)

# Fix accommodations
accommodations = Accommodation.objects.filter(is_published=True, status="draft")
count = accommodations.count()
if count > 0:
    accommodations.update(status="published")
    print(f"✅ Fixed {count} accommodations: draft → published")
else:
    print("✅ All accommodations already have correct status")

# Fix tours
tours = Tour.objects.filter(is_published=True, status="draft")
count = tours.count()
if count > 0:
    tours.update(status="published")
    print(f"✅ Fixed {count} tours: draft → published")
else:
    print("✅ All tours already have correct status")

# Fix rental cars
rental_cars = RentalCar.objects.filter(is_published=True, status="draft")
count = rental_cars.count()
if count > 0:
    rental_cars.update(status="published")
    print(f"✅ Fixed {count} rental cars: draft → published")
else:
    print("✅ All rental cars already have correct status")

# Also fix unpublished ones
unpublished_accs = Accommodation.objects.filter(is_published=False).exclude(
    status="draft"
)
if unpublished_accs.exists():
    unpublished_accs.update(status="draft")
    print(f"✅ Fixed {unpublished_accs.count()} unpublished accommodations → draft")

unpublished_tours = Tour.objects.filter(is_published=False).exclude(status="draft")
if unpublished_tours.exists():
    unpublished_tours.update(status="draft")
    print(f"✅ Fixed {unpublished_tours.count()} unpublished tours → draft")

print("\n" + "=" * 60)
print("✅ ALL LISTINGS FIXED!")
print("=" * 60)

# Show summary
print("\n📊 CURRENT STATUS:")
print(
    f"Accommodations - Published: {Accommodation.objects.filter(status='published').count()}"
)
print(f"Accommodations - Draft: {Accommodation.objects.filter(status='draft').count()}")
print(f"Tours - Published: {Tour.objects.filter(status='published').count()}")
print(f"Tours - Draft: {Tour.objects.filter(status='draft').count()}")
