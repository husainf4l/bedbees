from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytz

# Create your models here.

class UserProfile(models.Model):
    """Extended user profile to differentiate between hosts and travelers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_host = models.BooleanField(default=False)
    
    # Basic Profile Information
    profile_picture = models.ImageField(upload_to='user_profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    
    # Location Information
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Host-specific Information
    host_since = models.DateField(blank=True, null=True)
    languages_spoken = models.CharField(max_length=200, blank=True, null=True, help_text="Comma separated languages")
    response_time = models.CharField(max_length=50, blank=True, null=True)
    response_rate = models.IntegerField(default=0, help_text="Response rate percentage")

    # Business Information (for hosts)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    business_type = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('individual', 'Individual Host'),
        ('company', 'Company'),
        ('hotel_chain', 'Hotel Chain'),
        ('ngo', 'NGO'),
        ('family_business', 'Family Business'),
        ('tour_operator', 'Tour Operator'),
    ])
    business_registration = models.CharField(max_length=100, blank=True, null=True)
    tax_id = models.CharField(max_length=50, blank=True, null=True)
    mission_statement = models.TextField(max_length=300, blank=True, null=True)

    # Hosting Style
    hosting_approach = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('hands_on', 'Hands-on / Personal'),
        ('remote', 'Remote / Self Check-in'),
        ('team_managed', 'Team Managed'),
    ])
    special_services = models.TextField(max_length=500, blank=True, null=True, help_text="Special services offered (e.g., airport pickup, guided tours)")

    # Trust & Sustainability
    sustainability_practices = models.TextField(max_length=500, blank=True, null=True)
    awards_badges = models.TextField(max_length=300, blank=True, null=True, help_text="Awards or recognitions")

    # Business License Verification
    business_license_verified = models.BooleanField(default=False)
    payment_verified = models.BooleanField(default=False)
    
    # Social Media Links
    website = models.URLField(blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=True)
    
    # Verification Status
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    id_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.rule_type})"
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    def get_verification_score(self):
        """Calculate verification score out of 100"""
        score = 0
        if self.email_verified:
            score += 25
        if self.phone_verified:
            score += 25
        if self.id_verified:
            score += 25
        if self.business_license_verified:
            score += 15
        if self.payment_verified:
            score += 10
        return score

    def get_years_hosting(self):
        """Calculate years of hosting experience"""
        if self.host_since:
            from datetime import date
            years = (date.today() - self.host_since).days // 365
            return years if years > 0 else 0
        return 0

    def get_total_listings(self):
        """Get total number of active listings"""
        accommodations = self.user.accommodations.filter(is_active=True).count()
        tours = self.user.tours.filter(is_active=True).count()
        return accommodations + tours


class Accommodation(models.Model):
    """Accommodation listing model for hotels, apartments, villas, etc."""
    PROPERTY_TYPES = [
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('resort', 'Resort'),
        ('hostel', 'Hostel'),
        ('guesthouse', 'Guesthouse'),
        ('boutique', 'Boutique Hotel'),
        ('motel', 'Motel'),
        ('bed_breakfast', 'Bed & Breakfast'),
        ('cottage', 'Cottage'),
        ('cabin', 'Cabin'),
        ('chalet', 'Chalet'),
        ('bungalow', 'Bungalow'),
        ('penthouse', 'Penthouse'),
        ('studio', 'Studio'),
        ('loft', 'Loft'),
        ('townhouse', 'Townhouse'),
        ('farmhouse', 'Farmhouse'),
        ('castle', 'Castle'),
        ('palace', 'Palace'),
    ]

    BED_TYPES = [
        ('single', 'Single Bed'),
        ('twin', 'Twin Bed'),
        ('double', 'Double Bed'),
        ('full', 'Full Bed'),
        ('queen', 'Queen Bed'),
        ('king', 'King Bed'),
        ('california_king', 'California King'),
        ('bunk', 'Bunk Bed'),
        ('sofa_bed', 'Sofa Bed'),
        ('futon', 'Futon'),
        ('murphy', 'Murphy Bed'),
        ('mixed', 'Mixed Types'),
    ]

    AMENITIES = [
        # Basic Amenities
        ('wifi', 'WiFi'),
        ('parking', 'Free Parking'),
        ('air_conditioning', 'Air Conditioning'),
        ('heating', 'Heating'),
        ('tv', 'TV'),
        ('cable_tv', 'Cable TV'),
        ('streaming_services', 'Streaming Services'),
        ('sound_system', 'Sound System'),
        
        # Kitchen & Dining
        ('kitchen', 'Full Kitchen'),
        ('microwave', 'Microwave'),
        ('oven', 'Oven'),
        ('stove', 'Stove'),
        ('refrigerator', 'Refrigerator'),
        ('dishwasher', 'Dishwasher'),
        ('coffee_maker', 'Coffee Maker'),
        ('tea_kettle', 'Tea Kettle'),
        ('toaster', 'Toaster'),
        ('blender', 'Blender'),
        ('dining_area', 'Dining Area'),
        ('utensils', 'Cooking Utensils'),
        ('dishes', 'Dishes & Silverware'),
        
        # Bathroom
        ('private_bathroom', 'Private Bathroom'),
        ('shared_bathroom', 'Shared Bathroom'),
        ('bathtub', 'Bathtub'),
        ('shower', 'Shower'),
        ('hair_dryer', 'Hair Dryer'),
        ('shampoo', 'Shampoo'),
        ('body_soap', 'Body Soap'),
        ('towels', 'Towels'),
        ('linens', 'Bed Linens'),
        
        # Bedroom & Laundry
        ('bed_linen', 'Bed Linens'),
        ('extra_pillows', 'Extra Pillows'),
        ('blankets', 'Blankets'),
        ('wardrobe', 'Wardrobe/Closet'),
        ('washing_machine', 'Washing Machine'),
        ('dryer', 'Dryer'),
        ('iron', 'Iron'),
        ('ironing_board', 'Ironing Board'),
        
        # Outdoor & View
        ('balcony', 'Balcony'),
        ('terrace', 'Terrace'),
        ('garden', 'Garden'),
        ('patio', 'Patio'),
        ('pool', 'Swimming Pool'),
        ('hot_tub', 'Hot Tub'),
        ('fireplace', 'Fireplace'),
        ('bbq_grill', 'BBQ Grill'),
        ('outdoor_furniture', 'Outdoor Furniture'),
        ('mountain_view', 'Mountain View'),
        ('ocean_view', 'Ocean View'),
        ('city_view', 'City View'),
        ('garden_view', 'Garden View'),
        ('lake_view', 'Lake View'),
        
        # Safety & Security
        ('smoke_detector', 'Smoke Detector'),
        ('carbon_monoxide_detector', 'Carbon Monoxide Detector'),
        ('fire_extinguisher', 'Fire Extinguisher'),
        ('first_aid_kit', 'First Aid Kit'),
        ('security_cameras', 'Security Cameras'),
        ('safe', 'Safe'),
        ('lock_on_bedroom_door', 'Lock on Bedroom Door'),
        
        # Accessibility
        ('wheelchair_accessible', 'Wheelchair Accessible'),
        ('elevator', 'Elevator'),
        ('stair_gates', 'Stair Gates'),
        ('wide_doorways', 'Wide Doorways'),
        ('accessible_bathroom', 'Accessible Bathroom'),
        
        # Entertainment
        ('books', 'Books & Reading Material'),
        ('board_games', 'Board Games'),
        ('piano', 'Piano'),
        ('guitar', 'Guitar'),
        ('game_console', 'Game Console'),
        ('projector', 'Projector'),
        ('dvd_player', 'DVD Player'),
        
        # Business & Work
        ('workspace', 'Dedicated Workspace'),
        ('computer', 'Computer'),
        ('printer', 'Printer'),
        ('fax_machine', 'Fax Machine'),
        
        # Family & Kids
        ('crib', 'Crib'),
        ('high_chair', 'High Chair'),
        ('childrens_books', 'Children\'s Books'),
        ('toys', 'Toys'),
        ('babysitter_recommendations', 'Babysitter Recommendations'),
        ('family_friendly', 'Family/Kid Friendly'),
        
        # Pets
        ('pet_friendly', 'Pet Friendly'),
        ('pet_bowls', 'Pet Bowls'),
        
        # Wellness
        ('gym', 'Gym'),
        ('yoga_mats', 'Yoga Mats'),
        ('meditation_space', 'Meditation Space'),
        ('spa_services', 'Spa Services'),
        
        # Services
        ('housekeeping', 'Housekeeping'),
        ('concierge', 'Concierge Service'),
        ('room_service', 'Room Service'),
        ('laundry_service', 'Laundry Service'),
        ('airport_shuttle', 'Airport Shuttle'),
        ('car_rental', 'Car Rental'),
        ('tour_desk', 'Tour Desk'),
        ('ticket_service', 'Ticket Service'),
        
        # Other
        ('smoking_allowed', 'Smoking Allowed'),
        ('events_allowed', 'Events Allowed'),
        ('long_term_stays', 'Long Term Stays Allowed'),
        ('luggage_storage', 'Luggage Storage'),
        ('baggage_drop', '24-hour Check-in'),
    ]

    PROPERTY_FEATURES = [
        # Location Features
        ('beachfront', 'Beachfront'),
        ('lakefront', 'Lakefront'),
        ('mountain_location', 'Mountain Location'),
        ('city_center', 'City Center'),
        ('rural_location', 'Rural/Countryside'),
        ('historic_district', 'Historic District'),
        ('university_area', 'Near University'),
        ('business_district', 'Business District'),
        ('shopping_district', 'Shopping District'),
        ('entertainment_district', 'Entertainment District'),
        
        # Property Characteristics
        ('standalone_house', 'Standalone House'),
        ('apartment_building', 'Apartment Building'),
        ('condominium', 'Condominium'),
        ('townhouse', 'Townhouse'),
        ('duplex', 'Duplex'),
        ('triplex', 'Triplex'),
        ('penthouse', 'Penthouse'),
        ('basement_apartment', 'Basement Apartment'),
        ('loft', 'Loft'),
        ('studio', 'Studio'),
        
        # Architectural Style
        ('modern', 'Modern Architecture'),
        ('traditional', 'Traditional Architecture'),
        ('colonial', 'Colonial Style'),
        ('victorian', 'Victorian Style'),
        ('mediterranean', 'Mediterranean Style'),
        ('tropical', 'Tropical Style'),
        ('rustic', 'Rustic Style'),
        ('industrial', 'Industrial Style'),
        ('minimalist', 'Minimalist Design'),
        ('luxury', 'Luxury Finishes'),
        
        # Building Features
        ('elevator', 'Elevator'),
        ('staircase', 'Grand Staircase'),
        ('fireplace', 'Fireplace'),
        ('hardwood_floors', 'Hardwood Floors'),
        ('tile_floors', 'Tile Floors'),
        ('carpet', 'Carpet'),
        ('high_ceilings', 'High Ceilings'),
        ('exposed_beams', 'Exposed Beams'),
        ('skylights', 'Skylights'),
        ('bay_windows', 'Bay Windows'),
        
        # Outdoor Features
        ('private_garden', 'Private Garden'),
        ('shared_garden', 'Shared Garden'),
        ('rooftop_terrace', 'Rooftop Terrace'),
        ('balcony', 'Balcony'),
        ('patio', 'Patio'),
        ('deck', 'Deck'),
        ('porch', 'Porch'),
        ('veranda', 'Veranda'),
        ('courtyard', 'Courtyard'),
        ('fountain', 'Fountain'),
        
        # Water Features
        ('swimming_pool', 'Swimming Pool'),
        ('infinity_pool', 'Infinity Pool'),
        ('plunge_pool', 'Plunge Pool'),
        ('heated_pool', 'Heated Pool'),
        ('jacuzzi', 'Jacuzzi/Hot Tub'),
        ('sauna', 'Sauna'),
        ('steam_room', 'Steam Room'),
        ('outdoor_shower', 'Outdoor Shower'),
        ('pond', 'Pond'),
        ('waterfall', 'Waterfall'),
        
        # Sustainability
        ('solar_panels', 'Solar Panels'),
        ('rainwater_collection', 'Rainwater Collection'),
        ('composting', 'Composting Facilities'),
        ('recycling_program', 'Recycling Program'),
        ('energy_efficient', 'Energy Efficient Appliances'),
        ('green_certified', 'Green Certified'),
        ('eco_friendly', 'Eco-Friendly Materials'),
        
        # Unique Features
        ('wine_cellar', 'Wine Cellar'),
        ('home_theater', 'Home Theater'),
        ('game_room', 'Game Room'),
        ('library', 'Library'),
        ('art_collection', 'Art Collection'),
        ('antique_furniture', 'Antique Furniture'),
        ('grand_piano', 'Grand Piano'),
        ('billiard_table', 'Billiard Table'),
        ('tennis_court', 'Tennis Court'),
        ('basketball_court', 'Basketball Court'),
        
        # Business Features
        ('meeting_room', 'Meeting Room'),
        ('conference_facilities', 'Conference Facilities'),
        ('business_center', 'Business Center'),
        ('secretarial_services', 'Secretarial Services'),
        ('translation_services', 'Translation Services'),
        
        # Wellness Features
        ('spa', 'On-site Spa'),
        ('yoga_studio', 'Yoga Studio'),
        ('meditation_room', 'Meditation Room'),
        ('fitness_center', 'Fitness Center'),
        ('pilates_equipment', 'Pilates Equipment'),
        ('massage_room', 'Massage Room'),
        ('aromatherapy', 'Aromatherapy'),
        
        # Security Features
        ('24_hour_security', '24-Hour Security'),
        ('gated_community', 'Gated Community'),
        ('doorman', 'Doorman'),
        ('keycard_access', 'Keycard Access'),
        ('biometric_access', 'Biometric Access'),
        ('cctv', 'CCTV Surveillance'),
        ('alarm_system', 'Alarm System'),
        
        # Accessibility Features
        ('wheelchair_accessible', 'Wheelchair Accessible'),
        ('braille_signage', 'Braille Signage'),
        ('audio_guides', 'Audio Guides'),
        ('accessible_parking', 'Accessible Parking'),
        ('roll_in_shower', 'Roll-in Shower'),
        
        # Cultural Features
        ('museum_quality_art', 'Museum-Quality Art'),
        ('historical_artifacts', 'Historical Artifacts'),
        ('cultural_exhibits', 'Cultural Exhibits'),
        ('traditional_architecture', 'Traditional Architecture'),
        ('local_artisan_work', 'Local Artisan Work'),
    ]

    NEARBY_LANDMARKS = [
        # Natural Landmarks
        ('beach', 'Beach'),
        ('mountain', 'Mountain'),
        ('lake', 'Lake'),
        ('river', 'River'),
        ('ocean', 'Ocean'),
        ('forest', 'Forest'),
        ('national_park', 'National Park'),
        ('waterfall', 'Waterfall'),
        ('canyon', 'Canyon'),
        ('desert', 'Desert'),
        ('volcano', 'Volcano'),
        ('hot_springs', 'Hot Springs'),
        ('coral_reef', 'Coral Reef'),
        ('wetlands', 'Wetlands'),
        
        # Urban Landmarks
        ('city_center', 'City Center'),
        ('downtown', 'Downtown'),
        ('shopping_mall', 'Shopping Mall'),
        ('market', 'Local Market'),
        ('plaza', 'Plaza/Square'),
        ('park', 'City Park'),
        ('museum', 'Museum'),
        ('art_gallery', 'Art Gallery'),
        ('theater', 'Theater'),
        ('concert_hall', 'Concert Hall'),
        ('stadium', 'Stadium'),
        ('arena', 'Sports Arena'),
        
        # Historical Sites
        ('castle', 'Castle'),
        ('palace', 'Palace'),
        ('cathedral', 'Cathedral'),
        ('temple', 'Temple'),
        ('mosque', 'Mosque'),
        ('church', 'Church'),
        ('monastery', 'Monastery'),
        ('ruins', 'Ancient Ruins'),
        ('fortress', 'Fortress'),
        ('historic_district', 'Historic District'),
        ('archaeological_site', 'Archaeological Site'),
        ('memorial', 'Memorial/Monument'),
        
        # Cultural Attractions
        ('zoo', 'Zoo'),
        ('aquarium', 'Aquarium'),
        ('botanical_garden', 'Botanical Garden'),
        ('amusement_park', 'Amusement Park'),
        ('theme_park', 'Theme Park'),
        ('casino', 'Casino'),
        ('spa_resort', 'Spa Resort'),
        ('golf_course', 'Golf Course'),
        ('ski_resort', 'Ski Resort'),
        ('beach_resort', 'Beach Resort'),
        
        # Transportation Hubs
        ('airport', 'Airport'),
        ('train_station', 'Train Station'),
        ('bus_station', 'Bus Station'),
        ('ferry_terminal', 'Ferry Terminal'),
        ('metro_station', 'Metro Station'),
        ('tram_stop', 'Tram Stop'),
        ('bike_rental', 'Bike Rental'),
        ('car_rental', 'Car Rental'),
        
        # Educational Institutions
        ('university', 'University'),
        ('college', 'College'),
        ('school', 'School'),
        ('library', 'Library'),
        ('research_center', 'Research Center'),
        ('observatory', 'Observatory'),
        
        # Medical Facilities
        ('hospital', 'Hospital'),
        ('clinic', 'Medical Clinic'),
        ('pharmacy', 'Pharmacy'),
        ('spa', 'Spa/Medical Spa'),
        
        # Business & Commercial
        ('business_district', 'Business District'),
        ('convention_center', 'Convention Center'),
        ('trade_center', 'Trade Center'),
        ('industrial_park', 'Industrial Park'),
        ('technology_park', 'Technology Park'),
        
        # Recreational
        ('hiking_trail', 'Hiking Trail'),
        ('cycling_path', 'Cycling Path'),
        ('scenic_drive', 'Scenic Drive'),
        ('picnic_area', 'Picnic Area'),
        ('campground', 'Campground'),
        ('fishing_spot', 'Fishing Spot'),
        ('diving_site', 'Diving Site'),
        ('surfing_beach', 'Surfing Beach'),
        
        # Unique/Local
        ('local_vineyard', 'Local Vineyard'),
        ('farmers_market', 'Farmers Market'),
        ('craft_center', 'Arts & Crafts Center'),
        ('cultural_center', 'Cultural Center'),
        ('community_center', 'Community Center'),
        ('sports_complex', 'Sports Complex'),
        ('recreation_center', 'Recreation Center'),
    ]

    CANCELLATION_POLICIES = [
        ('flexible', 'Flexible - Free cancellation 24 hours before'),
        ('moderate', 'Moderate - Free cancellation 5 days before'),
        ('strict', 'Strict - 50% refund up to 7 days before'),
        ('no-refund', 'Non-refundable'),
    ]

    # Host Information
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accommodations')
    host_name = models.CharField(max_length=200)
    entity_type = models.CharField(max_length=50)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    business_address = models.TextField()
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    bank_account = models.CharField(max_length=100, blank=True, null=True)

    # Basic Property Info
    property_name = models.CharField(max_length=200)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    star_rating = models.IntegerField(blank=True, null=True, choices=[(i, f'{i} Star') for i in range(1, 6)])
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    # Capacity
    num_rooms = models.IntegerField()
    beds_per_room = models.IntegerField()
    bed_type = models.CharField(max_length=50, choices=BED_TYPES)
    num_bathrooms = models.IntegerField()
    max_guests = models.IntegerField()
    property_size = models.IntegerField(blank=True, null=True, help_text="Size in square meters")

    # Description
    tagline = models.CharField(max_length=150)
    full_description = models.TextField()
    property_features = models.TextField(blank=True, null=True)
    nearby_landmarks = models.TextField(blank=True, null=True)
    checkin_time = models.TimeField()
    checkout_time = models.TimeField()

    # Amenities (stored as JSON or comma-separated)
    amenities = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated amenities")

    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    cleaning_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    extra_guest_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Policies
    cancellation_policy = models.CharField(max_length=50, choices=CANCELLATION_POLICIES)
    house_rules = models.TextField(blank=True, null=True)

    # Status
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.property_name} - {self.city}, {self.country}"

    class Meta:
        ordering = ['-created_at']


class AccommodationPhoto(models.Model):
    """Photos for accommodation listings"""
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='accommodations/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.accommodation.property_name}"

    class Meta:
        ordering = ['order', '-uploaded_at']


class Tour(models.Model):
    """Tour and experience listing model"""
    TOUR_CATEGORIES = [
        ('cultural', 'Cultural Tour'),
        ('adventure', 'Adventure Tour'),
        ('food', 'Food & Drink'),
        ('nature', 'Nature & Wildlife'),
        ('water', 'Water Activities'),
        ('historical', 'Historical Sites'),
        ('wellness', 'Wellness & Spa'),
    ]

    LANGUAGES = [
        # Major World Languages
        ('english', 'English'),
        ('spanish', 'Spanish'),
        ('french', 'French'),
        ('german', 'German'),
        ('italian', 'Italian'),
        ('portuguese', 'Portuguese'),
        ('russian', 'Russian'),
        ('chinese_mandarin', 'Chinese (Mandarin)'),
        ('chinese_cantonese', 'Chinese (Cantonese)'),
        ('japanese', 'Japanese'),
        ('korean', 'Korean'),
        ('arabic', 'Arabic'),
        ('hindi', 'Hindi'),
        ('bengali', 'Bengali'),
        ('punjabi', 'Punjabi'),
        ('urdu', 'Urdu'),
        ('turkish', 'Turkish'),
        ('persian', 'Persian (Farsi)'),
        ('hebrew', 'Hebrew'),
        
        # European Languages
        ('dutch', 'Dutch'),
        ('swedish', 'Swedish'),
        ('norwegian', 'Norwegian'),
        ('danish', 'Danish'),
        ('finnish', 'Finnish'),
        ('polish', 'Polish'),
        ('czech', 'Czech'),
        ('slovak', 'Slovak'),
        ('hungarian', 'Hungarian'),
        ('romanian', 'Romanian'),
        ('bulgarian', 'Bulgarian'),
        ('greek', 'Greek'),
        ('serbian', 'Serbian'),
        ('croatian', 'Croatian'),
        ('bosnian', 'Bosnian'),
        ('slovenian', 'Slovenian'),
        ('albanian', 'Albanian'),
        ('macedonian', 'Macedonian'),
        ('ukrainian', 'Ukrainian'),
        ('belarusian', 'Belarusian'),
        ('lithuanian', 'Lithuanian'),
        ('latvian', 'Latvian'),
        ('estonian', 'Estonian'),
        ('icelandic', 'Icelandic'),
        ('irish', 'Irish'),
        ('scottish_gaelic', 'Scottish Gaelic'),
        ('welsh', 'Welsh'),
        ('catalan', 'Catalan'),
        ('basque', 'Basque'),
        ('galician', 'Galician'),
        
        # Asian Languages
        ('thai', 'Thai'),
        ('vietnamese', 'Vietnamese'),
        ('indonesian', 'Indonesian'),
        ('malay', 'Malay'),
        ('filipino', 'Filipino (Tagalog)'),
        ('burmese', 'Burmese'),
        ('khmer', 'Khmer'),
        ('lao', 'Lao'),
        ('tibetan', 'Tibetan'),
        ('nepali', 'Nepali'),
        ('sinhala', 'Sinhala'),
        ('tamil', 'Tamil'),
        ('telugu', 'Telugu'),
        ('kannada', 'Kannada'),
        ('malayalam', 'Malayalam'),
        ('marathi', 'Marathi'),
        ('gujarati', 'Gujarati'),
        ('oriya', 'Oriya'),
        ('assamese', 'Assamese'),
        ('sanskrit', 'Sanskrit'),
        
        # Middle Eastern & Central Asian Languages
        ('pashto', 'Pashto'),
        ('dari', 'Dari'),
        ('kurdish', 'Kurdish'),
        ('armenian', 'Armenian'),
        ('georgian', 'Georgian'),
        ('azerbaijani', 'Azerbaijani'),
        ('kazakh', 'Kazakh'),
        ('kyrgyz', 'Kyrgyz'),
        ('tajik', 'Tajik'),
        ('turkmen', 'Turkmen'),
        ('uzbek', 'Uzbek'),
        
        # African Languages
        ('swahili', 'Swahili'),
        ('hausa', 'Hausa'),
        ('yoruba', 'Yoruba'),
        ('igbo', 'Igbo'),
        ('amharic', 'Amharic'),
        ('somali', 'Somali'),
        ('zulu', 'Zulu'),
        ('xhosa', 'Xhosa'),
        ('afrikaans', 'Afrikaans'),
        ('arabic_egyptian', 'Egyptian Arabic'),
        ('arabic_moroccan', 'Moroccan Arabic'),
        ('arabic_saudi', 'Saudi Arabic'),
        ('arabic_levantine', 'Levantine Arabic'),
        
        # American Languages
        ('quechua', 'Quechua'),
        ('guarani', 'Guarani'),
        ('maya', 'Maya'),
        ('navajo', 'Navajo'),
        ('inuit', 'Inuit'),
        
        # Pacific Languages
        ('hawaiian', 'Hawaiian'),
        ('maori', 'Maori'),
        ('fijian', 'Fijian'),
        ('samoan', 'Samoan'),
        ('tongan', 'Tongan'),
        
        # Sign Languages
        ('sign_language_american', 'American Sign Language (ASL)'),
        ('sign_language_british', 'British Sign Language (BSL)'),
        ('sign_language_international', 'International Sign Language'),
    ]

    FITNESS_LEVELS = [
        ('easy', 'Easy - No fitness required'),
        ('moderate', 'Moderate - Some fitness required'),
        ('challenging', 'Challenging - Good fitness required'),
        ('difficult', 'Difficult - Excellent fitness required'),
    ]

    CANCELLATION_POLICIES = [
        ('flexible', 'Flexible - Free cancellation 24 hours before'),
        ('moderate', 'Moderate - Free cancellation 48 hours before'),
        ('strict', 'Strict - 50% refund up to 7 days before'),
    ]

    # Host/Guide Information
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tours')
    host_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    certifications = models.CharField(max_length=300, blank=True, null=True)

    # Tour Basic Info
    tour_name = models.CharField(max_length=200)
    tour_category = models.CharField(max_length=50, choices=TOUR_CATEGORIES)
    duration = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    languages = models.CharField(max_length=200)

    # Capacity
    min_participants = models.IntegerField()
    max_participants = models.IntegerField()
    age_restrictions = models.CharField(max_length=100, blank=True, null=True)

    # Description & Itinerary
    tagline = models.CharField(max_length=150)
    full_description = models.TextField()
    itinerary = models.TextField()
    meeting_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255, blank=True, null=True)
    highlights = models.TextField(blank=True, null=True)

    # Inclusions/Exclusions (stored as JSON or comma-separated)
    inclusions = models.CharField(max_length=500, blank=True, null=True)
    exclusions = models.TextField(blank=True, null=True)

    # Safety & Policies
    fitness_level = models.CharField(max_length=50, choices=FITNESS_LEVELS)
    safety_gear = models.TextField(blank=True, null=True)
    cancellation_policy = models.CharField(max_length=50, choices=CANCELLATION_POLICIES)

    # Pricing
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    group_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    child_discount = models.IntegerField(blank=True, null=True, help_text="Discount percentage for children")
    currency = models.CharField(max_length=10, default='USD')

    # Status
    is_published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tour_name} - {self.city}, {self.country}"

    class Meta:
        ordering = ['-created_at']


class TourPhoto(models.Model):
    """Photos for tour listings"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='tours/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.tour.tour_name}"

    class Meta:
        ordering = ['order', '-uploaded_at']


class AccommodationInventory(models.Model):
    """Daily inventory for accommodation availability, pricing, and rules"""
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='inventory')
    date = models.DateField()
    
    # Availability
    is_available = models.BooleanField(default=True)
    min_stay = models.IntegerField(default=1, help_text="Minimum nights required")
    max_stay = models.IntegerField(blank=True, null=True, help_text="Maximum nights allowed")
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weekend_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    seasonal_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    
    # Booking rules
    advance_booking_days = models.IntegerField(default=0, help_text="Days in advance required for booking")
    same_day_booking = models.BooleanField(default=True)
    instant_book = models.BooleanField(default=True)
    
    # Status
    is_blocked = models.BooleanField(default=False, help_text="Manually blocked by host")
    block_reason = models.CharField(max_length=200, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['accommodation', 'date']
        ordering = ['date']
        indexes = [
            models.Index(fields=['accommodation', 'date']),
            models.Index(fields=['date', 'is_available']),
        ]

    def __str__(self):
        return f"{self.accommodation.property_name} - {self.date}"

    def get_effective_price(self):
        """Calculate the effective price with seasonal multiplier"""
        base = self.base_price or self.accommodation.base_price
        return base * self.seasonal_multiplier


class TourInventory(models.Model):
    """Daily inventory for tour availability, pricing, and capacity"""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='inventory')
    date = models.DateField()
    time_slot = models.TimeField(blank=True, null=True, help_text="Specific time for tour")
    
    # Capacity
    total_capacity = models.IntegerField(help_text="Total participants allowed")
    available_spots = models.IntegerField(help_text="Currently available spots")
    min_participants = models.IntegerField(default=1)
    
    # Pricing
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    group_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    seasonal_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    
    # Availability
    is_available = models.BooleanField(default=True)
    advance_booking_hours = models.IntegerField(default=24, help_text="Hours in advance required")
    
    # Status
    is_blocked = models.BooleanField(default=False)
    block_reason = models.CharField(max_length=200, blank=True, null=True)
    
    # Weather dependent
    weather_dependent = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['tour', 'date', 'time_slot']
        ordering = ['date', 'time_slot']
        indexes = [
            models.Index(fields=['tour', 'date']),
            models.Index(fields=['date', 'is_available']),
        ]

    def __str__(self):
        time_str = f" at {self.time_slot}" if self.time_slot else ""
        return f"{self.tour.tour_name} - {self.date}{time_str}"

    def get_effective_price(self):
        """Calculate the effective price with seasonal multiplier"""
        base = self.price_per_person or self.tour.price_per_person
        return base * self.seasonal_multiplier

    def is_fully_booked(self):
        """Check if tour is fully booked"""
        return self.available_spots <= 0


class SeasonalRate(models.Model):
    """Seasonal pricing rules for accommodations and tours"""
    RATE_TYPES = [
        ('accommodation', 'Accommodation'),
        ('tour', 'Tour'),
    ]
    
    name = models.CharField(max_length=100, help_text="e.g., Summer Season, Christmas Week")
    rate_type = models.CharField(max_length=20, choices=RATE_TYPES)
    
    # Date range
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Rate adjustments
    price_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    fixed_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Rules
    min_stay = models.IntegerField(blank=True, null=True)
    is_blackout = models.BooleanField(default=False, help_text="Complete blackout period")
    
    # Applicable to specific properties
    accommodations = models.ManyToManyField(Accommodation, blank=True)
    tours = models.ManyToManyField(Tour, blank=True)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"


class RecurringRule(models.Model):
    """Recurring rules for availability and pricing"""
    RULE_TYPES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'), 
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    name = models.CharField(max_length=100)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    
    # Weekly rules
    weekdays = models.JSONField(blank=True, null=True, help_text="List of weekday numbers (0=Monday)")
    
    # Date range for rule application
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    # Rule settings
    is_available = models.BooleanField(default=True)
    price_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    min_stay = models.IntegerField(blank=True, null=True)
    
    # Applicable to
    accommodations = models.ManyToManyField(Accommodation, blank=True)
    tours = models.ManyToManyField(Tour, blank=True)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.name} ({self.rule_type})"


# Multi-Room Type Calendar Models

class Listing(models.Model):
    """Generic listing model for accommodations and tours with multi-room support"""
    LISTING_TYPES = [
        ('accommodation', 'Accommodation'),
        ('tour', 'Tour'),
    ]

    CURRENCIES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('CAD', 'Canadian Dollar'),
        ('AUD', 'Australian Dollar'),
        ('CHF', 'Swiss Franc'),
        ('CNY', 'Chinese Yuan'),
        ('SEK', 'Swedish Krona'),
        ('NZD', 'New Zealand Dollar'),
        ('MXN', 'Mexican Peso'),
        ('SGD', 'Singapore Dollar'),
        ('HKD', 'Hong Kong Dollar'),
        ('NOK', 'Norwegian Krone'),
        ('KRW', 'South Korean Won'),
        ('TRY', 'Turkish Lira'),
        ('RUB', 'Russian Ruble'),
        ('INR', 'Indian Rupee'),
        ('BRL', 'Brazilian Real'),
        ('ZAR', 'South African Rand'),
    ]

    # Basic Info
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    name = models.CharField(max_length=200)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES)

    # Location & Timezone
    timezone = models.CharField(max_length=50, default='UTC')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # Currency & Default Pricing
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='USD')
    default_price = models.DecimalField(max_digits=10, decimal_places=2)
    default_min_stay = models.IntegerField(default=1)

    # Status
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.listing_type})"

    def get_timezone_obj(self):
        """Get pytz timezone object"""
        try:
            return pytz.timezone(self.timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            return pytz.UTC


class RoomType(models.Model):
    """Room types within a listing (e.g., Standard Room, Deluxe Suite)"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_units = models.IntegerField(help_text="How many physical units exist of this room type")

    # Status
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['listing', 'name']
        ordering = ['name']

    def __str__(self):
        return f"{self.listing.name} - {self.name}"

    def clean(self):
        if self.total_units < 1:
            raise ValidationError("Total units must be at least 1")


class AvailabilityDay(models.Model):
    """Per-listing per-date availability and pricing overrides"""
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
        ('BLOCKED', 'Blocked'),
    ]

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='availability_days')
    date = models.DateField()

    # Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')

    # Pricing overrides (optional)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                               help_text="Override default price for this day")
    min_stay = models.IntegerField(blank=True, null=True,
                                  help_text="Override default min stay for this day")

    # Notes
    notes = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['listing', 'date']
        ordering = ['date']
        indexes = [
            models.Index(fields=['listing', 'date']),
            models.Index(fields=['date', 'status']),
        ]

    def __str__(self):
        return f"{self.listing.name} - {self.date} ({self.status})"

    def get_effective_price(self):
        """Get the effective price for this day"""
        return self.price if self.price is not None else self.listing.default_price

    def get_effective_min_stay(self):
        """Get the effective minimum stay for this day"""
        return self.min_stay if self.min_stay is not None else self.listing.default_min_stay


class DayRoomInventory(models.Model):
    """Per-listing per-room-type per-date inventory management"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    date = models.DateField()

    # Inventory
    units_open = models.IntegerField(help_text="How many units are offered for sale that day")
    units_booked = models.IntegerField(default=0, help_text="Units currently booked (read-only/derived)")

    # Restrictions
    stop_sell = models.BooleanField(default=False, help_text="True means do not accept bookings")
    cta = models.BooleanField(default=False, help_text="Close-to-arrival restriction")
    ctd = models.BooleanField(default=False, help_text="Close-to-departure restriction")

    # Price override per room type
    override_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Notes
    note = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['listing', 'room_type', 'date']
        ordering = ['date', 'room_type__name']
        indexes = [
            models.Index(fields=['listing', 'date']),
            models.Index(fields=['room_type', 'date']),
            models.Index(fields=['date', 'stop_sell']),
        ]

    def __str__(self):
        return f"{self.listing.name} - {self.room_type.name} - {self.date}"

    def clean(self):
        """Validate inventory constraints"""
        if self.units_open < 0:
            raise ValidationError("Units open cannot be negative")

        if self.units_open > self.room_type.total_units:
            raise ValidationError(f"Units open ({self.units_open}) cannot exceed total units ({self.room_type.total_units})")

        if self.units_booked < 0:
            raise ValidationError("Units booked cannot be negative")

        if self.units_booked > self.units_open:
            raise ValidationError(f"Units booked ({self.units_booked}) cannot exceed units open ({self.units_open})")

        if self.override_price is not None and self.override_price < 0:
            raise ValidationError("Override price cannot be negative")

    @property
    def available(self):
        """Calculate available units"""
        if self.stop_sell:
            return 0
        return max(0, self.units_open - self.units_booked)

    def get_effective_price(self):
        """Get the effective price for this room type on this date"""
        return self.override_price if self.override_price is not None else self.room_type.base_price

    def is_bookable(self):
        """Check if this room type is bookable on this date"""
        # Check listing-level availability
        try:
            day_availability = AvailabilityDay.objects.get(listing=self.listing, date=self.date)
            if day_availability.status in ['CLOSED', 'BLOCKED']:
                return False
        except AvailabilityDay.DoesNotExist:
            pass  # Default to open

        # Check room-level availability
        return not self.stop_sell and self.available > 0
