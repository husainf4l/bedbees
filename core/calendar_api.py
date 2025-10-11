"""
Calendar API Views for BedBees
Handles availability and pricing management for accommodations and tours
"""

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum, Avg
from datetime import datetime, timedelta, date
from decimal import Decimal
import json

from .models import (
    Accommodation, 
    Tour, 
    AccommodationAvailability, 
    TourAvailability,
    CalendarBulkUpdate
)


@login_required
@require_http_methods(["GET"])
def get_accommodation_calendar(request, accommodation_id):
    """
    Get calendar data for a specific accommodation
    Query params: start_date, end_date (YYYY-MM-DD format)
    """
    # Filter by User, not UserProfile (host field is ForeignKey to User)
    accommodation = get_object_or_404(Accommodation, id=accommodation_id, host=request.user)
    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    
    # Get availability records for date range
    availabilities = AccommodationAvailability.objects.filter(
        accommodation=accommodation,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')
    
    # Build calendar data
    calendar_data = []
    current_date = start_date
    
    while current_date <= end_date:
        # Try to get existing availability record
        availability = availabilities.filter(date=current_date).first()
        
        if availability:
            calendar_data.append({
                'date': current_date.isoformat(),
                'is_available': availability.is_available,
                'is_blocked': availability.is_blocked,
                'price': float(availability.price_per_night),
                'original_price': float(availability.original_price) if availability.original_price else None,
                'minimum_stay': availability.minimum_stay,
                'maximum_stay': availability.maximum_stay,
                'total_rooms': availability.total_rooms,
                'rooms_available': availability.rooms_available,
                'rooms_booked': availability.rooms_booked,
                'rooms_blocked': availability.rooms_blocked,
                'is_fully_booked': availability.is_fully_booked,
                'occupancy_percentage': float(availability.occupancy_percentage),
                'is_special_rate': availability.is_special_rate,
                'rate_type': availability.rate_type,
                'rate_note': availability.rate_note,
            })
        else:
            # Use default values from accommodation
            calendar_data.append({
                'date': current_date.isoformat(),
                'is_available': True,
                'is_blocked': False,
                'price': float(accommodation.base_price) if accommodation.base_price else 0,
                'original_price': None,
                'minimum_stay': 1,
                'maximum_stay': None,
                'total_rooms': 1,
                'rooms_available': 1,
                'rooms_booked': 0,
                'rooms_blocked': 0,
                'is_fully_booked': False,
                'occupancy_percentage': 0,
                'is_special_rate': False,
                'rate_type': '',
                'rate_note': '',
            })
        
        current_date += timedelta(days=1)
    
    # Calculate statistics
    stats = {
        'total_days': len(calendar_data),
        'available_days': sum(1 for d in calendar_data if d['is_available'] and not d['is_blocked']),
        'booked_days': sum(1 for d in calendar_data if d['rooms_booked'] > 0),
        'blocked_days': sum(1 for d in calendar_data if d['is_blocked']),
        'avg_price': sum(d['price'] for d in calendar_data) / len(calendar_data) if calendar_data else 0,
        'avg_occupancy': sum(d['occupancy_percentage'] for d in calendar_data) / len(calendar_data) if calendar_data else 0,
    }
    
    return JsonResponse({
        'success': True,
        'accommodation': {
            'id': accommodation.id,
            'name': accommodation.property_name,  # Use property_name, not name
        },
        'calendar': calendar_data,
        'stats': stats,
    })


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def update_accommodation_date(request, accommodation_id):
    """
    Update availability and pricing for a specific date
    Body: JSON with date and fields to update
    """
    accommodation = get_object_or_404(Accommodation, id=accommodation_id, host=request.user.profile)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    date_str = data.get('date')
    if not date_str:
        return JsonResponse({'error': 'Date is required'}, status=400)
    
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    
    # Get or create availability record
    availability, created = AccommodationAvailability.objects.get_or_create(
        accommodation=accommodation,
        date=date_obj,
        defaults={
            'price_per_night': accommodation.price_per_night if hasattr(accommodation, 'price_per_night') else 0,
            'total_rooms': 1,
        }
    )
    
    # Update fields
    if 'is_available' in data:
        availability.is_available = bool(data['is_available'])
    if 'is_blocked' in data:
        availability.is_blocked = bool(data['is_blocked'])
    if 'price' in data:
        availability.price_per_night = Decimal(str(data['price']))
    if 'original_price' in data:
        availability.original_price = Decimal(str(data['original_price'])) if data['original_price'] else None
    if 'minimum_stay' in data:
        availability.minimum_stay = int(data['minimum_stay'])
    if 'maximum_stay' in data:
        availability.maximum_stay = int(data['maximum_stay']) if data['maximum_stay'] else None
    if 'total_rooms' in data:
        availability.total_rooms = int(data['total_rooms'])
    if 'rooms_blocked' in data:
        availability.rooms_blocked = int(data['rooms_blocked'])
    if 'is_special_rate' in data:
        availability.is_special_rate = bool(data['is_special_rate'])
    if 'rate_type' in data:
        availability.rate_type = data['rate_type']
    if 'rate_note' in data:
        availability.rate_note = data['rate_note']
    
    availability.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Date updated successfully',
        'date': date_obj.isoformat(),
        'availability': {
            'is_available': availability.is_available,
            'is_blocked': availability.is_blocked,
            'price': float(availability.price_per_night),
            'rooms_available': availability.rooms_available,
        }
    })


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def bulk_update_accommodation_dates(request, accommodation_id):
    """
    Bulk update multiple dates at once
    Body: JSON with start_date, end_date, and fields to update
    """
    accommodation = get_object_or_404(Accommodation, id=accommodation_id, host=request.user.profile)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    
    if not start_date_str or not end_date_str:
        return JsonResponse({'error': 'start_date and end_date are required'}, status=400)
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    
    if end_date < start_date:
        return JsonResponse({'error': 'end_date must be after start_date'}, status=400)
    
    # Store previous values for audit
    previous_values = {}
    new_values = {}
    
    with transaction.atomic():
        current_date = start_date
        updated_count = 0
        
        while current_date <= end_date:
            # Get or create availability record
            availability, created = AccommodationAvailability.objects.get_or_create(
                accommodation=accommodation,
                date=current_date,
                defaults={
                    'price_per_night': accommodation.price_per_night if hasattr(accommodation, 'price_per_night') else 0,
                    'total_rooms': 1,
                }
            )
            
            # Store previous values if not created
            if not created:
                previous_values[current_date.isoformat()] = {
                    'price': float(availability.price_per_night),
                    'is_available': availability.is_available,
                    'is_blocked': availability.is_blocked,
                }
            
            # Update fields
            if 'is_available' in data:
                availability.is_available = bool(data['is_available'])
            if 'is_blocked' in data:
                availability.is_blocked = bool(data['is_blocked'])
            if 'price' in data:
                availability.price_per_night = Decimal(str(data['price']))
            if 'original_price' in data:
                availability.original_price = Decimal(str(data['original_price'])) if data['original_price'] else None
            if 'minimum_stay' in data:
                availability.minimum_stay = int(data['minimum_stay'])
            if 'maximum_stay' in data:
                availability.maximum_stay = int(data['maximum_stay']) if data['maximum_stay'] else None
            if 'is_special_rate' in data:
                availability.is_special_rate = bool(data['is_special_rate'])
            if 'rate_type' in data:
                availability.rate_type = data['rate_type']
            if 'rate_note' in data:
                availability.rate_note = data['rate_note']
            
            availability.save()
            
            # Store new values
            new_values[current_date.isoformat()] = {
                'price': float(availability.price_per_night),
                'is_available': availability.is_available,
                'is_blocked': availability.is_blocked,
            }
            
            updated_count += 1
            current_date += timedelta(days=1)
        
        # Create bulk update record for audit
        CalendarBulkUpdate.objects.create(
            listing_type='accommodation',
            listing_id=accommodation.id,
            start_date=start_date,
            end_date=end_date,
            update_type=data.get('update_type', 'bulk_edit'),
            previous_values=previous_values,
            new_values=new_values,
            user=request.user,
            notes=data.get('notes', ''),
        )
    
    return JsonResponse({
        'success': True,
        'message': f'Successfully updated {updated_count} dates',
        'dates_updated': updated_count,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
    })


@login_required
@require_http_methods(["GET"])
def get_tour_calendar(request, tour_id):
    """
    Get calendar data for a specific tour
    Query params: start_date, end_date (YYYY-MM-DD format)
    """
    tour = get_object_or_404(Tour, id=tour_id, host=request.user.profile)
    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    
    # Get availability records for date range
    availabilities = TourAvailability.objects.filter(
        tour=tour,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date', 'start_time')
    
    # Build calendar data
    calendar_data = []
    
    for availability in availabilities:
        calendar_data.append({
            'id': availability.id,
            'date': availability.date.isoformat(),
            'is_available': availability.is_available,
            'is_blocked': availability.is_blocked,
            'price': float(availability.price_per_person),
            'original_price': float(availability.original_price) if availability.original_price else None,
            'max_participants': availability.max_participants,
            'spots_available': availability.spots_available,
            'participants_booked': availability.participants_booked,
            'min_participants': availability.min_participants,
            'is_fully_booked': availability.is_fully_booked,
            'meets_minimum': availability.meets_minimum,
            'occupancy_percentage': float(availability.occupancy_percentage),
            'start_time': availability.start_time.isoformat() if availability.start_time else None,
            'end_time': availability.end_time.isoformat() if availability.end_time else None,
            'is_special_rate': availability.is_special_rate,
            'rate_type': availability.rate_type,
            'rate_note': availability.rate_note,
            'group_discount_percentage': float(availability.group_discount_percentage),
            'group_size_threshold': availability.group_size_threshold,
        })
    
    # Calculate statistics
    stats = {
        'total_slots': len(calendar_data),
        'available_slots': sum(1 for d in calendar_data if d['is_available'] and not d['is_blocked']),
        'booked_slots': sum(1 for d in calendar_data if d['participants_booked'] > 0),
        'fully_booked': sum(1 for d in calendar_data if d['is_fully_booked']),
        'avg_price': sum(d['price'] for d in calendar_data) / len(calendar_data) if calendar_data else 0,
        'avg_occupancy': sum(d['occupancy_percentage'] for d in calendar_data) / len(calendar_data) if calendar_data else 0,
    }
    
    return JsonResponse({
        'success': True,
        'tour': {
            'id': tour.id,
            'name': tour.name,
        },
        'calendar': calendar_data,
        'stats': stats,
    })


@login_required
@require_http_methods(["GET"])
def get_public_accommodation_availability(request, accommodation_id):
    """
    Public endpoint to check accommodation availability (for listing pages)
    Query params: start_date, end_date
    """
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)
    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if not start_date_str or not end_date_str:
        return JsonResponse({'error': 'start_date and end_date are required'}, status=400)
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
    
    # Get availability for date range
    availabilities = AccommodationAvailability.objects.filter(
        accommodation=accommodation,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')
    
    calendar_data = {}
    current_date = start_date
    
    while current_date <= end_date:
        availability = availabilities.filter(date=current_date).first()
        
        if availability:
            calendar_data[current_date.isoformat()] = {
                'available': availability.is_available and not availability.is_blocked and availability.rooms_available > 0,
                'price': float(availability.price_per_night),
                'rooms_available': availability.rooms_available,
                'minimum_stay': availability.minimum_stay,
            }
        else:
            # Default: available with base price
            calendar_data[current_date.isoformat()] = {
                'available': True,
                'price': float(accommodation.price_per_night) if hasattr(accommodation, 'price_per_night') else 0,
                'rooms_available': 1,
                'minimum_stay': 1,
            }
        
        current_date += timedelta(days=1)
    
    return JsonResponse({
        'success': True,
        'availability': calendar_data,
    })


@login_required
@require_http_methods(["GET"])
def get_user_accommodations(request):
    """
    Get all accommodations for the logged-in host
    """
    # Check if user has host profile
    if hasattr(request.user, 'profile') and not request.user.profile.is_host:
        return JsonResponse({'error': 'User is not a host'}, status=403)
    
    # Filter by the User, not UserProfile (host field is ForeignKey to User)
    accommodations = Accommodation.objects.filter(host=request.user).values(
        'id', 'property_name', 'property_type', 'city', 'country'
    )
    
    # Format the response with 'name' key for frontend compatibility
    accommodations_list = []
    for acc in accommodations:
        accommodations_list.append({
            'id': acc['id'],
            'name': acc['property_name'],
            'property_type': acc['property_type'],
            'city': acc['city'],
            'country': acc['country'],
        })
    
    return JsonResponse({
        'success': True,
        'accommodations': accommodations_list,
    })


@login_required
@require_http_methods(["GET"])
def get_user_tours(request):
    """
    Get all tours for the logged-in host
    """
    # Check if user has host profile
    if hasattr(request.user, 'profile') and not request.user.profile.is_host:
        return JsonResponse({'error': 'User is not a host'}, status=403)
    
    # Filter by the User, not UserProfile (host field is ForeignKey to User)
    tours = Tour.objects.filter(host=request.user).values(
        'id', 'name', 'category', 'city', 'country'
    )
    
    return JsonResponse({
        'success': True,
        'tours': list(tours),
    })
