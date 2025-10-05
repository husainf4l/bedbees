#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedbees.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Accommodation, Tour, AccommodationPhoto, TourPhoto
from decimal import Decimal
from django.core.files import File
import os

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

# Photo assignments for accommodations
accommodation_photos = {
    'Cozy Mountain Cabin': [
        'beautiful-luxury-outdoor-swimming-pool-hotel-resort.jpg',
        'travel-suitcase-with-hat-nature-beautiful-mountain.jpg',
        'swimming-pool-beach-luxury-hotel-type-entertainment-complex-amara-dolce-vita-luxury-hotel-resort-tekirova-kemer-turkey.jpg',
    ],
    'Beachfront Villa': [
        'woman-with-hat-sitting-chairs-beach-beautiful-tropical-beach-woman-relaxing-tropical-beach-koh-nangyuan-island.jpg',
        'dubai-sea-view-inside-room-big-glass.jpg',
        'beautiful-luxury-outdoor-swimming-pool-hotel-resort.jpg',
        'swimming-pool-beach-luxury-hotel-type-entertainment-complex-amara-dolce-vita-luxury-hotel-resort-tekirova-kemer-turkey.jpg',
    ],
    'Modern City Apartment': [
        'futuristic-dubai-landscape.jpg',
        'dubai-sea-view-inside-room-big-glass.jpg',
        'vertical-historical-al-rabi-tower-against-blue-cloudy-sky-united-arab-emirates.jpg',
    ],
}

for data in accommodations_data:
    acc, created = Accommodation.objects.get_or_create(
        host=user,
        property_name=data['property_name'],
        defaults=data
    )
    status = "Created" if created else "Already exists"
    print(f"  {status}: {acc.property_name}")

    # Add photos to accommodation
    if acc.property_name in accommodation_photos:
        photo_files = accommodation_photos[acc.property_name]
        for idx, photo_file in enumerate(photo_files):
            photo_path = f'core/static/core/images/{photo_file}'
            if os.path.exists(photo_path):
                # Check if photo already exists
                existing_photo = AccommodationPhoto.objects.filter(
                    accommodation=acc,
                    title=photo_file
                ).first()

                if not existing_photo:
                    with open(photo_path, 'rb') as f:
                        photo = AccommodationPhoto.objects.create(
                            accommodation=acc,
                            title=photo_file,
                            display_order=idx,
                            is_hero=(idx == 0),  # First photo is hero
                            visibility='public',
                            nsfw_rating='safe'
                        )
                        photo.original_file.save(photo_file, File(f), save=True)
                    print(f"    Added photo: {photo_file}")
                else:
                    print(f"    Photo already exists: {photo_file}")

# Create sample tours
tours_data = [
    {
        'tour_name': 'Mountain Hiking Adventure',
        'host_name': user.username,
        'full_description': 'Full-day guided hiking tour with breathtaking views',
        'tagline': 'Adventure in the Alps',
        'country': 'Switzerland',
        'city': 'Interlaken',
        'meeting_point': 'Town Square, Interlaken',
        'price_per_person': Decimal('80.00'),
        'duration': '8 hours',
        'max_participants': 12,
        'min_participants': 2,
        'fitness_level': 'moderate',
        'tour_category': 'adventure',
        'languages': 'english,german',
        'itinerary': 'Morning pickup, scenic drive to trailhead, guided hike with views, picnic lunch, return to town',
        'is_active': True,
    },
    {
        'tour_name': 'City Food Tour',
        'host_name': user.username,
        'full_description': 'Taste the best local cuisine with expert guide',
        'tagline': 'Culinary journey through Rome',
        'country': 'Italy',
        'city': 'Rome',
        'meeting_point': 'Piazza Navona, Rome',
        'price_per_person': Decimal('60.00'),
        'duration': '4 hours',
        'max_participants': 15,
        'min_participants': 2,
        'fitness_level': 'easy',
        'tour_category': 'food',
        'languages': 'english,italian',
        'itinerary': 'Meet at Piazza Navona, visit local markets, taste authentic Roman cuisine, wine tasting, end at historic piazza',
        'is_active': True,
    },
]

# Photo assignments for tours
tour_photos = {
    'Mountain Hiking Adventure': [
        'travel-suitcase-with-hat-nature-beautiful-mountain.jpg',
        'ruined-ancient-building-made-large-towers-rocks-clear-sky.jpg',
        'tourist-carrying-baggage.jpg',
    ],
    'City Food Tour': [
        'panoramic-istanbul-city-twilight-turkey.jpg',
        'old-mosque-cairo-egypt.jpg',
        'view-buildings-against-cloudy-sky.jpg',
        'historical-casbah-taourirt-ouarzazate-morocco-with-white.jpg',
    ],
}

for data in tours_data:
    tour, created = Tour.objects.get_or_create(
        host=user,
        tour_name=data['tour_name'],
        defaults=data
    )
    status = "Created" if created else "Already exists"
    print(f"  {status}: {tour.tour_name}")

    # Add photos to tour
    if tour.tour_name in tour_photos:
        photo_files = tour_photos[tour.tour_name]
        for idx, photo_file in enumerate(photo_files):
            photo_path = f'core/static/core/images/{photo_file}'
            if os.path.exists(photo_path):
                # Check if photo already exists
                existing_photo = TourPhoto.objects.filter(
                    tour=tour,
                    title=photo_file
                ).first()

                if not existing_photo:
                    with open(photo_path, 'rb') as f:
                        photo = TourPhoto.objects.create(
                            tour=tour,
                            title=photo_file,
                            display_order=idx,
                            is_hero=(idx == 0),  # First photo is hero
                            visibility='public',
                            nsfw_rating='safe'
                        )
                        photo.original_file.save(photo_file, File(f), save=True)
                    print(f"    Added photo: {photo_file}")
                else:
                    print(f"    Photo already exists: {photo_file}")

print("\n🎉 Sample data created successfully!")
print(f"📊 Total Accommodations: {Accommodation.objects.count()}")
print(f"📊 Total Tours: {Tour.objects.count()}")
print(f"📸 Total Accommodation Photos: {AccommodationPhoto.objects.count()}")
print(f"📸 Total Tour Photos: {TourPhoto.objects.count()}")
print(f"\n🌐 Visit: http://localhost:8000/hostdashboard/")
print(f"👤 Login with username: {user.username}")
