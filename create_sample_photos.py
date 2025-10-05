#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedbees.settings')
django.setup()

from core.models import Accommodation, Tour, AccommodationPhoto, TourPhoto
from django.core.files.base import ContentFile

# Get sample accommodations and tours
accommodations = Accommodation.objects.all()
tours = Tour.objects.all()

print(f"Found {accommodations.count()} accommodations and {tours.count()} tours")

# Create sample photos for accommodations
for acc in accommodations:
    # Create hero photo
    hero_photo, created = AccommodationPhoto.objects.get_or_create(
        accommodation=acc,
        title=f"{acc.property_name} - Main View",
        defaults={
            'media_type': 'image',
            'caption': f"Beautiful view of {acc.property_name}",
            'alt_text': f"{acc.property_name} accommodation",
            'display_order': 0,
            'is_hero': True,
            'visibility': 'public',
            'nsfw_rating': 'safe',
        }
    )
    if created:
        print(f"Created hero photo for {acc.property_name}")

    # Create additional photos
    for i in range(1, 4):
        photo, created = AccommodationPhoto.objects.get_or_create(
            accommodation=acc,
            title=f"{acc.property_name} - Room {i}",
            defaults={
                'media_type': 'image',
                'caption': f"Interior view {i} of {acc.property_name}",
                'alt_text': f"{acc.property_name} room {i}",
                'display_order': i,
                'is_hero': False,
                'visibility': 'public',
                'nsfw_rating': 'safe',
            }
        )
        if created:
            print(f"Created room photo {i} for {acc.property_name}")

# Create sample photos for tours
for tour in tours:
    # Create hero photo
    hero_photo, created = TourPhoto.objects.get_or_create(
        tour=tour,
        title=f"{tour.tour_name} - Main Activity",
        defaults={
            'media_type': 'image',
            'caption': f"Exciting {tour.tour_name} experience",
            'alt_text': f"{tour.tour_name} tour activity",
            'display_order': 0,
            'is_hero': True,
            'visibility': 'public',
            'nsfw_rating': 'safe',
        }
    )
    if created:
        print(f"Created hero photo for {tour.tour_name}")

    # Create additional photos
    for i in range(1, 3):
        photo, created = TourPhoto.objects.get_or_create(
            tour=tour,
            title=f"{tour.tour_name} - View {i}",
            defaults={
                'media_type': 'image',
                'caption': f"Scenic view {i} from {tour.tour_name}",
                'alt_text': f"{tour.tour_name} scenic view {i}",
                'display_order': i,
                'is_hero': False,
                'visibility': 'public',
                'nsfw_rating': 'safe',
            }
        )
        if created:
            print(f"Created view photo {i} for {tour.tour_name}")

print("\n🎉 Sample photos created successfully!")
print(f"📊 Total Accommodation Photos: {AccommodationPhoto.objects.count()}")
print(f"📊 Total Tour Photos: {TourPhoto.objects.count()}")