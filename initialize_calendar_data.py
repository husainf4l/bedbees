#!/usr/bin/env python
"""
Initialize calendar availability data for testing
Creates availability records for the next 90 days
"""
import django
import os
import sys
from datetime import datetime, timedelta

# Setup Django
sys.path.insert(0, '/home/aqlaan/Desktop/bedbees')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedbees.settings')
django.setup()

from core.models import Accommodation, AccommodationAvailability

def initialize_calendar_data():
    print("=" * 60)
    print("INITIALIZING CALENDAR DATA")
    print("=" * 60)
    
    try:
        acc = Accommodation.objects.get(id=53)
        print(f"\n✅ Found accommodation: {acc.property_name}")
        print(f"   Rooms: {acc.num_rooms}")
        print(f"   Base Price: ${acc.base_price}/night")
        
        # Create availability for next 90 days
        today = datetime.now().date()
        created = 0
        updated = 0
        
        print(f"\n📅 Creating availability records for next 90 days...")
        
        for days_ahead in range(90):
            date = today + timedelta(days=days_ahead)
            
            # Create or update availability
            avail, is_new = AccommodationAvailability.objects.update_or_create(
                accommodation=acc,
                date=date,
                defaults={
                    'is_available': True,
                    'is_blocked': False,
                    'price_per_night': acc.base_price,
                    'minimum_stay': 1,
                    'maximum_stay': 30,
                }
            )
            
            if is_new:
                created += 1
            else:
                updated += 1
            
            # Show progress every 10 days
            if (days_ahead + 1) % 10 == 0:
                print(f"   Progress: {days_ahead + 1}/90 days...")
        
        print(f"\n✅ Complete!")
        print(f"   Created: {created} new records")
        print(f"   Updated: {updated} existing records")
        print(f"   Total: {created + updated} availability records")
        
        # Show sample data
        print(f"\n📊 Sample Availability Data:")
        sample_dates = AccommodationAvailability.objects.filter(
            accommodation=acc,
            date__gte=today
        ).order_by('date')[:5]
        
        for avail in sample_dates:
            status = "✅ Available" if avail.is_available else "❌ Unavailable"
            print(f"   {avail.date}: {status} - ${avail.price_per_night}/night - Min stay: {avail.minimum_stay} nights")
        
        print("\n" + "=" * 60)
        print("SUCCESS! Calendar data initialized.")
        print("You can now use the Calendar & Pricing tab.")
        print("=" * 60)
        
    except Accommodation.DoesNotExist:
        print("❌ Accommodation ID 53 not found!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    initialize_calendar_data()
