#!/usr/bin/env python
"""
Fix the new listing's status
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bedbees.settings")
django.setup()

from core.models import Accommodation

print("🔧 Fixing new listing status...")

# Get the new listing
listing = Accommodation.objects.get(id=53)
print(f"\nFound: {listing.property_name}")
print(f"  Current: is_published={listing.is_published}, status={listing.status}")

# Fix the status mismatch
if listing.is_published and listing.status == "draft":
    listing.status = "published"
    listing.save()
    print(f"  ✅ Fixed: status changed to 'published'")
else:
    print(f"  ✅ Already correct!")

print("\n💡 Now log in as 'shadishadi' to see this listing at /manage-listings/")
