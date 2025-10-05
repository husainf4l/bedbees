#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedbees.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Accommodation, AccommodationPhoto
from decimal import Decimal
from django.core.files import File
import urllib.request
from io import BytesIO

# Get or create host user
user = User.objects.filter(profile__is_host=True).first()
if not user:
    print("Creating host user...")
    user = User.objects.create_user(username='demohost', email='host@example.com', password='demo123')
    UserProfile.objects.create(user=user, is_host=True)

print(f"✅ Creating hotel accommodations for host: {user.username}")

# Hotel data with real details
hotels_data = [
    {
        'property_name': 'Grand Plaza Hotel',
        'tagline': 'Luxury in the heart of the city',
        'full_description': 'Experience 5-star luxury at the Grand Plaza Hotel. Located in the city center, our hotel offers spacious rooms with modern amenities, a rooftop pool, fine dining restaurant, and world-class spa facilities. Perfect for business travelers and tourists alike.',
        'country': 'United Arab Emirates',
        'city': 'Dubai',
        'street_address': '123 Sheikh Zayed Road',
        'base_price': Decimal('350.00'),
        'num_rooms': 1,
        'num_bathrooms': 1,
        'max_guests': 2,
        'beds_per_room': 1,
        'bed_type': 'king',
        'property_type': 'hotel',
        'checkin_time': '15:00',
        'checkout_time': '12:00',
        'amenities': 'WiFi, Pool, Spa, Restaurant, Gym, Room Service, Concierge, Parking',
        'is_published': True,
        'is_active': True,
        'image_filename': 'futuristic-dubai-landscape.jpg',
    },
    {
        'property_name': 'Seaside Resort & Spa',
        'tagline': 'Tropical paradise awaits',
        'full_description': 'Escape to our beachfront resort featuring private bungalows, infinity pools, and pristine white sand beaches. Enjoy water sports, spa treatments, and fresh seafood at our ocean-view restaurant. All-inclusive packages available.',
        'country': 'Thailand',
        'city': 'Phuket',
        'street_address': '789 Beach Road, Patong',
        'base_price': Decimal('280.00'),
        'num_rooms': 1,
        'num_bathrooms': 1,
        'max_guests': 2,
        'beds_per_room': 2,
        'bed_type': 'queen',
        'property_type': 'resort',
        'checkin_time': '14:00',
        'checkout_time': '11:00',
        'amenities': 'WiFi, Beach Access, Pool, Spa, Water Sports, Restaurant, Bar, Gym',
        'is_published': True,
        'is_active': True,
        'image_filename': 'woman-with-hat-sitting-chairs-beach-beautiful-tropical-be_Pawis9h.jpg',
    },
    {
        'property_name': 'Heritage Palace Hotel',
        'tagline': 'Where history meets luxury',
        'full_description': 'Stay in a beautifully restored 19th-century palace featuring elegant rooms with period furniture, modern amenities, and stunning architecture. Located near historical sites and museums. Experience royal treatment with our butler service.',
        'country': 'Morocco',
        'city': 'Marrakech',
        'street_address': '45 Medina Quarter',
        'base_price': Decimal('220.00'),
        'num_rooms': 1,
        'num_bathrooms': 1,
        'max_guests': 2,
        'beds_per_room': 1,
        'bed_type': 'king',
        'property_type': 'hotel',
        'checkin_time': '15:00',
        'checkout_time': '12:00',
        'amenities': 'WiFi, Restaurant, Spa, Pool, Garden, Rooftop Terrace, Butler Service',
        'is_published': True,
        'is_active': True,
        'image_filename': 'historical-casbah-taourirt-ouarzazate-morocco-with-white.jpg',
    },
    {
        'property_name': 'Skyline Tower Hotel',
        'tagline': 'Modern elegance with panoramic views',
        'full_description': 'Our contemporary hotel offers breathtaking city views from every room. Features include smart room technology, rooftop bar, infinity pool, and Michelin-starred restaurant. Perfect for discerning travelers seeking luxury and convenience.',
        'country': 'Qatar',
        'city': 'Doha',
        'street_address': '88 West Bay',
        'base_price': Decimal('400.00'),
        'num_rooms': 1,
        'num_bathrooms': 1,
        'max_guests': 2,
        'beds_per_room': 1,
        'bed_type': 'king',
        'property_type': 'hotel',
        'checkin_time': '15:00',
        'checkout_time': '12:00',
        'amenities': 'WiFi, Pool, Restaurant, Bar, Gym, Spa, Concierge, Valet Parking, Business Center',
        'is_published': True,
        'is_active': True,
        'image_filename': 'skyline-doha-city-center-qatar-middle-east.jpg',
    },
    {
        'property_name': 'Bosphorus View Hotel',
        'tagline': 'Where two continents meet',
        'full_description': 'Experience Istanbul from our boutique hotel with stunning Bosphorus views. Rooms blend Ottoman elegance with modern comfort. Walking distance to major attractions. Enjoy Turkish breakfast and evening tea on our terrace.',
        'country': 'Turkey',
        'city': 'Istanbul',
        'street_address': '22 Ortakoy Square',
        'base_price': Decimal('190.00'),
        'num_rooms': 1,
        'num_bathrooms': 1,
        'max_guests': 2,
        'beds_per_room': 1,
        'bed_type': 'queen',
        'property_type': 'hotel',
        'checkin_time': '14:00',
        'checkout_time': '12:00',
        'amenities': 'WiFi, Restaurant, Terrace, Breakfast Included, Concierge, Airport Transfer',
        'is_published': True,
        'is_active': True,
        'image_filename': 'panoramic-istanbul-city-twilight-turkey.jpg',
    },
    {
        'property_name': 'Nile River Hotel',
        'tagline': 'Ancient wonders at your doorstep',
        'full_description': 'Overlook the majestic Nile River from our elegant hotel. Close to pyramids and museums. Features include traditional Egyptian restaurant, rooftop pool, and nightly entertainment. Guided tours available.',
        'country': 'Egypt',
        'city': 'Cairo',
        'street_address': '15 Corniche El Nil',
        'base_price': Decimal('180.00'),
        'num_rooms': 1,
        'num_bathrooms': 1,
        'max_guests': 2,
        'beds_per_room': 2,
        'bed_type': 'twin',
        'property_type': 'hotel',
        'checkin_time': '15:00',
        'checkout_time': '12:00',
        'amenities': 'WiFi, Pool, Restaurant, Bar, Tour Desk, Gym, River View',
        'is_published': True,
        'is_active': True,
        'image_filename': 'old-mosque-cairo-egypt.jpg',
    },
    {
        'property_name': 'Cedar Mountain Resort',
        'tagline': 'Mountain serenity and Mediterranean charm',
        'full_description': 'Nestled in the Lebanese mountains, our resort offers stunning valley views, ski access in winter, and hiking trails in summer. Features include spa, multiple restaurants, and cozy fireplaces. Perfect for romantic getaways.',
        'country': 'Lebanon',
        'city': 'Faraya',
        'street_address': '100 Mountain Highway',
        'base_price': Decimal('240.00'),
        'num_rooms': 1,
        'num_bathrooms': 1,
        'max_guests': 2,
        'beds_per_room': 1,
        'bed_type': 'king',
        'property_type': 'resort',
        'checkin_time': '14:00',
        'checkout_time': '11:00',
        'amenities': 'WiFi, Spa, Restaurant, Bar, Ski Access, Hiking Trails, Fireplace, Mountain View',
        'is_published': True,
        'is_active': True,
        'image_filename': 'beautiful-view-pigeon-rocks-promenade-center-beirut-lebanon.jpg',
    },
    {
        'property_name': 'Pearl Tower Hotel',
        'tagline': 'Island luxury redefined',
        'full_description': 'Experience modern Arabian hospitality at our landmark hotel. Featuring underwater restaurant, private beach, water park, and luxury shopping. All rooms offer sea views and premium amenities.',
        'country': 'Bahrain',
        'city': 'Manama',
        'street_address': '50 Diplomatic Area',
        'base_price': Decimal('320.00'),
        'num_rooms': 1,
        'num_bathrooms': 1,
        'max_guests': 2,
        'beds_per_room': 1,
        'bed_type': 'king',
        'property_type': 'hotel',
        'checkin_time': '15:00',
        'checkout_time': '12:00',
        'amenities': 'WiFi, Beach Access, Pool, Water Park, Spa, Multiple Restaurants, Shopping Mall, Gym',
        'is_published': True,
        'is_active': True,
        'image_filename': 'reflection-illuminated-buildings-water-against-bahrain-skyline.jpg',
    },
]

created_hotels = []

for hotel_data in hotels_data:
    # Extract image filename
    image_filename = hotel_data.pop('image_filename', None)

    # Create accommodation
    accommodation = Accommodation.objects.create(
        host=user,
        **hotel_data
    )

    print(f"✅ Created: {accommodation.property_name}")

    # Add photo if image file exists
    if image_filename:
        image_path = f'/home/aqlaan/Desktop/bedbees/core/static/core/images/{image_filename}'
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                photo = AccommodationPhoto.objects.create(
                    accommodation=accommodation,
                    media_type='image',
                    title=f"{accommodation.property_name} - Main View",
                    alt_text=f"View of {accommodation.property_name}",
                    display_order=0,
                    is_hero=True,
                    visibility='public'
                )
                photo.original_file.save(image_filename, File(img_file), save=True)
                print(f"   📷 Added photo: {image_filename}")
        else:
            print(f"   ⚠️  Image not found: {image_path}")

    created_hotels.append(accommodation)

print(f"\n✅ Successfully created {len(created_hotels)} hotel accommodations!")
print(f"All hotels are published and active, ready to display on the website.")
