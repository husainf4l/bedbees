from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from core.models import (
    Accommodation, AccommodationPhoto, Tour, TourPhoto,
    UserProfile, Listing, RoomType, AvailabilityDay, DayRoomInventory
)
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Seed demo data for accommodations and tours'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing demo data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing demo data...')
            self.clear_demo_data()

        self.stdout.write('Creating demo users...')
        users = self.create_demo_users()

        self.stdout.write('Creating demo accommodations...')
        accommodations = self.create_demo_accommodations(users)

        self.stdout.write('Creating demo tours...')
        tours = self.create_demo_tours(users)

        self.stdout.write('Creating demo listings and inventory...')
        self.create_demo_listings(accommodations, tours)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded demo data: {len(accommodations)} accommodations, {len(tours)} tours'
            )
        )

    def clear_demo_data(self):
        """Clear existing demo data"""
        Accommodation.objects.filter(property_name__startswith='Demo:').delete()
        Tour.objects.filter(tour_name__startswith='Demo:').delete()
        User.objects.filter(username__startswith='demo_host_').delete()

    def create_demo_users(self):
        """Create demo host users"""
        users = []
        for i in range(1, 6):  # Create 5 demo hosts
            username = f'demo_host_{i}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@demo.com',
                    'first_name': f'Demo Host {i}',
                    'last_name': 'User',
                    'is_staff': False,
                    'is_active': True,
                }
            )
            if created:
                user.set_password('demo123')
                user.save()

                # Create user profile
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'is_host': True,
                        'bio': f'Professional host with {random.randint(2, 10)} years of experience in hospitality.',
                        'languages_spoken': 'English, Arabic',
                        'phone_number': f'+971-50-{random.randint(1000000, 9999999)}',
                        'city': 'Dubai',
                        'country': 'UAE',
                        'business_name': f'Demo Hospitality {i}',
                        'business_type': 'company',
                    }
                )

            users.append(user)
        return users

    def create_demo_accommodations(self, users):
        """Create demo accommodations"""
        accommodations = []

        # Demo accommodation data
        demo_accommodations = [
            {
                'property_name': 'Demo: Burj Al Arab Jumeirah',
                'property_type': 'luxury_hotel',
                'country': 'UAE',
                'city': 'Dubai',
                'street_address': 'Jumeirah Beach Road',
                'base_price': 1200.00,
                'num_rooms': 2,
                'beds_per_room': 1,
                'bed_type': 'king',
                'num_bathrooms': 2,
                'max_guests': 4,
                'tagline': 'Iconic luxury hotel shaped like a sail',
                'full_description': 'Experience unparalleled luxury at the Burj Al Arab Jumeirah, Dubai\'s iconic seven-star hotel. This architectural masterpiece offers breathtaking views of the Arabian Gulf, world-class dining, and personalized service that exceeds expectations.',
                'amenities': 'WiFi,Pool,Spa,Restaurant,Fitness Center,Private Beach,Helipad,Valet Parking',
                'checkin_time': '15:00:00',
                'checkout_time': '12:00:00',
                'cancellation_policy': 'flexible',
                'is_published': True,
                'is_active': True,
            },
            {
                'property_name': 'Demo: Armani Hotel Dubai',
                'property_type': 'luxury_hotel',
                'country': 'UAE',
                'city': 'Dubai',
                'street_address': 'Burj Khalifa District',
                'base_price': 450.00,
                'num_rooms': 1,
                'beds_per_room': 1,
                'bed_type': 'king',
                'num_bathrooms': 1,
                'max_guests': 2,
                'tagline': 'Luxury redefined by Giorgio Armani',
                'full_description': 'Located in the heart of Dubai\'s business district, Armani Hotel Dubai offers minimalist luxury with Italian craftsmanship. The hotel features stunning architecture, contemporary design, and impeccable service.',
                'amenities': 'WiFi,Pool,Spa,Restaurant,Fitness Center,Business Center,Valet Parking',
                'checkin_time': '15:00:00',
                'checkout_time': '12:00:00',
                'cancellation_policy': 'moderate',
                'is_published': True,
                'is_active': True,
            },
            {
                'property_name': 'Demo: Atlantis The Palm',
                'property_type': 'beach_resort',
                'country': 'UAE',
                'city': 'Dubai',
                'street_address': 'Palm Jumeirah',
                'base_price': 350.00,
                'num_rooms': 1,
                'beds_per_room': 2,
                'bed_type': 'queen',
                'num_bathrooms': 1,
                'max_guests': 4,
                'tagline': 'Legendary resort on the Palm Jumeirah',
                'full_description': 'Atlantis The Palm is a legendary beach resort featuring an iconic architectural design inspired by the lost city of Atlantis. Enjoy world-class dining, thrilling water parks, and pristine beaches.',
                'amenities': 'WiFi,Pool,Water Park,Aquarium,Beach Access,Spa,Restaurant,Fitness Center',
                'checkin_time': '15:00:00',
                'checkout_time': '12:00:00',
                'cancellation_policy': 'flexible',
                'is_published': True,
                'is_active': True,
            },
            {
                'property_name': 'Demo: Four Seasons Hotel Cairo',
                'property_type': 'luxury_hotel',
                'country': 'Egypt',
                'city': 'Cairo',
                'street_address': 'Nile Plaza',
                'base_price': 320.00,
                'num_rooms': 1,
                'beds_per_room': 1,
                'bed_type': 'king',
                'num_bathrooms': 1,
                'max_guests': 2,
                'tagline': 'Luxury on the Nile with pyramids views',
                'full_description': 'Overlooking the Nile River and the pyramids, Four Seasons Hotel Cairo offers elegant accommodations and world-class service. Experience the perfect blend of modern luxury and ancient wonders.',
                'amenities': 'WiFi,Pool,Spa,Restaurant,Fitness Center,Nile View,Valet Parking',
                'checkin_time': '15:00:00',
                'checkout_time': '12:00:00',
                'cancellation_policy': 'moderate',
                'is_published': True,
                'is_active': True,
            },
            {
                'property_name': 'Demo: Kempinski Hotel Ishtar Dead Sea',
                'property_type': 'spa_resort',
                'country': 'Jordan',
                'city': 'Dead Sea',
                'street_address': 'Dead Sea Highway',
                'base_price': 220.00,
                'num_rooms': 1,
                'beds_per_room': 1,
                'bed_type': 'king',
                'num_bathrooms': 1,
                'max_guests': 2,
                'tagline': 'Therapeutic Dead Sea resort with mineral treatments',
                'full_description': 'Located on the shores of the Dead Sea, Kempinski Hotel Ishtar offers rejuvenating mineral treatments and floating experiences in the buoyant waters. This luxury spa resort provides the ultimate wellness retreat.',
                'amenities': 'WiFi,Pool,Spa,Private Beach,Restaurant,Fitness Center,Dead Sea Access',
                'checkin_time': '15:00:00',
                'checkout_time': '12:00:00',
                'cancellation_policy': 'flexible',
                'is_published': True,
                'is_active': True,
            },
            {
                'property_name': 'Demo: Ciragan Palace Kempinski Istanbul',
                'property_type': 'heritage_hotel',
                'country': 'Turkey',
                'city': 'Istanbul',
                'street_address': 'Ciragan Caddesi',
                'base_price': 420.00,
                'num_rooms': 1,
                'beds_per_room': 1,
                'bed_type': 'king',
                'num_bathrooms': 1,
                'max_guests': 2,
                'tagline': 'Historic palace turned luxury hotel on the Bosphorus',
                'full_description': 'Ciragan Palace Kempinski Istanbul transforms a 19th-century Ottoman palace into a modern luxury hotel. Enjoy Bosphorus views, Ottoman architecture, and world-class dining in this historic landmark.',
                'amenities': 'WiFi,Pool,Spa,Restaurant,Fitness Center,Bosphorus View,Valet Parking',
                'checkin_time': '15:00:00',
                'checkout_time': '12:00:00',
                'cancellation_policy': 'moderate',
                'is_published': True,
                'is_active': True,
            },
            {
                'property_name': 'Demo: Canaves Oia Boutique Hotel',
                'property_type': 'boutique_hotel',
                'country': 'Greece',
                'city': 'Santorini',
                'street_address': 'Oia Village',
                'base_price': 450.00,
                'num_rooms': 1,
                'beds_per_room': 1,
                'bed_type': 'king',
                'num_bathrooms': 1,
                'max_guests': 2,
                'tagline': 'Luxury boutique hotel with stunning caldera views',
                'full_description': 'Perched on the cliffs of Oia, Canaves Oia Boutique Hotel offers breathtaking views of the Santorini caldera. This intimate boutique hotel combines Cycladic architecture with modern luxury.',
                'amenities': 'WiFi,Pool,Spa,Restaurant,Caldera View,Fitness Center,Valet Parking',
                'checkin_time': '15:00:00',
                'checkout_time': '12:00:00',
                'cancellation_policy': 'strict',
                'is_published': True,
                'is_active': True,
            },
            {
                'property_name': 'Demo: Four Seasons Hotel Beirut',
                'property_type': 'luxury_hotel',
                'country': 'Lebanon',
                'city': 'Beirut',
                'street_address': 'Beirut Central District',
                'base_price': 350.00,
                'num_rooms': 1,
                'beds_per_room': 1,
                'bed_type': 'king',
                'num_bathrooms': 1,
                'max_guests': 2,
                'tagline': 'Luxury hotel in Beirut\'s vibrant Central District',
                'full_description': 'Four Seasons Hotel Beirut offers sophisticated luxury in the heart of Beirut\'s Central District. Experience world-class service, modern design, and proximity to the city\'s best dining and shopping.',
                'amenities': 'WiFi,Pool,Spa,Restaurant,Fitness Center,City View,Valet Parking',
                'checkin_time': '15:00:00',
                'checkout_time': '12:00:00',
                'cancellation_policy': 'moderate',
                'is_published': True,
                'is_active': True,
            },
        ]

        for i, acc_data in enumerate(demo_accommodations):
            host = random.choice(users)
            profile = UserProfile.objects.get(user=host)

            accommodation = Accommodation.objects.create(
                host=host,
                host_name=host.get_full_name(),
                entity_type='company',
                contact_email=host.email,
                contact_phone=profile.phone_number,
                business_address=f'{acc_data["city"]}, {acc_data["country"]}',
                **acc_data
            )

            # Create demo photos
            self.create_demo_photos(accommodation, 'accommodation')

            accommodations.append(accommodation)

        return accommodations

    def create_demo_tours(self, users):
        """Create demo tours"""
        tours = []

        # Demo tour data
        demo_tours = [
            {
                'tour_name': 'Demo: Dubai City Highlights Tour',
                'tour_category': 'cultural',
                'country': 'UAE',
                'city': 'Dubai',
                'duration': '8 hours',
                'price_per_person': 95.00,
                'min_participants': 2,
                'max_participants': 15,
                'age_restrictions': 'Suitable for all ages',
                'tagline': 'Explore Dubai\'s most iconic landmarks',
                'full_description': 'Discover Dubai\'s most famous attractions on this comprehensive city tour. Visit the Burj Khalifa, Dubai Mall, Jumeirah Mosque, and more. Learn about the city\'s transformation from desert trading post to modern metropolis.',
                'itinerary': '8:00 AM - Hotel pickup\n9:00 AM - Burj Khalifa visit\n11:00 AM - Dubai Mall exploration\n1:00 PM - Lunch break\n2:00 PM - Jumeirah Mosque\n4:00 PM - Traditional souk visit\n6:00 PM - Return to hotel',
                'inclusions': 'Professional guide,Entrance fees,Transportation,Lunch,Bottled water',
                'fitness_level': 'easy',
                'meeting_point': 'Hotel lobby or designated pickup point',
                'end_point': 'Hotel or designated drop-off point',
                'highlights': 'Burj Khalifa,Dubai Mall,Jumeirah Mosque,Gold Souk,Traditional culture',
                'languages': 'english,arabic',
                'cancellation_policy': 'flexible',
                'is_published': True,
                'is_active': True,
            },
            {
                'tour_name': 'Demo: Abu Dhabi Cultural Tour',
                'tour_category': 'cultural',
                'country': 'UAE',
                'city': 'Abu Dhabi',
                'duration': '6 hours',
                'price_per_person': 85.00,
                'min_participants': 2,
                'max_participants': 12,
                'age_restrictions': 'Suitable for all ages',
                'tagline': 'Experience Abu Dhabi\'s rich cultural heritage',
                'full_description': 'Explore Abu Dhabi\'s cultural landmarks including the Sheikh Zayed Grand Mosque, Louvre Abu Dhabi, and traditional souks. Discover the UAE\'s Islamic heritage and modern cultural institutions.',
                'itinerary': '9:00 AM - Hotel pickup\n10:00 AM - Sheikh Zayed Grand Mosque\n12:00 PM - Louvre Abu Dhabi\n2:00 PM - Traditional souk visit\n4:00 PM - Return to hotel',
                'inclusions': 'Professional guide,Entrance fees,Transportation,Bottled water',
                'fitness_level': 'easy',
                'meeting_point': 'Hotel lobby',
                'end_point': 'Hotel',
                'highlights': 'Sheikh Zayed Mosque,Louvre Abu Dhabi,Heritage sites,Cultural experience',
                'languages': 'english,arabic',
                'cancellation_policy': 'moderate',
                'is_published': True,
                'is_active': True,
            },
            {
                'tour_name': 'Demo: Desert Safari Experience',
                'tour_category': 'adventure',
                'country': 'UAE',
                'city': 'Dubai',
                'duration': '6 hours',
                'price_per_person': 75.00,
                'min_participants': 2,
                'max_participants': 8,
                'age_restrictions': 'Minimum age 8 years',
                'tagline': 'Thrilling desert adventure with dune bashing',
                'full_description': 'Experience the thrill of Dubai\'s desert on this exciting safari. Drive through massive sand dunes, enjoy traditional Bedouin hospitality, and witness a spectacular desert sunset.',
                'itinerary': '3:00 PM - Hotel pickup\n4:00 PM - Desert arrival and dune bashing\n5:30 PM - Sandboarding and camel riding\n6:30 PM - Traditional Bedouin camp\n7:30 PM - BBQ dinner and entertainment\n8:30 PM - Stargazing and return',
                'inclusions': '4x4 vehicle,Bedouin guide,Sandboarding,Camel riding,BBQ dinner,Tanoura dance show',
                'fitness_level': 'moderate',
                'meeting_point': 'Hotel lobby',
                'end_point': 'Hotel',
                'highlights': 'Dune bashing,Sandboarding,Camel riding,Bedouin camp,Sunset views',
                'languages': 'english,arabic',
                'cancellation_policy': 'flexible',
                'is_published': True,
                'is_active': True,
            },
            {
                'tour_name': 'Demo: Petra Full Day Tour',
                'tour_category': 'historical',
                'country': 'Jordan',
                'city': 'Petra',
                'duration': '8 hours',
                'price_per_person': 85.00,
                'min_participants': 1,
                'max_participants': 15,
                'age_restrictions': 'Suitable for all ages',
                'tagline': 'Explore the ancient Nabatean city of Petra',
                'full_description': 'Journey through the Siq canyon to discover the magnificent Treasury and other wonders of Petra. Walk among 2,000-year-old rock-cut architecture and learn about Nabatean civilization.',
                'itinerary': '8:00 AM - Hotel pickup\n9:30 AM - Arrive at Petra\n10:00 AM - Enter through Siq Canyon\n11:00 AM - Explore Treasury and lower city\n1:00 PM - Lunch break\n2:00 PM - Visit Monastery and upper city\n4:00 PM - Free exploration\n5:30 PM - Return to hotel',
                'inclusions': 'Professional guide,Entrance fees,Transportation,Lunch,Bottled water,Horse riding option',
                'fitness_level': 'moderate',
                'meeting_point': 'Hotel lobby',
                'end_point': 'Hotel',
                'highlights': 'Siq Canyon,Treasury,Monastery,Royal Tombs,Ancient water systems',
                'languages': 'english,arabic',
                'cancellation_policy': 'moderate',
                'is_published': True,
                'is_active': True,
            },
            {
                'tour_name': 'Demo: Cappadocia Hot Air Balloon Tour',
                'tour_category': 'adventure',
                'country': 'Turkey',
                'city': 'Cappadocia',
                'duration': '4 hours',
                'price_per_person': 180.00,
                'min_participants': 1,
                'max_participants': 20,
                'age_restrictions': 'Minimum age 6 years',
                'tagline': 'Soar above fairy chimneys at sunrise',
                'full_description': 'Experience Cappadocia from above on a magical hot air balloon ride. Float over surreal rock formations, ancient cave dwellings, and green valleys at sunrise.',
                'itinerary': '5:30 AM - Hotel pickup\n6:30 AM - Balloon preparation and safety briefing\n7:00 AM - Sunrise balloon flight (1 hour)\n8:00 AM - Landing and champagne toast\n8:30 AM - Return to hotel',
                'inclusions': 'Professional pilot,Hot air balloon,Transportation,Champagne toast,Certificate',
                'fitness_level': 'easy',
                'meeting_point': 'Hotel lobby',
                'end_point': 'Hotel',
                'highlights': 'Sunrise flight,Fairy chimneys,Green valleys,Champagne toast,Panoramic views',
                'languages': 'english,turkish',
                'cancellation_policy': 'strict',
                'is_published': True,
                'is_active': True,
            },
            {
                'tour_name': 'Demo: Santorini Sunset Cruise',
                'tour_category': 'nature',
                'country': 'Greece',
                'city': 'Santorini',
                'duration': '3 hours',
                'price_per_person': 65.00,
                'min_participants': 2,
                'max_participants': 50,
                'age_restrictions': 'Suitable for all ages',
                'tagline': 'Romantic sunset cruise around Santorini',
                'full_description': 'Sail around the stunning Santorini caldera on a romantic sunset cruise. Enjoy breathtaking views of the volcanic cliffs, swim in crystal-clear waters, and toast to the spectacular sunset.',
                'itinerary': '6:00 PM - Port pickup\n6:30 PM - Depart for cruise\n7:00 PM - Swimming stop\n7:30 PM - Wine and snacks\n8:00 PM - Spectacular sunset\n8:30 PM - Return to port',
                'inclusions': 'Boat cruise,Snacks and wine,Swimming equipment,Professional crew',
                'fitness_level': 'easy',
                'meeting_point': 'Santorini port',
                'end_point': 'Santorini port',
                'highlights': 'Caldera views,Sunset,Sailing,Swimming,Wine tasting',
                'languages': 'english,greek',
                'cancellation_policy': 'flexible',
                'is_published': True,
                'is_active': True,
            },
            {
                'tour_name': 'Demo: Beirut City Exploration',
                'tour_category': 'cultural',
                'country': 'Lebanon',
                'city': 'Beirut',
                'duration': '4 hours',
                'price_per_person': 45.00,
                'min_participants': 2,
                'max_participants': 15,
                'age_restrictions': 'Suitable for all ages',
                'tagline': 'Discover Beirut\'s vibrant culture and history',
                'full_description': 'Explore Beirut\'s fascinating blend of ancient history and modern culture. Visit historic sites, bustling souks, and contemporary attractions in the city known as the "Paris of the Middle East."',
                'itinerary': '9:00 AM - Hotel pickup\n9:30 AM - Martyrs Square and Parliament\n10:30 AM - Mohammad Al-Amin Mosque\n11:30 AM - Souk exploration\n12:30 PM - Lunch and return',
                'inclusions': 'Professional guide,Transportation,Bottled water',
                'fitness_level': 'easy',
                'meeting_point': 'Hotel lobby',
                'end_point': 'Hotel',
                'highlights': 'Martyrs Square,Mohammad Al-Amin Mosque,Traditional souks,Cultural sites',
                'languages': 'english,arabic,french',
                'cancellation_policy': 'moderate',
                'is_published': True,
                'is_active': True,
            },
            {
                'tour_name': 'Demo: Pyramids and Sphinx Full Day Tour',
                'tour_category': 'historical',
                'country': 'Egypt',
                'city': 'Cairo',
                'duration': '8 hours',
                'price_per_person': 65.00,
                'min_participants': 1,
                'max_participants': 12,
                'age_restrictions': 'Suitable for all ages',
                'tagline': 'Explore the legendary pyramids and Sphinx',
                'full_description': 'Visit the Great Pyramids of Giza, the Sphinx, and the Egyptian Museum on this comprehensive tour. Learn about ancient Egyptian civilization and its magnificent architectural achievements.',
                'itinerary': '8:00 AM - Hotel pickup\n9:00 AM - Pyramids of Giza and Sphinx\n11:00 AM - Egyptian Museum\n1:00 PM - Lunch break\n2:00 PM - Khan El Khalili bazaar\n4:00 PM - Return to hotel',
                'inclusions': 'Professional guide,Entrance fees,Transportation,Lunch,Bottled water',
                'fitness_level': 'moderate',
                'meeting_point': 'Hotel lobby',
                'end_point': 'Hotel',
                'highlights': 'Great Pyramids,Sphinx,Egyptian Museum,Khan El Khalili,Tutankhamun treasures',
                'languages': 'english,arabic',
                'cancellation_policy': 'moderate',
                'is_published': True,
                'is_active': True,
            },
        ]

        for i, tour_data in enumerate(demo_tours):
            host = random.choice(users)
            profile = UserProfile.objects.get(user=host)

            tour = Tour.objects.create(
                host=host,
                host_name=host.get_full_name(),
                contact_email=host.email,
                contact_phone=profile.phone_number,
                certifications='Licensed Tour Guide',
                **tour_data
            )

            # Create demo photos
            self.create_demo_photos(tour, 'tour')

            tours.append(tour)

        return tours

    def create_demo_photos(self, obj, obj_type):
        """Create demo photos for accommodation or tour"""
        # Demo photo URLs (using Unsplash)
        photo_urls = [
            'https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
        ]

        for i, url in enumerate(photo_urls[:3]):  # Create 3 photos per object
            if obj_type == 'accommodation':
                AccommodationPhoto.objects.create(
                    accommodation=obj,
                    original_file=url,
                    title=f'{obj.property_name} - Photo {i+1}',
                    caption=f'Beautiful view of {obj.property_name}',
                    display_order=i,
                    is_hero=(i == 0),
                )
            elif obj_type == 'tour':
                TourPhoto.objects.create(
                    tour=obj,
                    original_file=url,
                    title=f'{obj.tour_name} - Photo {i+1}',
                    caption=f'Experience {obj.tour_name}',
                    display_order=i,
                    is_hero=(i == 0),
                )

    def create_demo_listings(self, accommodations, tours):
        """Create demo listings with room types and inventory"""
        for accommodation in accommodations:
            # Create listing
            listing = Listing.objects.create(
                owner=accommodation.host,
                name=accommodation.property_name,
                listing_type='accommodation',
                country=accommodation.country,
                city=accommodation.city,
                currency='USD',
                default_price=accommodation.base_price,
                default_min_stay=1,
                is_active=True,
                is_published=True,
            )

            # Create room type
            room_type = RoomType.objects.create(
                listing=listing,
                name=f'Standard Room',
                base_price=accommodation.base_price,
                total_units=accommodation.num_rooms,
                is_active=True,
            )

            # Create availability for next 30 days
            self.create_availability_days(listing, room_type)

        for tour in tours:
            # Create listing
            listing = Listing.objects.create(
                owner=tour.host,
                name=tour.tour_name,
                listing_type='tour',
                country=tour.country,
                city=tour.city,
                currency='USD',
                default_price=tour.price_per_person,
                default_min_stay=1,
                is_active=True,
                is_published=True,
            )

            # Create room type (representing tour capacity)
            room_type = RoomType.objects.create(
                listing=listing,
                name=f'Tour Package',
                base_price=tour.price_per_person,
                total_units=tour.max_participants,
                is_active=True,
            )

            # Create availability for next 30 days
            self.create_availability_days(listing, room_type)

    def create_availability_days(self, listing, room_type):
        """Create availability days for the next 30 days"""
        today = datetime.now().date()

        for i in range(30):
            date = today + timedelta(days=i)

            # Create availability day
            availability_day = AvailabilityDay.objects.create(
                listing=listing,
                date=date,
                status='OPEN',
            )

            # Create day room inventory
            DayRoomInventory.objects.create(
                listing=listing,
                room_type=room_type,
                date=date,
                units_open=room_type.total_units,
                units_booked=0,
                stop_sell=False,
            )