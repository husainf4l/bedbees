from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytz
from slugify import slugify

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
        # Traditional Hotel Types
        ('hotel', 'Hotel'),
        ('boutique_hotel', 'Boutique Hotel'),
        ('business_hotel', 'Business Hotel'),
        ('luxury_hotel', 'Luxury Hotel'),
        ('resort_hotel', 'Resort Hotel'),
        ('spa_hotel', 'Spa Hotel'),
        ('casino_hotel', 'Casino Hotel'),
        ('airport_hotel', 'Airport Hotel'),
        ('extended_stay_hotel', 'Extended Stay Hotel'),
        ('eco_hotel', 'Eco Hotel'),
        ('heritage_hotel', 'Heritage Hotel'),
        ('floating_hotel', 'Floating Hotel'),
        
        # Apartment & Residential Types
        ('apartment', 'Apartment'),
        ('studio_apartment', 'Studio Apartment'),
        ('loft_apartment', 'Loft Apartment'),
        ('penthouse_apartment', 'Penthouse Apartment'),
        ('duplex_apartment', 'Duplex Apartment'),
        ('triplex_apartment', 'Triplex Apartment'),
        ('serviced_apartment', 'Serviced Apartment'),
        ('corporate_apartment', 'Corporate Apartment'),
        
        # Villa & House Types
        ('villa', 'Villa'),
        ('private_villa', 'Private Villa'),
        ('beach_villa', 'Beach Villa'),
        ('mountain_villa', 'Mountain Villa'),
        ('luxury_villa', 'Luxury Villa'),
        ('traditional_house', 'Traditional House'),
        ('modern_house', 'Modern House'),
        ('townhouse', 'Townhouse'),
        ('cottage', 'Cottage'),
        ('bungalow', 'Bungalow'),
        ('chalet', 'Chalet'),
        ('cabin', 'Cabin'),
        ('farmhouse', 'Farmhouse'),
        ('manor_house', 'Manor House'),
        ('castle', 'Castle'),
        ('palace', 'Palace'),
        ('mansion', 'Mansion'),
        ('estate', 'Estate'),
        
        # Resort & Leisure Types
        ('resort', 'Resort'),
        ('beach_resort', 'Beach Resort'),
        ('mountain_resort', 'Mountain Resort'),
        ('spa_resort', 'Spa Resort'),
        ('golf_resort', 'Golf Resort'),
        ('ski_resort', 'Ski Resort'),
        ('desert_resort', 'Desert Resort'),
        ('island_resort', 'Island Resort'),
        ('all_inclusive_resort', 'All-Inclusive Resort'),
        ('family_resort', 'Family Resort'),
        ('adult_only_resort', 'Adult-Only Resort'),
        
        # Budget & Alternative Types
        ('hostel', 'Hostel'),
        ('guesthouse', 'Guesthouse'),
        ('bed_breakfast', 'Bed & Breakfast'),
        ('homestay', 'Homestay'),
        ('farm_stay', 'Farm Stay'),
        ('treehouse', 'Treehouse'),
        ('yurt', 'Yurt'),
        ('cave_hotel', 'Cave Hotel'),
        ('ice_hotel', 'Ice Hotel'),
        ('underwater_hotel', 'Underwater Hotel'),
        ('capsule_hotel', 'Capsule Hotel'),
        ('micro_hotel', 'Micro Hotel'),
        
        # Unique & Specialty Types
        ('boutique', 'Boutique Property'),
        ('art_hotel', 'Art Hotel'),
        ('design_hotel', 'Design Hotel'),
        ('historic_inn', 'Historic Inn'),
        ('monastery_retreat', 'Monastery Retreat'),
        ('desert_camp', 'Desert Camp'),
        ('safari_lodge', 'Safari Lodge'),
        ('rainforest_lodge', 'Rainforest Lodge'),
        ('arctic_lodge', 'Arctic Lodge'),
        ('volcano_lodge', 'Volcano Lodge'),
        ('glacier_lodge', 'Glacier Lodge'),
        ('coral_reef_resort', 'Coral Reef Resort'),
        
        # Commercial & Business Types
        ('business_center', 'Business Center'),
        ('conference_center', 'Conference Center'),
        ('convention_hotel', 'Convention Hotel'),
        ('executive_suite', 'Executive Suite'),
        ('meeting_facility', 'Meeting Facility'),
        
        # Specialized Types
        ('medical_retreat', 'Medical Retreat'),
        ('wellness_center', 'Wellness Center'),
        ('yoga_retreat', 'Yoga Retreat'),
        ('meditation_center', 'Meditation Center'),
        ('artists_residence', 'Artists Residence'),
        ('writers_retreat', 'Writers Retreat'),
        ('film_location', 'Film Location Property'),
        ('photography_studio', 'Photography Studio'),
        ('music_studio', 'Music Studio'),
        ('art_studio', 'Art Studio'),
        
        # Transportation Hubs
        ('airport_lounge', 'Airport Lounge'),
        ('train_station_hotel', 'Train Station Hotel'),
        ('port_hotel', 'Port Hotel'),
        ('highway_hotel', 'Highway Hotel'),
        
        # Cultural & Religious Types
        ('pilgrimage_center', 'Pilgrimage Center'),
        ('religious_retreat', 'Religious Retreat'),
        ('cultural_center', 'Cultural Center'),
        ('museum_hotel', 'Museum Hotel'),
        ('historic_site', 'Historic Site Accommodation'),
        
        # Educational Types
        ('university_housing', 'University Housing'),
        ('student_residence', 'Student Residence'),
        ('research_facility', 'Research Facility'),
        ('conference_accommodation', 'Conference Accommodation'),
        
        # Emergency & Temporary Types
        ('emergency_shelter', 'Emergency Shelter'),
        ('disaster_relief_housing', 'Disaster Relief Housing'),
        ('temporary_housing', 'Temporary Housing'),
        ('relocation_housing', 'Relocation Housing'),
        
        # Other Specialty Types
        ('floating_home', 'Floating Home'),
        ('houseboat', 'Houseboat'),
        ('campervan', 'Campervan'),
        ('rv_park', 'RV Park'),
        ('glamping_site', 'Glamping Site'),
        ('tiny_house', 'Tiny House'),
        ('shipping_container_home', 'Shipping Container Home'),
        ('earthship', 'Earthship'),
        ('dome_home', 'Dome Home'),
        ('underground_home', 'Underground Home'),
    ]

    BED_TYPES = [
        # Standard Bed Types
        ('single', 'Single Bed (90cm x 190cm)'),
        ('twin', 'Twin Beds (2x 90cm x 190cm)'),
        ('double', 'Double Bed (135cm x 190cm)'),
        ('full', 'Full Bed (135cm x 190cm)'),
        ('queen', 'Queen Bed (150cm x 200cm)'),
        ('king', 'King Bed (180cm x 200cm)'),
        ('california_king', 'California King (183cm x 213cm)'),
        ('super_king', 'Super King (183cm x 213cm)'),
        ('emperor', 'Emperor Bed (200cm x 200cm)'),
        
        # Specialty Beds
        ('bunk', 'Bunk Bed'),
        ('triple_bunk', 'Triple Bunk Bed'),
        ('loft_bed', 'Loft Bed'),
        ('platform_bed', 'Platform Bed'),
        ('canopy_bed', 'Canopy Bed'),
        ('four_poster_bed', 'Four-Poster Bed'),
        ('day_bed', 'Day Bed'),
        ('sofa_bed', 'Sofa Bed / Pull-out Sofa'),
        ('futon', 'Futon'),
        ('tatami_mat', 'Tatami Mat'),
        ('waterbed', 'Waterbed'),
        ('air_mattress', 'Air Mattress'),
        ('inflatable_bed', 'Inflatable Bed'),
        ('hammock', 'Hammock'),
        
        # Luxury Beds
        ('luxury_memory_foam', 'Luxury Memory Foam Bed'),
        ('luxury_hybrid', 'Luxury Hybrid Bed'),
        ('luxury_latex', 'Luxury Latex Bed'),
        ('luxury_down_filled', 'Luxury Down-Filled Bed'),
        ('luxury_silk', 'Luxury Silk Bed'),
        ('luxury_temp_control', 'Luxury Temperature Control Bed'),
        
        # Specialty Sleep Systems
        ('capsule_bed', 'Capsule Bed'),
        ('pod_bed', 'Sleep Pod'),
        ('zero_gravity_bed', 'Zero Gravity Bed'),
        ('adjustable_bed', 'Adjustable Bed'),
        ('massage_bed', 'Massage Bed'),
        ('heated_bed', 'Heated Bed'),
        ('cooling_bed', 'Cooling Bed'),
        
        # Cultural & Traditional Beds
        ('japanese_futon', 'Japanese Futon'),
        ('korean_ondol', 'Korean Ondol Bed'),
        ('indian_charpoy', 'Indian Charpoy'),
        ('moroccan_bed', 'Moroccan Platform Bed'),
        ('african_bed', 'African Rope Bed'),
        ('balinese_bed', 'Balinese Daybed'),
        
        # Medical & Accessibility Beds
        ('hospital_bed', 'Hospital Bed'),
        ('accessible_bed', 'Accessible Bed'),
        ('bariatric_bed', 'Bariatric Bed'),
        ('therapeutic_bed', 'Therapeutic Bed'),
        
        # Unique Beds
        ('treehouse_bed', 'Treehouse Bed'),
        ('boat_bed', 'Boat Bed'),
        ('cave_bed', 'Cave Bed'),
        ('ice_bed', 'Ice Bed'),
        ('sand_bed', 'Sand Bed'),
        ('floating_bed', 'Floating Bed'),
        
        # Mixed Configurations
        ('mixed', 'Mixed Types'),
        ('custom_configuration', 'Custom Configuration'),
        ('modular_beds', 'Modular Beds'),
        ('convertible_spaces', 'Convertible Spaces'),
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
        ('telephone', 'Telephone'),
        ('alarm_clock', 'Alarm Clock'),
        ('clock_radio', 'Clock Radio'),
        
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
        ('food_processor', 'Food Processor'),
        ('rice_cooker', 'Rice Cooker'),
        ('slow_cooker', 'Slow Cooker'),
        ('pressure_cooker', 'Pressure Cooker'),
        ('dining_area', 'Dining Area'),
        ('utensils', 'Cooking Utensils'),
        ('dishes', 'Dishes & Silverware'),
        ('glassware', 'Glassware'),
        ('cutlery', 'Cutlery Set'),
        ('pots_pans', 'Pots & Pans'),
        ('baking_sheets', 'Baking Sheets'),
        ('mixing_bowls', 'Mixing Bowls'),
        ('kitchen_island', 'Kitchen Island'),
        ('bar_counter', 'Bar Counter'),
        ('wine_cooler', 'Wine Cooler'),
        ('ice_machine', 'Ice Machine'),
        
        # Bathroom
        ('private_bathroom', 'Private Bathroom'),
        ('shared_bathroom', 'Shared Bathroom'),
        ('ensuite_bathroom', 'Ensuite Bathroom'),
        ('bathtub', 'Bathtub'),
        ('shower', 'Shower'),
        ('rainfall_shower', 'Rainfall Shower'),
        ('steam_shower', 'Steam Shower'),
        ('bidet', 'Bidet'),
        ('hair_dryer', 'Hair Dryer'),
        ('shampoo', 'Shampoo'),
        ('body_soap', 'Body Soap'),
        ('conditioner', 'Conditioner'),
        ('body_lotion', 'Body Lotion'),
        ('bath_robes', 'Bath Robes'),
        ('slippers', 'Slippers'),
        ('towels', 'Towels'),
        ('beach_towels', 'Beach Towels'),
        ('hand_towels', 'Hand Towels'),
        ('washcloths', 'Washcloths'),
        ('linens', 'Bed Linens'),
        ('bathroom_scales', 'Bathroom Scales'),
        ('toiletries', 'Basic Toiletries'),
        ('cosmetics_mirror', 'Cosmetics Mirror'),
        ('vanity_area', 'Vanity Area'),
        
        # Bedroom & Laundry
        ('bed_linen', 'Bed Linens'),
        ('extra_pillows', 'Extra Pillows'),
        ('blankets', 'Blankets'),
        ('duvet', 'Duvet/Comforter'),
        ('quilt', 'Quilt'),
        ('mattress_topper', 'Mattress Topper'),
        ('wardrobe', 'Wardrobe/Closet'),
        ('dresser', 'Dresser'),
        ('nightstands', 'Nightstands'),
        ('bedside_lamps', 'Bedside Lamps'),
        ('reading_lights', 'Reading Lights'),
        ('full_length_mirror', 'Full-Length Mirror'),
        ('hangers', 'Hangers'),
        ('laundry_bag', 'Laundry Bag'),
        ('washing_machine', 'Washing Machine'),
        ('dryer', 'Dryer'),
        ('ironing_facilities', 'Ironing Facilities'),
        ('iron', 'Iron'),
        ('ironing_board', 'Ironing Board'),
        ('steam_iron', 'Steam Iron'),
        ('laundry_detergent', 'Laundry Detergent'),
        ('fabric_softener', 'Fabric Softener'),
        ('drying_rack', 'Drying Rack'),
        
        # Outdoor & View
        ('balcony', 'Balcony'),
        ('terrace', 'Terrace'),
        ('patio', 'Patio'),
        ('deck', 'Deck'),
        ('veranda', 'Veranda'),
        ('garden', 'Garden'),
        ('private_garden', 'Private Garden'),
        ('rooftop_access', 'Rooftop Access'),
        ('outdoor_furniture', 'Outdoor Furniture'),
        ('sun_loungers', 'Sun Loungers'),
        ('beach_chairs', 'Beach Chairs'),
        ('umbrella', 'Umbrella'),
        ('outdoor_dining', 'Outdoor Dining Area'),
        ('barbecue', 'Barbecue/Grill'),
        ('fire_pit', 'Fire Pit'),
        ('outdoor_fireplace', 'Outdoor Fireplace'),
        ('pool', 'Swimming Pool'),
        ('heated_pool', 'Heated Pool'),
        ('infinity_pool', 'Infinity Pool'),
        ('plunge_pool', 'Plunge Pool'),
        ('pool_toys', 'Pool Toys'),
        ('pool_towels', 'Pool Towels'),
        ('hot_tub', 'Hot Tub/Jacuzzi'),
        ('sauna', 'Sauna'),
        ('steam_room', 'Steam Room'),
        ('turkish_bath', 'Turkish Bath'),
        ('cold_plunge', 'Cold Plunge'),
        ('mountain_view', 'Mountain View'),
        ('ocean_view', 'Ocean View'),
        ('sea_view', 'Sea View'),
        ('lake_view', 'Lake View'),
        ('river_view', 'River View'),
        ('city_view', 'City View'),
        ('garden_view', 'Garden View'),
        ('forest_view', 'Forest View'),
        ('desert_view', 'Desert View'),
        ('valley_view', 'Valley View'),
        ('sunrise_view', 'Sunrise View'),
        ('sunset_view', 'Sunset View'),
        
        # Safety & Security
        ('smoke_detector', 'Smoke Detector'),
        ('carbon_monoxide_detector', 'Carbon Monoxide Detector'),
        ('fire_extinguisher', 'Fire Extinguisher'),
        ('first_aid_kit', 'First Aid Kit'),
        ('emergency_kit', 'Emergency Kit'),
        ('security_cameras', 'Security Cameras'),
        ('motion_sensor_lights', 'Motion Sensor Lights'),
        ('safe', 'Safe'),
        ('digital_safe', 'Digital Safe'),
        ('lock_on_bedroom_door', 'Lock on Bedroom Door'),
        ('master_key_access', 'Master Key Access'),
        ('keycard_access', 'Keycard Access'),
        ('biometric_access', 'Biometric Access'),
        ('smart_lock', 'Smart Lock'),
        ('doorman', 'Doorman'),
        ('24_hour_security', '24-Hour Security'),
        ('security_guard', 'Security Guard'),
        ('cctv', 'CCTV Surveillance'),
        ('alarm_system', 'Alarm System'),
        ('panic_button', 'Panic Button'),
        ('emergency_contacts', 'Emergency Contact Numbers'),
        
        # Accessibility Features
        ('wheelchair_accessible', 'Wheelchair Accessible'),
        ('wheelchair_rental', 'Wheelchair Rental Available'),
        ('ramp_access', 'Ramp Access'),
        ('ground_floor_access', 'Ground Floor Access'),
        ('elevator', 'Elevator'),
        ('wide_elevator', 'Wide Elevator'),
        ('stair_lift', 'Stair Lift'),
        ('stair_gates', 'Stair Gates'),
        ('wide_doorways', 'Wide Doorways (36"+)'),
        ('wide_hallways', 'Wide Hallways'),
        ('zero_step_entry', 'Zero-Step Entry'),
        ('accessible_bathroom', 'Accessible Bathroom'),
        ('roll_in_shower', 'Roll-in Shower'),
        ('shower_seat', 'Shower Seat'),
        ('grab_bars', 'Grab Bars'),
        ('raised_toilet', 'Raised Toilet'),
        ('accessible_sink', 'Accessible Sink'),
        ('braille_signage', 'Braille Signage'),
        ('tactile_signage', 'Tactile Signage'),
        ('audio_guides', 'Audio Guides'),
        ('visual_alerts', 'Visual Fire/Smoke Alerts'),
        ('hearing_loop', 'Hearing Loop System'),
        ('accessible_parking', 'Accessible Parking'),
        ('van_accessible', 'Van Accessible'),
        ('service_animal_friendly', 'Service Animal Friendly'),
        ('accessible_kitchen', 'Accessible Kitchen'),
        ('height_adjustable_counter', 'Height-Adjustable Counter'),
        ('lowered_shelves', 'Lowered Shelves'),
        ('easy_reach_items', 'Easy-Reach Storage'),
        ('accessible_laundry', 'Accessible Laundry Facilities'),
        ('accessible_pool', 'Accessible Pool'),
        ('pool_lift', 'Pool Lift'),
        ('accessible_hot_tub', 'Accessible Hot Tub'),
        ('beach_wheelchair', 'Beach Wheelchair'),
        ('accessible_transport', 'Accessible Transport Available'),
        
        # Entertainment
        ('books', 'Books & Reading Material'),
        ('magazines', 'Magazines'),
        ('newspapers', 'Newspapers'),
        ('board_games', 'Board Games'),
        ('card_games', 'Card Games'),
        ('puzzles', 'Puzzles'),
        ('chess_set', 'Chess Set'),
        ('backgammon', 'Backgammon'),
        ('piano', 'Piano'),
        ('guitar', 'Guitar'),
        ('ukulele', 'Ukulele'),
        ('drums', 'Drums'),
        ('violin', 'Violin'),
        ('flute', 'Flute'),
        ('harmonica', 'Harmonica'),
        ('karaoke_system', 'Karaoke System'),
        ('game_console', 'Game Console'),
        ('arcade_games', 'Arcade Games'),
        ('pinball_machine', 'Pinball Machine'),
        ('pool_table', 'Pool Table'),
        ('foosball', 'Foosball'),
        ('dartboard', 'Dartboard'),
        ('projector', 'Projector'),
        ('projection_screen', 'Projection Screen'),
        ('home_theater', 'Home Theater System'),
        ('surround_sound', 'Surround Sound'),
        ('blu_ray_player', 'Blu-ray Player'),
        ('dvd_player', 'DVD Player'),
        ('streaming_devices', 'Streaming Devices'),
        ('smart_tv', 'Smart TV'),
        ('satellite_tv', 'Satellite TV'),
        ('international_channels', 'International Channels'),
        ('movie_library', 'Movie Library'),
        ('music_library', 'Music Library'),
        
        # Business & Work
        ('workspace', 'Dedicated Workspace'),
        ('desk', 'Desk'),
        ('office_chair', 'Office Chair'),
        ('ergonomic_chair', 'Ergonomic Chair'),
        ('standing_desk', 'Standing Desk'),
        ('computer', 'Computer'),
        ('laptop', 'Laptop'),
        ('printer', 'Printer'),
        ('scanner', 'Scanner'),
        ('fax_machine', 'Fax Machine'),
        ('photocopier', 'Photocopier'),
        ('high_speed_internet', 'High-Speed Internet'),
        ('ethernet_cables', 'Ethernet Cables'),
        ('usb_ports', 'USB Ports'),
        ('power_outlets', 'Power Outlets'),
        ('extension_cords', 'Extension Cords'),
        ('surge_protectors', 'Surge Protectors'),
        ('webcam', 'Webcam'),
        ('microphone', 'Microphone'),
        ('headphones', 'Headphones'),
        ('speakers', 'Speakers'),
        ('video_conferencing', 'Video Conferencing Setup'),
        ('whiteboard', 'Whiteboard'),
        ('flipchart', 'Flipchart'),
        ('presentation_remote', 'Presentation Remote'),
        
        # Family & Kids
        ('crib', 'Crib'),
        ('bassinet', 'Bassinet'),
        ('portable_crib', 'Portable Crib'),
        ('toddler_bed', 'Toddler Bed'),
        ('high_chair', 'High Chair'),
        ('booster_seat', 'Booster Seat'),
        ('childrens_plates', 'Children\'s Plates & Utensils'),
        ('sippy_cups', 'Sippy Cups'),
        ('bibs', 'Bibs'),
        ('childrens_books', 'Children\'s Books'),
        ('educational_toys', 'Educational Toys'),
        ('building_blocks', 'Building Blocks'),
        ('puzzles', 'Children\'s Puzzles'),
        ('board_games_kids', 'Children\'s Board Games'),
        ('art_supplies', 'Art Supplies'),
        ('crayons', 'Crayons'),
        ('colored_pencils', 'Colored Pencils'),
        ('markers', 'Markers'),
        ('play_doh', 'Play-Doh'),
        ('toys', 'Toys'),
        ('stuffed_animals', 'Stuffed Animals'),
        ('dolls', 'Dolls'),
        ('action_figures', 'Action Figures'),
        ('lego', 'LEGO'),
        ('train_sets', 'Train Sets'),
        ('remote_control_toys', 'Remote Control Toys'),
        ('outdoor_toys', 'Outdoor Toys'),
        ('sandbox', 'Sandbox'),
        ('swing_set', 'Swing Set'),
        ('slide', 'Slide'),
        ('tricycle', 'Tricycle'),
        ('scooter', 'Scooter'),
        ('basketball_hoop', 'Basketball Hoop'),
        ('soccer_goals', 'Soccer Goals'),
        ('badminton_set', 'Badminton Set'),
        ('frisbee', 'Frisbee'),
        ('kite', 'Kite'),
        ('babysitter_recommendations', 'Babysitter Recommendations'),
        ('family_friendly', 'Family/Kid Friendly'),
        ('childcare_services', 'Childcare Services'),
        ('nanny_services', 'Nanny Services'),
        ('kids_club', 'Kids Club'),
        ('playroom', 'Playroom'),
        ('game_room', 'Game Room'),
        ('indoor_play_area', 'Indoor Play Area'),
        ('outdoor_play_area', 'Outdoor Play Area'),
        
        # Pets
        ('pet_friendly', 'Pet Friendly'),
        ('pet_bowls', 'Pet Bowls'),
        ('pet_food', 'Pet Food Available'),
        ('pet_treats', 'Pet Treats'),
        ('pet_toys', 'Pet Toys'),
        ('pet_bed', 'Pet Bed'),
        ('pet_blanket', 'Pet Blanket'),
        ('pet_crate', 'Pet Crate'),
        ('leash_hooks', 'Leash Hooks'),
        ('poop_bags', 'Poop Bags'),
        ('pet_waste_station', 'Pet Waste Station'),
        ('flea_treatment', 'Flea Treatment'),
        ('pet_grooming', 'Pet Grooming Services'),
        ('pet_sitting', 'Pet Sitting Services'),
        ('veterinarian_nearby', 'Veterinarian Nearby'),
        ('dog_park_nearby', 'Dog Park Nearby'),
        ('pet_walking', 'Pet Walking Services'),
        
        # Wellness & Spa
        ('gym', 'Gym'),
        ('fitness_equipment', 'Fitness Equipment'),
        ('treadmill', 'Treadmill'),
        ('exercise_bike', 'Exercise Bike'),
        ('elliptical', 'Elliptical'),
        ('weight_machine', 'Weight Machine'),
        ('free_weights', 'Free Weights'),
        ('resistance_bands', 'Resistance Bands'),
        ('yoga_mats', 'Yoga Mats'),
        ('meditation_cushions', 'Meditation Cushions'),
        ('meditation_space', 'Meditation Space'),
        ('prayer_room', 'Prayer Room'),
        ('chapel', 'Chapel'),
        ('spa_services', 'Spa Services'),
        ('massage_services', 'Massage Services'),
        ('aromatherapy', 'Aromatherapy'),
        ('essential_oils', 'Essential Oils'),
        ('incense', 'Incense'),
        ('candles', 'Candles'),
        ('salt_lamp', 'Salt Lamp'),
        ('crystal_collection', 'Crystal Collection'),
        ('sound_bath', 'Sound Bath Equipment'),
        ('reiki_crystals', 'Reiki Crystals'),
        ('acupressure_mat', 'Acupressure Mat'),
        ('foam_roller', 'Foam Roller'),
        ('massage_chair', 'Massage Chair'),
        ('infrared_sauna', 'Infrared Sauna'),
        ('cold_therapy', 'Cold Therapy Equipment'),
        ('herbal_tea', 'Herbal Tea Collection'),
        ('smoothie_maker', 'Smoothie Maker'),
        ('juicer', 'Juicer'),
        ('nutritional_supplements', 'Nutritional Supplements'),
        
        # Services
        ('housekeeping', 'Housekeeping'),
        ('daily_housekeeping', 'Daily Housekeeping'),
        ('concierge', 'Concierge Service'),
        ('personal_concierge', 'Personal Concierge'),
        ('butler_service', 'Butler Service'),
        ('room_service', 'Room Service'),
        ('24_hour_room_service', '24-Hour Room Service'),
        ('laundry_service', 'Laundry Service'),
        ('dry_cleaning', 'Dry Cleaning Service'),
        ('pressing_service', 'Pressing Service'),
        ('shoe_shine', 'Shoe Shine Service'),
        ('valet_service', 'Valet Service'),
        ('car_wash', 'Car Wash Service'),
        ('airport_shuttle', 'Airport Shuttle'),
        ('private_driver', 'Private Driver'),
        ('limousine_service', 'Limousine Service'),
        ('helicopter_service', 'Helicopter Service'),
        ('yacht_service', 'Yacht Service'),
        ('car_rental', 'Car Rental'),
        ('bicycle_rental', 'Bicycle Rental'),
        ('scooter_rental', 'Scooter Rental'),
        ('motorcycle_rental', 'Motorcycle Rental'),
        ('tour_desk', 'Tour Desk'),
        ('ticket_service', 'Ticket Service'),
        ('restaurant_reservations', 'Restaurant Reservations'),
        ('event_tickets', 'Event Tickets'),
        ('personal_shopper', 'Personal Shopper'),
        ('personal_trainer', 'Personal Trainer'),
        ('private_chef', 'Private Chef'),
        ('nutritionist', 'Nutritionist'),
        ('life_coach', 'Life Coach'),
        ('language_tutor', 'Language Tutor'),
        ('music_lessons', 'Music Lessons'),
        ('art_lessons', 'Art Lessons'),
        ('cooking_classes', 'Cooking Classes'),
        ('wine_tasting', 'Wine Tasting'),
        ('mixology_classes', 'Mixology Classes'),
        
        # Transportation & Local Services
        ('public_transport', 'Public Transport Access'),
        ('metro_access', 'Metro Access'),
        ('bus_stop', 'Bus Stop Nearby'),
        ('taxi_stand', 'Taxi Stand'),
        ('ride_sharing', 'Ride Sharing Pickup'),
        ('bike_shares', 'Bike Shares'),
        ('scooter_shares', 'Scooter Shares'),
        ('car_shares', 'Car Shares'),
        ('parking_garage', 'Parking Garage'),
        ('valet_parking', 'Valet Parking'),
        ('covered_parking', 'Covered Parking'),
        ('electric_vehicle_charging', 'Electric Vehicle Charging'),
        ('boat_dock', 'Boat Dock'),
        ('private_dock', 'Private Dock'),
        ('helicopter_pad', 'Hellicopter Pad'),
        
        # Communication & Technology
        ('high_speed_wifi', 'High-Speed WiFi'),
        ('fiber_internet', 'Fiber Internet'),
        ('smart_home_system', 'Smart Home System'),
        ('voice_assistant', 'Voice Assistant'),
        ('smart_locks', 'Smart Locks'),
        ('smart_thermostat', 'Smart Thermostat'),
        ('smart_lighting', 'Smart Lighting'),
        ('smart_blinds', 'Smart Blinds'),
        ('smart_security', 'Smart Security System'),
        ('smart_appliances', 'Smart Appliances'),
        ('robot_vacuum', 'Robot Vacuum'),
        ('smart_speaker', 'Smart Speaker'),
        ('tablet', 'Tablet Device'),
        ('smart_tv', 'Smart TV'),
        ('streaming_services', 'Streaming Services'),
        ('video_doorbell', 'Video Doorbell'),
        ('intercom_system', 'Intercom System'),
        ('baby_monitor', 'Baby Monitor'),
        ('security_monitor', 'Security Monitor'),
        
        # Food & Beverage
        ('minibar', 'Minibar'),
        ('fully_stocked_bar', 'Fully Stocked Bar'),
        ('wine_selection', 'Wine Selection'),
        ('champagne', 'Champagne'),
        ('cocktails', 'Cocktail Ingredients'),
        ('beer_selection', 'Beer Selection'),
        ('non_alcoholic_beverages', 'Non-Alcoholic Beverages'),
        ('fresh_juices', 'Fresh Juices'),
        ('smoothies', 'Smoothie Ingredients'),
        ('snacks', 'Snacks'),
        ('nuts', 'Nuts & Dried Fruits'),
        ('chocolates', 'Chocolates'),
        ('fresh_fruits', 'Fresh Fruits'),
        ('local_cheeses', 'Local Cheeses'),
        ('artisanal_breads', 'Artisanal Breads'),
        ('organic_products', 'Organic Products'),
        ('gluten_free_options', 'Gluten-Free Options'),
        ('vegan_options', 'Vegan Options'),
        ('halal_options', 'Halal Options'),
        ('kosher_options', 'Kosher Options'),
        ('dietary_restrictions', 'Accommodates Dietary Restrictions'),
        
        # Special Features
        ('smoking_allowed', 'Smoking Allowed'),
        ('designated_smoking_area', 'Designated Smoking Area'),
        ('vaping_allowed', 'Vaping Allowed'),
        ('events_allowed', 'Events Allowed'),
        ('wedding_venue', 'Wedding Venue'),
        ('party_facilities', 'Party Facilities'),
        ('conference_facilities', 'Conference Facilities'),
        ('photography_studio', 'Photography Studio'),
        ('art_studio', 'Art Studio'),
        ('music_studio', 'Music Studio'),
        ('dance_studio', 'Dance Studio'),
        ('yoga_studio', 'Yoga Studio'),
        ('meditation_center', 'Meditation Center'),
        ('library', 'Private Library'),
        ('observatory', 'Observatory'),
        ('telescope', 'Telescope'),
        ('planetarium', 'Planetarium'),
        ('indoor_pool', 'Indoor Pool'),
        ('indoor_tennis', 'Indoor Tennis Court'),
        ('indoor_basketball', 'Indoor Basketball Court'),
        ('indoor_soccer', 'Indoor Soccer Field'),
        ('bowling_alley', 'Bowling Alley'),
        ('movie_theater', 'Private Movie Theater'),
        ('concert_hall', 'Concert Hall'),
        ('art_gallery', 'Art Gallery'),
        ('museum', 'Private Museum'),
        ('wine_cellar', 'Wine Cellar'),
        ('cigar_lounge', 'Cigar Lounge'),
        ('whiskey_bar', 'Whiskey Bar'),
        ('cocktail_bar', 'Cocktail Bar'),
        ('beer_garden', 'Beer Garden'),
        ('tea_room', 'Tea Room'),
        ('coffee_lounge', 'Coffee Lounge'),
        
        # Sustainability & Eco-Friendly
        ('solar_power', 'Solar Power'),
        ('wind_power', 'Wind Power'),
        ('geothermal_heating', 'Geothermal Heating'),
        ('energy_efficient', 'Energy Efficient Appliances'),
        ('led_lighting', 'LED Lighting'),
        ('low_flow_fixtures', 'Low-Flow Fixtures'),
        ('water_recycling', 'Water Recycling'),
        ('composting', 'Composting Facilities'),
        ('recycling_program', 'Recycling Program'),
        ('organic_garden', 'Organic Garden'),
        ('permaculture', 'Permaculture Design'),
        ('green_certified', 'Green Certified'),
        ('carbon_neutral', 'Carbon Neutral'),
        ('eco_friendly_products', 'Eco-Friendly Products'),
        ('reusable_items', 'Reusable Items'),
        ('zero_waste', 'Zero Waste Initiative'),
        ('local_sourcing', 'Local Sourcing'),
        ('fair_trade', 'Fair Trade Products'),
        ('sustainable_fishing', 'Sustainable Fishing'),
        ('wildlife_protection', 'Wildlife Protection'),
        ('coral_reef_protection', 'Coral Reef Protection'),
        
        # Cultural & Local Experience
        ('local_art', 'Local Art Collection'),
        ('traditional_decor', 'Traditional Decor'),
        ('cultural_artifacts', 'Cultural Artifacts'),
        ('historical_documents', 'Historical Documents'),
        ('local_crafts', 'Local Crafts'),
        ('handmade_items', 'Handmade Items'),
        ('traditional_music', 'Traditional Music'),
        ('folk_instruments', 'Folk Instruments'),
        ('cultural_books', 'Cultural Books'),
        ('language_books', 'Language Learning Books'),
        ('local_history', 'Local History Materials'),
        ('indigenous_culture', 'Indigenous Culture Items'),
        ('religious_artifacts', 'Religious Artifacts'),
        ('spiritual_items', 'Spiritual Items'),
        ('meditation_aids', 'Meditation Aids'),
        ('prayer_beads', 'Prayer Beads'),
        ('incense_burner', 'Incense Burner'),
        ('altar_space', 'Altar Space'),
        
        # Emergency & Medical
        ('medical_kits', 'Medical Kits'),
        ('defibrillator', 'Defibrillator'),
        ('oxygen_tank', 'Oxygen Tank'),
        ('blood_pressure_monitor', 'Blood Pressure Monitor'),
        ('thermometer', 'Thermometer'),
        ('pulse_oximeter', 'Pulse Oximeter'),
        ('medication_storage', 'Medication Storage'),
        ('emergency_evacuation_plan', 'Emergency Evacuation Plan'),
        ('storm_shelter', 'Storm Shelter'),
        ('earthquake_kit', 'Earthquake Kit'),
        ('hurricane_supplies', 'Hurricane Supplies'),
        ('wildfire_kit', 'Wildfire Kit'),
        ('flood_protection', 'Flood Protection'),
        
        # Luxury & Premium Services
        ('private_jet_access', 'Private Jet Access'),
        ('yacht_charter', 'Yacht Charter'),
        ('helicopter_tours', 'Helicopter Tours'),
        ('submarine_tours', 'Submarine Tours'),
        ('hot_air_balloon', 'Hot Air Balloon'),
        ('private_concerts', 'Private Concerts'),
        ('celebrity_chef', 'Celebrity Chef'),
        ('personal_stylist', 'Personal Stylist'),
        ('beauty_services', 'Beauty Services'),
        ('hair_stylist', 'Hair Stylist'),
        ('makeup_artist', 'Makeup Artist'),
        ('personal_trainer', 'Personal Trainer'),
        ('yoga_instructor', 'Yoga Instructor'),
        ('meditation_teacher', 'Meditation Teacher'),
        ('life_coach', 'Life Coach'),
        ('business_consultant', 'Business Consultant'),
        ('legal_services', 'Legal Services'),
        ('financial_advisor', 'Financial Advisor'),
        
        # Other Amenities
        ('luggage_storage', 'Luggage Storage'),
        ('baggage_drop', '24-hour Check-in'),
        ('late_checkout', 'Late Checkout Available'),
        ('early_checkin', 'Early Check-in Available'),
        ('express_checkout', 'Express Checkout'),
        ('mobile_checkin', 'Mobile Check-in'),
        ('contactless_checkin', 'Contactless Check-in'),
        ('keyless_entry', 'Keyless Entry'),
        ('self_checkin', 'Self Check-in'),
        ('welcome_package', 'Welcome Package'),
        ('local_gifts', 'Local Gifts'),
        ('fresh_flowers', 'Fresh Flowers'),
        ('chocolate_covered_strawberries', 'Chocolate Covered Strawberries'),
        ('champagne_cooling', 'Champagne on Ice'),
        ('newspaper_delivery', 'Newspaper Delivery'),
        ('morning_briefing', 'Morning Briefing'),
        ('weather_reports', 'Weather Reports'),
        ('local_news', 'Local News Updates'),
        ('currency_exchange', 'Currency Exchange'),
        ('atm_access', 'ATM Access'),
        ('travel_insurance', 'Travel Insurance'),
        ('trip_cancellation_coverage', 'Trip Cancellation Coverage'),
        ('medical_emergency_coverage', 'Medical Emergency Coverage'),
        ('lost_luggage_protection', 'Lost Luggage Protection'),
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
        ('downtown', 'Downtown Location'),
        ('suburban', 'Suburban'),
        ('island_location', 'Island Location'),
        ('peninsula', 'Peninsula'),
        ('cliffside', 'Cliffside'),
        ('valley_location', 'Valley Location'),
        ('hilltop', 'Hilltop'),
        ('plateau', 'Plateau'),
        ('canyon', 'Canyon'),
        ('oasis', 'Oasis'),
        ('waterfront', 'Waterfront'),
        ('riverfront', 'Riverfront'),
        ('canal_view', 'Canal View'),
        ('fjord_view', 'Fjord View'),
        ('glacier_view', 'Glacier View'),
        ('volcano_view', 'Volcano View'),
        ('coral_reef_nearby', 'Coral Reef Nearby'),
        ('marine_reserve', 'Marine Reserve'),
        ('national_park', 'National Park'),
        ('wildlife_sanctuary', 'Wildlife Sanctuary'),
        ('bird_sanctuary', 'Bird Sanctuary'),
        ('butterfly_garden', 'Butterfly Garden'),
        ('botanical_garden', 'Botanical Garden'),
        ('zen_garden', 'Zen Garden'),
        ('mediterranean_garden', 'Mediterranean Garden'),
        ('english_garden', 'English Garden'),
        ('japanese_garden', 'Japanese Garden'),
        ('french_garden', 'French Garden'),
        ('italian_garden', 'Italian Garden'),
        ('tropical_garden', 'Tropical Garden'),
        ('desert_garden', 'Desert Garden'),
        ('rock_garden', 'Rock Garden'),
        ('water_garden', 'Water Garden'),
        ('roof_garden', 'Roof Garden'),
        ('vertical_garden', 'Vertical Garden'),
        ('hanging_gardens', 'Hanging Gardens'),
        ('secret_garden', 'Secret Garden'),
        ('moon_garden', 'Moon Garden'),
        ('night_blooming_garden', 'Night Blooming Garden'),
        ('healing_garden', 'Healing Garden'),
        ('meditation_garden', 'Meditation Garden'),
        ('prayer_garden', 'Prayer Garden'),
        ('contemplation_garden', 'Contemplation Garden'),
        ('labyrinth_garden', 'Labyrinth Garden'),
        ('maze_garden', 'Maze Garden'),
        ('topiary_garden', 'Topiary Garden'),
        ('rose_garden', 'Rose Garden'),
        ('orchid_house', 'Orchid House'),
        ('greenhouse', 'Greenhouse'),
        ('conservatory', 'Conservatory'),
        ('winter_garden', 'Winter Garden'),
        ('indoor_garden', 'Indoor Garden'),
        ('hydroponic_garden', 'Hydroponic Garden'),
        ('aquaponic_system', 'Aquaponic System'),
        ('organic_farm', 'Organic Farm'),
        ('vegetable_garden', 'Vegetable Garden'),
        ('herb_garden', 'Herb Garden'),
        ('spice_garden', 'Spice Garden'),
        ('fruit_orchard', 'Fruit Orchard'),
        ('olive_grove', 'Olive Grove'),
        ('vineyard', 'Vineyard'),
        ('tea_plantation', 'Tea Plantation'),
        ('coffee_plantation', 'Coffee Plantation'),
        ('cocoa_plantation', 'Cocoa Plantation'),
        ('nut_grove', 'Nut Grove'),
        ('palm_grove', 'Palm Grove'),
        ('bamboo_forest', 'Bamboo Forest'),
        ('pine_forest', 'Pine Forest'),
        ('eucalyptus_forest', 'Eucalyptus Forest'),
        ('rainforest', 'Rainforest'),
        ('cloud_forest', 'Cloud Forest'),
        ('temperate_forest', 'Temperate Forest'),
        ('boreal_forest', 'Boreal Forest'),
        ('tundra', 'Tundra'),
        ('arctic_location', 'Arctic Location'),
        ('antarctic_inspired', 'Antarctic Inspired'),
        ('polar_location', 'Polar Location'),
        ('ice_cave', 'Ice Cave'),
        ('lava_tube', 'Lava Tube'),
        ('underground_bunker', 'Underground Bunker'),
        ('cave_dwelling', 'Cave Dwelling'),
        ('earthship', 'Earthship'),
        ('geodesic_dome', 'Geodesic Dome'),
        ('biodome', 'Biodome'),
        ('biosphere', 'Biosphere'),
        ('eco_pod', 'Eco Pod'),
        ('treehouse', 'Treehouse'),
        ('stilt_house', 'Stilt House'),
        ('floating_house', 'Floating House'),
        ('houseboat', 'Houseboat'),
        ('yacht', 'Yacht'),
        ('sailboat', 'Sailboat'),
        ('catamaran', 'Catamaran'),
        ('motorboat', 'Motorboat'),
        ('submarine', 'Submarine'),
        ('airship', 'Airship'),
        ('hot_air_balloon', 'Hot Air Balloon'),
        ('glamping_tent', 'Glamping Tent'),
        ('yurt', 'Yurt'),
        ('teepee', 'Teepee'),
        ('wigwam', 'Wigwam'),
        ('igloo', 'Igloo'),
        ('mud_hut', 'Mud Hut'),
        ('thatch_roof', 'Thatch Roof'),
        ('straw_bale', 'Straw Bale Construction'),
        ('adobe', 'Adobe Construction'),
        ('stone_house', 'Stone House'),
        ('log_cabin', 'Log Cabin'),
        ('timber_frame', 'Timber Frame'),
        ('post_and_lintel', 'Post and Lintel'),
        ('brick_house', 'Brick House'),
        ('concrete_house', 'Concrete House'),
        ('steel_structure', 'Steel Structure'),
        ('glass_house', 'Glass House'),
        ('mirror_house', 'Mirror House'),
        ('camouflage_design', 'Camouflage Design'),
        ('invisible_house', 'Invisible House'),
        ('underground_house', 'Underground House'),
        ('earth_sheltered', 'Earth Sheltered'),
        ('passive_solar', 'Passive Solar Design'),
        ('active_solar', 'Active Solar Design'),
        ('wind_powered', 'Wind Powered'),
        ('geothermal', 'Geothermal'),
        ('off_grid', 'Off Grid'),
        ('self_sustaining', 'Self Sustaining'),
        ('zero_energy', 'Zero Energy'),
        ('carbon_neutral', 'Carbon Neutral'),
        ('green_building', 'Green Building'),
        ('leed_certified', 'LEED Certified'),
        ('breeam_certified', 'BREEAM Certified'),
        ('living_building', 'Living Building Challenge'),
        ('passive_house', 'Passive House'),
        ('earthship_standard', 'Earthship Standard'),
        ('net_zero', 'Net Zero'),
        ('energy_plus', 'Energy Plus'),
        ('smart_home', 'Smart Home'),
        ('iot_enabled', 'IoT Enabled'),
        ('voice_controlled', 'Voice Controlled'),
        ('app_controlled', 'App Controlled'),
        ('automation_system', 'Automation System'),
        ('security_system', 'Security System'),
        ('surveillance_system', 'Surveillance System'),
        ('access_control', 'Access Control'),
        ('biometric_security', 'Biometric Security'),
        ('retinal_scan', 'Retinal Scan'),
        ('facial_recognition', 'Facial Recognition'),
        ('fingerprint_access', 'Fingerprint Access'),
        ('keycard_system', 'Keycard System'),
        ('rfid_system', 'RFID System'),
        ('nfc_enabled', 'NFC Enabled'),
        ('bluetooth_enabled', 'Bluetooth Enabled'),
        ('wifi_enabled', 'WiFi Enabled'),
        ('cellular_enabled', 'Cellular Enabled'),
        ('satellite_internet', 'Satellite Internet'),
        ('starlink', 'Starlink'),
        ('mesh_network', 'Mesh Network'),
        ('fiber_optic', 'Fiber Optic'),
        ('5g_enabled', '5G Enabled'),
        ('6g_ready', '6G Ready'),
        ('quantum_secure', 'Quantum Secure'),
        ('encrypted_network', 'Encrypted Network'),
        ('vpn_server', 'VPN Server'),
        ('tor_network', 'Tor Network'),
        ('dark_web_access', 'Dark Web Access'),
        ('anonymous_network', 'Anonymous Network'),
        ('blockchain_secured', 'Blockchain Secured'),
        ('nft_owned', 'NFT Owned'),
        ('metaverse_access', 'Metaverse Access'),
        ('virtual_reality', 'Virtual Reality Ready'),
        ('augmented_reality', 'Augmented Reality Ready'),
        ('mixed_reality', 'Mixed Reality Ready'),
        ('holographic_display', 'Holographic Display'),
        ('projection_mapping', 'Projection Mapping'),
        ('light_show', 'Light Show'),
        ('sound_installation', 'Sound Installation'),
        ('interactive_art', 'Interactive Art'),
        ('kinetic_art', 'Kinetic Art'),
        ('digital_art', 'Digital Art'),
        ('nft_artwork', 'NFT Artwork'),
        ('crypto_art', 'Crypto Art'),
        ('generative_art', 'Generative Art'),
        ('ai_generated', 'AI Generated Design'),
        ('algorithmic_architecture', 'Algorithmic Architecture'),
        ('parametric_design', 'Parametric Design'),
        ('fractal_design', 'Fractal Design'),
        ('sacred_geometry', 'Sacred Geometry'),
        ('feng_shui', 'Feng Shui Design'),
        ('vaastu', 'Vaastu Design'),
        ('ba_gua', 'Ba Gua'),
        ('chakra_aligned', 'Chakra Aligned'),
        ('crystal_grid', 'Crystal Grid'),
        ('ley_lines', 'Ley Lines'),
        ('energy_vortex', 'Energy Vortex'),
        ('power_spot', 'Power Spot'),
        ('sacred_site', 'Sacred Site'),
        ('ancient_ruins', 'Ancient Ruins'),
        ('archeological_site', 'Archaeological Site'),
        ('historical_monument', 'Historical Monument'),
        ('world_heritage', 'World Heritage Site'),
        ('unesco_site', 'UNESCO Site'),
        ('cultural_heritage', 'Cultural Heritage'),
        ('indigenous_land', 'Indigenous Land'),
        ('native_territory', 'Native Territory'),
        ('traditional_territory', 'Traditional Territory'),
        ('ancestral_land', 'Ancestral Land'),
        ('sacred_land', 'Sacred Land'),
        ('burial_ground', 'Burial Ground'),
        ('ceremonial_site', 'Ceremonial Site'),
        ('vision_quest_site', 'Vision Quest Site'),
        ('shamanic_site', 'Shamanic Site'),
        ('mystical_site', 'Mystical Site'),
        ('magical_site', 'Magical Site'),
        ('fairy_realm', 'Fairy Realm'),
        ('dragon_lair', 'Dragon Lair'),
        ('unicorn_habitat', 'Unicorn Habitat'),
        ('mermaid_cove', 'Mermaid Cove'),
        ('atlantis_remnant', 'Atlantis Remnant'),
        ('lemuria_remnant', 'Lemuria Remnant'),
        ('mu_remnant', 'Mu Remnant'),
        ('shangri_la', 'Shangri-La'),
        ('avalon', 'Avalon'),
        ('el_dorado', 'El Dorado'),
        ('utopia', 'Utopia'),
        ('eden', 'Eden'),
        ('paradise', 'Paradise'),
        ('heaven_on_earth', 'Heaven on Earth'),
        ('nirvana', 'Nirvana'),
        ('enlightenment_center', 'Enlightenment Center'),
        ('ascended_master_retreat', 'Ascended Master Retreat'),
        ('angelic_realm', 'Angelic Realm'),
        ('archangel_retreat', 'Archangel Retreat'),
        ('christ_consciousness', 'Christ Consciousness Center'),
        ('buddha_nature', 'Buddha Nature Retreat'),
        ('tao_retreat', 'Tao Retreat'),
        ('zen_center', 'Zen Center'),
        ('meditation_retreat', 'Meditation Retreat'),
        ('yoga_retreat', 'Yoga Retreat'),
        ('spiritual_retreat', 'Spiritual Retreat'),
        ('mystical_retreat', 'Mystical Retreat'),
        ('esoteric_center', 'Esoteric Center'),
        ('occult_school', 'Occult School'),
        ('alchemy_lab', 'Alchemy Lab'),
        ('hermetic_academy', 'Hermetic Academy'),
        ('rosicrucian_center', 'Rosicrucian Center'),
        ('templar_commandery', 'Templar Commandery'),
        ('masonic_lodge', 'Masonic Lodge'),
        ('illuminati_headquarters', 'Illuminati Headquarters'),
        ('secret_society', 'Secret Society Meeting Place'),
        ('conspiracy_theory_hub', 'Conspiracy Theory Hub'),
        ('time_travel_portal', 'Time Travel Portal'),
        ('dimensional_portal', 'Dimensional Portal'),
        ('stargate', 'Stargate'),
        ('wormhole', 'Wormhole'),
        ('black_hole_observer', 'Black Hole Observer'),
        ('quantum_realm', 'Quantum Realm Access'),
        ('parallel_universe', 'Parallel Universe Gateway'),
        ('alternate_reality', 'Alternate Reality Hub'),
        ('simulation_center', 'Simulation Center'),
        ('matrix_node', 'Matrix Node'),
        ('neural_network', 'Neural Network Hub'),
        ('consciousness_expansion', 'Consciousness Expansion Center'),
        ('dna_activation', 'DNA Activation Chamber'),
        ('light_body', 'Light Body Sanctuary'),
        ('merkaba_vehicle', 'Merkaba Vehicle'),
        ('bi_location', 'Bi-Location Chamber'),
        ('astral_projection', 'Astral Projection Room'),
        ('remote_viewing', 'Remote Viewing Center'),
        ('telepathy_training', 'Telepathy Training'),
        ('psychic_development', 'Psychic Development'),
        ('intuition_training', 'Intuition Training'),
        ('clairvoyance_practice', 'Clairvoyance Practice'),
        ('mediumship_training', 'Mediumship Training'),
        ('channeling_room', 'Channeling Room'),
        ('oracle_chamber', 'Oracle Chamber'),
        ('divination_center', 'Divination Center'),
        ('tarot_reading', 'Tarot Reading Room'),
        ('rune_casting', 'Rune Casting Area'),
        ('crystal_ball', 'Crystal Ball Chamber'),
        ('pendulum_room', 'Pendulum Room'),
        ('dowsing_center', 'Dowsing Center'),
        ('scrying_mirror', 'Scrying Mirror'),
        ('magic_mirror', 'Magic Mirror'),
        ('hall_of_mirrors', 'Hall of Mirrors'),
        ('infinity_mirror', 'Infinity Mirror'),
        ('kaleidoscope_room', 'Kaleidoscope Room'),
        ('prism_chamber', 'Prism Chamber'),
        ('rainbow_room', 'Rainbow Room'),
        ('aurora_borealis', 'Aurora Borealis Simulator'),
        ('northern_lights', 'Northern Lights Chamber'),
        ('southern_lights', 'Southern Lights Room'),
        ('cosmic_energy', 'Cosmic Energy Generator'),
        ('zero_point_energy', 'Zero Point Energy Device'),
        ('free_energy', 'Free Energy Generator'),
        ('anti_gravity', 'Anti-Gravity Chamber'),
        ('levitation_room', 'Levitation Room'),
        ('teleportation_pad', 'Teleportation Pad'),
        ('beam_me_up', 'Beam Me Up Station'),
        ('transporter_room', 'Transporter Room'),
        ('holodeck', 'Holodeck'),
        ('replicator', 'Replicator'),
        ('tricorder_station', 'Tricorder Station'),
        ('phaser_range', 'Phaser Range'),
        ('lightsaber_training', 'Lightsaber Training'),
        ('force_training', 'Force Training Academy'),
        ('jedi_temple', 'Jedi Temple'),
        ('sith_academy', 'Sith Academy'),
        ('wizards_tower', 'Wizard\'s Tower'),
        ('witches_coven', 'Witch\'s Coven'),
        ('alchemists_laboratory', 'Alchemist\'s Laboratory'),
        ('sorcerers_study', 'Sorcerer\'s Study'),
        ('necromancers_lair', 'Necromancer\'s Lair'),
        ('vampire_castle', 'Vampire Castle'),
        ('werewolf_den', 'Werewolf Den'),
        ('zombie_apocalypse', 'Zombie Apocalypse Bunker'),
        ('alien_encounter', 'Alien Encounter Site'),
        ('ufo_landing_pad', 'UFO Landing Pad'),
        ('crop_circle', 'Crop Circle Research'),
        ('ancient_astronaut', 'Ancient Astronaut Theory'),
        ('lost_civilization', 'Lost Civilization Ruins'),
        ('atlantis_research', 'Atlantis Research Center'),
        ('pyramid_power', 'Pyramid Power Chamber'),
        ('megalithic_energy', 'Megalithic Energy Field'),
        ('stone_circle', 'Stone Circle'),
        ('menhir_field', 'Menhir Field'),
        ('dolmen_chamber', 'Dolmen Chamber'),
        ('cromlech', 'Cromlech'),
        ('henges', 'Henges'),
        ('moai_statues', 'Moai Statues'),
        ('easter_island', 'Easter Island Replica'),
        ('stonehenge_replica', 'Stonehenge Replica'),
        ('mayan_pyramid', 'Mayan Pyramid'),
        ('aztec_temple', 'Aztec Temple'),
        ('incan_citadel', 'Incan Citadel'),
        ('egyptian_tomb', 'Egyptian Tomb'),
        ('pharaohs_palace', 'Pharaoh\'s Palace'),
        ('roman_colosseum', 'Roman Colosseum'),
        ('greek_parthenon', 'Greek Parthenon'),
        ('persian_palace', 'Persian Palace'),
        ('chinese_imperial', 'Chinese Imperial Palace'),
        ('japanese_castle', 'Japanese Castle'),
        ('indian_maharaja', 'Indian Maharaja Palace'),
        ('ottoman_sultans', 'Ottoman Sultan\'s Palace'),
        ('mogul_emperor', 'Mogul Emperor\'s Palace'),
        ('byzantine_emperor', 'Byzantine Emperor\'s Palace'),
        ('russian_czar', 'Russian Czar\'s Palace'),
        ('french_king', 'French King\'s Palace'),
        ('english_queen', 'English Queen\'s Palace'),
        ('spanish_king', 'Spanish King\'s Palace'),
        ('portuguese_king', 'Portuguese King\'s Palace'),
        ('dutch_stadtholder', 'Dutch Stadtholder\'s Palace'),
        ('german_kaiser', 'German Kaiser\'s Palace'),
        ('austrian_emperor', 'Austrian Emperor\'s Palace'),
        ('hungarian_king', 'Hungarian King\'s Palace'),
        ('polish_king', 'Polish King\'s Palace'),
        ('swedish_king', 'Swedish King\'s Palace'),
        ('danish_king', 'Danish King\'s Palace'),
        ('norwegian_king', 'Norwegian King\'s Palace'),
        ('finnish_president', 'Finnish President\'s Palace'),
        ('icelandic_chieftain', 'Icelandic Chieftain\'s Hall'),
        ('scottish_laird', 'Scottish Laird\'s Castle'),
        ('irish_chieftain', 'Irish Chieftain\'s Fort'),
        ('welsh_prince', 'Welsh Prince\'s Palace'),
        ('breton_duke', 'Breton Duke\'s Manor'),
        ('corsican_leader', 'Corsican Leader\'s Villa'),
        ('sicilian_don', 'Sicilian Don\'s Estate'),
        ('calabrian_boss', 'Calabrian Boss\'s Villa'),
        ('sardinian_prince', 'Sardinian Prince\'s Palace'),
        ('cretean_king', 'Cretan King\'s Palace'),
        ('cyprus_king', 'Cyprus King\'s Palace'),
        ('rhodes_knight', 'Rhodes Knight\'s Castle'),
        ('malta_knight', 'Malta Knight\'s Palace'),
        ('jerusalem_king', 'Jerusalem King\'s Citadel'),
        ('constantinople_emperor', 'Constantinople Emperor\'s Palace'),
        ('alexandria_pharaoh', 'Alexandria Pharaoh\'s Palace'),
        ('carthage_queen', 'Carthage Queen\'s Palace'),
        ('numidia_king', 'Numidia King\'s Palace'),
        ('mauretania_king', 'Mauretania King\'s Palace'),
        ('garamantian_king', 'Garamantian King\'s Palace'),
        ('axumite_king', 'Axumite King\'s Palace'),
        ('kushite_pharaoh', 'Kushite Pharaoh\'s Palace'),
        ('meroitic_queen', 'Meroitic Queen\'s Palace'),
        ('napatan_king', 'Napatan King\'s Palace'),
        ('nubian_king', 'Nubian King\'s Palace'),
        ('blemmyes_chief', 'Blemmyes Chief\'s Camp'),
        ('nobatae_king', 'Nobatae King\'s Oasis'),
        ('makuria_king', 'Makuria King\'s Citadel'),
        ('alodia_queen', 'Alodia Queen\'s Palace'),
        ('dotawo_king', 'Dotawo King\'s Fortress'),
        ('medieval_castle', 'Medieval Castle'),
        ('renaissance_palace', 'Renaissance Palace'),
        ('baroque_mansion', 'Baroque Mansion'),
        ('rococo_chateau', 'Rococo Chateau'),
        ('neoclassical_villa', 'Neoclassical Villa'),
        ('gothic_cathedral', 'Gothic Cathedral'),
        ('romanesque_abbey', 'Romanesque Abbey'),
        ('byzantine_church', 'Byzantine Church'),
        ('orthodox_monastery', 'Orthodox Monastery'),
        ('catholic_cathedral', 'Catholic Cathedral'),
        ('protestant_church', 'Protestant Church'),
        ('anglican_cathedral', 'Anglican Cathedral'),
        ('lutheran_church', 'Lutheran Church'),
        ('calvinist_temple', 'Calvinist Temple'),
        ('methodist_chapel', 'Methodist Chapel'),
        ('baptist_church', 'Baptist Church'),
        ('pentecostal_hall', 'Pentecostal Hall'),
        ('evangelical_center', 'Evangelical Center'),
        ('fundamentalist_retreat', 'Fundamentalist Retreat'),
        ('charismatic_church', 'Charismatic Church'),
        ('non_denominational', 'Non-Denominational Center'),
        ('interfaith_temple', 'Interfaith Temple'),
        ('universalist_hall', 'Universalist Hall'),
        ('unitarian_church', 'Unitarian Church'),
        ('quaker_meeting', 'Quaker Meeting House'),
        ('shaker_village', 'Shaker Village'),
        ('amish_farm', 'Amish Farm'),
        ('mennonite_community', 'Mennonite Community'),
        ('hutterite_colony', 'Hutterite Colony'),
        ('dunkard_settlement', 'Dunkard Settlement'),
        ('brethren_house', 'Brethren House'),
        ('moravian_settlement', 'Moravian Settlement'),
        ('pietist_retreat', 'Pietist Retreat'),
        ('jansenist_abbey', 'Jansenist Abbey'),
        ('quietist_monastery', 'Quietist Monastery'),
        ('mystic_retreat', 'Mystic Retreat'),
        ('contemplative_center', 'Contemplative Center'),
        ('monastic_life', 'Monastic Life Experience'),
        ('cenobitic_monastery', 'Cenobitic Monastery'),
        ('eremitic_hermitage', 'Eremitic Hermitage'),
        ('anchorite_cell', 'Anchorite Cell'),
        ('recluse_retreat', 'Recluse Retreat'),
        ('solitary_life', 'Solitary Life Experience'),
        ('hermit_cabin', 'Hermit Cabin'),
        ('solitude_retreat', 'Solitude Retreat'),
        ('silence_center', 'Center for Silence'),
        ('mindfulness_retreat', 'Mindfulness Retreat'),
        ('vipassana_center', 'Vipassana Center'),
        ('zen_monastery', 'Zen Monastery'),
        ('chan_buddhist', 'Chan Buddhist Temple'),
        ('son_buddhist', 'Son Buddhist Temple'),
        ('rinzai_zen', 'Rinzai Zen Center'),
        ('soto_zen', 'Soto Zen Center'),
        ('tibetan_buddhist', 'Tibetan Buddhist Monastery'),
        ('theravada_center', 'Theravada Center'),
        ('mahayana_temple', 'Mahayana Temple'),
        ('vajrayana_center', 'Vajrayana Center'),
        ('tantric_retreat', 'Tantric Retreat'),
        ('kundalini_center', 'Kundalini Center'),
        ('chakra_center', 'Chakra Center'),
        ('prana_center', 'Prana Center'),
        ('qi_gong_center', 'Qi Gong Center'),
        ('tai_chi_retreat', 'Tai Chi Retreat'),
        ('falun_gong', 'Falun Gong Center'),
        ('falun_dafa', 'Falun Dafa Retreat'),
        ('baha_i_house', 'Baha\'i House of Worship'),
        ('zoroastrian_fire', 'Zoroastrian Fire Temple'),
        ('jain_temple', 'Jain Temple'),
        ('sikh_gurdwara', 'Sikh Gurdwara'),
        ('hindu_temple', 'Hindu Temple'),
        ('buddhist_temple', 'Buddhist Temple'),
        ('confucian_temple', 'Confucian Temple'),
        ('taoist_temple', 'Taoist Temple'),
        ('shinto_shrine', 'Shinto Shrine'),
        ('caodai_temple', 'Caodai Temple'),
        ('kami_no_michi', 'Kami no Michi Shrine'),
        ('animist_shrine', 'Animist Shrine'),
        ('totem_pole', 'Totem Pole Site'),
        ('dreamtime_site', 'Dreamtime Sacred Site'),
        ('aboriginal_sacred', 'Aboriginal Sacred Site'),
        ('native_american', 'Native American Sacred Site'),
        ('first_nations', 'First Nations Sacred Land'),
        ('inuit_sacred', 'Inuit Sacred Site'),
        ('maori_marae', 'Maori Marae'),
        ('aboriginal_dreaming', 'Aboriginal Dreaming Site'),
        ('songline_center', 'Songline Center'),
        ('bush_tucker', 'Bush Tucker Experience'),
        ('didgeridoo', 'Didgeridoo Sacred Site'),
        ('corroboree_ground', 'Corroboree Ground'),
        ('walkabout_trail', 'Walkabout Trail'),
        ('spirit_ancestor', 'Spirit Ancestor Site'),
        ('rainbow_serpent', 'Rainbow Serpent Site'),
        ('dreaming_track', 'Dreaming Track'),
        ('totemic_site', 'Totemic Site'),
        ('clan_territory', 'Clan Territory'),
        ('tribal_land', 'Tribal Land'),
        ('shaman_territory', 'Shaman Territory'),
        ('medicine_wheel', 'Medicine Wheel'),
        ('vision_quest', 'Vision Quest Site'),
        ('sweat_lodge', 'Sweat Lodge'),
        ('sun_dance', 'Sun Dance Circle'),
        ('ghost_dance', 'Ghost Dance Site'),
        ('peyote_ceremony', 'Peyote Ceremony Site'),
        ('ayahuasca_retreat', 'Ayahuasca Retreat'),
        ('iboga_center', 'Iboga Center'),
        ('sacred_mushroom', 'Sacred Mushroom Retreat'),
        ('entheogenic_center', 'Entheogenic Center'),
        ('psychedelic_retreat', 'Psychedelic Retreat'),
        ('consciousness_research', 'Consciousness Research Center'),
        ('neuroscience_lab', 'Neuroscience Laboratory'),
        ('brain_research', 'Brain Research Center'),
        ('cognitive_science', 'Cognitive Science Lab'),
        ('psychology_research', 'Psychology Research Center'),
        ('philosophy_center', 'Philosophy Center'),
        ('ethics_research', 'Ethics Research Center'),
        ('anthropology_lab', 'Anthropology Laboratory'),
        ('sociology_center', 'Sociology Center'),
        ('history_research', 'History Research Center'),
        ('archaeology_site', 'Archaeology Site'),
        ('paleontology_dig', 'Paleontology Dig Site'),
        ('fossil_site', 'Fossil Site'),
        ('dinosaur_track', 'Dinosaur Track Site'),
        ('meteor_crater', 'Meteor Crater'),
        ('impact_site', 'Impact Site'),
        ('volcanic_site', 'Volcanic Site'),
        ('geyser_field', 'Geyser Field'),
        ('hot_spring', 'Hot Spring'),
        ('mineral_spring', 'Mineral Spring'),
        ('healing_spring', 'Healing Spring'),
        ('sacred_spring', 'Sacred Spring'),
        ('wishing_well', 'Wishing Well'),
        ('fountain_of_youth', 'Fountain of Youth'),
        ('elixir_source', 'Elixir Source'),
        ('philosophers_stone', 'Philosopher\'s Stone Site'),
        ('alchemical_spring', 'Alchemical Spring'),
        ('mercury_spring', 'Mercury Spring'),
        ('sulfur_spring', 'Sulfur Spring'),
        ('salt_spring', 'Salt Spring'),
        ('copper_spring', 'Copper Spring'),
        ('iron_spring', 'Iron Spring'),
        ('gold_spring', 'Gold Spring'),
        ('silver_spring', 'Silver Spring'),
        ('crystal_spring', 'Crystal Spring'),
        ('gem_spring', 'Gem Spring'),
        ('diamond_spring', 'Diamond Spring'),
        ('ruby_spring', 'Ruby Spring'),
        ('sapphire_spring', 'Sapphire Spring'),
        ('emerald_spring', 'Emerald Spring'),
        ('amethyst_spring', 'Amethyst Spring'),
        ('quartz_spring', 'Quartz Spring'),
        ('opal_spring', 'Opal Spring'),
        ('jade_spring', 'Jade Spring'),
        ('turquoise_spring', 'Turquoise Spring'),
        ('lapis_spring', 'Lapis Spring'),
        ('malachite_spring', 'Malachite Spring'),
        ('azurite_spring', 'Azurite Spring'),
        ('citrine_spring', 'Citrine Spring'),
        ('topaz_spring', 'Topaz Spring'),
        ('peridot_spring', 'Peridot Spring'),
        ('aquamarine_spring', 'Aquamarine Spring'),
        ('garnet_spring', 'Garnet Spring'),
        ('moonstone_spring', 'Moonstone Spring'),
        ('sunstone_spring', 'Sunstone Spring'),
        ('labradorite_spring', 'Labradorite Spring'),
        ('obsidian_spring', 'Obsidian Spring'),
        ('onyx_spring', 'Onyx Spring'),
        ('agate_spring', 'Agate Spring'),
        ('jasper_spring', 'Jasper Spring'),
        ('carnelian_spring', 'Carnelian Spring'),
        ('bloodstone_spring', 'Bloodstone Spring'),
        ('heliotrope_spring', 'Heliotrope Spring'),
        ('sard_spring', 'Sard Spring'),
        ('sardonyx_spring', 'Sardonyx Spring'),
        ('chalcedony_spring', 'Chalcedony Spring'),
        ('chrysoprase_spring', 'Chrysoprase Spring'),
        ('chrysocolla_spring', 'Chrysocolla Spring'),
        ('dumortierite_spring', 'Dumortierite Spring'),
        ('fluorite_spring', 'Fluorite Spring'),
        ('iolite_spring', 'Iolite Spring'),
        ('kyanite_spring', 'Kyanite Spring'),
        ('lepidolite_spring', 'Lepidolite Spring'),
        ('morganite_spring', 'Morganite Spring'),
        ('moss_agate_spring', 'Moss Agate Spring'),
        ('rhodochrosite_spring', 'Rhodochrosite Spring'),
        ('rhodonite_spring', 'Rhodonite Spring'),
        ('rose_quartz_spring', 'Rose Quartz Spring'),
        ('scolecite_spring', 'Scolecite Spring'),
        ('selenite_spring', 'Selenite Spring'),
        ('seraphinite_spring', 'Seraphinite Spring'),
        ('shungite_spring', 'Shungite Spring'),
        ('sodalite_spring', 'Sodalite Spring'),
        ('stilbite_spring', 'Stilbite Spring'),
        ('sugilite_spring', 'Sugilite Spring'),
        ('tanzanite_spring', 'Tanzanite Spring'),
        ('tiger_eye_spring', 'Tiger Eye Spring'),
        ('tourmaline_spring', 'Tourmaline Spring'),
        ('unakite_spring', 'Unakite Spring'),
        ('variscite_spring', 'Variscite Spring'),
        ('vesuvianite_spring', 'Vesuvianite Spring'),
        ('wulfenite_spring', 'Wulfenite Spring'),
        ('zeolite_spring', 'Zeolite Spring'),
        ('zoisite_spring', 'Zoisite Spring'),
        ('zunyite_spring', 'Zunyite Spring'),
        ('zwieselite_spring', 'Zwieselite Spring'),
        ('zygadite_spring', 'Zygadite Spring'),
        
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
    """Enhanced photos for accommodation listings with gallery support"""
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('360', '360° Image'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('hidden', 'Hidden'),
        ('private', 'Private'),
    ]

    NSFW_CHOICES = [
        ('safe', 'Safe'),
        ('mild', 'Mild NSFW'),
        ('adult', 'Adult Content'),
    ]

    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='photos')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')

    # File fields
    original_file = models.FileField(upload_to='accommodations/gallery/%Y/%m/')
    thumbnail = models.ImageField(upload_to='accommodations/gallery/thumbs/', blank=True, null=True)
    small = models.ImageField(upload_to='accommodations/gallery/small/', blank=True, null=True)
    medium = models.ImageField(upload_to='accommodations/gallery/medium/', blank=True, null=True)
    large = models.ImageField(upload_to='accommodations/gallery/large/', blank=True, null=True)
    xl = models.ImageField(upload_to='accommodations/gallery/xl/', blank=True, null=True)

    # Metadata
    title = models.CharField(max_length=200, blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    attribution = models.CharField(max_length=200, blank=True, null=True, help_text="Photographer or source")
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated tags")

    # Display settings
    display_order = models.IntegerField(default=0)
    is_hero = models.BooleanField(default=False, help_text="Use as hero/main image")
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    nsfw_rating = models.CharField(max_length=10, choices=NSFW_CHOICES, default='safe')

    # Video specific fields
    video_duration = models.DurationField(blank=True, null=True)
    video_thumbnail_time = models.FloatField(default=0, help_text="Time in seconds for video thumbnail")

    # Technical metadata
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    mime_type = models.CharField(max_length=100, blank=True, null=True)

    # EXIF data (stored as JSON)
    exif_data = models.JSONField(blank=True, null=True)

    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-uploaded_at']
        indexes = [
            models.Index(fields=['accommodation', 'display_order']),
            models.Index(fields=['accommodation', 'is_hero']),
            models.Index(fields=['accommodation', 'visibility']),
            models.Index(fields=['media_type']),
        ]

    def __str__(self):
        return f"{self.accommodation.property_name} - {self.title or 'Photo'}"

    def get_image_url(self, size='medium'):
        """Get URL for specific image size"""
        if size == 'thumbnail' and self.thumbnail and self.thumbnail.name:
            return self.thumbnail.url
        elif size == 'small' and self.small and self.small.name:
            return self.small.url
        elif size == 'medium' and self.medium and self.medium.name:
            return self.medium.url
        elif size == 'large' and self.large and self.large.name:
            return self.large.url
        elif size == 'xl' and self.xl and self.xl.name:
            return self.xl.url
        elif self.original_file and self.original_file.name:
            return self.original_file.url
        return None

    def get_srcset(self):
        """Generate srcset for responsive images"""
        srcset = []
        if self.small:
            srcset.append(f"{self.small.url} 480w")
        if self.medium:
            srcset.append(f"{self.medium.url} 960w")
        if self.large:
            srcset.append(f"{self.large.url} 1440w")
        if self.xl:
            srcset.append(f"{self.xl.url} 2048w")
        return ', '.join(srcset)

    def get_sizes(self):
        """Get sizes attribute for responsive images"""
        return "(max-width: 640px) 480px, (max-width: 1024px) 960px, (max-width: 1440px) 1440px, 2048px"

    @property
    def is_image(self):
        return self.media_type == 'image'

    @property
    def is_video(self):
        return self.media_type == 'video'

    @property
    def is_360(self):
        return self.media_type == '360'


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
    """Enhanced photos for tour listings with gallery support"""
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('360', '360° Image'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('hidden', 'Hidden'),
        ('private', 'Private'),
    ]

    NSFW_CHOICES = [
        ('safe', 'Safe'),
        ('mild', 'Mild NSFW'),
        ('adult', 'Adult Content'),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='photos')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')

    # File fields
    original_file = models.FileField(upload_to='tours/gallery/%Y/%m/')
    thumbnail = models.ImageField(upload_to='tours/gallery/thumbs/', blank=True, null=True)
    small = models.ImageField(upload_to='tours/gallery/small/', blank=True, null=True)
    medium = models.ImageField(upload_to='tours/gallery/medium/', blank=True, null=True)
    large = models.ImageField(upload_to='tours/gallery/large/', blank=True, null=True)
    xl = models.ImageField(upload_to='tours/gallery/xl/', blank=True, null=True)

    # Metadata
    title = models.CharField(max_length=200, blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    attribution = models.CharField(max_length=200, blank=True, null=True, help_text="Photographer or source")
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated tags")

    # Display settings
    display_order = models.IntegerField(default=0)
    is_hero = models.BooleanField(default=False, help_text="Use as hero/main image")
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    nsfw_rating = models.CharField(max_length=10, choices=NSFW_CHOICES, default='safe')

    # Video specific fields
    video_duration = models.DurationField(blank=True, null=True)
    video_thumbnail_time = models.FloatField(default=0, help_text="Time in seconds for video thumbnail")

    # Technical metadata
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    mime_type = models.CharField(max_length=100, blank=True, null=True)

    # EXIF data (stored as JSON)
    exif_data = models.JSONField(blank=True, null=True)

    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-uploaded_at']
        indexes = [
            models.Index(fields=['tour', 'display_order']),
            models.Index(fields=['tour', 'is_hero']),
            models.Index(fields=['tour', 'visibility']),
            models.Index(fields=['media_type']),
        ]

    def __str__(self):
        return f"{self.tour.tour_name} - {self.title or 'Photo'}"

    def get_image_url(self, size='medium'):
        """Get URL for specific image size"""
        if size == 'thumbnail' and self.thumbnail and self.thumbnail.name:
            return self.thumbnail.url
        elif size == 'small' and self.small and self.small.name:
            return self.small.url
        elif size == 'medium' and self.medium and self.medium.name:
            return self.medium.url
        elif size == 'large' and self.large and self.large.name:
            return self.large.url
        elif size == 'xl' and self.xl and self.xl.name:
            return self.xl.url
        elif self.original_file and self.original_file.name:
            return self.original_file.url
        return None

    def get_srcset(self):
        """Generate srcset for responsive images"""
        srcset = []
        if self.small:
            srcset.append(f"{self.small.url} 480w")
        if self.medium:
            srcset.append(f"{self.medium.url} 960w")
        if self.large:
            srcset.append(f"{self.large.url} 1440w")
        if self.xl:
            srcset.append(f"{self.xl.url} 2048w")
        return ', '.join(srcset)

    def get_sizes(self):
        """Get sizes attribute for responsive images"""
        return "(max-width: 640px) 480px, (max-width: 1024px) 960px, (max-width: 1440px) 1440px, 2048px"

    @property
    def is_image(self):
        return self.media_type == 'image'

    @property
    def is_video(self):
        return self.media_type == 'video'

    @property
    def is_360(self):
        return self.media_type == '360'


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


class TourGuide(models.Model):
    """Tour Guide profile and services listing"""
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('arabic', 'Arabic'),
        ('french', 'French'),
        ('spanish', 'Spanish'),
        ('german', 'German'),
        ('italian', 'Italian'),
        ('chinese', 'Chinese'),
        ('japanese', 'Japanese'),
        ('other', 'Other'),
    ]

    SPECIALIZATION_CHOICES = [
        ('historical', 'Historical & Cultural'),
        ('adventure', 'Adventure & Outdoor'),
        ('food', 'Food & Culinary'),
        ('nature', 'Nature & Wildlife'),
        ('photography', 'Photography'),
        ('religious', 'Religious Sites'),
        ('architecture', 'Architecture'),
        ('art', 'Art & Museums'),
        ('general', 'General Tourism'),
    ]

    # Basic Information
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tour_guides')
    guide_name = models.CharField(max_length=200, help_text="Guide's full name")
    tagline = models.CharField(max_length=300, blank=True, help_text="Brief description (e.g., 'Expert historian with 10 years experience')")
    bio = models.TextField(help_text="Detailed biography and experience")
    profile_photo = models.ImageField(upload_to='tour_guides/photos/%Y/%m/', blank=True, null=True)

    # Certifications & Credentials
    is_licensed = models.BooleanField(default=False, help_text="Licensed/Certified tour guide")
    license_number = models.CharField(max_length=100, blank=True)
    certifications = models.TextField(blank=True, help_text="List of certifications (comma-separated)")
    years_experience = models.IntegerField(default=0, help_text="Years of experience as a guide")

    # Languages & Specializations
    languages = models.CharField(max_length=500, help_text="Languages spoken (comma-separated)")
    specializations = models.CharField(max_length=500, help_text="Areas of expertise (comma-separated)")

    # Service Details
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Rate per hour")
    half_day_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Rate for half day (4 hours)")
    full_day_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Rate for full day (8 hours)")
    max_group_size = models.IntegerField(default=10, help_text="Maximum group size")

    # Location
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    service_area = models.TextField(help_text="Areas/cities where services are available")

    # Availability
    available_days = models.CharField(max_length=200, default="Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday")
    minimum_booking_hours = models.IntegerField(default=2, help_text="Minimum booking duration in hours")

    # Additional Services
    transportation_provided = models.BooleanField(default=False)
    accommodation_assistance = models.BooleanField(default=False)
    custom_itineraries = models.BooleanField(default=True)

    # Contact & Professional Details
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)

    # Additional Info
    tour_types_offered = models.TextField(blank=True, help_text="Types of tours you offer (e.g., Walking tours, Bus tours, Private tours)")
    equipment_provided = models.TextField(blank=True, help_text="Equipment you provide (e.g., Audio guides, Maps, Water)")
    accessibility = models.TextField(blank=True, help_text="Accessibility options (e.g., Wheelchair accessible, Family-friendly)")
    covid_safety = models.TextField(blank=True, help_text="COVID-19 safety measures")
    reviews_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_tours_completed = models.IntegerField(default=0)

    # Policies
    cancellation_policy = models.TextField(default="Free cancellation up to 24 hours before service")
    terms_and_conditions = models.TextField(blank=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tour Guide'
        verbose_name_plural = 'Tour Guides'

    def __str__(self):
        return f"{self.guide_name} - {self.city}, {self.country}"


class RentalCar(models.Model):
    """Rental car/vehicle listing model"""
    VEHICLE_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('van', 'Van/Minivan'),
        ('luxury', 'Luxury'),
        ('sports', 'Sports Car'),
        ('electric', 'Electric'),
        ('convertible', 'Convertible'),
        ('truck', 'Pickup Truck'),
        ('compact', 'Compact'),
        ('economy', 'Economy'),
    ]

    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]

    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol/Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    # Basic Information
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rental_cars')
    vehicle_name = models.CharField(max_length=200, help_text="e.g., 'Toyota Camry 2023' or 'Mercedes S-Class'")
    brand = models.CharField(max_length=100, help_text="Vehicle brand/make")
    model = models.CharField(max_length=100, help_text="Vehicle model")
    year = models.IntegerField(help_text="Manufacturing year")
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPE_CHOICES, default='sedan')

    # Description
    tagline = models.CharField(max_length=300, blank=True, help_text="Brief description")
    full_description = models.TextField(help_text="Detailed description of the vehicle")

    # Vehicle Specifications
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='automatic')
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, default='petrol')
    seating_capacity = models.IntegerField(default=5, help_text="Number of seats")
    doors = models.IntegerField(default=4, help_text="Number of doors")
    luggage_capacity = models.IntegerField(default=2, help_text="Number of large suitcases")

    # Features & Amenities
    features = models.TextField(help_text="Comma-separated list (e.g., 'GPS, AC, Bluetooth, USB')")
    air_conditioning = models.BooleanField(default=True)
    gps_navigation = models.BooleanField(default=False)
    bluetooth = models.BooleanField(default=True)

    # Pricing
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per day")
    weekly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Price per week (optional)")
    monthly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Price per month (optional)")
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, help_text="Refundable security deposit")

    # Additional Costs
    insurance_included = models.BooleanField(default=True)
    insurance_cost_per_day = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    mileage_limit_per_day = models.IntegerField(default=200, help_text="KM per day (0 for unlimited)")
    extra_mileage_cost = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Cost per extra KM")

    # Location & Delivery
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=300, help_text="Where customers pick up the vehicle")
    airport_delivery = models.BooleanField(default=False)
    hotel_delivery = models.BooleanField(default=False)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Fee for delivery service")

    # Requirements
    minimum_age = models.IntegerField(default=21, help_text="Minimum driver age")
    minimum_license_years = models.IntegerField(default=1, help_text="Minimum years of driving license")

    # Availability
    minimum_rental_days = models.IntegerField(default=1, help_text="Minimum rental period in days")

    # Policies
    cancellation_policy = models.TextField(default="Free cancellation up to 24 hours before pickup")
    fuel_policy = models.CharField(max_length=200, default="Full to Full (pick up and return with full tank)")
    terms_and_conditions = models.TextField(blank=True)

    # Status & Condition
    odometer_reading = models.IntegerField(default=0, help_text="Current KM/Mileage")
    condition = models.CharField(max_length=100, default="Excellent", help_text="Vehicle condition")
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    # Additional Details
    color = models.CharField(max_length=50, blank=True)
    license_plate = models.CharField(max_length=20, blank=True)
    vin_number = models.CharField(max_length=17, blank=True, help_text="Vehicle Identification Number")
    registration_number = models.CharField(max_length=50, blank=True)

    # Extra Features
    child_seat_available = models.BooleanField(default=False)
    ski_rack = models.BooleanField(default=False)
    bike_rack = models.BooleanField(default=False)
    roof_rack = models.BooleanField(default=False)

    # Contact & Owner Info
    owner_name = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)

    # Additional Policies
    smoking_allowed = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    cross_border_allowed = models.BooleanField(default=False)
    late_return_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    cleaning_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Rental Car'
        verbose_name_plural = 'Rental Cars'

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) - {self.city}"


class TourGuidePhoto(models.Model):
    """Photos for tour guide profiles"""
    tour_guide = models.ForeignKey(TourGuide, on_delete=models.CASCADE, related_name='photos')
    original_file = models.ImageField(upload_to='tour_guides/gallery/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.IntegerField(default=0)
    is_profile_photo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'created_at']

    def __str__(self):
        return f"Photo for {self.tour_guide.guide_name}"


class RentalCarPhoto(models.Model):
    """Photos for rental car listings"""
    rental_car = models.ForeignKey(RentalCar, on_delete=models.CASCADE, related_name='photos')
    original_file = models.ImageField(upload_to='rental_cars/gallery/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False, help_text="Primary/featured photo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'created_at']

    def __str__(self):
        return f"Photo for {self.rental_car.vehicle_name}"


class Country(models.Model):
    """Country model for destinations"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=3, unique=True, help_text="ISO country code")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True, help_text="URL to country image")
    accommodations_count = models.IntegerField(default=0)
    tours_count = models.IntegerField(default=0)
    attractions = models.JSONField(blank=True, null=True, help_text="List of attractions")

    # Status
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class AccommodationAvailability(models.Model):
    """
    Per-date availability and pricing for accommodations.
    Allows hosts to set availability status, pricing, and rules for specific dates.
    """
    accommodation = models.ForeignKey(
        Accommodation, 
        on_delete=models.CASCADE, 
        related_name='availability_calendar'
    )
    date = models.DateField(db_index=True)
    
    # Availability Status
    is_available = models.BooleanField(default=True, help_text="Is this date available for booking?")
    is_blocked = models.BooleanField(default=False, help_text="Manually blocked by host")
    
    # Pricing
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price for this specific date"
    )
    original_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Original price before discounts"
    )
    
    # Booking Rules
    minimum_stay = models.IntegerField(default=1, help_text="Minimum nights required")
    maximum_stay = models.IntegerField(null=True, blank=True, help_text="Maximum nights allowed")
    
    # Special Rates
    is_special_rate = models.BooleanField(default=False)
    rate_type = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('weekend', 'Weekend Rate'),
            ('holiday', 'Holiday Rate'),
            ('seasonal', 'Seasonal Rate'),
            ('early_bird', 'Early Bird Discount'),
            ('last_minute', 'Last Minute Deal'),
            ('long_stay', 'Long Stay Discount'),
            ('custom', 'Custom Rate'),
        ]
    )
    rate_note = models.CharField(max_length=200, blank=True, help_text="Note about this rate")
    
    # Inventory Management
    total_rooms = models.IntegerField(default=1, help_text="Total rooms available")
    rooms_booked = models.IntegerField(default=0, help_text="Number of rooms already booked")
    rooms_blocked = models.IntegerField(default=0, help_text="Number of rooms blocked")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date']
        verbose_name = 'Accommodation Availability'
        verbose_name_plural = 'Accommodation Availabilities'
        unique_together = ['accommodation', 'date']
        indexes = [
            models.Index(fields=['accommodation', 'date']),
            models.Index(fields=['date', 'is_available']),
        ]
    
    def __str__(self):
        return f"{self.accommodation.name} - {self.date}"
    
    @property
    def rooms_available(self):
        """Calculate remaining available rooms"""
        return max(0, self.total_rooms - self.rooms_booked - self.rooms_blocked)
    
    @property
    def is_fully_booked(self):
        """Check if all rooms are booked"""
        return self.rooms_available == 0
    
    @property
    def occupancy_percentage(self):
        """Calculate occupancy percentage"""
        if self.total_rooms == 0:
            return 0
        occupied = self.rooms_booked + self.rooms_blocked
        return (occupied / self.total_rooms) * 100


class TourAvailability(models.Model):
    """
    Per-date availability and pricing for tours.
    Tracks tour slots, participant capacity, and dynamic pricing.
    """
    tour = models.ForeignKey(
        'Tour', 
        on_delete=models.CASCADE, 
        related_name='availability_calendar'
    )
    date = models.DateField(db_index=True)
    
    # Availability Status
    is_available = models.BooleanField(default=True, help_text="Is this tour date available?")
    is_blocked = models.BooleanField(default=False, help_text="Manually blocked by host")
    
    # Pricing
    price_per_person = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price per person for this date"
    )
    original_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Original price before discounts"
    )
    
    # Group Pricing
    group_discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Discount percentage for groups"
    )
    group_size_threshold = models.IntegerField(
        default=5,
        help_text="Minimum group size for discount"
    )
    
    # Capacity Management
    max_participants = models.IntegerField(help_text="Maximum participants for this date")
    participants_booked = models.IntegerField(default=0, help_text="Number of participants booked")
    min_participants = models.IntegerField(default=1, help_text="Minimum participants to run tour")
    
    # Tour Schedule
    start_time = models.TimeField(null=True, blank=True, help_text="Tour start time")
    end_time = models.TimeField(null=True, blank=True, help_text="Tour end time")
    
    # Special Rates
    is_special_rate = models.BooleanField(default=False)
    rate_type = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('weekend', 'Weekend Rate'),
            ('holiday', 'Holiday Rate'),
            ('peak_season', 'Peak Season'),
            ('off_season', 'Off Season'),
            ('early_bird', 'Early Bird Discount'),
            ('last_minute', 'Last Minute Deal'),
            ('group_special', 'Group Special'),
            ('custom', 'Custom Rate'),
        ]
    )
    rate_note = models.CharField(max_length=200, blank=True)
    
    # Cancellation Status
    is_cancelled = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = 'Tour Availability'
        verbose_name_plural = 'Tour Availabilities'
        unique_together = ['tour', 'date', 'start_time']
        indexes = [
            models.Index(fields=['tour', 'date']),
            models.Index(fields=['date', 'is_available']),
        ]
    
    def __str__(self):
        return f"{self.tour.name} - {self.date}"
    
    @property
    def spots_available(self):
        """Calculate remaining available spots"""
        return max(0, self.max_participants - self.participants_booked)
    
    @property
    def is_fully_booked(self):
        """Check if tour is fully booked"""
        return self.spots_available == 0
    
    @property
    def meets_minimum(self):
        """Check if minimum participants requirement is met"""
        return self.participants_booked >= self.min_participants
    
    @property
    def occupancy_percentage(self):
        """Calculate occupancy percentage"""
        if self.max_participants == 0:
            return 0
        return (self.participants_booked / self.max_participants) * 100
    
    @property
    def group_price(self):
        """Calculate price with group discount applied"""
        if self.participants_booked >= self.group_size_threshold:
            discount = self.price_per_person * (self.group_discount_percentage / 100)
            return self.price_per_person - discount
        return self.price_per_person


class CalendarBulkUpdate(models.Model):
    """
    Track bulk calendar updates for audit and undo functionality.
    Stores information about batch updates to availability/pricing.
    """
    LISTING_TYPE_CHOICES = [
        ('accommodation', 'Accommodation'),
        ('tour', 'Tour'),
    ]
    
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)
    listing_id = models.IntegerField(help_text="ID of the accommodation or tour")
    
    # Update Details
    start_date = models.DateField()
    end_date = models.DateField()
    update_type = models.CharField(
        max_length=50,
        choices=[
            ('price_change', 'Price Change'),
            ('availability_change', 'Availability Change'),
            ('block_dates', 'Block Dates'),
            ('unblock_dates', 'Unblock Dates'),
            ('minimum_stay', 'Minimum Stay Change'),
            ('special_rate', 'Special Rate Applied'),
            ('bulk_edit', 'Bulk Edit'),
        ]
    )
    
    # Update Values
    previous_values = models.JSONField(help_text="Store previous values for undo")
    new_values = models.JSONField(help_text="Store new values applied")
    
    # Metadata
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    is_undone = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Calendar Bulk Update'
        verbose_name_plural = 'Calendar Bulk Updates'
    
    def __str__(self):
        return f"{self.listing_type} #{self.listing_id} - {self.update_type} ({self.start_date} to {self.end_date})"
