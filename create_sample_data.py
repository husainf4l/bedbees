#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedbees.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Accommodation, Tour
from decimal import Decimal

# Get first host user
user = User.objects.filter(profile__is_host=True).first()
if not user:
    print("❌ No host users found!")
    exit(1)

print(f"✅ Creating sample data for host: {user.username}")

# Create sample accommodations
accommodations_data = [
    {
        'property_name': 'Cozy Mountain Cabin',
        'host_name': user.username,
        'full_description': 'Beautiful cabin in the mountains with stunning views',
        'tagline': 'Mountain getaway with breathtaking views',
        'country': 'Switzerland',
        'city': 'Zermatt',
        'street_address': '123 Mountain Road',
        'base_price': Decimal('150.00'),
        'num_rooms': 3,
        'num_bathrooms': 2,
        'max_guests': 6,
        'beds_per_room': 2,
        'bed_type': 'queen',
        'property_type': 'cabin',
        'checkin_time': '14:00',
        'checkout_time': '11:00',
        'is_active': True,
    },
    {
        'property_name': 'Beachfront Villa',
        'host_name': user.username,
        'full_description': 'Luxury villa with private beach access',
        'tagline': 'Luxury beachfront paradise',
        'country': 'Thailand',
        'city': 'Phuket',
        'street_address': '456 Beach Road',
        'base_price': Decimal('300.00'),
        'num_rooms': 5,
        'num_bathrooms': 4,
        'max_guests': 10,
        'beds_per_room': 2,
        'bed_type': 'king',
        'property_type': 'villa',
        'checkin_time': '15:00',
        'checkout_time': '12:00',
        'is_active': True,
    },
    {
        'property_name': 'Modern City Apartment',
        'host_name': user.username,
        'full_description': 'Stylish apartment in the heart of the city',
        'tagline': 'Urban luxury in Manhattan',
        'country': 'USA',
        'city': 'New York',
        'street_address': '789 Park Avenue',
        'base_price': Decimal('200.00'),
        'num_rooms': 2,
        'num_bathrooms': 2,
        'max_guests': 4,
        'beds_per_room': 1,
        'bed_type': 'queen',
        'property_type': 'apartment',
        'checkin_time': '16:00',
        'checkout_time': '10:00',
        'is_active': False,
    },
]

for data in accommodations_data:
    acc, created = Accommodation.objects.get_or_create(
        host=user,
        property_name=data['property_name'],
        defaults=data
    )
    status = "Created" if created else "Already exists"
    print(f"  {status}: {acc.property_name}")

# Create sample tours
tours_data = [
    {
        'tour_name': 'Mountain Hiking Adventure',
        'host_name': user.username,
        'full_description': 'Full-day guided hiking tour with breathtaking views',
        'tagline': 'Adventure in the Alps',
        'country': 'Switzerland',
        'city': 'Interlaken',
        'meeting_address': 'Town Square, Interlaken',
        'price_per_person': Decimal('80.00'),
        'duration_hours': 8,
        'max_group_size': 12,
        'difficulty_level': 'moderate',
        'is_active': True,
    },
    {
        'tour_name': 'City Food Tour',
        'host_name': user.username,
        'full_description': 'Taste the best local cuisine with expert guide',
        'tagline': 'Culinary journey through Rome',
        'country': 'Italy',
        'city': 'Rome',
        'meeting_address': 'Piazza Navona, Rome',
        'price_per_person': Decimal('60.00'),
        'duration_hours': 4,
        'max_group_size': 15,
        'difficulty_level': 'easy',
        'is_active': True,
    },
]

for data in tours_data:
    tour, created = Tour.objects.get_or_create(
        host=user,
        tour_name=data['tour_name'],
        defaults=data
    )
    status = "Created" if created else "Already exists"
    print(f"  {status}: {tour.tour_name}")

print("\n🎉 Sample data created successfully!")
print(f"📊 Total Accommodations: {Accommodation.objects.count()}")
print(f"📊 Total Tours: {Tour.objects.count()}")
print(f"\n🌐 Visit: http://localhost:8000/hostdashboard/")
print(f"👤 Login with username: {user.username}")
