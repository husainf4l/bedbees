from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Country


class Command(BaseCommand):
    help = 'Seed demo data for countries/destinations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing demo data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing demo countries...')
            self.clear_demo_data()

        self.stdout.write('Creating demo countries...')
        countries = self.create_demo_countries()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded demo data: {len(countries)} countries'
            )
        )

    def clear_demo_data(self):
        """Clear existing demo countries"""
        Country.objects.filter(name__startswith='Demo:').delete()

    def create_demo_countries(self):
        """Create demo countries from the demo data"""
        countries = []

        # Demo countries data (extracted from views.py demo_destinations)
        demo_countries = [
            {
                'name': 'Jordan',
                'code': 'jordan',
                'description': 'Explore the ancient wonders of Jordan, from the rose-red city of Petra to the salty shores of the Dead Sea.',
                'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
                'accommodations_count': 245,
                'tours_count': 450,
                'attractions': ['Petra', 'Dead Sea', 'Wadi Rum', 'Jerash', 'Amman Citadel']
            },
            {
                'name': 'Tunisia',
                'code': 'tunisia',
                'description': 'Discover the Mediterranean jewel with Roman ruins, Sahara Desert, and ancient Carthage.',
                'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 298,
                'tours_count': 142,
                'attractions': ['Carthage', 'Sidi Bou Said', 'Djerba Island', 'Sahara Desert', 'Tunis Medina']
            },
            {
                'name': 'Algeria',
                'code': 'algeria',
                'description': 'Experience North Africa\'s largest country with ancient Roman cities, stunning Sahara, and Mediterranean coast.',
                'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 215,
                'tours_count': 98,
                'attractions': ['Algiers Casbah', 'Timgad', 'Djemila', 'Tassili n\'Ajjer', 'Tipaza']
            },
            {
                'name': 'Turkey',
                'code': 'turkey',
                'description': 'Bridge between Europe and Asia, offering rich history, stunning landscapes, and warm hospitality.',
                'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 423,
                'tours_count': 950,
                'attractions': ['Istanbul', 'Cappadocia', 'Pamukkale', 'Ephesus', 'Antalya']
            },
            {
                'name': 'Egypt',
                'code': 'egypt',
                'description': 'Home to the ancient pyramids and pharaohs, with a rich history spanning thousands of years.',
                'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 389,
                'tours_count': 600,
                'attractions': ['Pyramids of Giza', 'Luxor', 'Aswan', 'Cairo', 'Red Sea']
            },
            {
                'name': 'Morocco',
                'code': 'morocco',
                'description': 'A land of contrasts with bustling souks, stunning deserts, and the majestic Atlas Mountains.',
                'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 278,
                'tours_count': 145,
                'attractions': ['Marrakech', 'Sahara Desert', 'Chefchaouen', 'Atlas Mountains', 'Fes']
            },
            {
                'name': 'United Arab Emirates',
                'code': 'uae',
                'description': 'A modern oasis of luxury and innovation, blending traditional Arabian culture with cutting-edge architecture.',
                'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 892,
                'tours_count': 800,
                'attractions': ['Burj Khalifa', 'Palm Jumeirah', 'Dubai Mall', 'Sheikh Zayed Mosque', 'Dubai Desert Safari']
            },
            {
                'name': 'Lebanon',
                'code': 'lebanon',
                'description': 'A Mediterranean jewel known for its ancient history, vibrant culture, and stunning coastal beauty.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 234,
                'tours_count': 350,
                'attractions': ['Beirut', 'Baalbek', 'Byblos', 'Jeita Grotto', 'Cedars of God']
            },
            {
                'name': 'Qatar',
                'code': 'qatar',
                'description': 'A modern Arabian nation blending rich heritage with world-class luxury and sporting excellence.',
                'image': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 167,
                'tours_count': 280,
                'attractions': ['Doha', 'Museum of Islamic Art', 'Souq Waqif', 'Katara Cultural Village', 'Al Zubarah Fort']
            },
            {
                'name': 'Saudi Arabia',
                'code': 'saudi-arabia',
                'description': 'The heart of Islam with ancient deserts, modern cities, and sacred pilgrimage sites.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 445,
                'tours_count': 320,
                'attractions': ['Mecca', 'Medina', 'Riyadh', 'AlUla', 'Red Sea Coast']
            },
            {
                'name': 'Kuwait',
                'code': 'kuwait',
                'description': 'A modern Gulf state with rich cultural heritage, stunning desert landscapes, and warm hospitality.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 123,
                'tours_count': 180,
                'attractions': ['Kuwait City', 'Kuwait Towers', 'Liberation Tower', 'Tareq Rajab Museum', 'Al Shaheed Park']
            },
            {
                'name': 'Bahrain',
                'code': 'bahrain',
                'description': 'An island kingdom blending ancient Dilmun civilization with modern Arabian Gulf culture.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 89,
                'tours_count': 120,
                'attractions': ['Manama', 'Bahrain Fort', 'Al Fateh Grand Mosque', 'Bahrain World Trade Center', 'Tree of Life']
            },
            {
                'name': 'Oman',
                'code': 'oman',
                'description': 'An Arabian paradise of stunning deserts, turquoise coasts, and ancient fortresses.',
                'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 156,
                'tours_count': 250,
                'attractions': ['Muscat', 'Nizwa Fort', 'Wahiba Sands', 'Jebel Shams', 'Sur']
            },
            {
                'name': 'Syria',
                'code': 'syria',
                'description': 'Ancient land of civilization with rich history, stunning architecture, and Mediterranean charm.',
                'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 89,
                'tours_count': 150,
                'attractions': ['Damascus', 'Aleppo', 'Palmyra', 'Krak des Chevaliers', 'Bosra']
            },
            {
                'name': 'Iraq',
                'code': 'iraq',
                'description': 'Land of ancient Mesopotamia with rich history, archaeological treasures, and cultural heritage.',
                'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 67,
                'tours_count': 100,
                'attractions': ['Baghdad', 'Babylon', 'Uruk', 'Karbala', 'Erbil Citadel']
            },
            {
                'name': 'Yemen',
                'code': 'yemen',
                'description': 'Ancient land of spices, towering mountains, and rich cultural heritage.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 45,
                'tours_count': 80,
                'attractions': ['Sana\'a', 'Socotra Island', 'Zabid', 'Shibam', 'Aden']
            }
        ]

        with transaction.atomic():
            for country_data in demo_countries:
                country, created = Country.objects.get_or_create(
                    code=country_data['code'],
                    defaults=country_data
                )
                if created:
                    countries.append(country)
                    self.stdout.write(f'Created country: {country.name}')
                else:
                    self.stdout.write(f'Country already exists: {country.name}')

        return countries