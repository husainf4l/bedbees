#!/usr/bin/env python
"""
Test amenities parsing
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bedbees.settings")
django.setup()

from core.models import Accommodation

print("=" * 60)
print("🔍 TESTING AMENITIES PARSING")
print("=" * 60)

# Get an accommodation with amenities
accommodations = Accommodation.objects.exclude(amenities__isnull=True).exclude(
    amenities=""
)[:3]

for acc in accommodations:
    print(f"\n📋 {acc.property_name}")
    print(f"  Raw amenities field: {acc.amenities[:100]}...")
    print(f"  Parsed list:")
    for amenity in acc.get_amenities_list():
        print(f"    ✓ {amenity}")

print("\n" + "=" * 60)
print("✅ If you see individual amenities above, it's working!")
print("=" * 60)
