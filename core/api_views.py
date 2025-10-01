from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Listing, RoomType, AvailabilityDay, DayRoomInventory,
    UserProfile
)
from .serializers import (
    CalendarDaySerializer, DayRoomInventorySerializer,
    BulkCalendarUpdateSerializer, DayUpdateSerializer,
    DayRoomUpdateSerializer
)
from .permissions import IsListingOwner, IsListingOwnerFromParams
import logging

logger = logging.getLogger(__name__)


class CalendarViewSet(viewsets.ViewSet):
    """Calendar API for multi-room type accommodation management"""
    permission_classes = [IsAuthenticated, IsListingOwnerFromParams]

    def get_listing(self, listing_id):
        """Get listing and verify ownership"""
        listing = get_object_or_404(Listing, id=listing_id)
        self.check_object_permissions(self.request, listing)
        return listing

    @action(detail=False, methods=['get'], url_path='listing/(?P<listing_id>[^/.]+)')
    def get_calendar(self, request, listing_id=None):
        """Get calendar data for a listing within date range"""
        try:
            listing = self.get_listing(listing_id)
            
            # Parse date range
            from_date = request.query_params.get('from')
            to_date = request.query_params.get('to')
            
            if not from_date or not to_date:
                return Response(
                    {'error': 'Both from and to dates are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if from_date >= to_date:
                return Response(
                    {'error': 'from_date must be before to_date'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get all dates in range
            current_date = from_date
            calendar_data = []
            
            while current_date <= to_date:
                day_data = self._get_day_data(listing, current_date)
                calendar_data.append(day_data)
                current_date += timedelta(days=1)
            
            return Response({
                'listing': {
                    'id': listing.id,
                    'name': listing.name,
                    'currency': listing.currency,
                    'default_price': str(listing.default_price),
                    'default_min_stay': listing.default_min_stay,
                },
                'calendar': calendar_data
            })
            
        except Exception as e:
            logger.error(f"Error getting calendar: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _get_day_data(self, listing, date):
        """Get comprehensive day data including room inventory"""
        # Get availability day data
        try:
            availability_day = AvailabilityDay.objects.get(listing=listing, date=date)
            day_status = availability_day.status
            day_price = availability_day.price
            day_min_stay = availability_day.min_stay
            day_notes = availability_day.notes
        except AvailabilityDay.DoesNotExist:
            day_status = 'OPEN'
            day_price = None
            day_min_stay = None
            day_notes = None
        
        # Get room inventory data
        room_inventory = []
        total_available = 0
        total_capacity = 0
        stop_sell_count = 0
        
        for room_type in listing.room_types.filter(is_active=True):
            try:
                inventory = DayRoomInventory.objects.get(
                    listing=listing,
                    room_type=room_type,
                    date=date
                )
                available = inventory.available
                total_available += available
                total_capacity += room_type.total_units
                if inventory.stop_sell:
                    stop_sell_count += 1
                
                room_inventory.append({
                    'room_type_id': room_type.id,
                    'room_name': room_type.name,
                    'base_price': str(room_type.base_price),
                    'total_units': room_type.total_units,
                    'units_open': inventory.units_open,
                    'units_booked': inventory.units_booked,
                    'available': available,
                    'stop_sell': inventory.stop_sell,
                    'cta': inventory.cta,
                    'ctd': inventory.ctd,
                    'override_price': str(inventory.override_price) if inventory.override_price else None,
                    'note': inventory.note,
                })
            except DayRoomInventory.DoesNotExist:
                # No inventory record - assume all units available at base price
                available = room_type.total_units
                total_available += available
                total_capacity += room_type.total_units
                
                room_inventory.append({
                    'room_type_id': room_type.id,
                    'room_name': room_type.name,
                    'base_price': str(room_type.base_price),
                    'total_units': room_type.total_units,
                    'units_open': room_type.total_units,
                    'units_booked': 0,
                    'available': available,
                    'stop_sell': False,
                    'cta': False,
                    'ctd': False,
                    'override_price': None,
                    'note': None,
                })
        
        # Calculate summary status
        if day_status in ['CLOSED', 'BLOCKED']:
            effective_status = day_status
        elif stop_sell_count == len(room_inventory):
            effective_status = 'STOP_SELL'
        elif total_available == 0:
            effective_status = 'FULL'
        else:
            effective_status = 'OPEN'
        
        return {
            'date': date.isoformat(),
            'status': day_status,
            'effective_status': effective_status,
            'price': str(day_price) if day_price else None,
            'min_stay': day_min_stay,
            'notes': day_notes,
            'summary': {
                'total_rooms': len(room_inventory),
                'available_rooms': len([r for r in room_inventory if r['available'] > 0 and not r['stop_sell']]),
                'total_capacity': total_capacity,
                'total_available': total_available,
                'stop_sell_count': stop_sell_count,
            },
            'rooms': room_inventory,
        }

    @action(detail=False, methods=['patch'], url_path='day')
    def update_day(self, request):
        """Update availability and pricing for a specific day"""
        try:
            listing_id = request.data.get('listing')
            date_str = request.data.get('date')
            
            if not listing_id or not date_str:
                return Response(
                    {'error': 'listing and date are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            listing = self.get_listing(listing_id)
            
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update or create availability day
            availability_day, created = AvailabilityDay.objects.get_or_create(
                listing=listing,
                date=date,
                defaults={}
            )
            
            # Update fields
            if 'status' in request.data:
                availability_day.status = request.data['status']
            if 'price' in request.data:
                availability_day.price = request.data['price']
            if 'min_stay' in request.data:
                availability_day.min_stay = request.data['min_stay']
            if 'notes' in request.data:
                availability_day.notes = request.data['notes']
            
            availability_day.save()
            
            return Response({
                'success': True,
                'message': f'Day {date} updated successfully',
                'data': self._get_day_data(listing, date)
            })
            
        except Exception as e:
            logger.error(f"Error updating day: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['patch'], url_path='day/rooms')
    def update_day_rooms(self, request):
        """Update room inventory for a specific day"""
        try:
            listing_id = request.data.get('listing')
            date_str = request.data.get('date')
            room_updates = request.data.get('rooms', [])
            
            if not listing_id or not date_str or not room_updates:
                return Response(
                    {'error': 'listing, date, and rooms are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            listing = self.get_listing(listing_id)
            
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            errors = []
            updated_rooms = []
            
            for room_data in room_updates:
                room_type_id = room_data.get('room_type_id')
                if not room_type_id:
                    errors.append({'error': 'room_type_id is required for each room update'})
                    continue
                
                try:
                    room_type = RoomType.objects.get(id=room_type_id, listing=listing)
                except RoomType.DoesNotExist:
                    errors.append({'room_type_id': room_type_id, 'error': 'Room type not found'})
                    continue
                
                # Validate units_open
                units_open = room_data.get('units_open', room_type.total_units)
                if units_open < 0 or units_open > room_type.total_units:
                    errors.append({
                        'room_type_id': room_type_id,
                        'error': f'units_open must be between 0 and {room_type.total_units}'
                    })
                    continue
                
                # Get or create inventory record
                inventory, created = DayRoomInventory.objects.get_or_create(
                    listing=listing,
                    room_type=room_type,
                    date=date,
                    defaults={'units_open': room_type.total_units}
                )
                
                # Check if reducing units_open below booked units
                units_booked = inventory.units_booked
                if units_open < units_booked:
                    errors.append({
                        'room_type_id': room_type_id,
                        'error': f'Cannot reduce units_open below {units_booked} booked units'
                    })
                    continue
                
                # Update inventory
                inventory.units_open = units_open
                if 'stop_sell' in room_data:
                    inventory.stop_sell = room_data['stop_sell']
                if 'cta' in room_data:
                    inventory.cta = room_data['cta']
                if 'ctd' in room_data:
                    inventory.ctd = room_data['ctd']
                if 'override_price' in room_data:
                    override_price = room_data['override_price']
                    if override_price is not None and override_price < 0:
                        errors.append({
                            'room_type_id': room_type_id,
                            'error': 'override_price cannot be negative'
                        })
                        continue
                    inventory.override_price = override_price
                if 'note' in room_data:
                    inventory.note = room_data['note']
                
                inventory.save()
                updated_rooms.append(room_type_id)
            
            if errors:
                return Response({
                    'success': False,
                    'errors': errors,
                    'message': f'Updated {len(updated_rooms)} rooms, {len(errors)} errors'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'success': True,
                'message': f'Updated {len(updated_rooms)} rooms successfully',
                'data': self._get_day_data(listing, date)
            })
            
        except Exception as e:
            logger.error(f"Error updating day rooms: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='bulk')
    def bulk_update(self, request):
        """Bulk update calendar data across multiple dates"""
        try:
            listing_id = request.data.get('listing')
            date_range = request.data.get('date_range')
            weekday_filter = request.data.get('weekday_filter')  # Optional: [0-6] for Mon-Sun
            updates = request.data.get('updates', {})
            
            if not listing_id or not date_range:
                return Response(
                    {'error': 'listing and date_range are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            listing = self.get_listing(listing_id)
            
            # Parse date range
            try:
                from_date = datetime.strptime(date_range['from'], '%Y-%m-%d').date()
                to_date = datetime.strptime(date_range['to'], '%Y-%m-%d').date()
            except (KeyError, ValueError):
                return Response(
                    {'error': 'Invalid date_range format. Use {"from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if from_date >= to_date:
                return Response(
                    {'error': 'from_date must be before to_date'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Generate dates to update
            dates_to_update = []
            current_date = from_date
            while current_date <= to_date:
                if not weekday_filter or current_date.weekday() in weekday_filter:
                    dates_to_update.append(current_date)
                current_date += timedelta(days=1)
            
            if not dates_to_update:
                return Response(
                    {'error': 'No dates match the specified criteria'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            errors = []
            updated_dates = []
            
            with transaction.atomic():
                for date in dates_to_update:
                    try:
                        # Update availability day if specified
                        if any(key in updates for key in ['status', 'price', 'min_stay', 'notes']):
                            availability_day, created = AvailabilityDay.objects.get_or_create(
                                listing=listing,
                                date=date,
                                defaults={}
                            )
                            
                            if 'status' in updates:
                                availability_day.status = updates['status']
                            if 'price' in updates:
                                availability_day.price = updates['price']
                            if 'min_stay' in updates:
                                availability_day.min_stay = updates['min_stay']
                            if 'notes' in updates:
                                availability_day.notes = updates['notes']
                            
                            availability_day.save()
                        
                        # Update room inventory if specified
                        if any(key in updates for key in ['units_open', 'stop_sell', 'cta', 'ctd', 'override_price', 'note']):
                            for room_type in listing.room_types.filter(is_active=True):
                                inventory, created = DayRoomInventory.objects.get_or_create(
                                    listing=listing,
                                    room_type=room_type,
                                    date=date,
                                    defaults={'units_open': room_type.total_units}
                                )
                                
                                # Apply inventory updates
                                if 'units_open' in updates:
                                    units_open = updates['units_open']
                                    # Handle percentage
                                    if isinstance(units_open, str) and units_open.endswith('%'):
                                        percentage = float(units_open[:-1]) / 100
                                        units_open = int(room_type.total_units * percentage)
                                    
                                    if units_open < inventory.units_booked:
                                        errors.append({
                                            'date': date.isoformat(),
                                            'room_type': room_type.name,
                                            'error': f'Cannot set units_open below {inventory.units_booked} booked units'
                                        })
                                        continue
                                    
                                    inventory.units_open = min(units_open, room_type.total_units)
                                
                                if 'stop_sell' in updates:
                                    inventory.stop_sell = updates['stop_sell']
                                if 'cta' in updates:
                                    inventory.cta = updates['cta']
                                if 'ctd' in updates:
                                    inventory.ctd = updates['ctd']
                                if 'override_price' in updates:
                                    override_price = updates['override_price']
                                    if isinstance(override_price, str) and override_price.startswith('+'):
                                        # Relative price adjustment
                                        adjustment = float(override_price[1:])
                                        base_price = inventory.override_price or room_type.base_price
                                        inventory.override_price = base_price * (1 + adjustment / 100)
                                    elif isinstance(override_price, str) and override_price.startswith('-'):
                                        # Relative price adjustment
                                        adjustment = float(override_price[1:])
                                        base_price = inventory.override_price or room_type.base_price
                                        inventory.override_price = base_price * (1 - adjustment / 100)
                                    else:
                                        inventory.override_price = override_price
                                if 'note' in updates:
                                    inventory.note = updates['note']
                                
                                inventory.save()
                        
                        updated_dates.append(date.isoformat())
                        
                    except Exception as e:
                        errors.append({
                            'date': date.isoformat(),
                            'error': str(e)
                        })
            
            if errors:
                return Response({
                    'success': False,
                    'errors': errors,
                    'message': f'Updated {len(updated_dates)} dates, {len(errors)} errors'
                }, status=status.HTTP_207_MULTI_STATUS)
            
            return Response({
                'success': True,
                'message': f'Successfully updated {len(updated_dates)} dates',
                'updated_dates': updated_dates
            })
            
        except Exception as e:
            logger.error(f"Error in bulk update: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
