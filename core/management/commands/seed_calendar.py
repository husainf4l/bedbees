from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from datetime import date, timedelta
from decimal import Decimal
import random
from ...models import Listing, RoomType, AvailabilityDay, DayRoomInventory


class Command(BaseCommand):
    help = 'Seed calendar data for October 2025 with realistic availability patterns'

    def add_arguments(self, parser):
        parser.add_argument(
            '--listing-id',
            type=int,
            help='Specific listing ID to seed (optional - seeds all listings if not provided)',
        )
        parser.add_argument(
            '--clear-existing',
            action='store_true',
            help='Clear existing calendar data before seeding',
        )

    def handle(self, *args, **options):
        listing_id = options.get('listing_id')
        clear_existing = options.get('clear_existing')
        
        if listing_id:
            try:
                listing = Listing.objects.get(id=listing_id)
                listings = [listing]
            except Listing.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Listing with ID {listing_id} does not exist')
                )
                return
        else:
            listings = Listing.objects.filter(is_active=True)
        
        if not listings:
            self.stdout.write(
                self.style.WARNING('No active listings found to seed')
            )
            return
        
        self.stdout.write(f'Seeding calendar data for {len(listings)} listing(s)...')
        
        with transaction.atomic():
            if clear_existing:
                self.stdout.write('Clearing existing calendar data...')
                if listing_id:
                    AvailabilityDay.objects.filter(listing_id=listing_id).delete()
                    DayRoomInventory.objects.filter(listing_id=listing_id).delete()
                else:
                    AvailabilityDay.objects.all().delete()
                    DayRoomInventory.objects.all().delete()
            
            # Seed October 2025 (31 days)
            start_date = date(2025, 10, 1)
            end_date = date(2025, 10, 31)
            
            total_days = (end_date - start_date).days + 1
            total_records = 0
            
            for listing in listings:
                self.stdout.write(f'Seeding listing: {listing.name}')
                
                # Get room types for this listing
                room_types = list(listing.room_types.filter(is_active=True))
                if not room_types:
                    self.stdout.write(
                        self.style.WARNING(f'No active room types for listing {listing.name}, skipping...')
                    )
                    continue
                
                current_date = start_date
                while current_date <= end_date:
                    # Generate realistic availability patterns
                    day_of_week = current_date.weekday()  # 0=Monday, 6=Sunday
                    
                    # Weekend pricing (Friday-Sunday)
                    is_weekend = day_of_week in [4, 5, 6]  # Friday, Saturday, Sunday
                    
                    # Seasonal patterns (mid-October might be peak)
                    is_peak = 10 <= current_date.day <= 20
                    
                    # Random events (closed/blocked days)
                    is_closed = random.random() < 0.05  # 5% chance of being closed
                    is_blocked = random.random() < 0.02  # 2% chance of being blocked
                    
                    # Base price calculation
                    base_price = listing.default_price or Decimal('100.00')
                    if is_weekend:
                        price_multiplier = Decimal('1.2')  # 20% weekend premium
                    elif is_peak:
                        price_multiplier = Decimal('1.1')  # 10% peak season premium
                    else:
                        price_multiplier = Decimal('0.9')  # 10% weekday discount
                    
                    final_price = base_price * price_multiplier
                    
                    # Create availability day
                    if is_closed:
                        status = 'CLOSED'
                        final_price = None
                    elif is_blocked:
                        status = 'BLOCKED'
                        final_price = None
                    else:
                        status = 'OPEN'
                    
                    availability_day = AvailabilityDay.objects.create(
                        listing=listing,
                        date=current_date,
                        status=status,
                        price=final_price,
                        min_stay=listing.default_min_stay or 1,
                        notes=self._generate_notes(current_date, status)
                    )
                    
                    # Create room inventory for each room type
                    for room_type in room_types:
                        # Simulate bookings (reduce available units)
                        booking_probability = 0.3 if is_weekend else 0.2  # Higher bookings on weekends
                        if status in ['CLOSED', 'BLOCKED']:
                            units_booked = 0
                            units_open = 0
                        else:
                            # Random bookings
                            max_bookings = min(room_type.total_units, 3)  # Max 3 units booked per room type
                            units_booked = random.randint(0, max_bookings) if random.random() < booking_probability else 0
                            units_open = max(0, room_type.total_units - units_booked)
                        
                        # Random stop-sell (5% chance)
                        stop_sell = random.random() < 0.05 and status == 'OPEN'
                        
                        # Price override (10% chance)
                        override_price = None
                        if random.random() < 0.1 and status == 'OPEN':
                            override_multiplier = Decimal(str(random.uniform(0.8, 1.3)))
                            override_price = room_type.base_price * override_multiplier
                        
                        DayRoomInventory.objects.create(
                            listing=listing,
                            room_type=room_type,
                            date=current_date,
                            units_open=units_open,
                            units_booked=units_booked,
                            stop_sell=stop_sell,
                            cta=random.random() < 0.02,  # 2% chance
                            ctd=random.random() < 0.02,  # 2% chance
                            override_price=override_price,
                            note=self._generate_room_note(current_date, room_type) if random.random() < 0.1 else None
                        )
                    
                    current_date += timedelta(days=1)
                    total_records += 1
                    
                    # Progress indicator
                    if total_records % 100 == 0:
                        self.stdout.write(f'Processed {total_records} records...')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully seeded {total_records} calendar records for October 2025'
                )
            )
    
    def _generate_notes(self, date, status):
        """Generate realistic notes for availability days"""
        notes_templates = {
            'CLOSED': [
                'Maintenance day',
                'Private event',
                'Staff holiday',
                'Cleaning day',
                'Under renovation'
            ],
            'BLOCKED': [
                'Booked for private event',
                'Reserved for maintenance',
                'Unavailable for booking',
                'Blocked for special occasion'
            ],
            'OPEN': [
                'Standard rates apply',
                'Early check-in available',
                'Late checkout possible',
                'Breakfast included',
                'Welcome discount available'
            ]
        }
        
        if status in notes_templates and random.random() < 0.3:  # 30% chance of having notes
            return random.choice(notes_templates[status])
        return None
    
    def _generate_room_note(self, date, room_type):
        """Generate realistic notes for room inventory"""
        notes = [
            f'Special rate for {room_type.name}',
            'Limited availability',
            'Best available rate',
            'Non-refundable',
            'Flexible cancellation',
            'Includes breakfast',
            'Ocean view upgrade',
            'Premium location'
        ]
        return random.choice(notes) if random.random() < 0.5 else None
