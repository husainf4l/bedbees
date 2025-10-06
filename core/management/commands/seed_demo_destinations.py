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

        # Demo countries data (extracted from views.py)
        demo_countries = [
            {
                'name': 'Jordan',
                'code': 'JO',
                'description': 'Jordan, a Middle Eastern country on the Arabian Peninsula, is known for its ancient history, stunning landscapes, and warm hospitality. From the rose-red city of Petra to the mineral-rich waters of the Dead Sea, Jordan offers a unique blend of archaeological wonders and natural beauty.',
                'image': 'https://images.unsplash.com/photo-1559628376-f2b5d2e67b6a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 45,
                'tours_count': 32,
                'attractions': [
                    {'name': 'Petra', 'slug': 'petra', 'description': 'Ancient Nabatean city carved into rose-red cliffs'},
                    {'name': 'Dead Sea', 'slug': 'dead-sea', 'description': 'Lowest point on Earth with mineral-rich waters'},
                    {'name': 'Wadi Rum', 'slug': 'wadi-rum', 'description': 'Desert landscape with towering sandstone mountains'},
                    {'name': 'Jerash', 'slug': 'jerash', 'description': 'Well-preserved Roman city with colonnaded streets'},
                    {'name': 'Amman Citadel', 'slug': 'amman-citadel', 'description': 'Ancient fortress overlooking the capital city'}
                ]
            },
            {
                'name': 'Cyprus',
                'code': 'CY',
                'description': 'Cyprus, the third-largest island in the Mediterranean, offers a perfect blend of history, culture, and natural beauty. With its stunning beaches, ancient ruins, and charming villages, Cyprus is a paradise for history enthusiasts and beach lovers alike.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 28,
                'tours_count': 19,
                'attractions': [
                    {'name': 'Nicosia Old City', 'slug': 'nicosia-old-city', 'description': 'Historic walled city with Venetian and Ottoman architecture'},
                    {'name': 'Paphos Archaeological Park', 'slug': 'paphos-archaeological-park', 'description': 'UNESCO site with ancient mosaics and tombs'},
                    {'name': 'Troodos Mountains', 'slug': 'troodos-mountains', 'description': 'Mountain range with Byzantine churches and hiking trails'},
                    {'name': 'Ayia Napa', 'slug': 'ayia-napa', 'description': 'Popular beach resort with golden sands and nightlife'},
                    {'name': 'Limassol Castle', 'slug': 'limassol-castle', 'description': 'Medieval castle housing the Cyprus Medieval Museum'}
                ]
            },
            {
                'name': 'Greece',
                'code': 'GR',
                'description': 'Greece, the cradle of Western civilization, boasts a rich history spanning thousands of years. From the iconic Acropolis in Athens to the stunning islands of the Aegean Sea, Greece offers an unparalleled journey through ancient mythology, philosophy, and breathtaking landscapes.',
                'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 156,
                'tours_count': 89,
                'attractions': [
                    {'name': 'Acropolis of Athens', 'slug': 'acropolis-athens', 'description': 'Ancient citadel with Parthenon and other temples'},
                    {'name': 'Santorini Caldera', 'slug': 'santorini-caldera', 'description': 'Stunning volcanic crater with white-washed buildings'},
                    {'name': 'Meteora Monasteries', 'slug': 'meteora-monasteries', 'description': 'Monasteries perched on towering rock pillars'},
                    {'name': 'Delphi Archaeological Site', 'slug': 'delphi-archaeological-site', 'description': 'Ancient sanctuary of Apollo with theater and stadium'},
                    {'name': 'Mykonos Windmills', 'slug': 'mykonos-windmills', 'description': 'Iconic white windmills overlooking the Aegean Sea'}
                ]
            },
            {
                'name': 'Turkey',
                'code': 'TR',
                'description': 'Turkey, straddling Europe and Asia, is a land of contrasts where East meets West. From the bustling streets of Istanbul to the fairy-tale landscapes of Cappadocia, Turkey offers a tapestry of cultures, cuisines, and natural wonders that captivate every traveler.',
                'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 203,
                'tours_count': 145,
                'attractions': [
                    {'name': 'Hagia Sophia', 'slug': 'hagia-sophia', 'description': 'Iconic Byzantine cathedral turned mosque turned museum'},
                    {'name': 'Cappadocia', 'slug': 'cappadocia', 'description': 'Surreal landscape with cave dwellings and hot air balloons'},
                    {'name': 'Pamukkale', 'slug': 'pamukkale', 'description': 'Natural thermal springs with white travertine terraces'},
                    {'name': 'Ephesus Ancient City', 'slug': 'ephesus-ancient-city', 'description': 'Well-preserved Roman city with Library of Celsus'},
                    {'name': 'Topkapi Palace', 'slug': 'topkapi-palace', 'description': 'Ottoman imperial residence housing sacred relics'}
                ]
            },
            {
                'name': 'Egypt',
                'code': 'EG',
                'description': 'Egypt, the land of the pharaohs, is home to some of the world\'s most iconic ancient wonders. From the pyramids of Giza to the temples of Luxor, Egypt offers an unforgettable journey through one of humanity\'s greatest civilizations.',
                'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 98,
                'tours_count': 67,
                'attractions': [
                    {'name': 'Pyramids of Giza', 'slug': 'pyramids-giza', 'description': 'Ancient wonders including the Great Pyramid and Sphinx'},
                    {'name': 'Valley of the Kings', 'slug': 'valley-kings', 'description': 'Royal necropolis with tombs of pharaohs'},
                    {'name': 'Karnak Temple Complex', 'slug': 'karnak-temple-complex', 'description': 'Largest ancient religious site in the world'},
                    {'name': 'Nile River Cruise', 'slug': 'nile-river-cruise', 'description': 'Scenic journey along the lifeblood of ancient Egypt'},
                    {'name': 'Egyptian Museum', 'slug': 'egyptian-museum', 'description': 'World\'s largest collection of Pharaonic antiquities'}
                ]
            },
            {
                'name': 'Morocco',
                'code': 'MA',
                'description': 'Morocco, a North African gem, enchants with its vibrant colors, aromatic spices, and rich cultural heritage. From the bustling souks of Marrakech to the blue-washed streets of Chefchaouen, Morocco is a sensory feast for the adventurous traveler.',
                'image': 'https://images.unsplash.com/photo-1539020140153-e365f6b6e12f?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 76,
                'tours_count': 52,
                'attractions': [
                    {'name': 'Bahia Palace', 'slug': 'bahia-palace', 'description': '19th-century palace with intricate Islamic architecture'},
                    {'name': 'Chefchaouen', 'slug': 'chefchaouen', 'description': 'Blue-washed mountain town with stunning views'},
                    {'name': 'Sahara Desert', 'slug': 'sahara-desert', 'description': 'Endless dunes and Berber camps under starry skies'},
                    {'name': 'Jemaa el-Fnaa', 'slug': 'jemaa-el-fnaa', 'description': 'Vibrant main square with street performers and food stalls'},
                    {'name': 'Saadian Tombs', 'slug': 'saadian-tombs', 'description': 'Royal necropolis with stunning Moroccan architecture'}
                ]
            },
            {
                'name': 'United Arab Emirates',
                'code': 'AE',
                'description': 'The UAE, a federation of seven emirates, represents the pinnacle of modern luxury and innovation. From Dubai\'s towering skyscrapers to Abu Dhabi\'s cultural landmarks, the UAE seamlessly blends tradition with cutting-edge technology.',
                'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 134,
                'tours_count': 78,
                'attractions': [
                    {'name': 'Burj Khalifa', 'slug': 'burj-khalifa', 'description': 'World\'s tallest building with observation decks'},
                    {'name': 'Palm Jumeirah', 'slug': 'palm-jumeirah', 'description': 'Artificial island shaped like a palm tree'},
                    {'name': 'Dubai Mall', 'slug': 'dubai-mall', 'description': 'World\'s largest shopping and entertainment center'},
                    {'name': 'Sheikh Zayed Grand Mosque', 'slug': 'sheikh-zayed-grand-mosque', 'description': 'Stunning mosque with capacity for 40,000 worshippers'},
                    {'name': 'Dubai Fountain', 'slug': 'dubai-fountain', 'description': 'World\'s largest choreographed fountain system'}
                ]
            },
            {
                'name': 'Lebanon',
                'code': 'LB',
                'description': 'Lebanon, often called the "Switzerland of the Middle East," offers a unique blend of Mediterranean charm, rich history, and vibrant culture. From the ancient ruins of Baalbek to the bustling streets of Beirut, Lebanon is a country of remarkable diversity and resilience.',
                'image': 'https://images.unsplash.com/photo-1541343672885-9be56236302a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 67,
                'tours_count': 43,
                'attractions': [
                    {'name': 'Baalbek', 'slug': 'baalbek', 'description': 'Ancient Roman temple complex with massive stone blocks'},
                    {'name': 'Beirut Central District', 'slug': 'beirut-central-district', 'description': 'Modern downtown with Roman, Ottoman, and French influences'},
                    {'name': 'Jeita Grotto', 'slug': 'jeita-grotto', 'description': 'Spectacular limestone cave with underground river'},
                    {'name': 'Byblos', 'slug': 'byblos', 'description': 'Oldest continuously inhabited city in the world'},
                    {'name': 'Cedars of God', 'slug': 'cedars-god', 'description': 'Ancient cedar forest in the mountains'}
                ]
            },
            {
                'name': 'Qatar',
                'code': 'QA',
                'description': 'Qatar, a peninsula jutting into the Persian Gulf, has transformed itself from a pearl-diving backwater into a modern metropolis. Doha\'s skyline of futuristic architecture and world-class museums reflects Qatar\'s ambitious vision for the future.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 45,
                'tours_count': 28,
                'attractions': [
                    {'name': 'Museum of Islamic Art', 'slug': 'museum-islamic-art', 'description': 'World-class collection of Islamic art and artifacts'},
                    {'name': 'Souq Waqif', 'slug': 'souq-waqif', 'description': 'Traditional market with spices, perfumes, and falconry'},
                    {'name': 'Katara Cultural Village', 'slug': 'katara-cultural-village', 'description': 'Cultural complex with theaters, galleries, and beach'},
                    {'name': 'Doha Corniche', 'slug': 'doha-corniche', 'description': 'Scenic waterfront promenade with modern architecture'},
                    {'name': 'Al Zubarah Fort', 'slug': 'al-zubarah-fort', 'description': '18th-century fort and UNESCO World Heritage site'}
                ]
            },
            {
                'name': 'Saudi Arabia',
                'code': 'SA',
                'description': 'Saudi Arabia, the birthplace of Islam, is a vast desert kingdom with ancient cities, stunning landscapes, and a rapidly modernizing society. From the holy cities of Mecca and Medina to the Red Sea coast, Saudi Arabia offers spiritual journeys and natural wonders.',
                'image': 'https://images.unsplash.com/photo-1559628376-f2b5d2e67b6a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 89,
                'tours_count': 56,
                'attractions': [
                    {'name': 'Masjid al-Haram', 'slug': 'masjid-al-haram', 'description': 'Islam\'s holiest mosque surrounding the Kaaba'},
                    {'name': 'Al-Masjid an-Nabawi', 'slug': 'al-masjid-an-nabawi', 'description': 'Second holiest mosque containing Prophet Muhammad\'s tomb'},
                    {'name': 'Red Sea Coast', 'slug': 'red-sea-coast', 'description': 'Pristine beaches and coral reefs for diving and relaxation'},
                    {'name': 'Al-Ula', 'slug': 'al-ula', 'description': 'Ancient oasis city with Nabatean tombs and rock carvings'},
                    {'name': 'Edge of the World', 'slug': 'edge-world', 'description': 'Dramatic escarpment overlooking vast desert landscapes'}
                ]
            },
            {
                'name': 'Kuwait',
                'code': 'KW',
                'description': 'Kuwait, a small but wealthy Gulf state, combines traditional Islamic culture with modern urban life. The country\'s strategic location and rich history make it a fascinating destination for those interested in Middle Eastern culture and architecture.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 34,
                'tours_count': 22,
                'attractions': [
                    {'name': 'Kuwait Towers', 'slug': 'kuwait-towers', 'description': 'Iconic trio of towers symbolizing Kuwait\'s modernity'},
                    {'name': 'Grand Mosque', 'slug': 'grand-mosque', 'description': 'Largest mosque in Kuwait with stunning Islamic architecture'},
                    {'name': 'Souq Al-Mubarakiya', 'slug': 'souq-al-mubarakiya', 'description': 'Historic market with traditional crafts and spices'},
                    {'name': 'Al-Shaheed Park', 'slug': 'al-shaheed-park', 'description': 'Memorial park honoring Kuwait\'s liberation'},
                    {'name': 'Scientific Center', 'slug': 'scientific-center', 'description': 'Interactive science museum and planetarium'}
                ]
            },
            {
                'name': 'Bahrain',
                'code': 'BH',
                'description': 'Bahrain, the smallest Arab country, is an archipelago in the Persian Gulf known for its rich history and modern development. From ancient Dilmun civilization sites to contemporary financial centers, Bahrain offers a unique blend of past and present.',
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 28,
                'tours_count': 19,
                'attractions': [
                    {'name': 'Bahrain Fort', 'slug': 'bahrain-fort', 'description': 'Ancient Portuguese fort with museum and sea views'},
                    {'name': 'Al Fateh Grand Mosque', 'slug': 'al-fateh-grand-mosque', 'description': 'Largest mosque in Bahrain accommodating 7,000 worshippers'},
                    {'name': 'Bahrain National Museum', 'slug': 'bahrain-national-museum', 'description': 'Showcases Bahrain\'s history from Dilmun to modern times'},
                    {'name': 'Tree of Life', 'slug': 'tree-life', 'description': 'Ancient mesquite tree in desert oasis'},
                    {'name': 'A\'ali Burial Mounds', 'slug': 'aali-burial-mounds', 'description': '5,000-year-old burial site from Dilmun civilization'}
                ]
            },
            {
                'name': 'Oman',
                'code': 'OM',
                'description': 'Oman, with its dramatic mountain landscapes and pristine coastline, offers an authentic Arabian experience. From the ancient city of Muscat to the vast Empty Quarter desert, Oman preserves traditional culture while embracing sustainable tourism.',
                'image': 'https://images.unsplash.com/photo-1559628376-f2b5d2e67b6a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 52,
                'tours_count': 35,
                'attractions': [
                    {'name': 'Sultan Qaboos Grand Mosque', 'slug': 'sultan-qaboos-grand-mosque', 'description': 'Stunning mosque with world\'s second-largest carpet'},
                    {'name': 'Nizwa Fort', 'slug': 'nizwa-fort', 'description': '16th-century fort with impressive round towers'},
                    {'name': 'Wahiba Sands', 'slug': 'wahiba-sands', 'description': 'Spectacular desert dunes and Bedouin culture'},
                    {'name': 'Musandam Peninsula', 'slug': 'musandam-peninsula', 'description': 'Dramatic fjords and traditional dhow cruises'},
                    {'name': 'Jebel Shams', 'slug': 'jebel-shams', 'description': 'Oman\'s highest mountain with breathtaking views'}
                ]
            },
            {
                'name': 'Syria',
                'code': 'SY',
                'description': 'Syria, once a crossroads of ancient civilizations, boasts a rich archaeological heritage. From the magnificent ruins of Palmyra to the coastal city of Tartus, Syria offers insights into the cradle of human civilization.',
                'image': 'https://images.unsplash.com/photo-1559628376-f2b5d2e67b6a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 23,
                'tours_count': 15,
                'attractions': [
                    {'name': 'Palmyra', 'slug': 'palmyra', 'description': 'Ancient oasis city with Roman ruins and theater'},
                    {'name': 'Damascus Old City', 'slug': 'damascus-old-city', 'description': 'World\'s oldest continuously inhabited city'},
                    {'name': 'Bosra', 'slug': 'bosra', 'description': 'Roman theater carved from black basalt stone'},
                    {'name': 'Krak des Chevaliers', 'slug': 'krak-des-chevaliers', 'description': 'Medieval castle and UNESCO World Heritage site'},
                    {'name': 'Umayyad Mosque', 'slug': 'umayyad-mosque', 'description': 'One of Islam\'s largest and oldest mosques'}
                ]
            },
            {
                'name': 'Iraq',
                'code': 'IQ',
                'description': 'Iraq, the land between the Tigris and Euphrates rivers, is the birthplace of civilization. From the ancient ziggurats of Ur to the modern city of Baghdad, Iraq offers a profound journey through human history and cultural heritage.',
                'image': 'https://images.unsplash.com/photo-1559628376-f2b5d2e67b6a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 18,
                'tours_count': 12,
                'attractions': [
                    {'name': 'Babylon', 'slug': 'babylon', 'description': 'Ancient city with Hanging Gardens and Ishtar Gate'},
                    {'name': 'Ziggurat of Ur', 'slug': 'ziggurat-ur', 'description': 'Sumerian temple tower dating back 4,000 years'},
                    {'name': 'Samarra', 'slug': 'samarra', 'description': 'Great Mosque with world\'s largest minaret'},
                    {'name': 'Erbil Citadel', 'slug': 'erbil-citadel', 'description': 'Ancient fortified settlement and UNESCO site'},
                    {'name': 'Kurdistan Mountains', 'slug': 'kurdistan-mountains', 'description': 'Stunning landscapes and traditional villages'}
                ]
            },
            {
                'name': 'Yemen',
                'code': 'YE',
                'description': 'Yemen, at the southwestern tip of the Arabian Peninsula, is a land of ancient civilizations and stunning landscapes. From the towering mud-brick skyscrapers of Sana\'a to the Socotra islands, Yemen offers unique cultural and natural experiences.',
                'image': 'https://images.unsplash.com/photo-1559628376-f2b5d2e67b6a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 15,
                'tours_count': 9,
                'attractions': [
                    {'name': 'Old City of Sana\'a', 'slug': 'old-city-sanaa', 'description': 'UNESCO site with multi-story mud-brick buildings'},
                    {'name': 'Socotra Island', 'slug': 'socotra-island', 'description': 'Archipelago with unique dragon\'s blood trees'},
                    {'name': 'Zabid', 'slug': 'zabid', 'description': 'Medieval city and center of Islamic learning'},
                    {'name': 'Shibam', 'slug': 'shibam', 'description': 'Ancient skyscraper city made of mud bricks'},
                    {'name': 'Wadi Hadramaut', 'slug': 'wadi-hadramaut', 'description': 'Spectacular canyon landscapes and traditional villages'}
                ]
            },
            {
                'name': 'Tunisia',
                'code': 'TN',
                'description': 'Tunisia, North Africa\'s smallest country, bridges the Mediterranean world with the Sahara Desert. From Roman ruins in Carthage to Berber villages in the south, Tunisia offers a fascinating mix of cultures and landscapes.',
                'image': 'https://images.unsplash.com/photo-1539020140153-e365f6b6e12f?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 41,
                'tours_count': 28,
                'attractions': [
                    {'name': 'Carthage', 'slug': 'carthage', 'description': 'Ancient Phoenician city with Roman ruins'},
                    {'name': 'Sidi Bou Said', 'slug': 'sidi-bou-said', 'description': 'Charming blue-and-white cliffside village'},
                    {'name': 'El Jem Amphitheater', 'slug': 'el-jem-amphitheater', 'description': 'Third-largest Roman amphitheater in the world'},
                    {'name': 'Dougga', 'slug': 'dougga', 'description': 'Extensive Roman city ruins in rural setting'},
                    {'name': 'Matmata', 'slug': 'matmata', 'description': 'Underground Berber villages and Star Wars filming location'}
                ]
            },
            {
                'name': 'Algeria',
                'code': 'DZ',
                'description': 'Algeria, Africa\'s largest country by land area, boasts diverse landscapes from Mediterranean coasts to vast Sahara deserts. Rich in history and culture, Algeria offers ancient Roman ruins, Islamic architecture, and stunning natural beauty.',
                'image': 'https://images.unsplash.com/photo-1539020140153-e365f6b6e12f?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 35,
                'tours_count': 24,
                'attractions': [
                    {'name': 'Casbah of Algiers', 'slug': 'casbah-algiers', 'description': 'Historic citadel and UNESCO World Heritage site'},
                    {'name': 'Timgad', 'slug': 'timgad', 'description': 'Roman city ruins in the Aurès Mountains'},
                    {'name': 'Hoggar Mountains', 'slug': 'hoggar-mountains', 'description': 'Spectacular volcanic peaks and Tuareg culture'},
                    {'name': 'Djémila', 'slug': 'djémila', 'description': 'Roman ruins perched on a mountainside'},
                    {'name': 'M\'Zab Valley', 'slug': 'mzab-valley', 'description': 'Five ksar villages with traditional architecture'}
                ]
            },
            {
                'name': 'Palestine',
                'code': 'PS',
                'description': 'Palestine, the Holy Land, holds profound religious and historical significance for Judaism, Christianity, and Islam. From Jerusalem\'s ancient walls to Bethlehem\'s churches, Palestine offers spiritual journeys and cultural experiences.',
                'image': 'https://images.unsplash.com/photo-1559628376-f2b5d2e67b6a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 22,
                'tours_count': 16,
                'attractions': [
                    {'name': 'Old City of Jerusalem', 'slug': 'old-city-jerusalem', 'description': 'Ancient walled city with holy sites for three religions'},
                    {'name': 'Church of the Holy Sepulchre', 'slug': 'church-holy-sepulchre', 'description': 'Christian holy site believed to be Jesus\' tomb'},
                    {'name': 'Western Wall', 'slug': 'western-wall', 'description': 'Sacred Jewish prayer site and remnant of Second Temple'},
                    {'name': 'Bethlehem', 'slug': 'bethlehem', 'description': 'Birthplace of Jesus with Church of the Nativity'},
                    {'name': 'Dead Sea Scrolls', 'slug': 'dead-sea-scrolls', 'description': 'Ancient manuscripts discovered in Qumran caves'}
                ]
            },
            {
                'name': 'Libya',
                'code': 'LY',
                'description': 'Libya, with its extensive Mediterranean coastline and vast Sahara interior, has been a crossroads of civilizations for millennia. From Greek and Roman ruins to Islamic architecture, Libya offers a rich tapestry of historical and cultural experiences.',
                'image': 'https://images.unsplash.com/photo-1539020140153-e365f6b6e12f?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 19,
                'tours_count': 13,
                'attractions': [
                    {'name': 'Leptis Magna', 'slug': 'leptis-magna', 'description': 'Extensive Roman city ruins on the Mediterranean coast'},
                    {'name': 'Sabha', 'slug': 'sabha', 'description': 'Desert city known as the "Bride of the Desert"'},
                    {'name': 'Cyrene', 'slug': 'cyrene', 'description': 'Ancient Greek colony with theater and temples'},
                    {'name': 'Ghadames', 'slug': 'ghadames', 'description': 'Medieval desert oasis with traditional architecture'},
                    {'name': 'Tripoli Medina', 'slug': 'tripoli-medina', 'description': 'Historic old city with Ottoman and Italian influences'}
                ]
            },
            {
                'name': 'Sudan',
                'code': 'SD',
                'description': 'Sudan, Africa\'s third-largest country, is a land of ancient pyramids, vast deserts, and the life-giving Nile River. From the Nubian pyramids to the Red Sea coast, Sudan offers archaeological treasures and diverse cultural experiences.',
                'image': 'https://images.unsplash.com/photo-1539020140153-e365f6b6e12f?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'accommodations_count': 16,
                'tours_count': 11,
                'attractions': [
                    {'name': 'Meroë Pyramids', 'slug': 'meroe-pyramids', 'description': 'Ancient Nubian pyramids and royal city'},
                    {'name': 'Nubian Villages', 'slug': 'nubian-villages', 'description': 'Traditional mud-brick villages along the Nile'},
                    {'name': 'Red Sea Coast', 'slug': 'red-sea-coast', 'description': 'Coral reefs and beaches for diving and relaxation'},
                    {'name': 'Kerma', 'slug': 'kerma', 'description': 'Ancient Kushite capital with temple ruins'},
                    {'name': 'Dongola', 'slug': 'dongola', 'description': 'Historic city and center of Christian Nubia'}
                ]
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