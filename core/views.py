from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import HostRegistrationForm, HostProfileForm, AccommodationForm, TourForm, TourGuideForm, RentalCarForm
from .models import UserProfile, Accommodation, Tour, AccommodationPhoto, TourPhoto, TourGuide, TourGuidePhoto, RentalCar, RentalCarPhoto, Country

def home(request):
    """Home page view with role-based access"""
    # If user is authenticated, redirect based on their role
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.is_host:
                # Hosts should go directly to their dashboard
                return redirect('hostdashboard')
            else:
                # Travelers can access home page and all other pages
                pass
        except UserProfile.DoesNotExist:
            # Create profile for traveler if it doesn't exist
            UserProfile.objects.create(user=request.user, is_host=False)
    
    # Get data for homepage display
    countries = Country.objects.all()[:8]  # Limit to 8 for display
    accommodations = Accommodation.objects.filter(
        is_published=True, 
        is_active=True
    ).select_related('host').prefetch_related('photos')[:6]
    tours = Tour.objects.filter(
        is_published=True, 
        is_active=True
    ).select_related('host').prefetch_related('photos')[:6]
    
    context = {
        'countries': countries,
        'accommodations': accommodations,
        'tours': tours,
    }
    
    return render(request, 'core/home.html', context)

def search_results(request):
    """Search results page with filters"""
    # Get filter parameters from request
    search_type = request.GET.get('type', 'hotels')  # hotels or tours
    destination = request.GET.get('destination', '')
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    adults = request.GET.get('adults', '1')
    children = request.GET.get('children', '0')
    rooms = request.GET.get('rooms', '1')
    min_price = request.GET.get('min_price', '0')
    max_price = request.GET.get('max_price', '1000')

    # Property/Tour type filters
    property_types = request.GET.getlist('property_type')
    tour_types = request.GET.getlist('tour_type')

    # Star rating
    star_ratings = request.GET.getlist('star_rating')

    # Amenities
    amenities = request.GET.getlist('amenities')

    # Tour inclusions
    tour_inclusions = request.GET.getlist('tour_inclusions')

    # Review score
    review_score = request.GET.get('review_score', '')

    # Booking policies
    free_cancellation = request.GET.get('free_cancellation', False)
    no_prepayment = request.GET.get('no_prepayment', False)

    # Accessibility
    wheelchair = request.GET.get('wheelchair', False)
    elevator = request.GET.get('elevator', False)

    # Sorting
    sort_by = request.GET.get('sort', 'popular')

    # Query database based on search type
    if search_type == 'tours':
        results = Tour.objects.filter(
            is_published=True,
            is_active=True
        ).select_related('host').prefetch_related('photos')

        # Apply filters
        if destination:
            results = results.filter(city__icontains=destination)

        if min_price and max_price:
            results = results.filter(base_price__gte=min_price, base_price__lte=max_price)

    else:  # hotels/accommodations
        results = Accommodation.objects.filter(
            is_published=True,
            is_active=True
        ).select_related('host').prefetch_related('photos')

        # Apply filters
        if destination:
            results = results.filter(city__icontains=destination)

        if min_price and max_price:
            results = results.filter(base_price__gte=min_price, base_price__lte=max_price)

        if property_types:
            results = results.filter(property_type__in=property_types)

    # Apply sorting
    if sort_by == 'price_low':
        results = results.order_by('base_price')
    elif sort_by == 'price_high':
        results = results.order_by('-base_price')
    elif sort_by == 'newest':
        results = results.order_by('-created_at')
    else:
        results = results.order_by('-created_at')  # Default

    context = {
        'results': results,
        'search_type': search_type,
        'destination': destination,
        'checkin': checkin,
        'checkout': checkout,
        'adults': adults,
        'children': children,
        'rooms': rooms,
        'min_price': min_price,
        'max_price': max_price,
        'property_types': property_types,
        'tour_types': tour_types,
        'star_ratings': star_ratings,
        'amenities': amenities,
        'tour_inclusions': tour_inclusions,
        'review_score': review_score,
        'free_cancellation': free_cancellation,
        'no_prepayment': no_prepayment,
        'wheelchair': wheelchair,
        'elevator': elevator,
        'sort_by': sort_by,
        'results_count': results.count(),
    }

    return render(request, 'core/search_results.html', context)

def tours(request, category=None):
    """Tours page view"""

    # Get real tours from database (both published AND active)
    real_tours = Tour.objects.filter(
        is_published=True,
        is_active=True
    ).select_related('host')

    # Demo tours data (fallback if no real listings)
    demo_tours = [
        {
            'id': '1',
            'title': 'Historic Cyprus Cultural Walking Tour',
            'location': 'Nicosia, Cyprus',
            'description': 'Discover the rich history and culture of Cyprus\'s capital city through hidden alleys, ancient architecture, and local stories.',
            'price': 25,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Small groups (4-12)',
            'rating': 4.8,
            'reviews': 1850,
            'category': 'cultural',
            'tags': ['culture', 'history', 'walking'],
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '2',
            'title': 'Private Troodos Mountains Adventure',
            'location': 'Troodos, Cyprus',
            'description': 'Experience the stunning Troodos Mountains with a personalized private tour including waterfalls, traditional villages, and wine tasting.',
            'price': 150,
            'currency': 'USD',
            'duration': '8 hours',
            'group_size': 'Private (1-6)',
            'rating': 4.9,
            'reviews': 318,
            'category': 'private',
            'tags': ['mountains', 'nature', 'wine', 'private'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '13',
            'title': 'Private Dubai Luxury City Tour',
            'location': 'Dubai, UAE',
            'description': 'Exclusive private tour of Dubai with luxury vehicle, personal guide, and VIP access to iconic landmarks.',
            'price': 280,
            'currency': 'USD',
            'duration': '6 hours',
            'group_size': 'Private (1-8)',
            'rating': 4.8,
            'reviews': 456,
            'category': 'private',
            'tags': ['luxury', 'city', 'landmarks', 'private'],
            'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '14',
            'title': 'Private Jordan Petra & Wadi Rum Experience',
            'location': 'Petra & Wadi Rum, Jordan',
            'description': 'Private 2-day adventure exploring Petra ancient city and camping under stars in Wadi Rum desert.',
            'price': 480,
            'currency': 'USD',
            'duration': '2 days',
            'group_size': 'Private (1-4)',
            'rating': 4.9,
            'reviews': 234,
            'category': 'private',
            'tags': ['adventure', 'desert', 'petra', 'private'],
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '15',
            'title': 'Private Istanbul Cultural Heritage Tour',
            'location': 'Istanbul, Turkey',
            'description': 'Personalized tour of Istanbul\'s historic sites with private guide, skip-the-line access, and traditional Turkish lunch.',
            'price': 195,
            'currency': 'USD',
            'duration': '7 hours',
            'group_size': 'Private (1-6)',
            'rating': 4.8,
            'reviews': 678,
            'category': 'private',
            'tags': ['culture', 'history', 'heritage', 'private'],
            'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '16',
            'title': 'Private Santorini Sunset & Wine Tour',
            'location': 'Santorini, Greece',
            'description': 'Exclusive private tour of Santorini\'s wineries with sunset viewing at Oia and gourmet wine tasting.',
            'price': 320,
            'currency': 'USD',
            'duration': '5 hours',
            'group_size': 'Private (1-6)',
            'rating': 4.9,
            'reviews': 389,
            'category': 'private',
            'tags': ['wine', 'sunset', 'romantic', 'private'],
            'image': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80'
        },
        {
            'id': '17',
            'title': 'Private Cappadocia Hot Air Balloon & Tour',
            'location': 'Cappadocia, Turkey',
            'description': 'Private hot air balloon flight followed by personalized underground cities and fairy chimneys exploration.',
            'price': 420,
            'currency': 'USD',
            'duration': '8 hours',
            'group_size': 'Private (1-4)',
            'rating': 4.8,
            'reviews': 567,
            'category': 'private',
            'tags': ['balloon', 'adventure', 'unique', 'private'],
            'image': 'https://images.unsplash.com/photo-1578271887552-5ac9e7c7b5d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '18',
            'title': 'Private Doha Modern & Traditional Tour',
            'location': 'Doha, Qatar',
            'description': 'Personalized exploration of Doha combining modern skyscrapers with traditional souqs and cultural sites.',
            'price': 240,
            'currency': 'USD',
            'duration': '6 hours',
            'group_size': 'Private (1-8)',
            'rating': 4.7,
            'reviews': 123,
            'category': 'private',
            'tags': ['modern', 'traditional', 'culture', 'private'],
            'image': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '19',
            'title': 'Private Beirut Food & Culture Walking Tour',
            'location': 'Beirut, Lebanon',
            'description': 'Private culinary journey through Beirut\'s neighborhoods with local food tastings and cultural insights.',
            'price': 125,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': 'Private (1-6)',
            'rating': 4.8,
            'reviews': 345,
            'category': 'private',
            'tags': ['food', 'culture', 'walking', 'private'],
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '3',
            'title': 'Paphos Archaeological Group Tour',
            'location': 'Paphos, Cyprus',
            'description': 'Join a group of history enthusiasts to explore the UNESCO World Heritage archaeological sites of Paphos with an expert archaeologist guide.',
            'price': 35,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': 'Groups (8-20)',
            'rating': 4.7,
            'reviews': 624,
            'category': 'group',
            'tags': ['archaeology', 'history', 'unesco', 'group'],
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '4',
            'title': 'Sinai Mountain Sunrise Trek',
            'location': 'Mount Sinai, Egypt',
            'description': 'Experience the breathtaking sunrise from the summit of Mount Sinai, following the ancient path of Moses.',
            'price': 85,
            'currency': 'USD',
            'duration': '12 hours',
            'group_size': 'Small groups (4-15)',
            'rating': 4.6,
            'reviews': 892,
            'category': 'adventure',
            'tags': ['adventure', 'spiritual', 'sunrise', 'hiking'],
            'image': 'https://images.unsplash.com/photo-1464822759844-d150f38d609c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '5',
            'title': 'Red Sea Scuba Diving Adventure',
            'location': 'Aqaba, Jordan',
            'description': 'Explore the vibrant underwater world of the Red Sea with professional PADI-certified instructors.',
            'price': 185,
            'currency': 'USD',
            'duration': '5 hours',
            'group_size': 'Small groups (1-6)',
            'rating': 4.8,
            'reviews': 756,
            'category': 'adventure',
            'tags': ['diving', 'scuba', 'marine', 'water'],
            'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '6',
            'title': 'Lebanon Paragliding Experience',
            'location': 'Harissa, Lebanon',
            'description': 'Soar above the stunning Lebanese coastline and mountains in a tandem paragliding flight.',
            'price': 220,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Private or small groups',
            'rating': 4.5,
            'reviews': 433,
            'category': 'adventure',
            'tags': ['paragliding', 'adventure', 'views', 'flying'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '7',
            'title': 'Traditional Middle Eastern Cooking Class',
            'location': 'Various locations',
            'description': 'Learn to cook authentic local cuisine with expert chefs. Includes market visit and hands-on cooking.',
            'price': 65,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': 'Small groups (max 12)',
            'rating': 4.7,
            'reviews': 1245,
            'category': 'food',
            'tags': ['cooking', 'culinary', 'food', 'class'],
            'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '8',
            'title': 'Jerusalem Old City Walking Tour',
            'location': 'Jerusalem, Palestine',
            'description': 'Explore the ancient streets of Jerusalem\'s Old City, visiting sacred sites of three major religions.',
            'price': 45,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': 'Small groups (max 15)',
            'rating': 4.8,
            'reviews': 2156,
            'category': 'walking',
            'tags': ['walking', 'historical', 'religious', 'cultural'],
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '9',
            'title': 'Petra by Night Experience',
            'location': 'Petra, Jordan',
            'description': 'Experience the magical atmosphere of Petra illuminated by candles, with traditional Bedouin music and storytelling.',
            'price': 45,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Small groups (max 20)',
            'rating': 4.9,
            'reviews': 1876,
            'category': 'cultural',
            'tags': ['petra', 'night', 'cultural', 'bedouin'],
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '10',
            'title': 'Dubai Desert Safari with BBQ',
            'location': 'Dubai, UAE',
            'description': 'Thrilling desert adventure with dune bashing, camel riding, traditional BBQ dinner, and belly dancing.',
            'price': 85,
            'currency': 'USD',
            'duration': '6 hours',
            'group_size': 'Groups (4-6)',
            'rating': 4.7,
            'reviews': 3245,
            'category': 'adventure',
            'tags': ['desert', 'safari', 'dune', 'bbq'],
            'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '11',
            'title': 'Amman Roman Theater Exploration',
            'location': 'Amman, Jordan',
            'description': 'Step back in time at Amman\'s Roman Theater, explore the ancient Citadel, and experience Jordan\'s modern capital.',
            'price': 35,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': 'Small groups',
            'rating': 4.6,
            'reviews': 987,
            'category': 'cultural',
            'tags': ['roman', 'theater', 'history', 'amman'],
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        },
        {
            'id': '12',
            'title': 'Muscat Coastal Dhow Cruise',
            'location': 'Muscat, Oman',
            'description': 'Experience Oman\'s stunning coastline with a traditional dhow cruise, visiting forts and fishing villages.',
            'price': 75,
            'currency': 'USD',
            'duration': '6 hours',
            'group_size': 'Small private groups',
            'rating': 4.8,
            'reviews': 654,
            'category': 'cultural',
            'tags': ['dhow', 'coastal', 'cruise', 'oman'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        }
    ]

    # Handle search functionality
    search_query = request.GET.get('q', '').strip()
    tours = demo_tours

    if search_query:
        # Filter tours based on search query
        filtered_tours = []
        query_lower = search_query.lower()

        for tour in demo_tours:
            # Search in title, location, description, category, and tags
            if (query_lower in tour['title'].lower() or
                query_lower in tour['location'].lower() or
                query_lower in tour['description'].lower() or
                query_lower in tour['category'].lower() or
                any(query_lower in tag.lower() for tag in tour['tags'])):
                filtered_tours.append(tour)

        tours = filtered_tours

    # Category mapping
    category_mapping = {
        'share-trip': 'share_trip',
        'private': 'private',
        'group': 'group',
        'cultural': 'cultural',
        'adventure': 'adventure',
        'food': 'food',
        'walking': 'walking',
        'all': None
    }

    # Filter tours by category (in addition to search)
    if category and category.lower() in category_mapping and not search_query:
        filter_cat = category_mapping[category.lower()]
        if filter_cat:
            tours = [tour for tour in tours if tour['category'] == filter_cat]

    # Category display names
    category_names = {
        'share-trip': 'Share Trip Tours',
        'private': 'Private Tours',
        'group': 'Group Tours',
        'cultural': 'Cultural Experiences',
        'adventure': 'Adventure & Outdoor',
        'food': 'Food Tours',
        'walking': 'Walking Tours',
        'all': 'Explore All Experiences'
    }

    display_category = category_names.get(category, 'Explore All Experiences') if category else 'Explore All Experiences'

    # Combine real and demo tours
    combined_tours = list(real_tours) + tours if real_tours.exists() else tours

    context = {
        'tours': combined_tours,
        'real_tours': real_tours,
        'category': category,
        'display_category': display_category,
        'total_tours': len(combined_tours),
        'all_categories': category_names,
        'search_query': search_query,
    }

    return render(request, 'core/tours.html', context)

def experiences(request):
    """Experiences page view - combining tours, activities, and unique local experiences"""

    # Get all active and published tours (experiences)
    real_experiences = Tour.objects.filter(
        is_published=True,
        is_active=True
    ).select_related('host')

    context = {
        'experiences': real_experiences,
        'total_experiences': real_experiences.count(),
    }

    return render(request, 'core/experiences.html', context)

def share_trip_tours(request):
    """Share Trip Tours page view"""
    share_trip_tours = [
        {
            'id': 'st1',
            'title': 'Historic Cyprus Cultural Walking Tour',
            'location': 'Nicosia, Cyprus',
            'description': 'Discover the rich history and culture of Cyprus\'s capital city through hidden alleys, ancient architecture, and local stories shared with fellow travelers.',
            'price': 25,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': '4-12 people',
            'rating': 4.8,
            'reviews': 1850,
            'difficulty': 'Easy',
            'highlights': ['Visit the last divided capital in Europe', 'Explore both Greek and Turkish quarters', 'Taste traditional Cypriot coffee'],
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Ledra Street Crossing',
            'includes': ['Professional guide', 'Traditional coffee tasting', 'Small group experience'],
            'excludes': ['Personal expenses', 'Transportation to meeting point']
        },
        {
            'id': 'st2',
            'title': 'Petra by Night Candlelight Experience',
            'location': 'Petra, Jordan',
            'description': 'Experience the magical atmosphere of Petra illuminated by over 1,500 candles, creating an unforgettable evening of wonder and mystery.',
            'price': 45,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Max 20 people',
            'rating': 4.9,
            'reviews': 1876,
            'difficulty': 'Easy',
            'highlights': ['Candlelit Treasury Building', 'Traditional Bedouin music', 'Storytelling session', 'Complimentary tea'],
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Petra Visitor Center',
            'includes': ['Candlelight experience', 'Traditional music performance', 'Storytelling', 'Herbal tea'],
            'excludes': ['Petra entrance fee', 'Transportation to Petra', 'Personal expenses']
        },
        {
            'id': 'st3',
            'title': 'Sinai Mountain Sunrise Trek',
            'location': 'Mount Sinai, Egypt',
            'description': 'Experience the breathtaking sunrise from the summit of Mount Sinai, following the ancient path of Moses with fellow adventurers.',
            'price': 85,
            'currency': 'USD',
            'duration': '12 hours',
            'group_size': '4-15 people',
            'rating': 4.6,
            'reviews': 892,
            'difficulty': 'Moderate',
            'highlights': ['Sunrise summit experience', 'Ancient Moses trail', 'Bedouin guide', 'Stunning desert views'],
            'image': 'https://images.unsplash.com/photo-1464822759844-d150f38d609c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Saint Catherine\'s Monastery',
            'includes': ['Professional guide', 'Transportation', 'Breakfast', 'Entrance fees'],
            'excludes': ['Personal expenses', 'Water bottle', 'Warm clothing']
        },
        {
            'id': 'st4',
            'title': 'Jerusalem Old City Walking Tour',
            'location': 'Jerusalem, Palestine',
            'description': 'Explore the ancient streets of Jerusalem\'s Old City, visiting sacred sites of three major religions with fellow travelers.',
            'price': 45,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': 'Max 15 people',
            'rating': 4.8,
            'reviews': 2156,
            'difficulty': 'Easy',
            'highlights': ['Western Wall visit', 'Church of the Holy Sepulchre', 'Temple Mount', 'Via Dolorosa'],
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Jaffa Gate',
            'includes': ['Expert guide', 'Small group experience', 'Historical insights'],
            'excludes': ['Site entrance fees', 'Personal expenses', 'Transportation']
        },
        {
            'id': 'st5',
            'title': 'Dubai Creek Traditional Dhow Dinner Cruise',
            'location': 'Dubai, UAE',
            'description': 'Join fellow travelers for a traditional dhow cruise along Dubai Creek, featuring authentic Arabian cuisine and cultural performances.',
            'price': 65,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Max 25 people',
            'rating': 4.7,
            'reviews': 1234,
            'difficulty': 'Easy',
            'highlights': ['Traditional dhow boat', 'Authentic Arabian cuisine', 'Cultural dance performance', 'Dubai Creek views'],
            'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Dubai Creek Harbour',
            'includes': ['Dhow cruise', 'Traditional dinner', 'Cultural performance', 'Soft drinks'],
            'excludes': ['Personal expenses', 'Transportation to meeting point', 'Alcoholic beverages']
        },
        {
            'id': 'st6',
            'title': 'Amman Roman Theater & Citadel Exploration',
            'location': 'Amman, Jordan',
            'description': 'Step back in time at Amman\'s Roman Theater and explore the ancient Citadel with fellow history enthusiasts.',
            'price': 35,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': 'Max 12 people',
            'rating': 4.6,
            'reviews': 987,
            'difficulty': 'Easy',
            'highlights': ['Roman Theater exploration', 'Amman Citadel visit', 'Ancient artifacts', 'City views'],
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Roman Theater entrance',
            'includes': ['Expert guide', 'Site entrance fees', 'Historical commentary'],
            'excludes': ['Personal expenses', 'Transportation', 'Food and drinks']
        },
        {
            'id': 'st7',
            'title': 'Traditional Middle Eastern Cooking Class',
            'location': 'Various locations',
            'description': 'Learn to cook authentic local cuisine with expert chefs. Includes market visit and hands-on cooking shared with fellow food enthusiasts.',
            'price': 65,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': 'Max 12 people',
            'rating': 4.7,
            'reviews': 1245,
            'difficulty': 'Easy',
            'highlights': ['Market visit with local vendors', 'Hands-on cooking experience', 'Traditional recipe secrets', 'Authentic meal tasting'],
            'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Local cooking school',
            'includes': ['Professional chef instructor', 'All cooking ingredients', 'Recipe booklet', 'Traditional meal'],
            'excludes': ['Transportation to venue', 'Personal shopping', 'Beverages']
        },
        {
            'id': 'st8',
            'title': 'Red Sea Scuba Diving Adventure',
            'location': 'Aqaba, Jordan',
            'description': 'Explore the vibrant underwater world of the Red Sea with professional PADI-certified instructors and fellow diving enthusiasts.',
            'price': 185,
            'currency': 'USD',
            'duration': '5 hours',
            'group_size': 'Max 6 people',
            'rating': 4.8,
            'reviews': 756,
            'difficulty': 'Intermediate',
            'highlights': ['Professional PADI instructors', 'Coral reef exploration', 'Marine life photography', 'Safety briefing included'],
            'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Aqaba diving center',
            'includes': ['PADI certified instructor', 'Full diving equipment', 'Safety briefing', 'Underwater photos'],
            'excludes': ['Transportation to site', 'Dive certification', 'Personal expenses']
        },
        {
            'id': 'st9',
            'title': 'Lebanon Paragliding Experience',
            'location': 'Harissa, Lebanon',
            'description': 'Soar above the stunning Lebanese coastline and mountains in a tandem paragliding flight with fellow adventure seekers.',
            'price': 220,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Max 8 people',
            'rating': 4.5,
            'reviews': 433,
            'difficulty': 'Easy',
            'highlights': ['Tandem paragliding flight', 'Stunning coastal views', 'Professional pilot', 'Safety equipment provided'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Harissa mountain station',
            'includes': ['Professional pilot', 'Safety equipment', 'Flight certificate', 'Transportation to takeoff'],
            'excludes': ['Personal expenses', 'Video recording', 'Additional flights']
        },
        {
            'id': 'st10',
            'title': 'Dubai Desert Safari with BBQ',
            'location': 'Dubai, UAE',
            'description': 'Thrilling desert adventure with dune bashing, camel riding, traditional BBQ dinner, and belly dancing shared with fellow travelers.',
            'price': 85,
            'currency': 'USD',
            'duration': '6 hours',
            'group_size': '4-6 people',
            'rating': 4.7,
            'reviews': 3245,
            'difficulty': 'Easy',
            'highlights': ['Dune bashing experience', 'Camel riding', 'Traditional BBQ dinner', 'Belly dancing performance'],
            'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Dubai desert camp pickup',
            'includes': ['4x4 desert vehicle', 'Camel riding', 'BBQ dinner', 'Cultural performance'],
            'excludes': ['Personal expenses', 'Transportation to pickup point', 'Alcoholic beverages']
        },
        {
            'id': 'st11',
            'title': 'Paphos Archaeological Group Tour',
            'location': 'Paphos, Cyprus',
            'description': 'Join a group of history enthusiasts to explore the UNESCO World Heritage archaeological sites of Paphos with an expert archaeologist guide.',
            'price': 35,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': '8-20 people',
            'rating': 4.7,
            'reviews': 624,
            'difficulty': 'Easy',
            'highlights': ['UNESCO World Heritage sites', 'Expert archaeologist guide', 'Ancient mosaics', 'Roman theaters'],
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Paphos archaeological park',
            'includes': ['Expert archaeologist guide', 'Site entrance fees', 'Historical commentary'],
            'excludes': ['Personal expenses', 'Transportation', 'Food and drinks']
        },
        {
            'id': 'st12',
            'title': 'Muscat Coastal Dhow Cruise',
            'location': 'Muscat, Oman',
            'description': 'Experience Oman\'s stunning coastline with a traditional dhow cruise, visiting forts and fishing villages with fellow travelers.',
            'price': 75,
            'currency': 'USD',
            'duration': '6 hours',
            'group_size': 'Max 15 people',
            'rating': 4.8,
            'reviews': 654,
            'difficulty': 'Easy',
            'highlights': ['Traditional dhow boat', 'Coastal fort visits', 'Fishing village exploration', 'Sunset views'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Muscat harbor',
            'includes': ['Traditional dhow cruise', 'Guided fort visits', 'Refreshments', 'Cultural commentary'],
            'excludes': ['Personal expenses', 'Transportation to harbor', 'Additional activities']
        },
        {
            'id': 'st13',
            'title': 'Istanbul Bosphorus Cruise',
            'location': 'Istanbul, Turkey',
            'description': 'Cruise the historic Bosphorus Strait, connecting Europe and Asia, with fellow travelers while enjoying stunning views and local culture.',
            'price': 55,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': 'Max 30 people',
            'rating': 4.6,
            'reviews': 1876,
            'difficulty': 'Easy',
            'highlights': ['Bosphorus Strait cruise', 'Europe-Asia crossing', 'Historic waterfront palaces', 'Local seafood lunch'],
            'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Istanbul cruise terminal',
            'includes': ['Bosphorus cruise', 'Guided commentary', 'Traditional lunch', 'Audio guide'],
            'excludes': ['Personal expenses', 'Transportation to terminal', 'Gratuities']
        },
        {
            'id': 'st14',
            'title': 'Marrakech Medina Food Tour',
            'location': 'Marrakech, Morocco',
            'description': 'Discover the vibrant flavors of Marrakech through its bustling souks and hidden food stalls with fellow culinary adventurers.',
            'price': 45,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Max 10 people',
            'rating': 4.8,
            'reviews': 1456,
            'difficulty': 'Easy',
            'highlights': ['Authentic street food tasting', 'Souk exploration', 'Local chef interactions', 'Traditional Moroccan sweets'],
            'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Jemaa el-Fnaa square',
            'includes': ['Local food guide', 'Food tastings', 'Cultural insights', 'Market navigation'],
            'excludes': ['Transportation', 'Full meals', 'Personal purchases']
        },
        {
            'id': 'st15',
            'title': 'Cairo Khan el-Khalili Bazaar Tour',
            'location': 'Cairo, Egypt',
            'description': 'Navigate the historic Khan el-Khalili bazaar, experiencing authentic Egyptian culture and shopping with fellow travelers.',
            'price': 30,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Max 12 people',
            'rating': 4.5,
            'reviews': 2134,
            'difficulty': 'Easy',
            'highlights': ['Historic bazaar exploration', 'Traditional crafts', 'Spice market visit', 'Mint tea ceremony'],
            'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Khan el-Khalili entrance',
            'includes': ['Local guide', 'Mint tea tasting', 'Cultural commentary', 'Market map'],
            'excludes': ['Personal purchases', 'Transportation', 'Full meals']
        },
        {
            'id': 'st16',
            'title': 'Beirut Food & Culture Walking Tour',
            'location': 'Beirut, Lebanon',
            'description': 'Experience Beirut\'s culinary renaissance through its diverse neighborhoods, tasting authentic Lebanese cuisine with fellow food lovers.',
            'price': 55,
            'currency': 'USD',
            'duration': '4 hours',
            'group_size': 'Max 8 people',
            'rating': 4.7,
            'reviews': 987,
            'difficulty': 'Easy',
            'highlights': ['Authentic Lebanese mezze', 'Local bakery visits', 'Street food exploration', 'Cultural insights'],
            'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Beirut city center',
            'includes': ['Local food expert guide', 'Food tastings', 'Cultural commentary', 'Walking tour'],
            'excludes': ['Transportation', 'Full meals', 'Alcoholic beverages']
        },
        {
            'id': 'st17',
            'title': 'Doha Souq Waqif Cultural Experience',
            'location': 'Doha, Qatar',
            'description': 'Immerse yourself in Qatari culture at Souq Waqif, exploring traditional markets and experiencing authentic Arabian hospitality.',
            'price': 40,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Max 15 people',
            'rating': 4.6,
            'reviews': 1456,
            'difficulty': 'Easy',
            'highlights': ['Traditional souq exploration', 'Arabic coffee ceremony', 'Craft demonstrations', 'Cultural performances'],
            'image': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Souq Waqif entrance',
            'includes': ['Local cultural guide', 'Arabic coffee tasting', 'Cultural demonstrations', 'Market navigation'],
            'excludes': ['Personal purchases', 'Transportation', 'Full meals']
        },
        {
            'id': 'st18',
            'title': 'Amman Downtown Cultural Walk',
            'location': 'Amman, Jordan',
            'description': 'Explore Amman\'s vibrant downtown district, discovering Roman theaters, Ottoman architecture, and local street life with fellow travelers.',
            'price': 35,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Max 12 people',
            'rating': 4.5,
            'reviews': 1234,
            'difficulty': 'Easy',
            'highlights': ['Roman Theater visit', 'Ottoman architecture', 'Local street food', 'Contemporary art scene'],
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Amman downtown square',
            'includes': ['Local guide', 'Site entrance fees', 'Cultural commentary', 'Street food tasting'],
            'excludes': ['Transportation', 'Full meals', 'Personal expenses']
        },
        {
            'id': 'st19',
            'title': 'Muscat Muttrah Souq Exploration',
            'location': 'Muscat, Oman',
            'description': 'Dive into Oman\'s maritime heritage at Muttrah Souq, exploring spice markets and traditional crafts with fellow cultural enthusiasts.',
            'price': 35,
            'currency': 'USD',
            'duration': '2 hours',
            'group_size': 'Max 10 people',
            'rating': 4.6,
            'reviews': 876,
            'difficulty': 'Easy',
            'highlights': ['Spice market exploration', 'Traditional crafts', 'Omani coffee tasting', 'Maritime history'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Muttrah Corniche',
            'includes': ['Local guide', 'Spice tasting', 'Cultural insights', 'Market navigation'],
            'excludes': ['Personal purchases', 'Transportation', 'Full meals']
        },
        {
            'id': 'st20',
            'title': 'Nicosia Green Line Buffer Zone Tour',
            'location': 'Nicosia, Cyprus',
            'description': 'Experience Cyprus\'s unique divided history on this guided tour of the Green Line, exploring the buffer zone that separates north and south.',
            'price': 40,
            'currency': 'USD',
            'duration': '3 hours',
            'group_size': 'Max 8 people',
            'rating': 4.7,
            'reviews': 654,
            'difficulty': 'Easy',
            'highlights': ['UN buffer zone exploration', 'Divided city history', 'Abandoned buildings', 'Peacekeeping insights'],
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'meeting_point': 'Nicosia city center',
            'includes': ['Expert guide', 'Historical commentary', 'Peacekeeping insights', 'Cultural context'],
            'excludes': ['Personal expenses', 'Transportation', 'Border crossing permits']
        }
    ]

    context = {
        'tours': share_trip_tours,
        'total_tours': len(share_trip_tours),
        'average_rating': 4.7,
        'total_reviews': sum(tour['reviews'] for tour in share_trip_tours)
    }
    return render(request, 'core/share_trip_tours.html', context)

def signin(request):
    """Sign in page view with role-based redirects"""
    # Clear any existing messages to prevent accumulation
    storage = messages.get_messages(request)
    storage.used = True
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Check user role for redirect
                try:
                    profile = user.profile
                    if profile.is_host:
                        messages.success(request, f"Welcome back, {username}! Redirecting to your host dashboard.")
                        return redirect('hostdashboard')
                    else:
                        messages.success(request, f"Welcome back, {username}! Explore amazing experiences.")
                        return redirect('dashboard')  # Traveler dashboard
                except UserProfile.DoesNotExist:
                    # Create profile if it doesn't exist (fallback)
                    UserProfile.objects.create(user=request.user, is_host=False)
                    messages.success(request, f"Welcome back, {username}!")
                    return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/signin.html', {'form': form})

def signup(request):
    """Sign up page view for travelers"""
    # Clear any existing messages to prevent accumulation
    storage = messages.get_messages(request)
    storage.used = True
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile for traveler
            UserProfile.objects.create(user=user, is_host=False)
            login(request, user)
            messages.success(request, f"Traveler account created successfully! Welcome, {user.username}! Start exploring amazing experiences.")
            return redirect('home')  # Redirect travelers to home page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def accommodations(request):
    """Accommodations page view"""

    # Get real accommodations from database (both published AND active)
    real_accommodations = Accommodation.objects.filter(
        is_published=True,
        is_active=True
    ).select_related('host')

    # Demo accommodations data (fallback if no real listings)
    demo_accommodations = [
        {
            'id': '1',
            'name': 'Luxury Beach Resort & Spa',
            'location': 'Maldives',
            'description': 'Experience paradise at our beachfront resort with private villas, world-class spa, and stunning ocean views.',
            'price': 450,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 1250,
            'type': 'resort',
            'amenities': ['WiFi', 'Pool', 'Spa', 'Beach Access', 'Restaurant'],
            'image': 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 2,
            'bathrooms': 2,
            'max_guests': 4,
            'room_type': 'Villa with Ocean View',
            'cancellation_policy': 'Free cancellation up to 24 hours',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['Private beach access', '24/7 concierge', 'Spa treatments included', 'Daily housekeeping']
        },
        {
            'id': '2',
            'name': 'Boutique City Hotel Downtown',
            'location': 'Dubai, UAE',
            'description': 'Charming boutique hotel in the heart of the city with modern design, rooftop bar, and easy access to attractions.',
            'price': 250,
            'currency': 'USD',
            'rating': 4.6,
            'reviews': 890,
            'type': 'hotel',
            'amenities': ['WiFi', 'Gym', 'Rooftop Bar', 'Concierge', 'Business Center'],
            'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Deluxe City View Room',
            'cancellation_policy': 'Free cancellation up to 48 hours',
            'check_in_time': '15:00',
            'check_out_time': '11:00',
            'property_highlights': ['Burj Khalifa views', 'Metro station nearby', 'Business center', 'Fitness center']
        },
        {
            'id': '3',
            'name': 'Mountain View Chalet',
            'location': 'Swiss Alps, Switzerland',
            'description': 'Rustic mountain chalet with stunning alpine views and modern amenities for the perfect mountain retreat.',
            'price': 350,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 567,
            'type': 'chalet',
            'amenities': ['WiFi', 'Fireplace', 'Hot Tub', 'Mountain Views', 'Ski Access'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 3,
            'bathrooms': 2,
            'max_guests': 6,
            'room_type': 'Alpine Chalet',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '16:00',
            'check_out_time': '10:00',
            'property_highlights': ['Ski-in/ski-out access', 'Wood-burning fireplace', 'Private hot tub', 'Mountain views']
        },
        {
            'id': '4',
            'name': 'Historic Riad Marrakech',
            'location': 'Marrakech, Morocco',
            'description': 'Traditional Moroccan riad in the heart of the medina with authentic architecture and modern comforts.',
            'price': 180,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 745,
            'type': 'riad',
            'amenities': ['WiFi', 'Courtyard', 'Traditional Decor', 'Rooftop Terrace', 'Hammam'],
            'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 4,
            'bathrooms': 3,
            'max_guests': 8,
            'room_type': 'Traditional Riad Suite',
            'cancellation_policy': 'Free cancellation up to 3 days',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['Medina location', 'Traditional Moroccan architecture', 'Rooftop terrace', 'Hammam spa']
        },
        {
            'id': '5',
            'name': 'Overwater Bungalow Paradise',
            'location': 'Bora Bora, French Polynesia',
            'description': 'Luxurious overwater bungalow with direct lagoon access and breathtaking sunset views.',
            'price': 650,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 423,
            'type': 'bungalow',
            'amenities': ['WiFi', 'Private Deck', 'Lagoon Access', 'Butler Service', 'Snorkeling'],
            'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Overwater Bungalow',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Crystal clear lagoon', 'Sunset views', 'Private butler service', 'Snorkeling equipment']
        },
        {
            'id': '6',
            'name': 'Urban Loft Apartment',
            'location': 'Tokyo, Japan',
            'description': 'Modern loft apartment in trendy Shibuya district with city views and contemporary design.',
            'price': 120,
            'currency': 'USD',
            'rating': 4.5,
            'reviews': 1100,
            'type': 'apartment',
            'amenities': ['WiFi', 'Kitchen', 'City Views', 'Washing Machine', 'Near Subway'],
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 3,
            'room_type': 'Modern Loft',
            'cancellation_policy': 'Free cancellation up to 5 days',
            'check_in_time': '15:00',
            'check_out_time': '10:00',
            'property_highlights': ['Shibuya district', 'City skyline views', 'Fully equipped kitchen', 'Subway access']
        },
        {
            'id': '7',
            'name': 'Desert Oasis Camp',
            'location': 'Sahara Desert, Morocco',
            'description': 'Authentic Bedouin camp in the heart of the Sahara with traditional tents and star-filled skies.',
            'price': 85,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 892,
            'type': 'camp',
            'amenities': ['Traditional Meals', 'Campfire', 'Desert Views', 'Guided Tours', 'Bedouin Hospitality'],
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Traditional Bedouin Tent',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '16:00',
            'check_out_time': '12:00',
            'property_highlights': ['Starry night skies', 'Traditional Bedouin experience', 'Camel treks available', 'Authentic Moroccan cuisine']
        },
        {
            'id': '8',
            'name': 'Lake Como Villa',
            'location': 'Lake Como, Italy',
            'description': 'Elegant villa overlooking Lake Como with private gardens and stunning mountain views.',
            'price': 420,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 634,
            'type': 'villa',
            'amenities': ['WiFi', 'Private Garden', 'Lake Views', 'Swimming Pool', 'Boat Dock'],
            'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 4,
            'bathrooms': 3,
            'max_guests': 8,
            'room_type': 'Lakefront Villa',
            'cancellation_policy': 'Free cancellation up to 10 days',
            'check_in_time': '16:00',
            'check_out_time': '10:00',
            'property_highlights': ['Private lake access', 'Mountain views', 'Professional chef available', 'Boat included']
        },
        {
            'id': '9',
            'name': 'Santorini Cave Hotel',
            'location': 'Santorini, Greece',
            'description': 'Unique cave hotel carved into volcanic rock with caldera views and traditional Cycladic architecture.',
            'price': 280,
            'currency': 'USD',
            'rating': 4.6,
            'reviews': 756,
            'type': 'hotel',
            'amenities': ['WiFi', 'Caldera Views', 'Infinity Pool', 'Spa Services', 'Restaurant'],
            'image': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Cave Suite with Caldera View',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Volcanic cave architecture', 'Sunset caldera views', 'Infinity pool', 'Traditional Greek breakfast']
        },
        {
            'id': '10',
            'name': 'Amazon Rainforest Lodge',
            'location': 'Amazon Rainforest, Brazil',
            'description': 'Eco-lodge deep in the Amazon with guided jungle walks and authentic indigenous experiences.',
            'price': 195,
            'currency': 'USD',
            'rating': 4.5,
            'reviews': 423,
            'type': 'lodge',
            'amenities': ['Eco-Friendly', 'Jungle Tours', 'Indigenous Guides', 'Sustainable Dining', 'Wildlife Viewing'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 2,
            'bathrooms': 2,
            'max_guests': 4,
            'room_type': 'Jungle Bungalow',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '12:00',
            'check_out_time': '11:00',
            'property_highlights': ['Sustainable tourism', 'Indigenous community support', 'Wildlife encounters', 'Eco-friendly practices']
        },
        {
            'id': '11',
            'name': 'Icelandic Glacier Retreat',
            'location': 'Vatnajökull, Iceland',
            'description': 'Glass-domed igloo on a glacier with northern lights views and ice cave explorations.',
            'price': 380,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 345,
            'type': 'igloo',
            'amenities': ['Northern Lights Views', 'Glacier Access', 'Ice Cave Tours', 'Thermal Bath', 'Arctic Dining'],
            'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Glass Igloo Suite',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '16:00',
            'check_out_time': '11:00',
            'property_highlights': ['Glass dome ceiling', 'Northern lights viewing', 'Glacier hiking', 'Ice cave exploration']
        },
        {
            'id': '12',
            'name': 'Parisian Haussmann Apartment',
            'location': 'Paris, France',
            'description': 'Elegant 19th-century apartment in a Haussmann building with original moldings and modern updates.',
            'price': 220,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 678,
            'type': 'apartment',
            'amenities': ['WiFi', 'Kitchen', 'Historic Architecture', 'Concierge', 'Laundry Service'],
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 2,
            'bathrooms': 1,
            'max_guests': 4,
            'room_type': 'Haussmann Apartment',
            'cancellation_policy': 'Free cancellation up to 5 days',
            'check_in_time': '15:00',
            'check_out_time': '10:00',
            'property_highlights': ['Historic 6th arrondissement', 'Walking distance to Louvre', 'Original architectural details', 'Concierge service']
        },
        {
            'id': '13',
            'name': 'Taj Mahal Palace Hotel',
            'location': 'Mumbai, India',
            'description': 'Iconic colonial-era hotel with opulent architecture, sea-facing rooms, and legendary hospitality.',
            'price': 320,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 1234,
            'type': 'hotel',
            'amenities': ['WiFi', 'Sea Views', 'Spa', 'Multiple Restaurants', 'Business Center'],
            'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Sea View Deluxe Room',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['Gateway of India views', 'Colonial architecture', 'Award-winning restaurants', 'Royal heritage']
        },
        {
            'id': '14',
            'name': 'Great Barrier Reef Resort',
            'location': 'Cairns, Australia',
            'description': 'Luxury resort with direct reef access, marine biology center, and underwater observatories.',
            'price': 480,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 567,
            'type': 'resort',
            'amenities': ['Reef Access', 'Marine Biology Center', 'Diving Center', 'Spa', 'Multiple Pools'],
            'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 2,
            'bathrooms': 2,
            'max_guests': 4,
            'room_type': 'Reef View Suite',
            'cancellation_policy': 'Free cancellation up to 10 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Direct reef access', 'Underwater observatory', 'Marine research center', 'Diving certification courses']
        },
        {
            'id': '15',
            'name': 'Scottish Highlands Castle',
            'location': 'Scottish Highlands, Scotland',
            'description': 'Historic castle in the Scottish Highlands with lochs, mountains, and traditional hospitality.',
            'price': 395,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 456,
            'type': 'castle',
            'amenities': ['WiFi', 'Fireplace', 'Loch Views', 'Whisky Bar', 'Gardens'],
            'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 5,
            'bathrooms': 4,
            'max_guests': 10,
            'room_type': 'Castle Suite',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '16:00',
            'check_out_time': '11:00',
            'property_highlights': ['Historic castle architecture', 'Loch and mountain views', 'Whisky tasting experiences', 'Private gardens']
        },
        {
            'id': '16',
            'name': 'Patagonia Glacier Lodge',
            'location': 'Torres del Paine, Chile',
            'description': 'Remote lodge in Patagonia with glacier views, hiking trails, and authentic Chilean hospitality.',
            'price': 265,
            'currency': 'USD',
            'rating': 4.6,
            'reviews': 389,
            'type': 'lodge',
            'amenities': ['Glacier Views', 'Hiking Trails', 'Fireplace', 'Local Cuisine', 'Guide Services'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 3,
            'bathrooms': 2,
            'max_guests': 6,
            'room_type': 'Glacier View Cabin',
            'cancellation_policy': 'Free cancellation up to 10 days',
            'check_in_time': '15:00',
            'check_out_time': '11:00',
            'property_highlights': ['Torres del Paine views', 'Guided hiking tours', 'Authentic Patagonian cuisine', 'Sustainable practices']
        },
        {
            'id': '17',
            'name': 'Venetian Canal Palace',
            'location': 'Venice, Italy',
            'description': 'Historic palace on the Grand Canal with Renaissance architecture and modern luxury amenities.',
            'price': 550,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 723,
            'type': 'palace',
            'amenities': ['Canal Views', 'Private Boat', 'Historic Architecture', 'Spa', 'Fine Dining'],
            'image': 'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 3,
            'bathrooms': 3,
            'max_guests': 6,
            'room_type': 'Canal View Palace Suite',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Grand Canal location', 'Renaissance architecture', 'Private boat service', 'Michelin-star dining']
        },
        {
            'id': '18',
            'name': 'Bali Rice Terrace Villa',
            'location': 'Ubud, Bali, Indonesia',
            'description': 'Luxurious villa nestled in rice terraces with traditional Balinese architecture and spa facilities.',
            'price': 195,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 891,
            'type': 'villa',
            'amenities': ['Rice Terrace Views', 'Private Pool', 'Spa', 'Traditional Architecture', 'Yoga Pavilion'],
            'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 3,
            'bathrooms': 3,
            'max_guests': 6,
            'room_type': 'Rice Terrace Villa',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['UNESCO rice terraces', 'Traditional Balinese design', 'Daily yoga sessions', 'Organic farm-to-table dining']
        },
        {
            'id': '19',
            'name': 'New York Penthouse',
            'location': 'Manhattan, New York, USA',
            'description': 'Ultra-luxury penthouse with Central Park views, private terrace, and 24/7 concierge service.',
            'price': 850,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 234,
            'type': 'penthouse',
            'amenities': ['Central Park Views', 'Private Terrace', 'Concierge', 'Spa Bathroom', 'Chef Service'],
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 3,
            'bathrooms': 3,
            'max_guests': 6,
            'room_type': 'Central Park Penthouse',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '15:00',
            'check_out_time': '11:00',
            'property_highlights': ['Central Park views', 'Private rooftop terrace', '24/7 concierge', 'Personal chef service']
        },
        {
            'id': '20',
            'name': 'Safari Luxury Tent Camp',
            'location': 'Serengeti, Tanzania',
            'description': 'Luxury safari camp with canvas tents, private decks, and unparalleled wildlife viewing opportunities.',
            'price': 425,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 567,
            'type': 'camp',
            'amenities': ['Wildlife Viewing', 'Private Decks', 'Guided Safaris', 'Butler Service', 'Luxury Camping'],
            'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Luxury Safari Tent',
            'cancellation_policy': 'Free cancellation up to 21 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Big Five wildlife viewing', 'Private viewing decks', 'Guided safari drives', 'Authentic Maasai cultural experiences']
        }
    ]

    # Handle search functionality
    search_query = request.GET.get('q', '').strip()
    accommodations = demo_accommodations

    if search_query:
        # Filter accommodations based on search query
        filtered_accommodations = []
        query_lower = search_query.lower()

        for accommodation in demo_accommodations:
            # Search in name, location, description, type, and amenities
            if (query_lower in accommodation['name'].lower() or
                query_lower in accommodation['location'].lower() or
                query_lower in accommodation['description'].lower() or
                query_lower in accommodation['type'].lower() or
                any(query_lower in amenity.lower() for amenity in accommodation['amenities'])):
                filtered_accommodations.append(accommodation)

        accommodations = filtered_accommodations

    # Filter by type if provided (in addition to search)
    accommodation_type = request.GET.get('type')
    if accommodation_type and not search_query:
        accommodations = [acc for acc in accommodations if acc['type'] == accommodation_type]

    # Get booking parameters
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    adults = request.GET.get('adults', '2')
    kids = request.GET.get('kids', '0')
    rooms = request.GET.get('rooms', '1')

    # Set default values if not provided
    if not checkin:
        from datetime import datetime, timedelta
        checkin = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    if not checkout:
        from datetime import datetime, timedelta
        checkout = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')

    # Combine real and demo accommodations
    combined_accommodations = list(real_accommodations) + accommodations if real_accommodations.exists() else accommodations

    context = {
        'accommodations': combined_accommodations,
        'real_accommodations': real_accommodations,
        'current_type': accommodation_type,
        'total_accommodations': len(combined_accommodations),
        'types': ['resort', 'hotel', 'chalet', 'riad', 'bungalow', 'apartment'],
        'search_query': search_query,
        'checkin': checkin,
        'checkout': checkout,
        'adults': adults,
        'kids': kids,
        'rooms': rooms,
    }

    return render(request, 'core/accommodations.html', context)

def accommodation_detail(request, id):
    """Individual accommodation detail page view - handles both demo and database accommodations"""

    # Demo accommodations data (IDs 1-20)
    demo_accommodations_dict = {}
    from datetime import datetime, timedelta

    # Get booking parameters from request or set defaults
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    adults = request.GET.get('adults', '2')
    kids = request.GET.get('kids', '0')
    rooms = request.GET.get('rooms', '1')

    # Set default values if not provided
    if not checkin:
        checkin = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    if not checkout:
        checkout = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')

    # First check if this is a demo accommodation (string ID)
    if str(id) in [str(i) for i in range(1, 21)]:
        # This is a demo accommodation - get it from the demo data in accommodations view
        # We'll import the demo data here
        demo_accommodations = [
        {
            'id': '1',
            'name': 'Luxury Beach Resort & Spa',
            'location': 'Maldives',
            'description': 'Experience paradise at our beachfront resort with private villas, world-class spa, and stunning ocean views.',
            'price': 450,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 1250,
            'type': 'resort',
            'amenities': ['WiFi', 'Pool', 'Spa', 'Beach Access', 'Restaurant'],
            'image': 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 2,
            'bathrooms': 2,
            'max_guests': 4,
            'room_type': 'Villa with Ocean View',
            'cancellation_policy': 'Free cancellation up to 24 hours',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['Private beach access', '24/7 concierge', 'Spa treatments included', 'Daily housekeeping']
        },
        {
            'id': '2',
            'name': 'Boutique City Hotel Downtown',
            'location': 'Dubai, UAE',
            'description': 'Charming boutique hotel in the heart of the city with modern design, rooftop bar, and easy access to attractions.',
            'price': 250,
            'currency': 'USD',
            'rating': 4.6,
            'reviews': 890,
            'type': 'hotel',
            'amenities': ['WiFi', 'Gym', 'Rooftop Bar', 'Concierge', 'Business Center'],
            'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Deluxe City View Room',
            'cancellation_policy': 'Free cancellation up to 48 hours',
            'check_in_time': '15:00',
            'check_out_time': '11:00',
            'property_highlights': ['Burj Khalifa views', 'Metro station nearby', 'Business center', 'Fitness center']
        },
        {
            'id': '3',
            'name': 'Mountain View Chalet',
            'location': 'Swiss Alps, Switzerland',
            'description': 'Rustic mountain chalet with stunning alpine views and modern amenities for the perfect mountain retreat.',
            'price': 350,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 567,
            'type': 'chalet',
            'amenities': ['WiFi', 'Fireplace', 'Hot Tub', 'Mountain Views', 'Ski Access'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 3,
            'bathrooms': 2,
            'max_guests': 6,
            'room_type': 'Alpine Chalet',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '16:00',
            'check_out_time': '10:00',
            'property_highlights': ['Ski-in/ski-out access', 'Wood-burning fireplace', 'Private hot tub', 'Mountain views']
        },
        {
            'id': '4',
            'name': 'Historic Riad Marrakech',
            'location': 'Marrakech, Morocco',
            'description': 'Traditional Moroccan riad in the heart of the medina with authentic architecture and modern comforts.',
            'price': 180,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 745,
            'type': 'riad',
            'amenities': ['WiFi', 'Courtyard', 'Traditional Decor', 'Rooftop Terrace', 'Hammam'],
            'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 4,
            'bathrooms': 3,
            'max_guests': 8,
            'room_type': 'Traditional Riad Suite',
            'cancellation_policy': 'Free cancellation up to 3 days',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['Medina location', 'Traditional Moroccan architecture', 'Rooftop terrace', 'Hammam spa']
        },
        {
            'id': '5',
            'name': 'Overwater Bungalow Paradise',
            'location': 'Bora Bora, French Polynesia',
            'description': 'Luxurious overwater bungalow with direct lagoon access and breathtaking sunset views.',
            'price': 650,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 423,
            'type': 'bungalow',
            'amenities': ['WiFi', 'Private Deck', 'Lagoon Access', 'Butler Service', 'Snorkeling'],
            'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Overwater Bungalow',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Crystal clear lagoon', 'Sunset views', 'Private butler service', 'Snorkeling equipment']
        },
        {
            'id': '6',
            'name': 'Urban Loft Apartment',
            'location': 'Tokyo, Japan',
            'description': 'Modern loft apartment in trendy Shibuya district with city views and contemporary design.',
            'price': 120,
            'currency': 'USD',
            'rating': 4.5,
            'reviews': 1100,
            'type': 'apartment',
            'amenities': ['WiFi', 'Kitchen', 'City Views', 'Washing Machine', 'Near Subway'],
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 3,
            'room_type': 'Modern Loft',
            'cancellation_policy': 'Free cancellation up to 5 days',
            'check_in_time': '15:00',
            'check_out_time': '10:00',
            'property_highlights': ['Shibuya district', 'City skyline views', 'Fully equipped kitchen', 'Subway access']
        },
        {
            'id': '7',
            'name': 'Desert Oasis Camp',
            'location': 'Sahara Desert, Morocco',
            'description': 'Authentic Bedouin camp in the heart of the Sahara with traditional tents and star-filled skies.',
            'price': 85,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 892,
            'type': 'camp',
            'amenities': ['Traditional Meals', 'Campfire', 'Desert Views', 'Guided Tours', 'Bedouin Hospitality'],
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Traditional Bedouin Tent',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '16:00',
            'check_out_time': '12:00',
            'property_highlights': ['Starry night skies', 'Traditional Bedouin experience', 'Camel treks available', 'Authentic Moroccan cuisine']
        },
        {
            'id': '8',
            'name': 'Lake Como Villa',
            'location': 'Lake Como, Italy',
            'description': 'Elegant villa overlooking Lake Como with private gardens and stunning mountain views.',
            'price': 420,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 634,
            'type': 'villa',
            'amenities': ['WiFi', 'Private Garden', 'Lake Views', 'Swimming Pool', 'Boat Dock'],
            'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 4,
            'bathrooms': 3,
            'max_guests': 8,
            'room_type': 'Lakefront Villa',
            'cancellation_policy': 'Free cancellation up to 10 days',
            'check_in_time': '16:00',
            'check_out_time': '10:00',
            'property_highlights': ['Private lake access', 'Mountain views', 'Professional chef available', 'Boat included']
        },
        {
            'id': '9',
            'name': 'Santorini Cave Hotel',
            'location': 'Santorini, Greece',
            'description': 'Unique cave hotel carved into volcanic rock with caldera views and traditional Cycladic architecture.',
            'price': 280,
            'currency': 'USD',
            'rating': 4.6,
            'reviews': 756,
            'type': 'hotel',
            'amenities': ['WiFi', 'Caldera Views', 'Infinity Pool', 'Spa Services', 'Restaurant'],
            'image': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Cave Suite with Caldera View',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Volcanic cave architecture', 'Sunset caldera views', 'Infinity pool', 'Traditional Greek breakfast']
        },
        {
            'id': '10',
            'name': 'Amazon Rainforest Lodge',
            'location': 'Amazon Rainforest, Brazil',
            'description': 'Eco-lodge deep in the Amazon with guided jungle walks and authentic indigenous experiences.',
            'price': 195,
            'currency': 'USD',
            'rating': 4.5,
            'reviews': 423,
            'type': 'lodge',
            'amenities': ['Eco-Friendly', 'Jungle Tours', 'Indigenous Guides', 'Sustainable Dining', 'Wildlife Viewing'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 2,
            'bathrooms': 2,
            'max_guests': 4,
            'room_type': 'Jungle Bungalow',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '12:00',
            'check_out_time': '11:00',
            'property_highlights': ['Sustainable tourism', 'Indigenous community support', 'Wildlife encounters', 'Eco-friendly practices']
        },
        {
            'id': '11',
            'name': 'Icelandic Glacier Retreat',
            'location': 'Vatnajökull, Iceland',
            'description': 'Glass-domed igloo on a glacier with northern lights views and ice cave explorations.',
            'price': 380,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 345,
            'type': 'igloo',
            'amenities': ['Northern Lights Views', 'Glacier Access', 'Ice Cave Tours', 'Thermal Bath', 'Arctic Dining'],
            'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Glass Igloo Suite',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '16:00',
            'check_out_time': '11:00',
            'property_highlights': ['Glass dome ceiling', 'Northern lights viewing', 'Glacier hiking', 'Ice cave exploration']
        },
        {
            'id': '12',
            'name': 'Parisian Haussmann Apartment',
            'location': 'Paris, France',
            'description': 'Elegant 19th-century apartment in a Haussmann building with original moldings and modern updates.',
            'price': 220,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 678,
            'type': 'apartment',
            'amenities': ['WiFi', 'Kitchen', 'Historic Architecture', 'Concierge', 'Laundry Service'],
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 2,
            'bathrooms': 1,
            'max_guests': 4,
            'room_type': 'Haussmann Apartment',
            'cancellation_policy': 'Free cancellation up to 5 days',
            'check_in_time': '15:00',
            'check_out_time': '10:00',
            'property_highlights': ['Historic 6th arrondissement', 'Walking distance to Louvre', 'Original architectural details', 'Concierge service']
        },
        {
            'id': '13',
            'name': 'Taj Mahal Palace Hotel',
            'location': 'Mumbai, India',
            'description': 'Iconic colonial-era hotel with opulent architecture, sea-facing rooms, and legendary hospitality.',
            'price': 320,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 1234,
            'type': 'hotel',
            'amenities': ['WiFi', 'Sea Views', 'Spa', 'Multiple Restaurants', 'Business Center'],
            'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Sea View Deluxe Room',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['Gateway of India views', 'Colonial architecture', 'Award-winning restaurants', 'Royal heritage']
        },
        {
            'id': '14',
            'name': 'Great Barrier Reef Resort',
            'location': 'Cairns, Australia',
            'description': 'Luxury resort with direct reef access, marine biology center, and underwater observatories.',
            'price': 480,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 567,
            'type': 'resort',
            'amenities': ['Reef Access', 'Marine Biology Center', 'Diving Center', 'Spa', 'Multiple Pools'],
            'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 2,
            'bathrooms': 2,
            'max_guests': 4,
            'room_type': 'Reef View Suite',
            'cancellation_policy': 'Free cancellation up to 10 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Direct reef access', 'Underwater observatory', 'Marine research center', 'Diving certification courses']
        },
        {
            'id': '15',
            'name': 'Scottish Highlands Castle',
            'location': 'Scottish Highlands, Scotland',
            'description': 'Historic castle in the Scottish Highlands with lochs, mountains, and traditional hospitality.',
            'price': 395,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 456,
            'type': 'castle',
            'amenities': ['WiFi', 'Fireplace', 'Loch Views', 'Whisky Bar', 'Gardens'],
            'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 5,
            'bathrooms': 4,
            'max_guests': 10,
            'room_type': 'Castle Suite',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '16:00',
            'check_out_time': '11:00',
            'property_highlights': ['Historic castle architecture', 'Loch and mountain views', 'Whisky tasting experiences', 'Private gardens']
        },
        {
            'id': '16',
            'name': 'Patagonia Glacier Lodge',
            'location': 'Torres del Paine, Chile',
            'description': 'Remote lodge in Patagonia with glacier views, hiking trails, and authentic Chilean hospitality.',
            'price': 265,
            'currency': 'USD',
            'rating': 4.6,
            'reviews': 389,
            'type': 'lodge',
            'amenities': ['Glacier Views', 'Hiking Trails', 'Fireplace', 'Local Cuisine', 'Guide Services'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 3,
            'bathrooms': 2,
            'max_guests': 6,
            'room_type': 'Glacier View Cabin',
            'cancellation_policy': 'Free cancellation up to 10 days',
            'check_in_time': '15:00',
            'check_out_time': '11:00',
            'property_highlights': ['Torres del Paine views', 'Guided hiking tours', 'Authentic Patagonian cuisine', 'Sustainable practices']
        },
        {
            'id': '17',
            'name': 'Venetian Canal Palace',
            'location': 'Venice, Italy',
            'description': 'Historic palace on the Grand Canal with Renaissance architecture and modern luxury amenities.',
            'price': 550,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 723,
            'type': 'palace',
            'amenities': ['Canal Views', 'Private Boat', 'Historic Architecture', 'Spa', 'Fine Dining'],
            'image': 'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 3,
            'bathrooms': 3,
            'max_guests': 6,
            'room_type': 'Canal View Palace Suite',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Grand Canal location', 'Renaissance architecture', 'Private boat service', 'Michelin-star dining']
        },
        {
            'id': '18',
            'name': 'Bali Rice Terrace Villa',
            'location': 'Ubud, Bali, Indonesia',
            'description': 'Luxurious villa nestled in rice terraces with traditional Balinese architecture and spa facilities.',
            'price': 195,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 891,
            'type': 'villa',
            'amenities': ['Rice Terrace Views', 'Private Pool', 'Spa', 'Traditional Architecture', 'Yoga Pavilion'],
            'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 3,
            'bathrooms': 3,
            'max_guests': 6,
            'room_type': 'Rice Terrace Villa',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['UNESCO rice terraces', 'Traditional Balinese design', 'Daily yoga sessions', 'Organic farm-to-table dining']
        },
        {
            'id': '19',
            'name': 'New York Penthouse',
            'location': 'Manhattan, New York, USA',
            'description': 'Ultra-luxury penthouse with Central Park views, private terrace, and 24/7 concierge service.',
            'price': 850,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 234,
            'type': 'penthouse',
            'amenities': ['Central Park Views', 'Private Terrace', 'Concierge', 'Spa Bathroom', 'Chef Service'],
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 3,
            'bathrooms': 3,
            'max_guests': 6,
            'room_type': 'Central Park Penthouse',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '15:00',
            'check_out_time': '11:00',
            'property_highlights': ['Central Park views', 'Private rooftop terrace', '24/7 concierge', 'Personal chef service']
        },
        {
            'id': '20',
            'name': 'Safari Luxury Tent Camp',
            'location': 'Serengeti, Tanzania',
            'description': 'Luxury safari camp with canvas tents, private decks, and unparalleled wildlife viewing opportunities.',
            'price': 425,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 567,
            'type': 'camp',
            'amenities': ['Wildlife Viewing', 'Private Decks', 'Guided Safaris', 'Butler Service', 'Luxury Camping'],
            'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'photos': [
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            ],
                        'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Luxury Safari Tent',
            'cancellation_policy': 'Free cancellation up to 21 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Big Five wildlife viewing', 'Private viewing decks', 'Guided safari drives', 'Authentic Maasai cultural experiences']
        }
    ]

        # Find the matching demo accommodation
        accommodation = None
        for demo_acc in demo_accommodations:
            if demo_acc['id'] == str(id):
                accommodation = demo_acc
                break

        if not accommodation:
            return redirect('accommodations')

        # For demo accommodations, create photo dictionaries from the photos array
        photos_urls = accommodation.get('photos', [accommodation.get('image')])
        hero_photos_json = []
        all_photos_json = []

        for idx, photo_url in enumerate(photos_urls):
            photo_dict = {
                'id': idx,
                'image_url': photo_url,
                'alt_text': f"{accommodation['name']} photo {idx+1}",
                'title': f"{accommodation['name']} - Image {idx+1}",
                'caption': '',
                'display_order': idx,
                'is_hero': idx < 6,
                'media_type': 'image',
            }
            all_photos_json.append(photo_dict)
            if idx < 6:
                hero_photos_json.append(photo_dict)

        total_photos = len(all_photos_json)

        context = {
            'accommodation': accommodation,
            'is_demo': True,
            'photos': photos_urls,
            'hero_photos': hero_photos_json,
            'all_photos': all_photos_json,
            'total_photos': total_photos,
            'checkin': checkin,
            'checkout': checkout,
            'adults': adults,
            'kids': kids,
            'rooms': rooms,
        }

        return render(request, 'core/accommodation_detail.html', context)

    # Otherwise, try to get from database
    try:
        accommodation = Accommodation.objects.get(id=id, is_published=True, is_active=True)
    except Accommodation.DoesNotExist:
        # If accommodation not found, redirect to accommodations list
        return redirect('accommodations')

    # Get photos for this accommodation, ordered by display_order
    photos = AccommodationPhoto.objects.filter(
        accommodation=accommodation,
        visibility__in=['public', 'hidden']
    ).order_by('display_order', 'id')

    # Separate hero photos (first few or marked as hero) and all photos
    hero_photos_queryset = photos.filter(is_hero=True)[:6]  # Up to 6 hero photos
    if not hero_photos_queryset.exists():
        # If no hero photos marked, use first 6 photos
        hero_photos_queryset = photos[:6]

    # All photos for lightbox
    all_photos_queryset = photos

    # Pass the QuerySets directly to template for rendering
    hero_photos = list(hero_photos_queryset)
    all_photos = list(all_photos_queryset)
    total_photos = len(all_photos)

    # Create serializable dictionaries for JSON (used by JavaScript)
    hero_photos_json = []
    for photo in hero_photos:
        hero_photos_json.append({
            'id': photo.id,
            'image_url': photo.get_image_url('large'),
            'alt_text': photo.alt_text or photo.title or f"{accommodation.property_name} photo",
            'title': photo.title,
            'caption': photo.caption,
            'display_order': photo.display_order,
            'is_hero': photo.is_hero,
            'media_type': photo.media_type,
        })

    all_photos_json = []
    for photo in all_photos:
        all_photos_json.append({
            'id': photo.id,
            'image_url': photo.get_image_url('large'),
            'alt_text': photo.alt_text or photo.title or f"{accommodation.property_name} photo",
            'title': photo.title,
            'caption': photo.caption,
            'display_order': photo.display_order,
            'is_hero': photo.is_hero,
            'media_type': photo.media_type,
        })

    context = {
        'accommodation': accommodation,
        'is_demo': False,
        'photos': photos,
        'hero_photos': hero_photos_json,  # Use JSON-serializable version
        'all_photos': all_photos_json,    # Use JSON-serializable version
        'hero_photos_objects': hero_photos,  # Keep objects for template rendering
        'all_photos_objects': all_photos,    # Keep objects for template rendering
        'total_photos': total_photos,
        'checkin': checkin,
        'checkout': checkout,
        'adults': adults,
        'kids': kids,
        'rooms': rooms,
    }

    return render(request, 'core/accommodation_detail.html', context)

def book_accommodation(request, id):
    """Booking page for accommodation - collect traveler information"""
    # Demo accommodations data
    demo_accommodations = [
        {
            'id': '1',
            'name': 'Luxury Beach Resort & Spa',
            'location': 'Maldives',
            'description': 'Experience paradise at our beachfront resort with private villas, world-class spa, and stunning ocean views.',
            'price': 450,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 1250,
            'type': 'resort',
            'amenities': ['WiFi', 'Pool', 'Spa', 'Beach Access', 'Restaurant'],
            'image': 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 2,
            'bathrooms': 2,
            'max_guests': 4,
            'room_type': 'Villa with Ocean View',
            'cancellation_policy': 'Free cancellation up to 24 hours',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['Private beach access', '24/7 concierge', 'Spa treatments included', 'Daily housekeeping']
        },
        {
            'id': '2',
            'name': 'Boutique City Hotel Downtown',
            'location': 'Dubai, UAE',
            'description': 'Charming boutique hotel in the heart of the city with modern design, rooftop bar, and easy access to attractions.',
            'price': 250,
            'currency': 'USD',
            'rating': 4.6,
            'reviews': 890,
            'type': 'hotel',
            'amenities': ['WiFi', 'Gym', 'Rooftop Bar', 'Concierge', 'Business Center'],
            'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Deluxe City View Room',
            'cancellation_policy': 'Free cancellation up to 48 hours',
            'check_in_time': '15:00',
            'check_out_time': '11:00',
            'property_highlights': ['Burj Khalifa views', 'Metro station nearby', 'Business center', 'Fitness center']
        },
        {
            'id': '3',
            'name': 'Mountain View Chalet',
            'location': 'Swiss Alps, Switzerland',
            'description': 'Rustic mountain chalet with stunning alpine views and modern amenities for the perfect mountain retreat.',
            'price': 350,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 567,
            'type': 'chalet',
            'amenities': ['WiFi', 'Fireplace', 'Hot Tub', 'Mountain Views', 'Ski Access'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 3,
            'bathrooms': 2,
            'max_guests': 6,
            'room_type': 'Alpine Chalet',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '16:00',
            'check_out_time': '10:00',
            'property_highlights': ['Ski-in/ski-out access', 'Wood-burning fireplace', 'Private hot tub', 'Mountain views']
        },
        {
            'id': '4',
            'name': 'Historic Riad Marrakech',
            'location': 'Marrakech, Morocco',
            'description': 'Traditional Moroccan riad in the heart of the medina with authentic architecture and modern comforts.',
            'price': 180,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 745,
            'type': 'riad',
            'amenities': ['WiFi', 'Courtyard', 'Traditional Decor', 'Rooftop Terrace', 'Hammam'],
            'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 4,
            'bathrooms': 3,
            'max_guests': 8,
            'room_type': 'Traditional Riad Suite',
            'cancellation_policy': 'Free cancellation up to 3 days',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['Medina location', 'Traditional Moroccan architecture', 'Rooftop terrace', 'Hammam spa']
        },
        {
            'id': '5',
            'name': 'Overwater Bungalow Paradise',
            'location': 'Bora Bora, French Polynesia',
            'description': 'Luxurious overwater bungalow with direct lagoon access and breathtaking sunset views.',
            'price': 650,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 423,
            'type': 'bungalow',
            'amenities': ['WiFi', 'Private Deck', 'Lagoon Access', 'Butler Service', 'Snorkeling'],
            'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Overwater Bungalow',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Crystal clear lagoon', 'Sunset views', 'Private butler service', 'Snorkeling equipment']
        },
        {
            'id': '6',
            'name': 'Urban Loft Apartment',
            'location': 'Tokyo, Japan',
            'description': 'Modern loft apartment in trendy Shibuya district with city views and contemporary design.',
            'price': 120,
            'currency': 'USD',
            'rating': 4.5,
            'reviews': 1100,
            'type': 'apartment',
            'amenities': ['WiFi', 'Kitchen', 'City Views', 'Washing Machine', 'Near Subway'],
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 3,
            'room_type': 'Modern Loft',
            'cancellation_policy': 'Free cancellation up to 5 days',
            'check_in_time': '15:00',
            'check_out_time': '10:00',
            'property_highlights': ['Shibuya district', 'City skyline views', 'Fully equipped kitchen', 'Subway access']
        },
        {
            'id': '7',
            'name': 'Desert Oasis Camp',
            'location': 'Sahara Desert, Morocco',
            'description': 'Authentic Bedouin camp in the heart of the Sahara with traditional tents and star-filled skies.',
            'price': 85,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 892,
            'type': 'camp',
            'amenities': ['Traditional Meals', 'Campfire', 'Desert Views', 'Guided Tours', 'Bedouin Hospitality'],
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Traditional Bedouin Tent',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '16:00',
            'check_out_time': '12:00',
            'property_highlights': ['Starry night skies', 'Traditional Bedouin experience', 'Camel treks available', 'Authentic Moroccan cuisine']
        },
        {
            'id': '8',
            'name': 'Lake Como Villa',
            'location': 'Lake Como, Italy',
            'description': 'Elegant villa overlooking Lake Como with private gardens and stunning mountain views.',
            'price': 420,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 634,
            'type': 'villa',
            'amenities': ['WiFi', 'Private Garden', 'Lake Views', 'Swimming Pool', 'Boat Dock'],
            'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 4,
            'bathrooms': 3,
            'max_guests': 8,
            'room_type': 'Lakefront Villa',
            'cancellation_policy': 'Free cancellation up to 10 days',
            'check_in_time': '16:00',
            'check_out_time': '10:00',
            'property_highlights': ['Private lake access', 'Mountain views', 'Professional chef available', 'Boat included']
        },
        {
            'id': '9',
            'name': 'Santorini Cave Hotel',
            'location': 'Santorini, Greece',
            'description': 'Unique cave hotel carved into volcanic rock with caldera views and traditional Cycladic architecture.',
            'price': 280,
            'currency': 'USD',
            'rating': 4.6,
            'reviews': 756,
            'type': 'hotel',
            'amenities': ['WiFi', 'Caldera Views', 'Infinity Pool', 'Spa Services', 'Restaurant'],
            'image': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Cave Suite with Caldera View',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Volcanic cave architecture', 'Sunset caldera views', 'Infinity pool', 'Traditional Greek breakfast']
        },
        {
            'id': '10',
            'name': 'Amazon Rainforest Lodge',
            'location': 'Amazon Rainforest, Brazil',
            'description': 'Eco-lodge deep in the Amazon with guided jungle walks and authentic indigenous experiences.',
            'price': 195,
            'currency': 'USD',
            'rating': 4.5,
            'reviews': 423,
            'type': 'lodge',
            'amenities': ['Eco-Friendly', 'Jungle Tours', 'Indigenous Guides', 'Sustainable Dining', 'Wildlife Viewing'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 2,
            'bathrooms': 2,
            'max_guests': 4,
            'room_type': 'Jungle Bungalow',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '12:00',
            'check_out_time': '11:00',
            'property_highlights': ['Sustainable tourism', 'Indigenous community support', 'Wildlife encounters', 'Eco-friendly practices']
        },
        {
            'id': '11',
            'name': 'Icelandic Glacier Retreat',
            'location': 'Vatnajökull, Iceland',
            'description': 'Glass-domed igloo on a glacier with northern lights views and ice cave explorations.',
            'price': 380,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 345,
            'type': 'igloo',
            'amenities': ['Northern Lights Views', 'Glacier Access', 'Ice Cave Tours', 'Thermal Bath', 'Arctic Dining'],
            'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Glass Igloo Suite',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '16:00',
            'check_out_time': '11:00',
            'property_highlights': ['Glass dome ceiling', 'Northern lights viewing', 'Glacier hiking', 'Ice cave exploration']
        },
        {
            'id': '12',
            'name': 'Parisian Haussmann Apartment',
            'location': 'Paris, France',
            'description': 'Elegant 19th-century apartment in a Haussmann building with original moldings and modern updates.',
            'price': 220,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 678,
            'type': 'apartment',
            'amenities': ['WiFi', 'Kitchen', 'Historic Architecture', 'Concierge', 'Laundry Service'],
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 2,
            'bathrooms': 1,
            'max_guests': 4,
            'room_type': 'Haussmann Apartment',
            'cancellation_policy': 'Free cancellation up to 5 days',
            'check_in_time': '15:00',
            'check_out_time': '10:00',
            'property_highlights': ['Historic 6th arrondissement', 'Walking distance to Louvre', 'Original architectural details', 'Concierge service']
        },
        {
            'id': '13',
            'name': 'Taj Mahal Palace Hotel',
            'location': 'Mumbai, India',
            'description': 'Iconic colonial-era hotel with opulent architecture, sea-facing rooms, and legendary hospitality.',
            'price': 320,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 1234,
            'type': 'hotel',
            'amenities': ['WiFi', 'Sea Views', 'Spa', 'Multiple Restaurants', 'Business Center'],
            'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Sea View Deluxe Room',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['Gateway of India views', 'Colonial architecture', 'Award-winning restaurants', 'Royal heritage']
        },
        {
            'id': '14',
            'name': 'Great Barrier Reef Resort',
            'location': 'Cairns, Australia',
            'description': 'Luxury resort with direct reef access, marine biology center, and underwater observatories.',
            'price': 480,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 567,
            'type': 'resort',
            'amenities': ['Reef Access', 'Marine Biology Center', 'Diving Center', 'Spa', 'Multiple Pools'],
            'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 2,
            'bathrooms': 2,
            'max_guests': 4,
            'room_type': 'Reef View Suite',
            'cancellation_policy': 'Free cancellation up to 10 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Direct reef access', 'Underwater observatory', 'Marine research center', 'Diving certification courses']
        },
        {
            'id': '15',
            'name': 'Scottish Highlands Castle',
            'location': 'Scottish Highlands, Scotland',
            'description': 'Historic castle in the Scottish Highlands with lochs, mountains, and traditional hospitality.',
            'price': 395,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 456,
            'type': 'castle',
            'amenities': ['WiFi', 'Fireplace', 'Loch Views', 'Whisky Bar', 'Gardens'],
            'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 5,
            'bathrooms': 4,
            'max_guests': 10,
            'room_type': 'Castle Suite',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '16:00',
            'check_out_time': '11:00',
            'property_highlights': ['Historic castle architecture', 'Loch and mountain views', 'Whisky tasting experiences', 'Private gardens']
        },
        {
            'id': '16',
            'name': 'Patagonia Glacier Lodge',
            'location': 'Torres del Paine, Chile',
            'description': 'Remote lodge in Patagonia with glacier views, hiking trails, and authentic Chilean hospitality.',
            'price': 265,
            'currency': 'USD',
            'rating': 4.6,
            'reviews': 389,
            'type': 'lodge',
            'amenities': ['Glacier Views', 'Hiking Trails', 'Fireplace', 'Local Cuisine', 'Guide Services'],
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 3,
            'bathrooms': 2,
            'max_guests': 6,
            'room_type': 'Glacier View Cabin',
            'cancellation_policy': 'Free cancellation up to 10 days',
            'check_in_time': '15:00',
            'check_out_time': '11:00',
            'property_highlights': ['Torres del Paine views', 'Guided hiking tours', 'Authentic Patagonian cuisine', 'Sustainable practices']
        },
        {
            'id': '17',
            'name': 'Venetian Canal Palace',
            'location': 'Venice, Italy',
            'description': 'Historic palace on the Grand Canal with Renaissance architecture and modern luxury amenities.',
            'price': 550,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 723,
            'type': 'palace',
            'amenities': ['Canal Views', 'Private Boat', 'Historic Architecture', 'Spa', 'Fine Dining'],
            'image': 'https://images.unsplash.com/photo-1531572753322-ad063cecc140?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 3,
            'bathrooms': 3,
            'max_guests': 6,
            'room_type': 'Canal View Palace Suite',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Grand Canal location', 'Renaissance architecture', 'Private boat service', 'Michelin-star dining']
        },
        {
            'id': '18',
            'name': 'Bali Rice Terrace Villa',
            'location': 'Ubud, Bali, Indonesia',
            'description': 'Luxurious villa nestled in rice terraces with traditional Balinese architecture and spa facilities.',
            'price': 195,
            'currency': 'USD',
            'rating': 4.7,
            'reviews': 891,
            'type': 'villa',
            'amenities': ['Rice Terrace Views', 'Private Pool', 'Spa', 'Traditional Architecture', 'Yoga Pavilion'],
            'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 3,
            'bathrooms': 3,
            'max_guests': 6,
            'room_type': 'Rice Terrace Villa',
            'cancellation_policy': 'Free cancellation up to 7 days',
            'check_in_time': '14:00',
            'check_out_time': '12:00',
            'property_highlights': ['UNESCO rice terraces', 'Traditional Balinese design', 'Daily yoga sessions', 'Organic farm-to-table dining']
        },
        {
            'id': '19',
            'name': 'New York Penthouse',
            'location': 'Manhattan, New York, USA',
            'description': 'Ultra-luxury penthouse with Central Park views, private terrace, and 24/7 concierge service.',
            'price': 850,
            'currency': 'USD',
            'rating': 4.9,
            'reviews': 234,
            'type': 'penthouse',
            'amenities': ['Central Park Views', 'Private Terrace', 'Concierge', 'Spa Bathroom', 'Chef Service'],
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 3,
            'bathrooms': 3,
            'max_guests': 6,
            'room_type': 'Central Park Penthouse',
            'cancellation_policy': 'Free cancellation up to 14 days',
            'check_in_time': '15:00',
            'check_out_time': '11:00',
            'property_highlights': ['Central Park views', 'Private rooftop terrace', '24/7 concierge', 'Personal chef service']
        },
        {
            'id': '20',
            'name': 'Safari Luxury Tent Camp',
            'location': 'Serengeti, Tanzania',
            'description': 'Luxury safari camp with canvas tents, private decks, and unparalleled wildlife viewing opportunities.',
            'price': 425,
            'currency': 'USD',
            'rating': 4.8,
            'reviews': 567,
            'type': 'camp',
            'amenities': ['Wildlife Viewing', 'Private Decks', 'Guided Safaris', 'Butler Service', 'Luxury Camping'],
            'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'bedrooms': 1,
            'bathrooms': 1,
            'max_guests': 2,
            'room_type': 'Luxury Safari Tent',
            'cancellation_policy': 'Free cancellation up to 21 days',
            'check_in_time': '14:00',
            'check_out_time': '11:00',
            'property_highlights': ['Big Five wildlife viewing', 'Private viewing decks', 'Guided safari drives', 'Authentic Maasai cultural experiences']
        }
    ]

    # Find the accommodation by ID
    accommodation = None
    for acc in demo_accommodations:
        if str(acc['id']) == str(id):
            accommodation = acc
            break

    if not accommodation:
        # If accommodation not found, redirect to accommodations list
        return redirect('accommodations')

    # Get booking parameters from request
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    adults = request.GET.get('adults', '2')
    kids = request.GET.get('kids', '0')
    rooms = request.GET.get('rooms', '1')

    # Calculate number of nights and total price
    from datetime import datetime
    try:
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
        nights = (checkout_date - checkin_date).days
        total_guests = int(adults) + int(kids)
        base_price = accommodation['price'] * nights
        cleaning_fee = 50  # Fixed cleaning fee
        service_fee = base_price * 0.08  # 8% service fee
        taxes = base_price * 0.10  # 10% taxes
        total_price = base_price + cleaning_fee + service_fee + taxes
    except:
        nights = 1
        total_guests = int(adults) + int(kids)
        base_price = accommodation['price'] * nights
        cleaning_fee = 50
        service_fee = base_price * 0.08
        taxes = base_price * 0.10
        total_price = base_price + cleaning_fee + service_fee + taxes

    if request.method == 'POST':
        # Process booking form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        paperless = request.POST.get('paperless') == 'on'
        booking_for = request.POST.get('booking_for')
        traveling_for_work = request.POST.get('traveling_for_work')
        airport_shuttle = request.POST.get('airport_shuttle') == 'on'
        car_rental = request.POST.get('car_rental') == 'on'
        taxi_shuttle = request.POST.get('taxi_shuttle') == 'on'
        special_requests = request.POST.get('special_requests')
        arrival_time = request.POST.get('arrival_time')
        terms = request.POST.get('terms') == 'on'

        # Basic validation
        if not all([first_name, last_name, email, country, phone, terms]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('book_accommodation', id=id)

        # Here you would normally save to database and process payment
        # For now, we'll just redirect to a confirmation page
        messages.success(request, f'Booking confirmed for {accommodation["name"]}! A confirmation email has been sent to {email}.')
        return redirect('dashboard')

    context = {
        'accommodation': accommodation,
        'checkin': checkin,
        'checkout': checkout,
        'adults': adults,
        'kids': kids,
        'rooms': rooms,
        'nights': nights,
        'total_guests': total_guests,
        'base_price': base_price,
        'cleaning_fee': cleaning_fee,
        'service_fee': service_fee,
        'taxes': taxes,
        'total_price': total_price,
    }

    return render(request, 'core/book_accommodation.html', context)

def dashboard(request):
    """User dashboard page"""
    return render(request, 'core/dashboard.html', {})

def hostregister(request):
    """Host registration page view"""
    # Clear any existing messages to prevent accumulation
    storage = messages.get_messages(request)
    storage.used = True
    
    if request.method == 'POST':
        form = HostRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile for host (form should handle this, but ensure it exists)
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'is_host': True}
            )
            if not created and not profile.is_host:
                profile.is_host = True
                profile.save()
            
            login(request, user)
            messages.success(request, f"Host account created successfully! Welcome to BedBees, {user.first_name or user.username}!")
            return redirect('hostdashboard')  # Always redirect hosts to host dashboard
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = HostRegistrationForm()
    return render(request, 'core/hostregister.html', {'form': form})

def tour_detail(request, id):
    """Individual tour detail page view"""
    try:
        tour = Tour.objects.get(id=id, is_published=True, is_active=True)
    except Tour.DoesNotExist:
        # If tour not found, redirect to tours list
        return redirect('tours')

    # Get photos for this tour, ordered by display_order
    photos = TourPhoto.objects.filter(
        tour=tour,
        visibility__in=['public', 'hidden']
    ).order_by('display_order', 'id')

    # Separate hero photos (first 6 or those marked as is_hero=True)
    hero_photos_queryset = photos.filter(is_hero=True)[:6]
    if not hero_photos_queryset:
        hero_photos_queryset = photos[:6]
    
    # All photos for lightbox
    all_photos_queryset = photos
    
    # Convert QuerySets to serializable lists for template
    hero_photos = []
    for photo in hero_photos_queryset:
        hero_photos.append({
            'id': photo.id,
            'image_url': photo.get_image_url('large'),
            'alt_text': photo.alt_text or photo.title or f"{tour.tour_name} photo",
            'title': photo.title,
            'caption': photo.caption,
            'display_order': photo.display_order,
            'is_hero': photo.is_hero,
        })
    
    all_photos = []
    for photo in all_photos_queryset:
        all_photos.append({
            'id': photo.id,
            'image_url': photo.get_image_url('large'),
            'alt_text': photo.alt_text or photo.title or f"{tour.tour_name} photo",
            'title': photo.title,
            'caption': photo.caption,
            'display_order': photo.display_order,
            'is_hero': photo.is_hero,
        })
    
    # Total photos count
    total_photos = len(all_photos)

    context = {
        'tour': tour,
        'hero_photos': hero_photos,
        'all_photos': all_photos,
        'total_photos': total_photos,
    }

    return render(request, 'core/tour_detail.html', context)

@login_required
def hostdashboard(request):
    """Host dashboard page view - only accessible to hosts"""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'is_host': True}
    )
    
    # Ensure only hosts can access this dashboard
    if not profile.is_host:
        messages.warning(request, "This page is only accessible to hosts. Redirecting to traveler dashboard.")
        return redirect('dashboard')
    
    # Handle profile form submission from dashboard
    if request.method == 'POST':
        form = HostProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('hostdashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = HostProfileForm(instance=profile, user=request.user)
    
    # Get host's listings
    accommodations = Accommodation.objects.filter(host=request.user).order_by('-created_at')
    tours = Tour.objects.filter(host=request.user).order_by('-created_at')

    context = {
        'user': request.user,
        'profile': profile,
        'form': form,
        'accommodations': accommodations,
        'tours': tours,
    }
    return render(request, 'core/hostdashboard.html', context)

@login_required  
def host_profile(request):
    """Host profile management view"""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'is_host': True}
    )
    
    if request.method == 'POST':
        form = HostProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('host_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = HostProfileForm(instance=profile, user=request.user)
    
    context = {
        'form': form,
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'core/host_profile.html', context)

def profile(request):
    """User profile page view"""
    if not request.user.is_authenticated:
        messages.warning(request, "Please sign in to access your profile.")
        return redirect('signin')

    context = {
        'user': request.user,
    }
    return render(request, 'core/profile.html', context)

def logout_view(request):
    """Custom logout view"""
    logout(request)
    # Clear any existing messages to prevent accumulation
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # Always redirect to home after logout

def create_listing(request):
    """Create listing selection page"""
    if not request.user.is_authenticated:
        messages.warning(request, "Please sign in to create a listing.")
        return redirect('signin')
    return render(request, 'core/create_listing.html')

@login_required
def create_accommodation(request):
    """Create accommodation listing page"""
    if request.method == 'POST':
        # Get checkbox list data
        amenities_list = request.POST.getlist('amenities')
        amenities_str = ','.join(amenities_list) if amenities_list else ''

        property_features_list = request.POST.getlist('property_features')
        property_features_str = ','.join(property_features_list) if property_features_list else ''

        nearby_landmarks_list = request.POST.getlist('nearby_landmarks')
        nearby_landmarks_str = ','.join(nearby_landmarks_list) if nearby_landmarks_list else ''

        # Create a mutable copy of POST data
        post_data = request.POST.copy()
        post_data['amenities'] = amenities_str
        post_data['property_features'] = property_features_str
        post_data['nearby_landmarks'] = nearby_landmarks_str

        form = AccommodationForm(post_data, request.FILES)
        if form.is_valid():
            accommodation = form.save(commit=False)
            accommodation.host = request.user
            accommodation.is_published = True
            
            # Explicitly set cancellation_policy from POST data
            cancellation_policy = request.POST.get('cancellation_policy')
            if cancellation_policy:
                accommodation.cancellation_policy = cancellation_policy
            
            accommodation.save()

            # Handle photo uploads
            photos = request.FILES.getlist('photos')
            for index, photo in enumerate(photos):
                AccommodationPhoto.objects.create(
                    accommodation=accommodation,
                    original_file=photo,
                    media_type='image',
                    is_hero=(index == 0),
                    display_order=index,
                    visibility='public'
                )

            messages.success(request, f'Accommodation "{accommodation.property_name}" created successfully!')
            return redirect('hostdashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AccommodationForm()

    return render(request, 'core/create_accommodation.html', {'form': form})

@login_required
def create_tour(request):
    """Create tour listing page"""
    if request.method == 'POST':
        # Get form data
        inclusions_list = request.POST.getlist('inclusions')
        inclusions_str = ','.join(inclusions_list) if inclusions_list else ''

        # Create a mutable copy of POST data
        post_data = request.POST.copy()
        post_data['inclusions'] = inclusions_str

        form = TourForm(post_data, request.FILES)
        if form.is_valid():
            tour = form.save(commit=False)
            tour.host = request.user
            tour.is_published = True
            tour.save()

            # Handle photo uploads
            photos = request.FILES.getlist('photos')
            for index, photo in enumerate(photos):
                TourPhoto.objects.create(
                    tour=tour,
                    image=photo,
                    is_primary=(index == 0),
                    order=index
                )

            messages.success(request, f'Tour "{tour.tour_name}" created successfully!')
            return redirect('hostdashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TourForm()

    return render(request, 'core/create_tour.html', {'form': form})

def bookings(request):
    """User bookings page view"""
    if not request.user.is_authenticated:
        messages.warning(request, "Please sign in to view your bookings.")
        return redirect('signin')

    # Mock bookings data (in a real app, this would come from the database)
    mock_bookings = [
        {
            'id': 'BK-2025-001',
            'type': 'tour',
            'title': 'Historic Cyprus Cultural Walking Tour',
            'location': 'Nicosia, Cyprus',
            'start_date': '2025-10-15',
            'end_date': '2025-10-15',
            'status': 'confirmed',
            'total_price': 2500,
            'currency': 'USD',
            'guests': 2,
            'image': 'hero/apartment.webp',
            'booking_date': '2025-09-20',
            'booking_reference': 'CY-001-2025',
            'provider': {
                'name': 'Cyprus Cultural Tours',
                'rating': 4.8,
                'reviews': 1247,
            },
            'cancellation_policy': 'Free cancellation up to 24 hours before',
            'special_requests': 'Vegetarian meals preferred',
            'contact_info': {
                'phone': '+357 22 123456',
                'email': 'info@cyprus-tours.com',
            },
        },
        {
            'id': 'BK-2025-002',
            'type': 'accommodation',
            'title': 'Luxury Downtown Hotel Suite',
            'location': 'New York, NY, USA',
            'start_date': '2025-11-01',
            'end_date': '2025-11-05',
            'status': 'confirmed',
            'total_price': 48000,
            'currency': 'USD',
            'guests': 2,
            'image': 'hero/hotel.webp',
            'booking_date': '2025-09-18',
            'booking_reference': 'NY-002-2025',
            'provider': {
                'name': 'Grand Hotel Manhattan',
                'rating': 4.6,
                'reviews': 2156,
            },
            'cancellation_policy': 'Free cancellation up to 48 hours before',
            'special_requests': 'Late check-out requested',
            'contact_info': {
                'phone': '+1 (555) 123-4567',
                'email': 'reservations@grandhotel.com',
            },
        },
        {
            'id': 'BK-2025-003',
            'type': 'tour',
            'title': 'Wadi Rum Desert Safari Adventure',
            'location': 'Wadi Rum, Jordan',
            'start_date': '2025-12-10',
            'end_date': '2025-12-10',
            'status': 'pending',
            'total_price': 14500,
            'currency': 'USD',
            'guests': 4,
            'image': 'hero/villa.webp',
            'booking_date': '2025-09-22',
            'booking_reference': 'JO-003-2025',
            'provider': {
                'name': 'Desert Adventures Co.',
                'rating': 4.9,
                'reviews': 892,
            },
            'cancellation_policy': 'Free cancellation up to 72 hours before',
            'special_requests': 'All participants are experienced hikers',
            'contact_info': {
                'phone': '+962 3 123456',
                'email': 'bookings@desert-adventures.com',
            },
        },
        {
            'id': 'BK-2025-004',
            'type': 'accommodation',
            'title': 'Mountain View Chalet',
            'location': 'Zermatt, Switzerland',
            'start_date': '2025-09-25',
            'end_date': '2025-09-28',
            'status': 'completed',
            'total_price': 14000,
            'currency': 'USD',
            'guests': 3,
            'image': 'hero/chalets.webp',
            'booking_date': '2025-08-15',
            'booking_reference': 'CH-004-2025',
            'provider': {
                'name': 'Alpine Chalets',
                'rating': 4.7,
                'reviews': 634,
            },
            'cancellation_policy': 'Free cancellation up to 7 days before',
            'special_requests': 'Ski equipment rental needed',
            'contact_info': {
                'phone': '+41 27 123 4567',
                'email': 'info@alpine-chalets.ch',
            },
        },
    ]

    # Get filter parameters from request
    filter_status = request.GET.get('status', 'all')
    filter_type = request.GET.get('type', 'all')
    sort_by = request.GET.get('sort', 'date-desc')

    # Filter bookings
    filtered_bookings = mock_bookings
    if filter_status != 'all':
        filtered_bookings = [b for b in filtered_bookings if b['status'] == filter_status]
    if filter_type != 'all':
        filtered_bookings = [b for b in filtered_bookings if b['type'] == filter_type]

    # Sort bookings
    if sort_by == 'date-desc':
        filtered_bookings.sort(key=lambda x: x['booking_date'], reverse=True)
    elif sort_by == 'date-asc':
        filtered_bookings.sort(key=lambda x: x['booking_date'])
    elif sort_by == 'price-desc':
        filtered_bookings.sort(key=lambda x: x['total_price'], reverse=True)
    elif sort_by == 'price-asc':
        filtered_bookings.sort(key=lambda x: x['total_price'])

    # Calculate stats
    total_bookings = len(filtered_bookings)
    upcoming_bookings = len([b for b in filtered_bookings if b['status'] in ['confirmed', 'pending']])
    total_spent = sum(b['total_price'] for b in filtered_bookings if b['status'] == 'confirmed')

    context = {
        'user': request.user,
        'bookings': filtered_bookings,
        'total_bookings': total_bookings,
        'upcoming_bookings': upcoming_bookings,
        'total_spent': total_spent,
        'filter_status': filter_status,
        'filter_type': filter_type,
        'sort_by': sort_by,
    }
    return render(request, 'core/bookings.html', context)


def countries(request):
    """Countries page view"""
    # Demo countries data
    demo_countries = [
        {
            'name': 'Jordan',
            'code': 'jordan',
            'description': 'Explore the ancient wonders of Jordan, from the rose-red city of Petra to the salty shores of the Dead Sea.',
            'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
            'accommodations_count': 245,
            'tours_count': 89,
            'attractions': ['Petra', 'Dead Sea', 'Wadi Rum', 'Jerash', 'Amman Citadel']
        },
        {
            'name': 'Cyprus',
            'code': 'cyprus',
            'description': 'Discover the Mediterranean paradise of Cyprus with its stunning beaches, ancient history, and vibrant culture.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 312,
            'tours_count': 156,
            'attractions': ['Nicosia', 'Limassol', 'Paphos', 'Troodos Mountains', 'Famagusta']
        },
        {
            'name': 'Greece',
            'code': 'greece',
            'description': 'Experience the birthplace of Western civilization with its iconic islands, ancient ruins, and delicious cuisine.',
            'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 567,
            'tours_count': 234,
            'attractions': ['Athens', 'Santorini', 'Mykonos', 'Crete', 'Olympia']
        },
        {
            'name': 'Turkey',
            'code': 'turkey',
            'description': 'Bridge between Europe and Asia, offering rich history, stunning landscapes, and warm hospitality.',
            'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 423,
            'tours_count': 198,
            'attractions': ['Istanbul', 'Cappadocia', 'Pamukkale', 'Ephesus', 'Antalya']
        },
        {
            'name': 'Egypt',
            'code': 'egypt',
            'description': 'Home to the ancient pyramids and pharaohs, with a rich history spanning thousands of years.',
            'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 389,
            'tours_count': 167,
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
            'tours_count': 345,
            'attractions': ['Burj Khalifa', 'Palm Jumeirah', 'Dubai Mall', 'Sheikh Zayed Grand Mosque', 'Dubai Desert Safari']
        },
        {
            'name': 'Lebanon',
            'code': 'lebanon',
            'description': 'A Mediterranean jewel known for its ancient history, vibrant culture, and stunning coastal beauty.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 234,
            'tours_count': 156,
            'attractions': ['Beirut', 'Baalbek', 'Byblos', 'Jeita Grotto', 'Cedars of God']
        },
        {
            'name': 'Qatar',
            'code': 'qatar',
            'description': 'A modern Arabian nation blending rich heritage with world-class luxury and sporting excellence.',
            'image': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 167,
            'tours_count': 89,
            'attractions': ['Doha', 'Museum of Islamic Art', 'Souq Waqif', 'Katara Cultural Village', 'Al Zubarah Fort']
        },
        {
            'name': 'Saudi Arabia',
            'code': 'saudi-arabia',
            'description': 'The heart of Islam with ancient deserts, modern cities, and sacred pilgrimage sites.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 445,
            'tours_count': 234,
            'attractions': ['Mecca', 'Medina', 'Riyadh', 'AlUla', 'Red Sea Coast']
        },
        {
            'name': 'Kuwait',
            'code': 'kuwait',
            'description': 'A modern Gulf state with rich cultural heritage, stunning desert landscapes, and warm hospitality.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 123,
            'tours_count': 67,
            'attractions': ['Kuwait City', 'Kuwait Towers', 'Liberation Tower', 'Tareq Rajab Museum', 'Al Shaheed Park']
        },
        {
            'name': 'Bahrain',
            'code': 'bahrain',
            'description': 'An island kingdom blending ancient Dilmun civilization with modern Arabian Gulf culture.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 89,
            'tours_count': 45,
            'attractions': ['Manama', 'Bahrain Fort', 'Al Fateh Grand Mosque', 'Bahrain World Trade Center', 'Tree of Life']
        },
        {
            'name': 'Oman',
            'code': 'oman',
            'description': 'An Arabian paradise of stunning deserts, turquoise coasts, and ancient fortresses.',
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 156,
            'tours_count': 78,
            'attractions': ['Muscat', 'Nizwa Fort', 'Wahiba Sands', 'Jebel Shams', 'Sur']
        },
        {
            'name': 'Syria',
            'code': 'syria',
            'description': 'Ancient land of civilization with rich history, stunning architecture, and Mediterranean charm.',
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 89,
            'tours_count': 45,
            'attractions': ['Damascus', 'Aleppo', 'Palmyra', 'Krak des Chevaliers', 'Bosra']
        },
        {
            'name': 'Iraq',
            'code': 'iraq',
            'description': 'Land of ancient Mesopotamia with rich history, archaeological treasures, and cultural heritage.',
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 67,
            'tours_count': 34,
            'attractions': ['Baghdad', 'Babylon', 'Uruk', 'Karbala', 'Erbil Citadel']
        },
        {
            'name': 'Yemen',
            'code': 'yemen',
            'description': 'Ancient land of spices, towering mountains, and rich cultural heritage.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 45,
            'tours_count': 23,
            'attractions': ['Sana\'a', 'Socotra Island', 'Zabid', 'Shibam', 'Aden']
        },
        {
            'name': 'Tunisia',
            'code': 'tunisia',
            'description': 'North African gem with ancient Carthage ruins, Mediterranean beaches, and vibrant souks.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 234,
            'tours_count': 156,
            'attractions': ['Tunis', 'Carthage', 'Sidi Bou Said', 'Kairouan', 'Sahara Desert']
        },
        {
            'name': 'Algeria',
            'code': 'algeria',
            'description': 'Maghreb nation with stunning Sahara landscapes, ancient Roman ruins, and coastal beauty.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 189,
            'tours_count': 98,
            'attractions': ['Algiers', 'Casbah of Algiers', 'Timgad', 'Hoggar Mountains', 'Sahara Dunes']
        },
        {
            'name': 'Palestine',
            'code': 'palestine',
            'description': 'Holy Land with ancient Jerusalem, biblical sites, and rich cultural heritage.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 167,
            'tours_count': 89,
            'attractions': ['Jerusalem', 'Bethlehem', 'Hebron', 'Nazareth', 'Dead Sea']
        },
        {
            'name': 'Libya',
            'code': 'libya',
            'description': 'Ancient land of the Sahara with Roman ruins, Mediterranean coast, and desert adventures.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 145,
            'tours_count': 78,
            'attractions': ['Tripoli', 'Leptis Magna', 'Sabratha', 'Benghazi', 'Sahara Desert']
        },
        {
            'name': 'Sudan',
            'code': 'sudan',
            'description': 'Land of ancient Nubian kingdoms, Nile River cataracts, and diverse wildlife.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 123,
            'tours_count': 67,
            'attractions': ['Khartoum', 'Meroë', 'Nubian Pyramids', 'Nile Cataracts', 'Red Sea Coast']
        }
    ]
    
    # Handle search functionality
    search_query = request.GET.get('q', '').strip()
    countries = demo_countries
    
    if search_query:
        # Filter countries based on search query
        filtered_countries = []
        query_lower = search_query.lower()
        
        for country in demo_countries:
            # Search in country name, description, and attractions
            if (query_lower in country['name'].lower() or 
                query_lower in country['description'].lower() or
                any(query_lower in attraction.lower() for attraction in country['attractions'])):
                filtered_countries.append(country)
        
        countries = filtered_countries
    
    context = {
        'countries': countries,
        'search_query': search_query,
    }
    return render(request, 'core/countries.html', context)


def destinations(request):
    """Destinations page view - shows available destinations with tour and accommodation counts"""
    # Demo destinations data (same as countries for now, but can be customized)
    demo_destinations = [
        {
            'name': 'Jordan',
            'code': 'jordan',
            'description': 'Explore the ancient wonders of Jordan, from the rose-red city of Petra to the salty shores of the Dead Sea.',
            'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
            'accommodations_count': 245,
            'tours_count': 89,
            'attractions': ['Petra', 'Dead Sea', 'Wadi Rum', 'Jerash', 'Amman Citadel']
        },
        {
            'name': 'Cyprus',
            'code': 'cyprus',
            'description': 'Discover the Mediterranean paradise of Cyprus with its stunning beaches, ancient history, and vibrant culture.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 312,
            'tours_count': 156,
            'attractions': ['Nicosia', 'Limassol', 'Paphos', 'Troodos Mountains', 'Famagusta']
        },
        {
            'name': 'Greece',
            'code': 'greece',
            'description': 'Experience the birthplace of Western civilization with its iconic islands, ancient ruins, and delicious cuisine.',
            'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 567,
            'tours_count': 234,
            'attractions': ['Athens', 'Santorini', 'Mykonos', 'Crete', 'Olympia']
        },
        {
            'name': 'Turkey',
            'code': 'turkey',
            'description': 'Bridge between Europe and Asia, offering rich history, stunning landscapes, and warm hospitality.',
            'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 423,
            'tours_count': 198,
            'attractions': ['Istanbul', 'Cappadocia', 'Pamukkale', 'Ephesus', 'Antalya']
        },
        {
            'name': 'Egypt',
            'code': 'egypt',
            'description': 'Home to the ancient pyramids and pharaohs, with a rich history spanning thousands of years.',
            'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 389,
            'tours_count': 167,
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
            'tours_count': 345,
            'attractions': ['Burj Khalifa', 'Palm Jumeirah', 'Dubai Mall', 'Sheikh Zayed Mosque', 'Dubai Desert Safari']
        },
        {
            'name': 'Lebanon',
            'code': 'lebanon',
            'description': 'A Mediterranean jewel known for its ancient history, vibrant culture, and stunning coastal beauty.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 234,
            'tours_count': 156,
            'attractions': ['Beirut', 'Baalbek', 'Byblos', 'Jeita Grotto', 'Cedars of God']
        },
        {
            'name': 'Qatar',
            'code': 'qatar',
            'description': 'A modern Arabian nation blending rich heritage with world-class luxury and sporting excellence.',
            'image': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 167,
            'tours_count': 89,
            'attractions': ['Doha', 'Museum of Islamic Art', 'Souq Waqif', 'Katara Cultural Village', 'Al Zubarah Fort']
        },
        {
            'name': 'Saudi Arabia',
            'code': 'saudi-arabia',
            'description': 'The heart of Islam with ancient deserts, modern cities, and sacred pilgrimage sites.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 445,
            'tours_count': 234,
            'attractions': ['Mecca', 'Medina', 'Riyadh', 'AlUla', 'Red Sea Coast']
        },
        {
            'name': 'Kuwait',
            'code': 'kuwait',
            'description': 'A modern Gulf state with rich cultural heritage, stunning desert landscapes, and warm hospitality.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 123,
            'tours_count': 67,
            'attractions': ['Kuwait City', 'Kuwait Towers', 'Liberation Tower', 'Tareq Rajab Museum', 'Al Shaheed Park']
        },
        {
            'name': 'Bahrain',
            'code': 'bahrain',
            'description': 'An island kingdom blending ancient Dilmun civilization with modern Arabian Gulf culture.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 89,
            'tours_count': 45,
            'attractions': ['Manama', 'Bahrain Fort', 'Al Fateh Grand Mosque', 'Bahrain World Trade Center', 'Tree of Life']
        },
        {
            'name': 'Oman',
            'code': 'oman',
            'description': 'An Arabian paradise of stunning deserts, turquoise coasts, and ancient fortresses.',
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 156,
            'tours_count': 78,
            'attractions': ['Muscat', 'Nizwa Fort', 'Wahiba Sands', 'Jebel Shams', 'Sur']
        },
        {
            'name': 'Syria',
            'code': 'syria',
            'description': 'Ancient land of civilization with rich history, stunning architecture, and Mediterranean charm.',
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 89,
            'tours_count': 45,
            'attractions': ['Damascus', 'Aleppo', 'Palmyra', 'Krak des Chevaliers', 'Bosra']
        },
        {
            'name': 'Iraq',
            'code': 'iraq',
            'description': 'Land of ancient Mesopotamia with rich history, archaeological treasures, and cultural heritage.',
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 67,
            'tours_count': 34,
            'attractions': ['Baghdad', 'Babylon', 'Uruk', 'Karbala', 'Erbil Citadel']
        },
        {
            'name': 'Yemen',
            'code': 'yemen',
            'description': 'Ancient land of spices, towering mountains, and rich cultural heritage.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 45,
            'tours_count': 23,
            'attractions': ['Sana\'a', 'Socotra Island', 'Zabid', 'Shibam', 'Aden']
        }
    ]
    
    # Handle search functionality
    search_query = request.GET.get('q', '').strip()
    destinations = demo_destinations
    
    if search_query:
        # Filter destinations based on search query
        filtered_destinations = []
        query_lower = search_query.lower()
        
        for destination in demo_destinations:
            # Search in destination name, description, and attractions
            if (query_lower in destination['name'].lower() or 
                query_lower in destination['description'].lower() or
                any(query_lower in attraction.lower() for attraction in destination['attractions'])):
                filtered_destinations.append(destination)
        
        destinations = filtered_destinations
    
    context = {
        'destinations': destinations,
        'search_query': search_query,
    }
    return render(request, 'core/destinations.html', context)


def cart(request):
    """Cart page view - shows user's selected accommodations and tours"""
    # Demo cart data (in a real app, this would come from session or database)
    demo_cart_items = [
        {
            'id': 1,
            'type': 'accommodation',
            'name': 'Petra Marriott\'s Wadi Rum Nabatean Resort',
            'location': 'Wadi Rum, Jordan',
            'check_in': '2024-02-15',
            'check_out': '2024-02-18',
            'guests': 2,
            'nights': 3,
            'price_per_night': 250,
            'total_price': 750,
            'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'rating': 4.8,
            'amenities': ['WiFi', 'Pool', 'Breakfast', 'Spa']
        },
        {
            'id': 2,
            'type': 'tour',
            'name': 'Petra Full Day Tour',
            'location': 'Petra, Jordan',
            'date': '2024-02-16',
            'participants': 2,
            'duration': '8 hours',
            'price_per_person': 85,
            'total_price': 170,
            'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
            'rating': 4.9,
            'inclusions': ['Guide', 'Transport', 'Entry fees', 'Lunch']
        },
        {
            'id': 3,
            'type': 'accommodation',
            'name': 'Mövenpick Resort Petra',
            'location': 'Petra, Jordan',
            'check_in': '2024-02-16',
            'check_out': '2024-02-19',
            'guests': 2,
            'nights': 3,
            'price_per_night': 180,
            'total_price': 540,
            'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
            'rating': 4.6,
            'amenities': ['WiFi', 'Restaurant', 'Bar', 'Fitness center']
        }
    ]
    
    # Calculate totals
    subtotal = sum(item['total_price'] for item in demo_cart_items)
    service_fee = round(subtotal * 0.08, 2)  # 8% service fee
    taxes = round(subtotal * 0.10, 2)  # 10% taxes
    total = subtotal + service_fee + taxes
    
    context = {
        'cart_items': demo_cart_items,
        'subtotal': subtotal,
        'service_fee': service_fee,
        'taxes': taxes,
        'total': total,
        'item_count': len(demo_cart_items),
    }
    return render(request, 'core/cart.html', context)


def wishlist(request):
    """Wishlist page view - shows user's saved accommodations and tours"""
    # Demo wishlist data (in a real app, this would come from database)
    demo_wishlist_items = [
        {
            'id': 1,
            'type': 'accommodation',
            'name': 'Burj Al Arab Jumeirah',
            'location': 'Dubai, UAE',
            'rating': 4.9,
            'price': 1200,
            'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'description': 'Iconic luxury hotel shaped like a sail, offering unparalleled luxury and service.',
            'amenities': ['Private Beach', 'Spa', 'Fine Dining', 'Helipad'],
            'added_date': '2024-01-15'
        },
        {
            'id': 2,
            'type': 'tour',
            'name': 'Sahara Desert Camel Trek',
            'location': 'Morocco',
            'rating': 4.9,
            'price': 220,
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'description': 'Experience the magic of the Sahara with traditional Bedouin camps and camel trekking.',
            'duration': '2 days',
            'inclusions': ['Camel Trek', 'Bedouin Camp', 'Traditional Dinner', 'Guide'],
            'added_date': '2024-01-12'
        },
        {
            'id': 3,
            'type': 'accommodation',
            'name': 'Canaves Oia Boutique Hotel',
            'location': 'Santorini, Greece',
            'rating': 4.9,
            'price': 450,
            'image': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80',
            'description': 'Luxury boutique hotel with stunning caldera views and personalized service.',
            'amenities': ['Caldera View', 'Infinity Pool', 'Spa', 'Restaurant'],
            'added_date': '2024-01-10'
        },
        {
            'id': 4,
            'type': 'tour',
            'name': 'Petra Full Day Tour',
            'location': 'Petra, Jordan',
            'rating': 4.9,
            'price': 85,
            'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
            'description': 'Explore the ancient rock-cut city of Petra, a UNESCO World Heritage Site.',
            'duration': '8 hours',
            'inclusions': ['Guide', 'Transport', 'Entry Fees', 'Lunch'],
            'added_date': '2024-01-08'
        },
        {
            'id': 5,
            'type': 'accommodation',
            'name': 'Ciragan Palace Kempinski Istanbul',
            'location': 'Istanbul, Turkey',
            'rating': 4.9,
            'price': 420,
            'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'description': 'Historic palace turned luxury hotel on the Bosphorus with Ottoman architecture.',
            'amenities': ['Bosphorus View', 'Spa', 'Fine Dining', 'Historic Building'],
            'added_date': '2024-01-05'
        },
        {
            'id': 6,
            'type': 'tour',
            'name': 'Cappadocia Hot Air Balloon Tour',
            'location': 'Cappadocia, Turkey',
            'rating': 4.9,
            'price': 180,
            'image': 'https://images.unsplash.com/photo-1578271887552-5ac9e7c7b5d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'description': 'Soar above the fairy chimneys in a hot air balloon at sunrise.',
            'duration': '4 hours',
            'inclusions': ['Hot Air Balloon', 'Transfer', 'Breakfast', 'Certificate'],
            'added_date': '2024-01-03'
        }
    ]
    
    # Separate accommodations and tours
    accommodations = [item for item in demo_wishlist_items if item['type'] == 'accommodation']
    tours = [item for item in demo_wishlist_items if item['type'] == 'tour']
    
    context = {
        'wishlist_items': demo_wishlist_items,
        'accommodations': accommodations,
        'tours': tours,
        'total_items': len(demo_wishlist_items),
        'accommodations_count': len(accommodations),
        'tours_count': len(tours),
    }
    return render(request, 'core/wishlist.html', context)


def country_detail(request, country):
    """Country detail page view"""
    # Demo country data
    countries_data = {
        'jordan': {
            'name': 'Jordan',
            'description': 'Explore the ancient wonders of Jordan, from the rose-red city of Petra to the salty shores of the Dead Sea.',
            'long_description': 'Jordan, a country steeped in history and natural beauty, offers travelers an unforgettable journey through time. From the majestic rock-cut architecture of Petra to the therapeutic waters of the Dead Sea, every corner tells a story of ancient civilizations and breathtaking landscapes.',
            'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
            'hero_image': '/static/core/images/ruined-ancient-building-made-large-towers-rocks-clear-sky.jpg',
            'accommodations_count': 245,
            'tours_count': 89,
            'attractions': [
                {'name': 'Petra', 'slug': 'petra', 'description': 'Ancient rock-cut city and UNESCO World Heritage Site', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Wadi Rum', 'slug': 'wadi-rum', 'description': 'Desert landscape known as Valley of the Moon', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dead Sea', 'slug': 'dead-sea', 'description': 'Lowest point on Earth with mineral-rich waters', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Jerash', 'slug': 'jerash', 'description': 'Ancient Roman city with well-preserved ruins', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mount Nebo', 'slug': 'mount-nebo', 'description': 'Sacred biblical site where Moses viewed the Promised Land', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Madaba', 'slug': 'madaba', 'description': 'City of Mosaics with famous 6th-century Byzantine map', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Amman Citadel', 'slug': 'amman-citadel', 'description': 'Ancient fortress with Temple of Hercules', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Aqaba', 'slug': 'aqaba', 'description': 'Red Sea resort city with diving and beaches', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bethany Beyond the Jordan', 'slug': 'bethany-beyond-jordan', 'description': 'UNESCO baptism site of Jesus', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ajloun Castle', 'slug': 'ajloun-castle', 'description': '12th-century fortress built by Saladin\'s forces', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Karak Castle', 'slug': 'karak-castle', 'description': 'Largest Crusader castle in the Levant', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dana Biosphere Reserve', 'slug': 'dana-reserve', 'description': 'Jordan\'s largest nature reserve with diverse ecosystems', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Umm Qais (Gadara)', 'slug': 'umm-qais', 'description': 'Ancient Decapolis city with views over three countries', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Qasr Amra', 'slug': 'qasr-amra', 'description': 'UNESCO desert castle with 8th-century frescoes', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Azraq Wetland Reserve', 'slug': 'azraq-wetland', 'description': 'Desert oasis and bird sanctuary', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Wadi Mujib', 'slug': 'wadi-mujib', 'description': 'Jordan\'s Grand Canyon with canyoning adventures', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Little Petra', 'slug': 'little-petra', 'description': 'Nabataean site with rare ancient frescoes', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Shobak Castle', 'slug': 'shobak-castle', 'description': 'First Crusader castle in the region', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Pella', 'slug': 'pella', 'description': 'Ancient city with 8,000 years of history', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Rainbow Street', 'slug': 'rainbow-street', 'description': 'Vibrant cultural hub in Amman', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Petra Marriott\'s Wadi Rum Nabatean Resort', 'location': 'Wadi Rum', 'rating': 4.8, 'price': 250, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mövenpick Resort Petra', 'location': 'Petra', 'rating': 4.6, 'price': 180, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Kempinski Hotel Ishtar Dead Sea', 'location': 'Dead Sea', 'rating': 4.7, 'price': 220, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Petra Full Day Tour', 'duration': '8 hours', 'price': 85, 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Wadi Rum Desert Safari', 'duration': '6 hours', 'price': 65, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dead Sea Experience', 'duration': '4 hours', 'price': 45, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'cyprus': {
            'name': 'Cyprus',
            'description': 'Discover the Mediterranean paradise of Cyprus with its stunning beaches, ancient history, and vibrant culture.',
            'long_description': 'Cyprus, the third largest island in the Mediterranean, offers a perfect blend of ancient history and modern luxury. From the divided capital of Nicosia to the stunning beaches of Paphos, Cyprus provides an unforgettable Mediterranean experience with rich cultural heritage and breathtaking natural beauty.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 312,
            'tours_count': 156,
            'attractions': [
                {'name': 'Kato Paphos Archaeological Park', 'slug': 'kato-paphos-archaeological-park', 'description': 'UNESCO site with Roman mosaics', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Tombs of the Kings', 'slug': 'tombs-of-the-kings', 'description': '4th century BC underground monuments', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Aphrodite\'s Rock Petra tou Romiou', 'slug': 'aphrodites-rock-petra-tou-romiou', 'description': 'Legendary birthplace of Aphrodite', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Paphos Castle', 'slug': 'paphos-castle', 'description': 'Medieval fort and cultural venue', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Kourion', 'slug': 'kourion', 'description': 'Ancient city on cliff with amphitheater', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Kolossi Castle', 'slug': 'kolossi-castle', 'description': '15th century Knights Templar castle', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mount Olympus Troodos', 'slug': 'mount-olympus-troodos', 'description': 'Highest point 1,952m', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Akamas Peninsula', 'slug': 'akamas-peninsula', 'description': 'Blue Lagoon and Aphrodite\'s baths', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Nissi Beach', 'slug': 'nissi-beach', 'description': '500m white sand beach', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ayia Napa', 'slug': 'ayia-napa', 'description': 'Party destination and beaches', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Nicosia Old Town', 'slug': 'nicosia-old-town', 'description': 'Divided capital with Green Line', 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Larnaca Salt Lake', 'slug': 'larnaca-salt-lake', 'description': 'Flamingo watching', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Kykkos Monastery', 'slug': 'kykkos-monastery', 'description': 'Famous mountain monastery', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Cape Greco', 'slug': 'cape-greco', 'description': 'National park with sea caves', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Limassol Castle', 'slug': 'limassol-castle', 'description': 'Medieval museum', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ancient Salamis', 'slug': 'ancient-salamis', 'description': 'Roman ruins near Famagusta', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bellapais Abbey', 'slug': 'bellapais-abbey', 'description': 'Gothic monastery ruins', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Protaras Fig Tree Bay', 'slug': 'protaras-fig-tree-bay', 'description': 'Family beach', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Amathus Beach Hotel Limassol', 'location': 'Limassol', 'rating': 4.7, 'price': 180, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Constantinou Bros Asimina Suites', 'location': 'Paphos', 'rating': 4.8, 'price': 220, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Four Seasons Hotel Limassol', 'location': 'Limassol', 'rating': 4.9, 'price': 350, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Nicosia Cultural Walking Tour', 'duration': '3 hours', 'price': 25, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Paphos Archaeological Park Tour', 'duration': '4 hours', 'price': 35, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Troodos Mountains Adventure', 'duration': '8 hours', 'price': 85, 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'greece': {
            'name': 'Greece',
            'description': 'Experience the birthplace of Western civilization with its iconic islands, ancient ruins, and delicious cuisine.',
            'long_description': 'Greece, the cradle of Western civilization, offers an extraordinary journey through ancient history and stunning natural beauty. From the iconic Acropolis in Athens to the breathtaking sunsets of Santorini, Greece combines archaeological wonders with pristine beaches and world-renowned cuisine.',
            'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80',
            'accommodations_count': 567,
            'tours_count': 234,
            'attractions': [
                {'name': 'Acropolis of Athens', 'slug': 'acropolis-of-athens', 'description': 'UNESCO World Heritage with Parthenon', 'image': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80'},
                {'name': 'Acropolis Museum', 'slug': 'acropolis-museum', 'description': '4,250+ ancient artifacts', 'image': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80'},
                {'name': 'Santorini Oia & Fira', 'slug': 'santorini-oia-fira', 'description': 'Clifftop villages with blue domes', 'image': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mykonos', 'slug': 'mykonos', 'description': 'Glamorous island with Paradise Beach', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Crete & Balos Lagoon', 'slug': 'crete-balos-lagoon', 'description': 'Beaches and ancient ruins', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ancient Delphi', 'slug': 'ancient-delphi', 'description': 'Oracle sanctuary UNESCO site', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Meteora Monasteries', 'slug': 'meteora-monasteries', 'description': 'Rock formations with Byzantine monasteries', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Rhodes Old Town', 'slug': 'rhodes-old-town', 'description': 'Medieval walled city', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Zakynthos Navagio Beach', 'slug': 'zakynthos-navagio-beach', 'description': 'Shipwreck beach', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Corfu Old Town', 'slug': 'corfu-old-town', 'description': 'Venetian architecture', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ancient Olympia', 'slug': 'ancient-olympia', 'description': 'Birthplace of Olympics', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Thessaloniki White Tower', 'slug': 'thessaloniki-white-tower', 'description': 'Byzantine monument', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Naxos', 'slug': 'naxos', 'description': 'Largest Cyclades island', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Akrotiri Santorini', 'slug': 'akrotiri-santorini', 'description': 'Bronze Age archaeological site', 'image': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Plaka Athens', 'slug': 'plaka-athens', 'description': 'Oldest neighborhood', 'image': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80'},
                {'name': 'Samaria Gorge Crete', 'slug': 'samaria-gorge-crete', 'description': '16km hiking trail', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Little Venice Mykonos', 'slug': 'little-venice-mykonos', 'description': 'Sunset viewing spot', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Knossos Palace Crete', 'slug': 'knossos-palace-crete', 'description': 'Minoan palace ruins', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Paros', 'slug': 'paros', 'description': 'Island with marble quarries', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Lindos Acropolis Rhodes', 'slug': 'lindos-acropolis-rhodes', 'description': 'Ancient citadel', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Canaves Oia Boutique Hotel', 'location': 'Santorini', 'rating': 4.9, 'price': 450, 'image': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80'},
                {'name': 'St. Regis Athens', 'location': 'Athens', 'rating': 4.8, 'price': 380, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Grace Hotel Mykonos', 'location': 'Mykonos', 'rating': 4.7, 'price': 320, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'}
            ],
            'tours': [
                {'name': 'Acropolis of Athens Tour', 'duration': '4 hours', 'price': 45, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80'},
                {'name': 'Santorini Sunset Cruise', 'duration': '3 hours', 'price': 65, 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mykonos Island Hopping', 'duration': '8 hours', 'price': 120, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'turkey': {
            'name': 'Turkey',
            'description': 'Bridge between Europe and Asia, offering rich history, stunning landscapes, and warm hospitality.',
            'long_description': 'Turkey, straddling two continents, offers a fascinating blend of Eastern and Western cultures. From the majestic Hagia Sophia in Istanbul to the surreal fairy chimneys of Cappadocia, Turkey provides an incredible diversity of experiences from ancient ruins to modern cities.',
            'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': 'https://images.unsplash.com/photo-1527838832700-5059252407fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 423,
            'tours_count': 198,
            'attractions': [
                {'name': 'Hagia Sophia Istanbul', 'slug': 'hagia-sophia-istanbul', 'description': 'Byzantine-Ottoman masterpiece', 'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Blue Mosque Istanbul', 'slug': 'blue-mosque-istanbul', 'description': 'Six minarets Ottoman mosque', 'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Cappadocia Hot Air Balloons', 'slug': 'cappadocia-hot-air-balloons', 'description': 'Fairy chimneys landscape', 'image': 'https://images.unsplash.com/photo-1578271887552-5ac9e7c7b5d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Göreme Open Air Museum', 'slug': 'goreme-open-air-museum', 'description': 'Cave churches UNESCO site', 'image': 'https://images.unsplash.com/photo-1578271887552-5ac9e7c7b5d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ephesus', 'slug': 'ephesus', 'description': 'Best preserved ancient city Library of Celsus', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Pamukkale', 'slug': 'pamukkale', 'description': 'White travertine terraces Cotton Castle', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Topkapi Palace Istanbul', 'slug': 'topkapi-palace-istanbul', 'description': 'Ottoman palace museum', 'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Grand Bazaar Istanbul', 'slug': 'grand-bazaar-istanbul', 'description': 'Historic covered market', 'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Cappadocia Underground Cities', 'slug': 'cappadocia-underground-cities', 'description': '18-storey ancient cities', 'image': 'https://images.unsplash.com/photo-1578271887552-5ac9e7c7b5d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Aspendos Theater', 'slug': 'aspendos-theater', 'description': 'Roman theater near Antalya', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Antalya Old Town', 'slug': 'antalya-old-town', 'description': 'Mediterranean resort', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Troy Archaeological Site', 'slug': 'troy-archaeological-site', 'description': 'Legendary ancient city', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mount Nemrut', 'slug': 'mount-nemrut', 'description': 'Summit with giant stone heads', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Sumela Monastery', 'slug': 'sumela-monastery', 'description': 'Cliffside monastery', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bodrum Castle', 'slug': 'bodrum-castle', 'description': 'Crusader castle and museum', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Pergamon', 'slug': 'pergamon', 'description': 'Ancient Greek city ruins', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Oludeniz Blue Lagoon', 'slug': 'oludeniz-blue-lagoon', 'description': 'Paragliding and beach', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ani Ruins', 'slug': 'ani-ruins', 'description': 'Medieval Armenian city', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mevlana Museum Konya', 'slug': 'mevlana-museum-konya', 'description': 'Whirling dervishes', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Galata Tower Istanbul', 'slug': 'galata-tower-istanbul', 'description': 'Medieval stone tower', 'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Ciragan Palace Kempinski Istanbul', 'location': 'Istanbul', 'rating': 4.9, 'price': 420, 'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Museum Hotel Cappadocia', 'location': 'Cappadocia', 'rating': 4.8, 'price': 280, 'image': 'https://images.unsplash.com/photo-1578271887552-5ac9e7c7b5d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Regnum Carya Golf & Spa Resort', 'location': 'Antalya', 'rating': 4.7, 'price': 250, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Istanbul Cultural Heritage Tour', 'duration': '7 hours', 'price': 75, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Cappadocia Hot Air Balloon Tour', 'duration': '4 hours', 'price': 180, 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1578271887552-5ac9e7c7b5d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ephesus and Pamukkale Day Trip', 'duration': '12 hours', 'price': 95, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'egypt': {
            'name': 'Egypt',
            'description': 'Home to the ancient pyramids and pharaohs, with a rich history spanning thousands of years.',
            'long_description': 'Egypt, the land of the pharaohs, offers an unparalleled journey through one of the world\'s greatest ancient civilizations. From the majestic pyramids of Giza to the temples of Luxor, Egypt combines archaeological wonders with modern cities and the stunning Red Sea coastline.',
            'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': '/static/core/images/young-man-walking-towards-great-sphinx-giza.jpg',
            'accommodations_count': 389,
            'tours_count': 167,
            'attractions': [
                {'name': 'Pyramids of Giza & Sphinx', 'slug': 'pyramids-of-giza', 'description': 'Legendary pyramids and one of the Seven Wonders of the Ancient World', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Grand Egyptian Museum', 'slug': 'grand-egyptian-museum', 'description': 'World\'s largest archaeological museum housing Tutankhamun treasures', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Valley of the Kings', 'slug': 'valley-of-the-kings', 'description': 'Royal burial site with rock-cut tombs of pharaohs including Tutankhamun', 'image': 'https://images.unsplash.com/photo-1464822759844-d150f38d609c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Karnak Temple Complex', 'slug': 'karnak-temple', 'description': 'One of the largest religious sites with towering columns and ancient ruins', 'image': 'https://images.unsplash.com/photo-1464822759844-d150f38d609c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Luxor Temple', 'slug': 'luxor-temple', 'description': 'Ancient temple dedicated to Amun, stunning when illuminated at night', 'image': 'https://images.unsplash.com/photo-1464822759844-d150f38d609c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Abu Simbel Temples', 'slug': 'abu-simbel', 'description': 'Rock-hewn temples of Ramses II and Queen Nefertari', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Philae Temple', 'slug': 'philae-temple', 'description': 'Island temple dedicated to goddess Isis with scenic boat access', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Egyptian Museum Cairo', 'slug': 'egyptian-museum', 'description': 'Tahrir Square museum with 120,000 artifacts and Tutankhamun gold mask', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Islamic Cairo', 'slug': 'islamic-cairo', 'description': 'Historic district with Sultan Hassan Mosque and Khan El Khalili bazaar', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Muhammad Ali Mosque', 'slug': 'muhammad-ali-mosque', 'description': 'Alabaster mosque atop Cairo Citadel with panoramic city views', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Hurghada', 'slug': 'hurghada', 'description': 'Premier Red Sea resort for SCUBA diving and snorkeling', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Sharm El-Sheikh', 'slug': 'sharm-el-sheikh', 'description': 'Luxury Red Sea destination with world-class diving sites', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bibliotheca Alexandrina', 'slug': 'bibliotheca-alexandrina', 'description': 'Modern library honoring the ancient Library of Alexandria', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Citadel of Qaitbay', 'slug': 'citadel-qaitbay', 'description': 'Fortress built on ruins of the ancient Pharos Lighthouse', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Aswan High Dam', 'slug': 'aswan-high-dam', 'description': 'Engineering marvel controlling Nile flooding with Lake Nasser views', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Siwa Oasis', 'slug': 'siwa-oasis', 'description': 'Remote desert oasis with natural springs and Temple of Oracle of Amun', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Hatshepsut Temple', 'slug': 'hatshepsut-temple', 'description': 'Memorial temple of Egypt\'s female pharaoh carved into cliffsides', 'image': 'https://images.unsplash.com/photo-1464822759844-d150f38d609c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dahab', 'slug': 'dahab', 'description': 'Laid-back Red Sea town famous for diving at Blue Hole', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Marsa Alam', 'slug': 'marsa-alam', 'description': 'Pristine Red Sea destination for marine life and ocean activities', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Catacombs of Kom El Shoqafa', 'slug': 'catacombs-kom-el-shoqafa', 'description': 'Fascinating underground necropolis blending Egyptian and Roman art', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Four Seasons Hotel Cairo at Nile Plaza', 'location': 'Cairo', 'rating': 4.8, 'price': 320, 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Kempinski Nile Hotel Cairo', 'location': 'Cairo', 'rating': 4.7, 'price': 280, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Jaz Makadi Star & Spa Resort', 'location': 'Red Sea', 'rating': 4.6, 'price': 220, 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Pyramids and Sphinx Full Day Tour', 'duration': '8 hours', 'price': 65, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Luxor and Karnak Temple Tour', 'duration': '6 hours', 'price': 55, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1464822759844-d150f38d609c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Nile River Felucca Cruise', 'duration': '3 hours', 'price': 35, 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'morocco': {
            'name': 'Morocco',
            'description': 'A land of contrasts with bustling souks, stunning deserts, and the majestic Atlas Mountains.',
            'long_description': 'Morocco, a North African gem, offers an exotic blend of ancient traditions and vibrant modernity. From the bustling souks of Marrakech to the vast Sahara Desert, Morocco provides an unforgettable journey through colorful markets, stunning architecture, and breathtaking landscapes.',
            'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'accommodations_count': 278,
            'tours_count': 145,
            'attractions': [
                {'name': 'Djemaa el-Fna Square Marrakech', 'slug': 'djemaa-el-fna-square-marrakech', 'description': 'Old medina center with markets', 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Koutoubia Mosque Marrakech', 'slug': 'koutoubia-mosque-marrakech', 'description': 'Iconic red city mosque', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Majorelle Gardens Marrakech', 'slug': 'majorelle-gardens-marrakech', 'description': 'Yves Saint Laurent gardens', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bahia Palace Marrakech', 'slug': 'bahia-palace-marrakech', 'description': '19th century palace', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Saadian Tombs Marrakech', 'slug': 'saadian-tombs-marrakech', 'description': 'Royal necropolis', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Fes el-Bali Medina', 'slug': 'fes-el-bali-medina', 'description': 'UNESCO maze of narrow streets', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'University of Al Quaraouiyine Fes', 'slug': 'university-of-al-quaraouiyine-fes', 'description': 'World\'s oldest university 859 AD', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Fes Tanneries', 'slug': 'fes-tanneries', 'description': 'Ancient leather processing', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Hassan II Mosque Casablanca', 'slug': 'hassan-ii-mosque-casablanca', 'description': 'World\'s biggest minaret Atlantic coast', 'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Casablanca Corniche', 'slug': 'casablanca-corniche', 'description': 'Seafront promenade', 'image': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Merzouga Sahara Desert', 'slug': 'merzouga-sahara-desert', 'description': 'Erg Chebbi dunes camel treks', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Chefchaouen', 'slug': 'chefchaouen', 'description': 'Blue-painted mountain town', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Essaouira', 'slug': 'essaouira', 'description': 'UNESCO coastal medina blue and white buildings', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ait Benhaddou', 'slug': 'ait-benhaddou', 'description': 'UNESCO Kasbah from Game of Thrones', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Rabat Hassan Tower', 'slug': 'rabat-hassan-tower', 'description': 'Capital city minaret', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Meknes Bab Mansour Gate', 'slug': 'meknes-bab-mansour-gate', 'description': 'UNESCO 11th century', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Todra Gorge', 'slug': 'todra-gorge', 'description': 'Red-rock canyon for hiking', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Volubilis', 'slug': 'volubilis', 'description': 'Roman ruins UNESCO site', 'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Atlas Mountains', 'slug': 'atlas-mountains', 'description': 'Berber villages and hiking', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Agadir Beach', 'slug': 'agadir-beach', 'description': 'Atlantic resort town', 'image': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Nomad Palace Camp', 'location': 'Sahara Desert', 'rating': 4.8, 'price': 180, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Riad Kniza Marrakech', 'location': 'Marrakech', 'rating': 4.7, 'price': 150, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dar Moha Hotel', 'location': 'Marrakech', 'rating': 4.6, 'price': 120, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'}
            ],
            'tours': [
                {'name': 'Marrakech Medina Walking Tour', 'duration': '4 hours', 'price': 35, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Atlas Mountains Trek', 'duration': '3 days', 'price': 280, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Sahara Desert Camel Trek', 'duration': '2 days', 'price': 220, 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'uae': {
            'name': 'United Arab Emirates',
            'description': 'A modern oasis of luxury and innovation, blending traditional Arabian culture with cutting-edge architecture.',
            'long_description': 'The United Arab Emirates represents the pinnacle of modern luxury and cultural fusion. From the iconic Burj Khalifa in Dubai to the traditional souks of Abu Dhabi, the UAE offers an extraordinary blend of ancient Bedouin heritage and futuristic innovation.',
            'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': '/static/core/images/futuristic-dubai-landscape.jpg',
            'accommodations_count': 892,
            'tours_count': 345,
            'attractions': [
                {'name': 'Burj Khalifa', 'slug': 'burj-khalifa', 'description': 'World\'s tallest building with stunning city views', 'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Sheikh Zayed Grand Mosque', 'slug': 'sheikh-zayed-mosque', 'description': 'Magnificent mosque with intricate Islamic architecture', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Palm Jumeirah', 'slug': 'palm-jumeirah', 'description': 'Artificial island paradise with luxury resorts', 'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Mall', 'slug': 'dubai-mall', 'description': 'World\'s largest shopping and entertainment complex', 'image': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Desert Safari', 'slug': 'dubai-desert-safari', 'description': 'Thrilling desert adventure with dune bashing', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Marina', 'slug': 'dubai-marina', 'description': 'Modern waterfront district with luxury yachts and entertainment', 'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Burj Al Arab', 'slug': 'burj-al-arab', 'description': 'Iconic seven-star hotel with world-class luxury', 'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Fountain', 'slug': 'dubai-fountain', 'description': 'World\'s largest choreographed fountain system', 'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Louvre Abu Dhabi', 'slug': 'louvre-abu-dhabi', 'description': 'World-class art museum with universal collection', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Creek', 'slug': 'dubai-creek', 'description': 'Historic waterway dividing old and new Dubai', 'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Jumeirah Beach', 'slug': 'jumeirah-beach', 'description': 'Pristine beach with luxury resorts and water activities', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Museum', 'slug': 'dubai-museum', 'description': 'Ancient fort showcasing Dubai\'s history and culture', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Al Fahidi Historical Neighbourhood', 'slug': 'al-fahidi-historical', 'description': 'Traditional wind-tower houses and cultural district', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Frame', 'slug': 'dubai-frame', 'description': 'Massive picture frame structure with city views', 'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Miracle Garden', 'slug': 'dubai-miracle-garden', 'description': 'World\'s largest flower garden with floral displays', 'image': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Global Village Dubai', 'slug': 'global-village-dubai', 'description': 'Cultural theme park showcasing world cultures', 'image': 'https://images.unsplash.com/photo-1542204165-65bf26472b9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ferrari World Abu Dhabi', 'slug': 'ferrari-world-abu-dhabi', 'description': 'High-speed racing theme park with Ferrari experiences', 'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Yas Marina Circuit', 'slug': 'yas-marina-circuit', 'description': 'F1 race track and entertainment complex', 'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Abu Dhabi Corniche', 'slug': 'abu-dhabi-corniche', 'description': 'Scenic waterfront promenade with beaches and parks', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Aquarium', 'slug': 'dubai-aquarium', 'description': 'Massive underwater aquarium with tunnel experience', 'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ski Dubai', 'slug': 'ski-dubai', 'description': 'Indoor ski resort in the desert with slopes and penguins', 'image': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Atlantis The Palm', 'slug': 'atlantis-the-palm', 'description': 'Luxury resort with water park and marine attractions', 'image': 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Wild Wadi Water Park', 'slug': 'wild-wadi-water-park', 'description': 'Adventure water park with thrilling slides and waves', 'image': 'https://images.unsplash.com/photo-1530549387789-4c1017266635?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Zoo', 'slug': 'dubai-zoo', 'description': 'Modern zoo with diverse animal exhibits and conservation', 'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Burj Al Arab Jumeirah', 'location': 'Dubai', 'rating': 4.9, 'price': 1200, 'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Armani Hotel Dubai', 'location': 'Dubai', 'rating': 4.8, 'price': 450, 'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Emirates Palace', 'location': 'Abu Dhabi', 'rating': 4.9, 'price': 580, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Dubai City Highlights Tour', 'duration': '8 hours', 'price': 95, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Abu Dhabi Cultural Tour', 'duration': '6 hours', 'price': 85, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Desert Safari Experience', 'duration': '6 hours', 'price': 75, 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'lebanon': {
            'name': 'Lebanon',
            'description': 'A Mediterranean jewel known for its ancient history, vibrant culture, and stunning coastal beauty.',
            'long_description': 'Lebanon, often called the "Paris of the Middle East," offers a fascinating blend of ancient Phoenician heritage and modern Mediterranean charm. From the historic ruins of Baalbek to the vibrant streets of Beirut, Lebanon provides an unforgettable journey through time and culture.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': '/static/core/images/beautiful-view-pigeon-rocks-promenade-center-beirut-lebanon.jpg',
            'accommodations_count': 234,
            'tours_count': 156,
            'attractions': [
                {'name': 'Baalbek Temples', 'slug': 'baalbek-temples', 'description': 'City of the Sun Roman temples', 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Byblos', 'slug': 'byblos', 'description': 'Oldest inhabited city ancient port', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Jeita Grotto', 'slug': 'jeita-grotto', 'description': 'Limestone caves New 7 Wonders finalist', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Cedars of God', 'slug': 'cedars-of-god', 'description': 'UNESCO ancient cedar forest', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Qadisha Valley', 'slug': 'qadisha-valley', 'description': 'UNESCO monasteries and hiking', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Pigeon Rocks Raouché', 'slug': 'pigeon-rocks-raouche', 'description': 'Natural offshore rock formations', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Mohammad Al-Amin Mosque Beirut', 'slug': 'mohammad-al-amin-mosque-beirut', 'description': 'Blue Mosque Ottoman architecture', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Beirut Souks', 'slug': 'beirut-souks', 'description': '200+ shopping outlets', 'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'National Museum Beirut', 'slug': 'national-museum-beirut', 'description': '100,000 antiquities archaeology museum', 'image': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Our Lady of Lebanon Harissa', 'slug': 'our-lady-of-lebanon-harissa', 'description': 'Pilgrimage bronze sculpture', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Beirut Corniche', 'slug': 'beirut-corniche', 'description': '5km shoreline boardwalk', 'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Tyre', 'slug': 'tyre', 'description': 'Historic Phoenician city Roman Hippodrome', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Anjar', 'slug': 'anjar', 'description': 'Umayyad-era Islamic city', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'MIM Mineral Museum Beirut', 'slug': 'mim-mineral-museum-beirut', 'description': '2000 minerals 450 species', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Tripoli Citadel', 'slug': 'tripoli-citadel', 'description': 'Crusader castle old souks', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Sidon Sea Castle', 'slug': 'sidon-sea-castle', 'description': 'Crusader fortress', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Tannourine Cedars Reserve', 'slug': 'tannourine-cedars-reserve', 'description': 'Protected cedar forest', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Batroun', 'slug': 'batroun', 'description': 'Phoenician seaside town', 'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Four Seasons Hotel Beirut', 'location': 'Beirut', 'rating': 4.8, 'price': 350, 'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Le Gray Beirut', 'location': 'Beirut', 'rating': 4.7, 'price': 280, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'The Mayflower Hotel', 'location': 'Beirut', 'rating': 4.6, 'price': 220, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'}
            ],
            'tours': [
                {'name': 'Beirut City Exploration', 'duration': '4 hours', 'price': 45, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Baalbek and Anjar Day Trip', 'duration': '8 hours', 'price': 85, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Byblos and Jbeil Coastal Tour', 'duration': '6 hours', 'price': 65, 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'qatar': {
            'name': 'Qatar',
            'description': 'A modern Arabian nation blending rich heritage with world-class luxury and sporting excellence.',
            'long_description': 'Qatar, a peninsula nation in the Arabian Gulf, represents the perfect fusion of ancient Bedouin traditions and modern architectural marvels. From the stunning Museum of Islamic Art in Doha to the spectacular venues that hosted the FIFA World Cup, Qatar offers an extraordinary cultural and sporting experience.',
            'image': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': '/static/core/images/skyline-doha-city-center-qatar-middle-east.jpg',
            'accommodations_count': 167,
            'tours_count': 89,
            'attractions': [
                {'name': 'Doha', 'slug': 'doha', 'description': 'Modern capital with stunning Islamic architecture', 'image': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Museum of Islamic Art', 'slug': 'museum-of-islamic-art', 'description': 'World-class museum showcasing Islamic art and culture', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Souq Waqif', 'slug': 'souq-waqif', 'description': 'Traditional market with authentic Arabian atmosphere', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Katara Cultural Village', 'slug': 'katara-cultural-village', 'description': 'Cultural complex showcasing Qatari heritage', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Al Zubarah Fort', 'slug': 'al-zubarah-fort', 'description': '18th-century fort and UNESCO World Heritage Site', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Four Seasons Hotel Doha', 'location': 'Doha', 'rating': 4.9, 'price': 420, 'image': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mandarin Oriental Doha', 'location': 'Doha', 'rating': 4.8, 'price': 380, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'The St. Regis Doha', 'location': 'Doha', 'rating': 4.7, 'price': 320, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'}
            ],
            'tours': [
                {'name': 'Doha City Highlights Tour', 'duration': '6 hours', 'price': 75, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Desert Safari Adventure', 'duration': '8 hours', 'price': 120, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Cultural Heritage Tour', 'duration': '4 hours', 'price': 55, 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'saudi-arabia': {
            'name': 'Saudi Arabia',
            'description': 'The heart of Islam with ancient deserts, modern cities, and sacred pilgrimage sites.',
            'long_description': 'Saudi Arabia, the birthplace of Islam and home to its holiest sites, offers a profound journey through ancient deserts and ultramodern cities. From the sacred mosques of Mecca and Medina to the futuristic developments of Riyadh and NEOM, Saudi Arabia represents the perfect blend of spiritual heritage and visionary innovation.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': '/static/core/images/view-buildings-against-cloudy-sky.jpg',
            'accommodations_count': 445,
            'tours_count': 234,
            'attractions': [
                {'name': 'AlUla Hegra', 'slug': 'alula-hegra', 'description': 'UNESCO Nabataean tombs', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Masjid al-Haram Mecca', 'slug': 'masjid-al-haram-mecca', 'description': 'World\'s largest mosque with Kaaba', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Madinah Al-Masjid an-Nabawi', 'slug': 'madinah-al-masjid-an-nabawi', 'description': 'Second holiest site green dome', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Masmak Fortress Riyadh', 'slug': 'masmak-fortress-riyadh', 'description': 'Mud brick birthplace of kingdom', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Kingdom Centre Tower Riyadh', 'slug': 'kingdom-centre-tower-riyadh', 'description': '99-floor skyscraper', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Edge of the World Riyadh', 'slug': 'edge-of-the-world-riyadh', 'description': 'Dramatic cliff escarpment', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Diriyah At-Turaif District', 'slug': 'diriyah-at-turaif-district', 'description': 'UNESCO first Saudi capital', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Al-Balad Jeddah', 'slug': 'al-balad-jeddah', 'description': 'UNESCO historic coral-stone buildings', 'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Jeddah Corniche', 'slug': 'jeddah-corniche', 'description': 'Red Sea palm-lined waterfront', 'image': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Al Ahsa Oasis', 'slug': 'al-ahsa-oasis', 'description': 'UNESCO world\'s largest oasis 30,000 acres', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Farasan Islands', 'slug': 'farasan-islands', 'description': 'Red Sea coral reefs diving', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Taif', 'slug': 'taif', 'description': 'Mountain city rose gardens', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Jabal Ikmah AlUla', 'slug': 'jabal-ikmah-alula', 'description': 'Open library rock inscriptions', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Nasseef House Jeddah', 'slug': 'nasseef-house-jeddah', 'description': '1872 museum cultural center', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Rijal Almaa', 'slug': 'rijal-almaa', 'description': 'Mountain village painted houses museum', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dumat Al-Jandal', 'slug': 'dumat-al-jandal', 'description': 'Ancient fort and mosque', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Ushaiger Heritage Village', 'slug': 'ushaiger-heritage-village', 'description': 'Mud brick Najdi architecture', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Red Sea Project', 'slug': 'red-sea-project', 'description': 'Luxury coastal resort development', 'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Abha', 'slug': 'abha', 'description': 'Asir region mountains and cable car', 'image': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'National Museum Riyadh', 'slug': 'national-museum-riyadh', 'description': 'Saudi history culture heritage', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Four Seasons Hotel Riyadh', 'location': 'Riyadh', 'rating': 4.9, 'price': 380, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'The Ritz-Carlton Riyadh', 'location': 'Riyadh', 'rating': 4.8, 'price': 350, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Shangri-La Hotel AlUla', 'location': 'AlUla', 'rating': 4.9, 'price': 420, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Riyadh Cultural Tour', 'duration': '6 hours', 'price': 85, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'AlUla Ancient Wonders Tour', 'duration': '8 hours', 'price': 120, 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Red Sea Coastal Adventure', 'duration': '10 hours', 'price': 150, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'kuwait': {
            'name': 'Kuwait',
            'description': 'A modern Gulf state with rich cultural heritage, stunning desert landscapes, and warm hospitality.',
            'long_description': 'Kuwait, a small but vibrant Gulf nation, offers a perfect blend of traditional Arabian culture and modern urban sophistication. From the magnificent Kuwait Towers to the pristine beaches along the Arabian Gulf, Kuwait provides an authentic Arabian experience with world-class museums and cultural sites.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': '/static/core/images/drone-photo-kuwait-city-kuwait-tower-from-sky.jpg',
            'accommodations_count': 123,
            'tours_count': 67,
            'attractions': [
                {'name': 'Kuwait City', 'slug': 'kuwait-city', 'description': 'Modern capital with traditional souks and contemporary architecture', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Kuwait Towers', 'slug': 'kuwait-towers', 'description': 'Iconic water towers symbolizing Kuwait\'s modernity', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Liberation Tower', 'slug': 'liberation-tower', 'description': 'Tallest structure in Kuwait with panoramic views', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Tareq Rajab Museum', 'slug': 'tareq-rajab-museum', 'description': 'Cultural museum showcasing Kuwaiti heritage', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Al Shaheed Park', 'slug': 'al-shaheed-park', 'description': 'Beautiful coastal park with beaches and recreational facilities', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'The Regency Hotel Kuwait', 'location': 'Kuwait City', 'rating': 4.7, 'price': 220, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Crowne Plaza Kuwait', 'location': 'Kuwait City', 'rating': 4.6, 'price': 180, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Marina Hotel Kuwait', 'location': 'Kuwait City', 'rating': 4.5, 'price': 150, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Kuwait City Sightseeing Tour', 'duration': '4 hours', 'price': 45, 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Desert Safari Experience', 'duration': '6 hours', 'price': 85, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Cultural Heritage Tour', 'duration': '5 hours', 'price': 55, 'rating': 4.5, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'bahrain': {
            'name': 'Bahrain',
            'description': 'An island kingdom blending ancient Dilmun civilization with modern Arabian Gulf culture.',
            'long_description': 'Bahrain, the smallest Arab country, offers a fascinating journey through 5,000 years of civilization. From the ancient Bahrain Fort to the modern Bahrain World Trade Center, this island kingdom provides an authentic Arabian experience with pristine beaches, rich cultural heritage, and warm hospitality.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': '/static/core/images/reflection-illuminated-buildings-water-against-bahrain-skyline.jpg',
            'accommodations_count': 89,
            'tours_count': 45,
            'attractions': [
                {'name': 'Manama', 'slug': 'manama', 'description': 'Vibrant capital with modern skyscrapers and traditional souks', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bahrain Fort', 'slug': 'bahrain-fort', 'description': 'Ancient fort dating back to 2800 BC', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Al Fateh Grand Mosque', 'slug': 'al-fateh-grand-mosque', 'description': 'Largest mosque in Bahrain with stunning architecture', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bahrain World Trade Center', 'slug': 'bahrain-world-trade-center', 'description': 'Iconic twin towers with integrated wind turbines', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Tree of Life', 'slug': 'tree-of-life', 'description': 'Ancient tree in the desert, a natural wonder', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Four Seasons Hotel Bahrain Bay', 'location': 'Manama', 'rating': 4.8, 'price': 320, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'The Ritz-Carlton Bahrain', 'location': 'Manama', 'rating': 4.7, 'price': 280, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Gulf Hotel Bahrain', 'location': 'Manama', 'rating': 4.5, 'price': 180, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Manama City Tour', 'duration': '4 hours', 'price': 45, 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Historical Bahrain Tour', 'duration': '6 hours', 'price': 65, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Desert and Coastal Adventure', 'duration': '8 hours', 'price': 95, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'oman': {
            'name': 'Oman',
            'description': 'An Arabian paradise of stunning deserts, turquoise coasts, and ancient fortresses.',
            'long_description': 'Oman, a land of dramatic landscapes and rich maritime heritage, offers an extraordinary Arabian experience. From the rugged Hajar Mountains to the pristine beaches of the Arabian Sea, Oman combines ancient forts and traditional souks with modern luxury resorts and warm Omani hospitality.',
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': '/static/core/images/historical-casbah-taourirt-ouarzazate-morocco-with-white.jpg',
            'accommodations_count': 156,
            'tours_count': 78,
            'attractions': [
                {'name': 'Muscat', 'slug': 'muscat', 'description': 'Beautiful capital with white-washed buildings and harbor', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Nizwa Fort', 'slug': 'nizwa-fort', 'description': 'Impressive 17th-century fort with circular towers', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Wahiba Sands', 'slug': 'wahiba-sands', 'description': 'Spectacular desert with red dunes and Bedouin camps', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Jebel Shams', 'slug': 'jebel-shams', 'description': 'Highest mountain in Oman with breathtaking views', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Sur', 'slug': 'sur', 'description': 'Coastal town famous for traditional dhow building', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'The Chedi Muscat', 'location': 'Muscat', 'rating': 4.9, 'price': 380, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Al Bustan Palace', 'location': 'Muscat', 'rating': 4.8, 'price': 420, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Anantara Al Jabal Al Akhdar Resort', 'location': 'Jabal Akhdar', 'rating': 4.7, 'price': 280, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Muscat City and Forts Tour', 'duration': '6 hours', 'price': 75, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Desert Safari Adventure', 'duration': '8 hours', 'price': 120, 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mountain and Coastal Exploration', 'duration': '10 hours', 'price': 150, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'syria': {
            'name': 'Syria',
            'description': 'Ancient land of civilization with rich history, stunning architecture, and Mediterranean charm.',
            'long_description': 'Syria, the cradle of civilization, offers an extraordinary journey through thousands of years of human history. From the ancient city of Damascus to the stunning Crusader castles, Syria represents the perfect blend of Mediterranean culture, Islamic architecture, and archaeological wonders.',
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': '/static/core/images/building-with-clock-front-cloudy-sky-background.jpg',
            'accommodations_count': 89,
            'tours_count': 45,
            'attractions': [
                {'name': 'Damascus', 'slug': 'damascus', 'description': 'Ancient capital city with Umayyad Mosque and souks', 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Aleppo', 'slug': 'aleppo', 'description': 'Historic city with Citadel and ancient medina', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Palmyra', 'slug': 'palmyra', 'description': 'Ancient oasis city with Roman ruins', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Krak des Chevaliers', 'slug': 'krak-des-chevaliers', 'description': 'Magnificent Crusader castle and UNESCO site', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bosra', 'slug': 'bosra', 'description': 'Ancient Roman theater and archaeological site', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Four Seasons Hotel Damascus', 'location': 'Damascus', 'rating': 4.6, 'price': 220, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Sham Palace Hotel', 'location': 'Damascus', 'rating': 4.4, 'price': 150, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Dedeman Damascus Hotel', 'location': 'Damascus', 'rating': 4.3, 'price': 120, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Damascus Old City Tour', 'duration': '4 hours', 'price': 35, 'rating': 4.5, 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Palmyra and Krak des Chevaliers', 'duration': '10 hours', 'price': 85, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Aleppo Cultural Heritage Tour', 'duration': '6 hours', 'price': 55, 'rating': 4.4, 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'iraq': {
            'name': 'Iraq',
            'description': 'Land of ancient Mesopotamia with rich history, archaeological treasures, and cultural heritage.',
            'long_description': 'Iraq, the birthplace of civilization, offers an unparalleled journey through the cradle of human history. From the ancient ziggurats of Mesopotamia to the magnificent mosques of Baghdad, Iraq represents thousands of years of cultural and scientific achievements that shaped the modern world.',
            'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': '/static/core/images/vertical-historical-al-rabi-tower-against-blue-cloudy-sky-united-arab-emirates.jpg',
            'accommodations_count': 67,
            'tours_count': 34,
            'attractions': [
                {'name': 'Baghdad', 'slug': 'baghdad', 'description': 'Historic capital with Abbasid heritage and modern developments', 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Babylon', 'slug': 'babylon', 'description': 'Ancient city with Hanging Gardens and Ishtar Gate', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Uruk', 'slug': 'uruk', 'description': 'Ancient Sumerian city and birthplace of writing', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Karbala', 'slug': 'karbala', 'description': 'Sacred city with Imam Hussein Shrine', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Erbil Citadel', 'slug': 'erbil-citadel', 'description': 'Ancient fortified settlement and UNESCO World Heritage Site', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Palestine Hotel Baghdad', 'location': 'Baghdad', 'rating': 4.2, 'price': 120, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Erbil Rotana Hotel', 'location': 'Erbil', 'rating': 4.4, 'price': 150, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Karbala Meridien Hotel', 'location': 'Karbala', 'rating': 4.1, 'price': 100, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Baghdad Historical Tour', 'duration': '4 hours', 'price': 35, 'rating': 4.3, 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mesopotamia Ancient Sites Tour', 'duration': '8 hours', 'price': 75, 'rating': 4.5, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Kurdish Cultural Experience', 'duration': '6 hours', 'price': 55, 'rating': 4.4, 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        },
        'yemen': {
            'name': 'Yemen',
            'description': 'Ancient land of spices, towering mountains, and rich cultural heritage.',
            'long_description': 'Yemen, the land of the Queen of Sheba, offers an extraordinary journey through ancient history and stunning landscapes. From the towering mud-brick skyscrapers of Sana\'a to the pristine Socotra islands, Yemen represents a unique blend of Arabian culture, ancient architecture, and natural wonders.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'hero_image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
            'accommodations_count': 45,
            'tours_count': 23,
            'attractions': [
                {'name': 'Sana\'a', 'description': 'Ancient capital with unique mud-brick architecture', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Socotra Island', 'slug': 'socotra-island', 'description': 'Unique island with dragon\'s blood trees and biodiversity', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Zabid', 'slug': 'zabid', 'description': 'Historic city and UNESCO World Heritage Site', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Shibam', 'slug': 'shibam', 'description': 'Manhattan of the desert with mud skyscrapers', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Aden', 'slug': 'aden', 'description': 'Port city with volcanic crater and British colonial history', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'accommodations': [
                {'name': 'Moevenpick Hotel Sana\'a', 'location': 'Sana\'a', 'rating': 4.3, 'price': 140, 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Hilton Aden Resort', 'location': 'Aden', 'rating': 4.2, 'price': 120, 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Socotra Hotel', 'location': 'Socotra', 'rating': 3.8, 'price': 80, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ],
            'tours': [
                {'name': 'Sana\'a Old City Walking Tour', 'duration': '3 hours', 'price': 25, 'rating': 4.2, 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Socotra Island Adventure', 'duration': '5 days', 'price': 450, 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Wadi Hadramaut Exploration', 'duration': '4 hours', 'price': 45, 'rating': 4.1, 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
            ]
        }
    }
    
    country_data = countries_data.get(country.lower())
    if not country_data:
        # If country not found, redirect to countries list
        return redirect('countries')

    # Query real accommodations from database for this country
    real_accommodations = Accommodation.objects.filter(
        country__iexact=country_data['name'],
        is_published=True,
        is_active=True
    ).select_related('host').prefetch_related('photos')

    # Convert real accommodations to dict format for template
    real_accommodation_list = []
    for acc in real_accommodations:
        primary_photo = acc.photos.filter(is_hero=True).first()
        if not primary_photo:
            primary_photo = acc.photos.first()

        real_accommodation_list.append({
            'id': acc.id,
            'name': acc.property_name,
            'location': acc.city,
            'price': float(acc.base_price),
            'image': primary_photo.get_image_url() if primary_photo else 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'rating': 4.5,  # Placeholder until review system is implemented
        })

    # Query real tours from database for this country
    real_tours = Tour.objects.filter(
        country__iexact=country_data['name'],
        is_published=True,
        is_active=True
    ).select_related('host').prefetch_related('photos')

    # Convert real tours to dict format for template
    real_tour_list = []
    for tour in real_tours:
        primary_photo = tour.photos.filter(is_hero=True).first()
        if not primary_photo:
            primary_photo = tour.photos.first()

        real_tour_list.append({
            'id': tour.id,
            'name': tour.tour_name,
            'duration': tour.duration,
            'price': float(tour.price_per_person),
            'image': primary_photo.get_image_url() if primary_photo else 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
            'rating': 4.5,  # Placeholder until review system is implemented
        })

    # Update counts with real data
    country_data['accommodations_count'] = real_accommodations.count()
    country_data['tours_count'] = real_tours.count()

    # Merge real data with demo data (real data first)
    if real_accommodation_list:
        country_data['accommodations'] = real_accommodation_list + country_data.get('accommodations', [])

    if real_tour_list:
        country_data['tours'] = real_tour_list + country_data.get('tours', [])

    context = {
        'country': country_data,
    }
    return render(request, 'core/country_detail.html', context)


def demo_accommodation_detail(request, country, slug):
    """Demo accommodation detail page view"""
    # Demo accommodation data by country and slug
    demo_accommodations = {
        'jordan': {
            'petra-marriotts-wadi-rum-nabatean-resort': {
                'id': 'petra-marriott-wadi-rum',
                'name': 'Petra Marriott\'s Wadi Rum Nabatean Resort',
                'location': 'Wadi Rum, Jordan',
                'description': 'Experience the magic of Wadi Rum at this luxurious desert resort. Nestled among the stunning red sand dunes and ancient rock formations, this Marriott property offers world-class accommodations with authentic Bedouin hospitality.',
                'long_description': 'Petra Marriott\'s Wadi Rum Nabatean Resort is a luxurious oasis in the heart of the Jordanian desert. This award-winning resort combines modern luxury with traditional Bedouin culture, offering guests an unforgettable desert experience. The resort features elegantly designed rooms and suites with panoramic views of the dramatic Wadi Rum landscape, a world-class spa, multiple dining options, and guided desert excursions.',
                'price': 250,
                'currency': 'USD',
                'rating': 4.8,
                'reviews': 1247,
                'type': 'resort',
                'amenities': ['WiFi', 'Pool', 'Spa', 'Restaurant', 'Desert Tours', 'Fitness Center', 'Concierge'],
                'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'photos': [
                    'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                ],
                'bedrooms': 2,
                'bathrooms': 2,
                'max_guests': 4,
                'room_type': 'Desert View Suite',
                'cancellation_policy': 'Free cancellation up to 24 hours',
                'check_in_time': '14:00',
                'check_out_time': '12:00',
                'property_highlights': ['Stunning desert views', 'Authentic Bedouin experience', 'Guided desert safaris', 'World-class spa facilities']
            },
            'movenpick-resort-petra': {
                'id': 'movenpick-resort-petra',
                'name': 'Mövenpick Resort Petra',
                'location': 'Petra, Jordan',
                'description': 'Located just steps from the ancient city of Petra, this resort offers modern luxury with breathtaking views of the rose-red rock formations and easy access to one of the world\'s greatest archaeological wonders.',
                'long_description': 'Mövenpick Resort Petra provides the perfect base for exploring the ancient Nabatean city. This contemporary resort features spacious rooms with private balconies overlooking the Petra mountains, multiple restaurants serving international and local cuisine, a large swimming pool, and a fitness center. The resort\'s convenient location allows guests to walk to the Petra entrance, making it ideal for visitors wanting to maximize their time exploring this UNESCO World Heritage Site.',
                'price': 180,
                'currency': 'USD',
                'rating': 4.6,
                'reviews': 892,
                'type': 'resort',
                'amenities': ['WiFi', 'Pool', 'Restaurant', 'Fitness Center', 'Concierge', 'Petra Views', 'Room Service'],
                'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
                'photos': [
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
                    'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                ],
                'bedrooms': 1,
                'bathrooms': 1,
                'max_guests': 2,
                'room_type': 'Petra View Room',
                'cancellation_policy': 'Free cancellation up to 48 hours',
                'check_in_time': '15:00',
                'check_out_time': '11:00',
                'property_highlights': ['Walking distance to Petra', 'Mountain views', 'Multiple dining options', 'Petra expert guides available']
            },
            'kempinski-hotel-ishtar-dead-sea': {
                'id': 'kempinski-hotel-ishtar-dead-sea',
                'name': 'Kempinski Hotel Ishtar Dead Sea',
                'location': 'Dead Sea, Jordan',
                'description': 'Luxury resort on the shores of the Dead Sea offering mineral-rich mud treatments, floating experiences in the buoyant waters, and stunning views of the desert landscape.',
                'long_description': 'Kempinski Hotel Ishtar Dead Sea is a luxurious beachfront resort offering the ultimate Dead Sea experience. This five-star property features spacious rooms and suites with private balconies, a private beach area with mineral-rich mud for therapeutic treatments, multiple swimming pools, a world-class spa, and panoramic views of the Jordan Valley. The resort provides the perfect setting for relaxation and rejuvenation in one of the world\'s most unique natural environments.',
                'price': 220,
                'currency': 'USD',
                'rating': 4.7,
                'reviews': 756,
                'type': 'resort',
                'amenities': ['WiFi', 'Pool', 'Spa', 'Private Beach', 'Restaurant', 'Fitness Center', 'Dead Sea Access'],
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'photos': [
                    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                ],
                'bedrooms': 1,
                'bathrooms': 1,
                'max_guests': 2,
                'room_type': 'Dead Sea View Room',
                'cancellation_policy': 'Free cancellation up to 7 days',
                'check_in_time': '14:00',
                'check_out_time': '12:00',
                'property_highlights': ['Private Dead Sea beach', 'Therapeutic mud treatments', 'Floating experiences', 'Desert valley views']
            }
        }
    }

    # Get the accommodation data
    country_data = demo_accommodations.get(country.lower())
    if not country_data:
        return redirect('countries')

    accommodation = country_data.get(slug)
    if not accommodation:
        return redirect('country_detail', country=country)

    # Create photo dictionaries for the template
    photos_urls = accommodation.get('photos', [accommodation.get('image')])
    hero_photos_json = []
    all_photos_json = []

    for idx, photo_url in enumerate(photos_urls):
        photo_dict = {
            'id': idx,
            'image_url': photo_url,
            'alt_text': f"{accommodation['name']} photo {idx+1}",
            'title': f"{accommodation['name']} - Image {idx+1}",
            'caption': '',
            'display_order': idx,
            'is_hero': idx < 6,
            'media_type': 'image',
        }
        all_photos_json.append(photo_dict)
        if idx < 6:
            hero_photos_json.append(photo_dict)

    total_photos = len(all_photos_json)

    context = {
        'accommodation': accommodation,
        'is_demo': True,
        'photos': photos_urls,
        'hero_photos': hero_photos_json,
        'all_photos': all_photos_json,
        'total_photos': total_photos,
        'country': country,
    }

    return render(request, 'core/accommodation_detail.html', context)


def demo_tour_detail(request, country, slug):
    """Demo tour detail page view"""
    # Demo tour data by country and slug
    demo_tours = {
        'jordan': {
            'petra-full-day-tour': {
                'id': 'petra-full-day-tour',
                'name': 'Petra Full Day Tour',
                'location': 'Petra, Jordan',
                'description': 'Explore the ancient Nabatean city of Petra on a comprehensive full-day tour. Walk through the Siq canyon, marvel at the Treasury, and discover the hidden wonders of this UNESCO World Heritage Site.',
                'long_description': 'Join our expert-guided full-day tour of Petra, one of the world\'s most spectacular archaeological sites. Your journey begins with a scenic drive from your hotel, followed by a walk through the narrow Siq canyon that leads to the magnificent Treasury building. Continue exploring the ancient city with visits to the Monastery, Royal Tombs, and other hidden treasures. Learn about the Nabatean civilization that carved this city from rose-red rock over 2,000 years ago. The tour includes entrance fees, professional guide, transportation, and lunch.',
                'duration': '8 hours',
                'price': 85,
                'currency': 'USD',
                'rating': 4.9,
                'reviews': 1247,
                'type': 'cultural',
                'inclusions': ['Professional guide', 'Entrance fees', 'Transportation', 'Lunch', 'Bottled water', 'Hotel pickup'],
                'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
                'photos': [
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
                    'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                ],
                'max_participants': 15,
                'min_participants': 2,
                'age_restrictions': 'Suitable for all ages',
                'difficulty': 'Moderate',
                'highlights': ['Siq Canyon entrance', 'The Treasury (Al-Khazneh)', 'Monastery (Ad Deir)', 'Royal Tombs', 'Ancient water systems'],
                'itinerary': '8:00 AM - Hotel pickup\n9:00 AM - Arrive at Petra\n9:30 AM - Enter through Siq Canyon\n10:30 AM - Explore Treasury and lower city\n12:00 PM - Lunch break\n1:00 PM - Visit Monastery and upper city\n3:00 PM - Free time for exploration\n4:30 PM - Return to hotel',
                'cancellation_policy': 'Free cancellation up to 24 hours'
            },
            'wadi-rum-desert-safari': {
                'id': 'wadi-rum-desert-safari',
                'name': 'Wadi Rum Desert Safari',
                'location': 'Wadi Rum, Jordan',
                'description': 'Experience the stunning desert landscape of Wadi Rum on an exciting safari adventure. Drive through massive sand dunes, explore ancient rock formations, and enjoy traditional Bedouin hospitality.',
                'long_description': 'Embark on an unforgettable desert safari through Wadi Rum, also known as the "Valley of the Moon." This protected area features towering sandstone mountains, red sand dunes, and rock formations that have been shaped by wind and water over millions of years. Your experienced Bedouin guide will take you on a 4x4 vehicle tour through the desert, stopping at key sites including Lawrence of Arabia\'s house, natural rock bridges, and ancient petroglyphs. Enjoy traditional Bedouin tea, learn about desert survival techniques, and witness a spectacular desert sunset.',
                'duration': '6 hours',
                'price': 65,
                'currency': 'USD',
                'rating': 4.8,
                'reviews': 892,
                'type': 'adventure',
                'inclusions': ['4x4 vehicle tour', 'Bedouin guide', 'Traditional tea', 'Entrance fees', 'Hotel pickup/drop-off', 'Bottled water'],
                'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'photos': [
                    'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                ],
                'max_participants': 6,
                'min_participants': 2,
                'age_restrictions': 'Minimum age 8 years',
                'difficulty': 'Easy to Moderate',
                'highlights': ['Lawrence of Arabia house', 'Rock bridges and arches', 'Ancient petroglyphs', 'Sand dune exploration', 'Traditional Bedouin camp'],
                'itinerary': '2:00 PM - Hotel pickup\n3:00 PM - Arrive at Wadi Rum\n3:30 PM - 4x4 desert tour begins\n4:30 PM - Visit Lawrence house and rock formations\n5:30 PM - Traditional Bedouin tea ceremony\n6:00 PM - Sand dune exploration\n7:00 PM - Sunset viewing\n8:00 PM - Return to hotel',
                'cancellation_policy': 'Free cancellation up to 48 hours'
            },
            'dead-sea-experience': {
                'id': 'dead-sea-experience',
                'name': 'Dead Sea Experience',
                'location': 'Dead Sea, Jordan',
                'description': 'Relax and rejuvenate at the lowest point on Earth. Float in the mineral-rich waters, enjoy therapeutic mud treatments, and experience the unique buoyancy of the Dead Sea.',
                'long_description': 'Discover the therapeutic wonders of the Dead Sea on this relaxing full-day experience. Located 400 meters below sea level, the Dead Sea is the lowest point on Earth and contains ten times more salt and minerals than ordinary seawater. Your day includes transportation to the Dead Sea, time to float in the buoyant waters, application of mineral-rich mud for skin therapy, and relaxation at a beach club. Learn about the historical and geological significance of this unique body of water while enjoying the health benefits of its mineral-rich environment.',
                'duration': '4 hours',
                'price': 45,
                'currency': 'USD',
                'rating': 4.7,
                'reviews': 756,
                'type': 'wellness',
                'inclusions': ['Round-trip transportation', 'Beach access', 'Mud treatment', 'Towel and shower facilities', 'Bottled water', 'Hotel pickup'],
                'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                'photos': [
                    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                ],
                'max_participants': 20,
                'min_participants': 2,
                'age_restrictions': 'Suitable for all ages',
                'difficulty': 'Easy',
                'highlights': ['Floating in Dead Sea waters', 'Mineral mud therapy', 'Lowest point on Earth', 'Jordan Valley views', 'Relaxation facilities'],
                'itinerary': '9:00 AM - Hotel pickup\n10:00 AM - Arrive at Dead Sea beach\n10:30 AM - Safety briefing and flotation demonstration\n11:00 AM - Free time for swimming and floating\n12:00 PM - Mud treatment application\n1:00 PM - Lunch and relaxation\n2:00 PM - Return to hotel',
                'cancellation_policy': 'Free cancellation up to 24 hours'
            }
        }
    }

    # Get the tour data
    country_data = demo_tours.get(country.lower())
    if not country_data:
        return redirect('countries')

    tour = country_data.get(slug)
    if not tour:
        return redirect('country_detail', country=country)

    # Create photo dictionaries for the template
    photos_urls = tour.get('photos', [tour.get('image')])
    hero_photos_json = []
    all_photos_json = []

    for idx, photo_url in enumerate(photos_urls):
        photo_dict = {
            'id': idx,
            'image_url': photo_url,
            'alt_text': f"{tour['name']} photo {idx+1}",
            'title': f"{tour['name']} - Image {idx+1}",
            'caption': '',
            'display_order': idx,
            'is_hero': idx < 6,
            'media_type': 'image',
        }
        all_photos_json.append(photo_dict)
        if idx < 6:
            hero_photos_json.append(photo_dict)

    total_photos = len(all_photos_json)

    context = {
        'tour': tour,
        'is_demo': True,
        'photos': photos_urls,
        'hero_photos': hero_photos_json,
        'all_photos': all_photos_json,
        'total_photos': total_photos,
        'country': country,
    }

    return render(request, 'core/tour_detail.html', context)


def attraction_detail(request, country, slug):
    """Attraction detail page view"""
    # Demo attraction data by country and slug
    demo_attractions = {
        'jordan': {
            'petra': {
                'id': 'petra',
                'name': 'Petra',
                'location': 'Ma\'an Governorate, Jordan',
                'description': 'Ancient rock-cut city and UNESCO World Heritage Site, famous for its stunning architecture carved into rose-red sandstone cliffs.',
                'long_description': 'Petra, often called the "Rose City" due to the color of the stone from which it is carved, is one of the world\'s most famous archaeological sites and a UNESCO World Heritage Site. This ancient Nabataean city, hidden in the rugged mountains of southern Jordan, features spectacular rock-cut architecture and water conduit systems that are engineering marvels of the ancient world.',
                'historical_significance': 'Petra was established as the capital of the Nabataean Kingdom around the 4th century BCE. The Nabataeans were Arab traders who controlled the spice routes between Arabia, Egypt, Syria, and the Mediterranean. They developed sophisticated water management systems and carved elaborate tombs and temples directly into the sandstone cliffs. The city flourished for centuries, reaching its peak in the 1st century CE with a population of around 20,000-30,000 people.',
                'discovery': 'Petra remained largely unknown to the Western world until 1812 when it was rediscovered by Swiss explorer Johann Ludwig Burckhardt. He was told about the site by local Bedouins and entered the city disguised as an Arab pilgrim. The site became famous worldwide after being featured in films like "Indiana Jones and the Last Crusade."',
                'architecture': 'Petra\'s most famous structure is the Treasury (Al-Khazneh), a magnificent facade carved into the rock that served as a tomb for Nabataean kings. Other notable sites include the Monastery (Ad Deir), the largest rock-cut monument in Petra; the Royal Tombs, elaborate burial chambers for the Nabataean elite; and the Great Temple, a complex of buildings that served as the city\'s main religious center.',
                'water_system': 'One of Petra\'s most remarkable achievements was its sophisticated water management system. The Nabataeans built dams, cisterns, and channels to capture and store rainwater from the surrounding mountains. This allowed the city to thrive in the arid desert environment and support its large population.',
                'cultural_impact': 'Petra has been designated a UNESCO World Heritage Site and is considered one of the New Seven Wonders of the World. It attracts over 1 million visitors annually and has been featured in numerous films, books, and works of art. The site continues to be an active area of archaeological research.',
                'best_time_to_visit': 'The best time to visit Petra is during the cooler months from March to May or September to November. Summer temperatures can exceed 40°C (104°F), making exploration difficult. Winter months are mild but can be rainy.',
                'how_to_get_there': 'Petra is located about 240 km (150 miles) south of Amman. Most visitors arrive by organized tour bus, taxi, or rental car. The journey takes about 3-4 hours by road. There are also domestic flights from Amman to Ma\'an Airport, about 120 km from Petra.',
                'entrance_fees': 'Entrance fees for foreigners are approximately 50 JOD (about $70 USD) for a one-day pass, or 55 JOD for a two-day pass. Jordanian citizens and residents of Arab countries pay reduced rates. Children under 12 enter free.',
                'opening_hours': 'Petra opens at 6:00 AM year-round. Closing times vary by season: 6:00 PM in summer (April 15-October 15) and 4:00 PM in winter (October 16-April 14).',
                'what_to_wear': 'Comfortable walking shoes are essential as there is a lot of walking on uneven terrain. Wear light, breathable clothing in summer and layers in cooler months. Bring a hat, sunglasses, and sunscreen. Modest clothing is recommended when visiting religious sites.',
                'health_safety': 'Stay hydrated, especially in summer. The site has medical facilities and first aid stations. Some areas involve climbing stairs or uneven terrain, so visitors with mobility issues should check accessibility. Horse and donkey rides are available but should be approached with caution.',
                'guided_tours': 'Guided tours are highly recommended to fully appreciate Petra\'s history and significance. Official guides are available at the entrance and provide detailed explanations of the sites. Audio guides are also available in multiple languages.',
                'nearby_attractions': 'Nearby attractions include Little Petra (Siq al-Barid), a smaller Nabataean site; Wadi Rum desert; and the Dead Sea. Many visitors combine Petra with these sites in multi-day tours.',
                'conservation': 'Petra faces challenges from weathering, tourism, and development. UNESCO and the Jordanian government have implemented conservation programs to protect the site. Visitors are asked to stay on marked paths and not climb on the monuments.',
                'facts': [
                    'Petra is mentioned in the Bible as the place where Moses struck a rock to bring forth water',
                    'The city was an important trading hub for frankincense, myrrh, and spices',
                    'Petra\'s water system could supply the city for several months during dry periods',
                    'The Treasury facade is 30 meters high and 25 meters wide',
                    'Petra was occupied for over 1,000 years before being largely abandoned',
                    'The site covers an area of about 264 square kilometers',
                    'Petra receives over 1 million visitors annually',
                    'The Monastery is located 800 steps up a mountain and offers panoramic views'
                ],
                'key_sites': [
                    {
                        'name': 'The Treasury (Al-Khazneh)',
                        'description': 'The most famous monument in Petra, a magnificent rock-cut tomb with intricate carvings and a mysterious urn on top.',
                        'significance': 'Built around 100 CE as a tomb for Nabataean kings. The urn was believed to contain treasure, hence the name "Treasury."'
                    },
                    {
                        'name': 'The Monastery (Ad Deir)',
                        'description': 'The largest rock-cut monument in Petra, measuring 50 meters wide and 45 meters high.',
                        'significance': 'Located high on a mountain, it served as a religious center. The name "Monastery" was given by Bedouins who used it as a hermitage.'
                    },
                    {
                        'name': 'The Royal Tombs',
                        'description': 'Elaborate burial chambers carved into the cliffs, including the Urn Tomb, Silk Tomb, and Corinthian Tomb.',
                        'significance': 'These tombs demonstrate the Nabataeans\' advanced architectural skills and their reverence for their rulers.'
                    },
                    {
                        'name': 'The Great Temple',
                        'description': 'A complex of buildings that served as Petra\'s main religious and civic center.',
                        'significance': 'Features colonnaded courtyards, temples, and administrative buildings, showing the city\'s urban sophistication.'
                    },
                    {
                        'name': 'The Siq',
                        'description': 'A narrow canyon, 1.2 km long, that serves as the main entrance to Petra.',
                        'significance': 'This natural gorge was enhanced by the Nabataeans with water channels and carvings. It creates dramatic anticipation before revealing the Treasury.'
                    }
                ],
                'visitor_tips': [
                    'Start early in the morning to avoid crowds and heat',
                    'Bring plenty of water and snacks',
                    'Consider a guided tour for deeper understanding',
                    'Horse or donkey rides are available but walking is recommended for the full experience',
                    'Allow at least 4-6 hours to explore the main sites',
                    'Purchase tickets online in advance during peak season',
                    'Respect the site by not climbing on monuments or removing artifacts'
                ],
                'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
                'hero_image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
                'photos': [
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80',
                    'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80',
                    'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '30.3285° N, 35.4444° E',
                'unesco_status': 'UNESCO World Heritage Site since 1985',
                'area': '264 square kilometers',
                'peak_population': '20,000-30,000 (1st century CE)',
                'annual_visitors': 'Over 1 million',
                'entrance_fee': '50 JOD (approx. $70 USD) for one day',
                'best_time': 'March-May or September-November',
                'climate': 'Desert climate with hot summers and mild winters'
            },
            'wadi-rum': {
                'id': 'wadi-rum',
                'name': 'Wadi Rum',
                'location': 'Aqaba Governorate, Jordan',
                'description': 'Desert wilderness also known as the Valley of the Moon, featuring dramatic sandstone mountains and vast red sand dunes.',
                'long_description': 'Wadi Rum, also known as the Valley of the Moon, is a valley cut into sandstone and granite rock in southern Jordan. With an area of 720 km², it is the largest wadi in Jordan. The desert landscape stretches into the horizon, with red sandy terrain punctuated by fantastic rock formations, craggy mountains and narrow canyons. Gargantuan rock formations, rippled sand dunes, and clear night skies create an almost fairy-tale setting across an unpopulated area the size of New York City.',
                'historical_significance': 'Various human cultures have inhabited Wadi Rum since prehistoric times, with many cultures–including the Nabataeans–leaving their mark in the form of petroglyphs, inscriptions, and temple ruins. The area was part of the Kingdom of Edom between the 13th and 6th centuries BCE. The Nabateans reigned for about 500 years (400 BCE - 106 CE) in Arabia until they were annexed by the Romans in 106 CE.',
                'discovery': 'The vast desert expanse of Wadi Rum became a pivotal backdrop for Lawrence\'s wartime activities, when in 1917 he was tasked with supporting the Arab Revolt against Ottoman rule. Wadi Rum was one of the theatres of the revolt, as Prince Faisal and British officer T.E. Lawrence recruited Bedouin tribes to join and fight the Ottomans.',
                'cultural_impact': 'Desert scenes of Wadi Rum in Lawrence of Arabia from 1962 kick-started Jordan\'s tourism industry. The Wadi Rum Protected Area has been a UNESCO World Heritage site since 2011. Today, Wadi Rum is one of Jordan\'s most popular tourist sites, attracting 162,000 tourists in 2017.',
                'entrance_fees': 'Entry to the Wadi Rum Protected Area costs 5 JOD (about $7 USD) for foreigners. Visitors with Jordan Pass enter free.',
                'opening_hours': 'The protected area is open 24/7, but visitor center hours are 8:00 AM to 4:00 PM',
                'best_time': 'October to April for mild temperatures',
                'how_to_get_there': 'Wadi Rum is about 60 km east of Aqaba and 320 km south of Amman. Most visitors arrive by organized tour, rental car, or taxi from Aqaba or Petra.',
                'what_to_wear': 'Light, breathable clothing in layers. Bring warm clothes for evenings as desert temperatures drop significantly at night. Comfortable walking shoes and sandals.',
                'guided_tours': 'Bedouin guides offer jeep tours, camel rides, and overnight camping experiences. Most tours depart from Wadi Rum village.',
                'nearby_attractions': 'Petra (120 km north), Aqaba Red Sea coast (60 km west), and the Desert Highway connecting to the Dead Sea.',
                'facts': [
                    'The geological features include massive mesas that pop straight up from the sea of sand',
                    'The area is colored red by iron oxide, making it the "reddest" part of Jordan',
                    'Lawrence of Arabia used Wadi Rum as his base during the Arab Revolt',
                    'The village was only established around 1980; before this, locals lived nomadically',
                    'Wadi Rum has been featured in films like The Martian, Star Wars, and Dune',
                    'The Nabateans built a dam and temple ruins that can still be seen today'
                ],
                'key_sites': [
                    {'name': 'Seven Pillars of Wisdom', 'slug': 'seven-pillars-of-wisdom', 'description': 'A massive rock formation named after T.E. Lawrence\'s book', 'significance': 'One of the most iconic landmarks in Wadi Rum'},
                    {'name': 'Lawrence\'s Spring', 'description': 'A natural spring with Nabataean inscriptions and a water tank', 'significance': 'Named after T.E. Lawrence who reportedly bathed here'},
                    {'name': 'Khazali Canyon', 'slug': 'khazali-canyon', 'description': 'A narrow siq with ancient petroglyphs and inscriptions', 'significance': 'Contains 4,000-year-old rock art depicting humans and animals'},
                    {'name': 'Umm Fruth Rock Bridge', 'slug': 'umm-fruth-rock-bridge', 'description': 'A natural rock bridge arch formation', 'significance': 'Popular for climbing and photography'}
                ],
                'visitor_tips': [
                    'Stay overnight in a Bedouin camp for the full desert experience',
                    'Book jeep tours in advance during peak season',
                    'Bring cash as most camps don\'t accept cards',
                    'Watch the sunset and sunrise for spectacular desert colors',
                    'Stargazing at night is phenomenal due to no light pollution'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '29.5753° N, 35.4207° E',
                'unesco_status': 'UNESCO World Heritage Site since 2011',
                'area': '720 square kilometers',
                'annual_visitors': '162,000 (2017)',
                'climate': 'Desert climate with extreme temperature variations between day and night'
            },
            'dead-sea': {
                'id': 'dead-sea',
                'name': 'Dead Sea',
                'location': 'Jordan-Israel Border',
                'description': 'The lowest point on Earth at 439 meters below sea level, famous for its extremely salty waters and therapeutic mud.',
                'long_description': 'The Dead Sea is a landlocked salt lake bordered by Jordan to the east and Israel to the west. As of 2025, its surface is 439.78 meters below sea level, making its shores the lowest land-based elevation on Earth. With a salinity of 342 g/kg, or 34.2%, it is one of the world\'s saltiest bodies of water, 9.6 times as salty as the ocean. This extreme salinity creates buoyancy that allows people to float effortlessly on the water\'s surface.',
                'historical_significance': 'The Dead Sea has been a place of refuge and health resort since ancient times. It is mentioned in the Bible and was one of the world\'s first health resorts for Herod the Great. The ancient Egyptians used salts from the Dead Sea for mummification.',
                'facts': [
                    'The Dead Sea is 304 meters deep, the deepest hypersaline lake in the world',
                    'Its main tributary is the Jordan River',
                    'The water level drops by about 1 meter annually',
                    'The surface area has shrunk from 1,050 km² in 1930 to 605 km² today',
                    'The high salt content means no fish or aquatic life can survive',
                    'The mineral-rich mud has therapeutic properties for skin conditions'
                ],
                'entrance_fees': 'Access through various beach resorts ranges from 15-30 JOD. Public beaches may be free or charge minimal fees.',
                'opening_hours': 'Beach resorts typically open 8:00 AM to 6:00 PM',
                'best_time': 'March-May and September-November for moderate temperatures',
                'how_to_get_there': 'The Dead Sea is about 50 km from Amman, accessible by car or organized tour. Many hotels offer shuttle services.',
                'what_to_wear': 'Swimwear and waterproof sandals. Avoid shaving before visiting as salt water stings cuts.',
                'health_safety': 'Do not stay in the water for more than 15-20 minutes. Avoid getting water in eyes or mouth. Shower immediately after. Not recommended for people with open wounds or certain health conditions.',
                'guided_tours': 'Most visits are independent, but tours from Amman often combine the Dead Sea with other sites like Mount Nebo or Bethany.',
                'nearby_attractions': 'Mount Nebo (30 km), Bethany Beyond the Jordan (40 km), and Madaba (40 km).',
                'conservation': 'The Dead Sea is receding at an alarming rate due to water diversion from the Jordan River. The Red Sea-Dead Sea Water Conveyance project aims to help stabilize water levels.',
                'visitor_tips': [
                    'Float on your back and avoid splashing',
                    'Apply mineral mud for therapeutic benefits',
                    'Bring flip-flops as the salt deposits can be sharp',
                    'Don\'t shave 24 hours before visiting',
                    'Bring fresh water to rinse eyes in case of splashing',
                    'Visit early morning or late afternoon to avoid midday heat'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.5° N, 35.5° E',
                'area': '605 square kilometers (currently)',
                'climate': 'Hot desert climate, year-round warm temperatures'
            },
            'jerash': {
                'id': 'jerash',
                'name': 'Jerash',
                'location': 'Jerash Governorate, Jordan',
                'description': 'One of the best-preserved Roman provincial towns in the world, known as the "Pompeii of the Middle East".',
                'long_description': 'The ruined city of Jerash is Jordan\'s largest and most interesting Roman site. The city\'s golden age came under Roman rule, during which time it was known as Gerasa. The site is now generally acknowledged to be one of the best-preserved Roman provincial towns in the world. The ancient city boasts an unbroken chain of human occupation dating back more than 6,500 years.',
                'historical_significance': 'Jerash was inhabited since the 4th century BC and abandoned after an earthquake in 749 AD. Its imposing ceremonial gates, colonnaded avenues, temples and theatres all speak to the time when this was an important imperial centre. The city was part of the Decapolis, a league of ten cities in the eastern Roman Empire.',
                'architecture': 'The site includes several remarkable structures: the Oval Forum with 56 Ionic columns, the Cardo Maximus stretching 800m, Hadrian\'s Arch built in 129 AD, the South Theatre with capacity for 5,000 spectators, and the massive hippodrome that could seat 15,000 spectators.',
                'facts': [
                    'The Oval Forum is unusual for its shape: 90m long and 80m wide',
                    'The Cardo Maximus is still paved with original stones rutted by ancient chariots',
                    'Hadrian\'s Arch was built to commemorate Emperor Hadrian\'s visit in 129 AD',
                    'The Nymphaeum fountain was constructed in 191 AD with water cascading through lion\'s heads',
                    'Walking at leisure takes a minimum of 3-4 hours to see the main ruins',
                    'Jerash is the second-most popular tourist attraction in Jordan after Petra'
                ],
                'key_sites': [
                    {'name': 'Oval Forum', 'slug': 'oval-forum', 'description': 'Unique oval-shaped plaza surrounded by 56 Ionic columns', 'significance': 'Links the cardo maximus with the Temple of Zeus'},
                    {'name': 'Cardo Maximus', 'slug': 'cardo-maximus', 'description': '800-meter colonnaded street with original paving stones', 'significance': 'The city\'s main thoroughfare showing ancient urban planning'},
                    {'name': 'Hadrian\'s Arch', 'description': 'Splendid triumphal arch at the southern entrance', 'significance': 'Built to honor Emperor Hadrian\'s visit in 129 AD'},
                    {'name': 'South Theatre', 'slug': 'south-theatre', 'description': '1st-century theatre with 5,000-seat capacity', 'significance': 'Still used for performances during the Jerash Festival'},
                    {'name': 'Nymphaeum', 'slug': 'nymphaeum', 'description': 'Ornamental fountain from 191 AD', 'significance': 'Dedicated to the Nymphs with elaborate marble and plaster decoration'}
                ],
                'entrance_fees': '10 JOD (about $14 USD) for foreigners. Free with Jordan Pass.',
                'opening_hours': 'Summer (Apr-Oct): 8:00 AM to 7:00 PM; Winter (Nov-Mar): 8:00 AM to 4:00 PM',
                'best_time': 'Spring (March-May) or fall (September-November) for pleasant weather',
                'how_to_get_there': 'Jerash is 50 km north of Amman, accessible by rental car, taxi, or organized tour. The journey takes about 1 hour.',
                'what_to_wear': 'Comfortable walking shoes, hat, sunglasses. Modest clothing recommended.',
                'guided_tours': 'Official guides available at the entrance provide detailed historical explanations. Audio guides available in multiple languages.',
                'nearby_attractions': 'Ajloun Castle (30 km west), Umm Qais (50 km north), and Amman (50 km south).',
                'conservation': 'UNESCO and Jordanian authorities work to preserve the site. The Jerash Festival of Culture and Arts is held annually in July.',
                'visitor_tips': [
                    'Visit early morning to avoid crowds and heat',
                    'Allow at least 3-4 hours to explore properly',
                    'Bring water and snacks as there are limited facilities inside',
                    'The Roman Army and Chariot Experience show is worth seeing',
                    'Visit during the Jerash Festival in July for cultural performances'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '32.2811° N, 35.8911° E',
                'annual_visitors': 'Over 250,000',
                'climate': 'Mediterranean climate with hot summers and mild winters'
            },
            'mount-nebo': {
                'id': 'mount-nebo',
                'name': 'Mount Nebo',
                'location': 'Madaba Governorate, Jordan',
                'description': 'Sacred biblical site where Moses viewed the Promised Land before his death, offering panoramic views of the Holy Land.',
                'long_description': 'Mount Nebo is an elevated ridge approximately 700 meters above sea level, part of the Abarim mountain range. According to the Bible, Moses ascended Mount Nebo in the land of Moab and from there he saw the Land of Canaan, which God had said he would not enter. Moses then died there and the Bible says his burial place was unknown.',
                'historical_significance': 'The church was first constructed in the second half of the 4th century to commemorate the place of Moses\' death. On the highest point of the mountain, Syagha, the remains of a Byzantine church and monastery were discovered in 1933. It has been a pilgrimage site for many people and is a sacred location for three major religions.',
                'facts': [
                    'The view from the summit provides a panorama across the Jordan River valley',
                    'On clear days, Jerusalem is visible from the summit',
                    'The city of Jericho is usually visible from the top',
                    'Pope John Paul II visited on March 20, 2000, and planted an olive tree',
                    'The olive tree planted by the Pope symbolizes peace',
                    'A serpentine cross sculpture stands outside, symbolizing Moses\' bronze serpent and Jesus\' crucifixion'
                ],
                'key_sites': [
                    {'name': 'Byzantine Church', 'slug': 'byzantine-church', 'description': 'Ruins of a 4th-century church with beautiful mosaics', 'significance': 'Built to commemorate Moses\' death, contains some of the finest Byzantine mosaics'},
                    {'name': 'Memorial Church of Moses', 'slug': 'memorial-church-of-moses', 'description': 'Modern church built over the original Byzantine structure', 'significance': 'Active place of worship and pilgrimage'},
                    {'name': 'Brazen Serpent Monument', 'slug': 'brazen-serpent-monument', 'description': 'Serpentine cross sculpture by Giovanni Fantoni', 'significance': 'Symbolizes Moses\' bronze serpent and Christ\'s crucifixion'},
                    {'name': 'Pope\'s Olive Tree', 'description': 'Olive tree planted by Pope John Paul II in 2000', 'significance': 'Symbol of peace planted during papal visit'}
                ],
                'entrance_fees': '2 JOD (about $3 USD). Free with Jordan Pass.',
                'opening_hours': 'Summer: 8:00 AM to 6:00 PM; Winter: 8:00 AM to 4:00 PM',
                'best_time': 'Early morning for clearest views and cooler temperatures',
                'how_to_get_there': 'Mount Nebo is 10 km from Madaba and 40 km from Amman. Accessible by car or organized tour.',
                'what_to_wear': 'Comfortable shoes for walking. Modest clothing required as it\'s a religious site.',
                'guided_tours': 'Guides available on-site. Many tours combine Mount Nebo with Madaba and the Dead Sea.',
                'nearby_attractions': 'Madaba with its famous mosaic map (10 km), Dead Sea (30 km), and Bethany Beyond the Jordan (35 km).',
                'visitor_tips': [
                    'Visit on a clear day for the best views',
                    'Combine with a visit to Madaba\'s mosaic churches',
                    'Respect the religious significance of the site',
                    'The gift shop supports the local Franciscan community',
                    'Allow 1-2 hours for the visit'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.7690° N, 35.7272° E',
                'unesco_status': 'Part of the Bethany Beyond the Jordan UNESCO World Heritage Site',
                'climate': 'Mediterranean climate with cool winters and warm summers'
            },
            'madaba': {
                'id': 'madaba',
                'name': 'Madaba',
                'location': 'Madaba Governorate, Jordan',
                'description': 'The "City of Mosaics" famous for the 6th-century Byzantine mosaic map of the Holy Land.',
                'long_description': 'Madaba is best known for its spectacular Byzantine and Umayyad mosaics, especially the famous 6th-century Mosaic Map of Jerusalem and the Holy Land in the Greek Orthodox Church of St. George. With two million pieces of colored stone, the map depicts an area from Lebanon to the Nile Delta and from the Mediterranean to the Eastern Desert.',
                'historical_significance': 'The Madaba Map was constructed in the second half of the sixth century CE, possibly during the reign of Byzantine Emperor Justinian. Originally measuring 21 by 7 meters, it is the oldest surviving map of the Holy Land and a key source on Byzantine Jerusalem. The map was discovered during church construction in 1884.',
                'cultural_impact': 'The Madaba Map is a unique artifact representing the world\'s oldest floor map and the most impressive surviving example of Byzantine map-making. The city contains numerous other mosaics in various churches and the Archaeological Park.',
                'facts': [
                    'The original mosaic map had over two million tesserae (colored stone pieces)',
                    'Current dimensions are 16 by 5 meters (originally 21 by 7 meters)',
                    'The map was created between 542 and 614 CE',
                    'Madaba is mentioned in the Bible and was conquered by King David',
                    'The city has been inhabited since the Bronze Age',
                    'Over 50 churches have been discovered in Madaba and surroundings'
                ],
                'key_sites': [
                    {'name': 'St. George\'s Church Mosaic Map', 'description': '6th-century mosaic floor map of the Holy Land', 'significance': 'The oldest known geographic floor mosaic in art history'},
                    {'name': 'Archaeological Park', 'slug': 'archaeological-park', 'description': 'Complex of Byzantine churches with stunning mosaics', 'significance': 'Contains the Church of the Virgin and Hippolytus Hall mosaics'},
                    {'name': 'Madaba Museum', 'slug': 'madaba-museum', 'description': 'Museum housed in old houses displaying local artifacts', 'significance': 'Features mosaics and artifacts from various periods'},
                    {'name': 'Church of the Apostles', 'slug': 'church-of-the-apostles', 'description': 'Church with personification of the sea mosaic', 'significance': 'Contains one of the most famous mosaics in Madaba'}
                ],
                'entrance_fees': 'St. George Church: 1 JOD. Archaeological Park: 3 JOD. Free with Jordan Pass.',
                'opening_hours': 'Most sites: 8:00 AM to 6:00 PM (may vary by season)',
                'best_time': 'Year-round, but spring and fall offer the most pleasant weather',
                'how_to_get_there': 'Madaba is 30 km southwest of Amman, about 30 minutes by car or bus.',
                'what_to_wear': 'Modest clothing for church visits. Comfortable walking shoes.',
                'guided_tours': 'Local guides available. Often combined with Mount Nebo and Dead Sea tours.',
                'nearby_attractions': 'Mount Nebo (10 km), Dead Sea (40 km), and Bethany Beyond the Jordan (40 km).',
                'visitor_tips': [
                    'Visit St. George\'s Church when it\'s not during services',
                    'Allow 2-3 hours to see the main mosaic sites',
                    'The Archaeological Park ticket includes multiple churches',
                    'Shop for modern mosaics in the town\'s craft shops',
                    'Combine with Mount Nebo for a half-day trip'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.7197° N, 35.7936° E',
                'annual_visitors': 'Over 100,000',
                'climate': 'Mediterranean climate with mild winters and warm summers'
            },
            'amman-citadel': {
                'id': 'amman-citadel',
                'name': 'Amman Citadel',
                'location': 'Amman, Jordan',
                'description': 'Ancient fortress site on Jebel al-Qal\'a featuring the Temple of Hercules and offering panoramic views of Amman.',
                'long_description': 'The Amman Citadel, known as Jebel al-Qal\'a, is a historical site located on one of the seven hills of Amman. The site has been inhabited since the Bronze Age and contains remains from the Roman, Byzantine, and Umayyad periods. The most notable structure is the Temple of Hercules, built during the reign of Roman co-emperors Marcus Aurelius and Lucius Verus.',
                'historical_significance': 'The Citadel has been continuously occupied for over 7,000 years. The Temple of Hercules was built around 162-166 AD when Geminius Marcianus was governor of the Province of Arabia. The hand of Hercules, a massive marble fragment, is believed to be part of a colossal statue that could have measured 40 feet high.',
                'architecture': 'The Temple of Hercules stood on a podium 43 by 27 meters. The restored columns measure 13.5 meters tall. The portico at the front had six columns, making it one of the most impressive Roman temples in the region.',
                'facts': [
                    'The Hand of Hercules represents three fingers from a colossal statue',
                    'The original Hercules statue may have been 40 feet tall',
                    'Three columns have been restored, becoming an icon of Amman\'s skyline',
                    'The site includes a Byzantine church and Umayyad Palace',
                    'The Jordan Archaeological Museum is located on the Citadel grounds',
                    'Offers 360-degree panoramic views of Amman'
                ],
                'key_sites': [
                    {'name': 'Temple of Hercules', 'slug': 'temple-of-hercules', 'description': 'Roman temple with massive restored columns', 'significance': 'Dedicated to co-emperors Marcus Aurelius and Lucius Verus'},
                    {'name': 'Hand of Hercules', 'slug': 'hand-of-hercules', 'description': 'Massive marble hand fragment from colossal statue', 'significance': 'One of the largest known marble statue fragments from antiquity'},
                    {'name': 'Umayyad Palace', 'slug': 'umayyad-palace', 'description': 'Large palatial complex from the 8th century', 'significance': 'Shows the Islamic period\'s architectural achievements'},
                    {'name': 'Byzantine Church', 'slug': 'byzantine-church', 'description': 'Ruins of an early Christian basilica', 'significance': 'Evidence of early Christianity in the region'}
                ],
                'entrance_fees': '3 JOD (about $4 USD). Free with Jordan Pass.',
                'opening_hours': 'Summer: 8:00 AM to 7:00 PM; Winter: 8:00 AM to 4:00 PM',
                'best_time': 'Late afternoon for sunset views over Amman',
                'how_to_get_there': 'Located in downtown Amman, accessible by taxi or on foot from the Roman Theatre area.',
                'what_to_wear': 'Comfortable walking shoes. Sun protection recommended.',
                'guided_tours': 'Guides available at the entrance. Often combined with Roman Theatre and downtown Amman tours.',
                'nearby_attractions': 'Roman Theatre (walking distance), Jordan Museum (3 km), and Rainbow Street (2 km).',
                'conservation': 'Ongoing conservation by the Department of Antiquities. The three restored columns are now an iconic symbol of Amman.',
                'visitor_tips': [
                    'Visit late afternoon for beautiful sunset views',
                    'Combine with the nearby Roman Theatre',
                    'Visit the Jordan Archaeological Museum on-site',
                    'Allow 1-2 hours for exploration',
                    'Great for photography, especially the Hand of Hercules'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.9539° N, 35.9346° E',
                'climate': 'Mediterranean climate with hot summers and mild winters'
            },
            'aqaba': {
                'id': 'aqaba',
                'name': 'Aqaba',
                'location': 'Aqaba Governorate, Jordan',
                'description': 'Jordan\'s only coastal city on the Red Sea, famous for diving, beaches, and coral reefs.',
                'long_description': 'Aqaba is Jordan\'s only seaport and major tourism resort on the northern tip of the Red Sea. With the red mountains of Wadi Rum in the background and pristine coral reefs offshore, Aqaba offers a unique combination of desert adventures and underwater exploration. The city features year-round warm weather and crystal-clear waters perfect for diving and snorkeling.',
                'historical_significance': 'Aqaba has been an important trading port since ancient times. The city was conquered by various civilizations including the Nabataeans, Romans, and Crusaders. The Mamluk Fort dates from the 16th century and represents the Islamic period of the city.',
                'facts': [
                    'The Red Sea has more than 1,200 species of fish',
                    '44 species of sharks live in the Red Sea',
                    'Nearly 20% of Red Sea marine species are found nowhere else',
                    'Water temperature averages 66°F in winter, 84°F in summer',
                    'The Aqaba Marine Park includes 21 dive sites',
                    '14 dive sites are accessible from shore',
                    'Aqaba is a tax-free economic zone'
                ],
                'key_sites': [
                    {'name': 'Aqaba Marine Park', 'slug': 'aqaba-marine-park', 'description': 'Protected area with 21 dive sites featuring coral reefs', 'significance': 'Home to diverse marine life and well-preserved coral gardens'},
                    {'name': 'Aqaba Fort', 'slug': 'aqaba-fort', 'description': '16th-century Mamluk fortress', 'significance': 'Historical military structure overlooking the city'},
                    {'name': 'Public Beach', 'slug': 'public-beach', 'description': 'Free public beach with facilities', 'significance': 'Accessible beach for swimming and relaxation'},
                    {'name': 'Dive Centers', 'slug': 'dive-centers', 'description': 'Multiple PADI-certified dive centers', 'significance': 'Offer diving courses and trips to coral reefs and wrecks'}
                ],
                'entrance_fees': 'Beaches vary: public beaches free, resort beaches 10-30 JOD',
                'opening_hours': 'Beaches and dive centers typically 8:00 AM to sunset',
                'best_time': 'October to April for diving; year-round for beaches',
                'how_to_get_there': 'Aqaba is 330 km south of Amman (4-hour drive). King Hussein International Airport serves the city with domestic and international flights.',
                'what_to_wear': 'Swimwear, waterproof sandals, sun protection. Bring or rent diving equipment.',
                'health_safety': 'Stay hydrated. Use reef-safe sunscreen to protect coral. Follow dive safety guidelines.',
                'guided_tours': 'Diving tours, snorkeling trips, glass-bottom boat tours, and day trips to Wadi Rum available.',
                'nearby_attractions': 'Wadi Rum (60 km), Petra (120 km), and the Saudi Arabia border crossing.',
                'conservation': 'The Aqaba Marine Park protects coral reefs. Visitors must follow environmental guidelines to preserve the ecosystem.',
                'visitor_tips': [
                    'Book diving trips in advance during peak season',
                    'Try night diving for a different perspective',
                    'Visit the wreck dive sites for unique underwater exploration',
                    'Combine beach time with a desert trip to Wadi Rum',
                    'Tax-free shopping available in Aqaba Special Economic Zone'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '29.5269° N, 35.0071° E',
                'annual_visitors': 'Over 500,000',
                'climate': 'Hot desert climate with mild winters and very hot summers'
            },
            'bethany-beyond-jordan': {
                'id': 'bethany-beyond-jordan',
                'name': 'Bethany Beyond the Jordan',
                'location': 'Balqa Governorate, Jordan',
                'description': 'UNESCO World Heritage baptism site where Jesus was baptized by John the Baptist.',
                'long_description': 'Bethany Beyond the Jordan, also known as Al-Maghtas, is considered by the majority of Christian Churches to be the location where John the Baptist baptized Jesus. This archaeological World Heritage Site on the east bank of the Jordan River features Roman and Byzantine remains including churches, chapels, monasteries, caves used by hermits, and baptismal pools.',
                'historical_significance': 'The site consists of two distinct areas: Tell Al-Kharrar (Elijah\'s Hill) and the area of churches near the river. The remains of more than 20 Christian sites have been discovered, testifying to the religious character of the place since Byzantine times. Dr. Mohammad Waheeb rediscovered the ancient site in 1997.',
                'cultural_impact': 'The site was designated a UNESCO World Heritage Site in 2015. Pope John Paul II became the first papal to visit Bethany Beyond the Jordan in 2000. Jordan fully reopened Al-Maghtas in 2002, and it has since become one of the most important Christian pilgrimage sites in the Middle East.',
                'facts': [
                    'The archaeological site has remains from Roman and Byzantine periods',
                    'More than 20 Christian sites have been discovered',
                    'Features sophisticated water reticulation system',
                    'Pope John Paul II visited in 2000',
                    'Designated UNESCO World Heritage Site in 2015',
                    'Jordan reopened the site in 2002 after extensive excavation'
                ],
                'key_sites': [
                    {'name': 'Tell Al-Kharrar (Elijah\'s Hill)', 'description': 'Archaeological tel with Byzantine church remains', 'significance': 'Believed to be where Elijah ascended to heaven and John the Baptist lived'},
                    {'name': 'Churches of St. John the Baptist', 'slug': 'churches-of-st-john-the-baptist', 'description': 'Complex of churches near the Jordan River', 'significance': 'Multiple churches built over centuries at the baptism site'},
                    {'name': 'Baptismal Pools', 'slug': 'baptismal-pools', 'description': 'Ancient pools used for baptism ceremonies', 'significance': 'Show the continuous use of the site for baptisms'},
                    {'name': 'Hermit Caves', 'slug': 'hermit-caves', 'description': 'Caves used by early Christian hermits', 'significance': 'Evidence of early monastic life in the area'}
                ],
                'entrance_fees': '12 JOD (about $17 USD). Free with Jordan Pass.',
                'opening_hours': 'Summer: 8:00 AM to 6:00 PM; Winter: 8:00 AM to 4:00 PM',
                'best_time': 'Spring and fall for moderate temperatures',
                'how_to_get_there': 'Located 9 km north of the Dead Sea, about 50 km from Amman. Accessible by tour or rental car.',
                'what_to_wear': 'Modest clothing required. Comfortable walking shoes.',
                'guided_tours': 'Guided tours included with admission. Tours explain the biblical and archaeological significance.',
                'nearby_attractions': 'Dead Sea (9 km), Mount Nebo (35 km), and Madaba (40 km).',
                'conservation': 'UNESCO and Jordanian authorities work to preserve the site. Ongoing archaeological excavations continue to uncover new findings.',
                'visitor_tips': [
                    'Guided tour is mandatory and included in the ticket price',
                    'Allow 1.5-2 hours for the full tour',
                    'Bring baptism certificate if you wish to be baptized',
                    'Photography is allowed',
                    'Respect the sacred nature of the site'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.8367° N, 35.5486° E',
                'unesco_status': 'UNESCO World Heritage Site since 2015',
                'climate': 'Hot desert climate with mild winters'
            },
            'ajloun-castle': {
                'id': 'ajloun-castle',
                'name': 'Ajloun Castle',
                'location': 'Ajloun Governorate, Jordan',
                'description': '12th-century Muslim fortress built by Saladin\'s forces to defend against Crusaders.',
                'long_description': 'Ajloun Castle, also known as Qal\'at ar-Rabad, is a 12th-century Muslim castle situated in northwestern Jordan at 1,250 meters above sea level. Built between 1184-1188 by Izz al-Din Usama, a general of Saladin, the castle served as a military outpost to protect the region from Crusader invasions and control iron mining operations.',
                'historical_significance': 'The fortress was built on Saladin\'s order as part of a major military tactic to stop the expansion of Crusader territory. From its strategic location, it dominated the northern Jordan Valley and controlled three main passages. It was also part of a chain of beacons and pigeon posts enabling messages to be transmitted from Damascus to Cairo in a single day.',
                'architecture': 'The original castle had four corner towers connected by curtain walls and a double gate. Arrow slits were incorporated in thick walls, and it was surrounded by a moat averaging 16 meters wide and 12-15 meters deep. The castle was enlarged in 1214-1215 by Mamluk governor Aibak ibn Abdullah.',
                'facts': [
                    'Built between 1184-1188 by Saladin\'s nephew Izz al-Din Usama',
                    'Part of a defensive network against Crusaders',
                    'Protected communication routes between southern Jordan and Syria',
                    'Also protected iron mines of Ajloun',
                    'Part of beacon chain from Damascus to Cairo',
                    'Damaged by earthquakes in 1837 and 1927',
                    'Recently restored by Department of Antiquities'
                ],
                'key_sites': [
                    {'name': 'Corner Towers', 'slug': 'corner-towers', 'description': 'Four defensive towers at castle corners', 'significance': 'Provided 360-degree defensive coverage'},
                    {'name': 'Moat', 'slug': 'moat', 'description': 'Defensive ditch 16m wide and 12-15m deep', 'significance': 'Protected the castle from ground attacks'},
                    {'name': 'Museum Exhibition', 'slug': 'museum-exhibition', 'description': 'Display of artifacts from various periods', 'significance': 'Shows the history of the region through artifacts'},
                    {'name': 'Arrow Slits', 'slug': 'arrow-slits', 'description': 'Narrow openings in thick walls', 'significance': 'Allowed archers to defend while protected'}
                ],
                'entrance_fees': '3 JOD (about $4 USD). Free with Jordan Pass.',
                'opening_hours': 'Summer: 8:00 AM to 7:00 PM; Winter: 8:00 AM to 4:00 PM',
                'best_time': 'Spring and fall for pleasant weather and green landscapes',
                'how_to_get_there': 'Ajloun is 75 km northwest of Amman, about 1.5 hours by car. Often combined with Jerash visits.',
                'what_to_wear': 'Comfortable walking shoes for exploring the castle. Layers recommended as it can be cool.',
                'guided_tours': 'Guides available at entrance. Museum exhibitions provide historical context.',
                'nearby_attractions': 'Jerash Roman ruins (30 km), Ajloun Forest Reserve, and Dibeen Forest Reserve.',
                'conservation': 'The Department of Antiquities has sponsored restoration and consolidation of walls and rebuilt the bridge over the moat.',
                'visitor_tips': [
                    'Visit in spring when surrounding hills are green',
                    'Combine with Jerash for a full day trip',
                    'Explore the museum inside the castle',
                    'Enjoy panoramic views from the towers',
                    'Allow 1-2 hours for visit'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '32.3319° N, 35.7519° E',
                'climate': 'Mediterranean climate with cool winters and mild summers'
            },
            'karak-castle': {
                'id': 'karak-castle',
                'name': 'Karak Castle',
                'location': 'Karak Governorate, Jordan',
                'description': 'One of the largest Crusader castles in the Levant, built in the 12th century.',
                'long_description': 'Kerak Castle is a large medieval castle located in al-Karak, Jordan, sitting 900m above sea level inside the walls of the old city. It is one of the largest castles in the Levant. Construction began in the 1140s under Pagan and Fulk, King of Jerusalem. The castle controlled trade routes from Damascus to Egypt and Mecca due to its strategic position east of the Dead Sea.',
                'historical_significance': 'The Crusaders called it Crac des Moabites. In 1176, Raynald of Châtillon gained possession and used it to harass trade caravans and even attempted an attack on Mecca. Saladin besieged the castle in 1183, and it finally surrendered in 1188 after the Crusader defeat at the Battle of Hattin, having been in Crusader hands for only 46 years.',
                'architecture': 'The castle extends across seven levels including towers, barracks, a kitchen, a church and mosque, prison cells, an underground marketplace, a museum, and a palace. The most notable Crusader feature is the north wall with immense arched halls on two levels used for living quarters, stables, and as fighting galleries.',
                'facts': [
                    'Construction began in the 1140s',
                    'In Crusader hands for 46 years',
                    'Raynald of Châtillon attacked trade caravans from here',
                    'Fell to Saladin in 1188 after year-long siege',
                    'Extends across seven levels',
                    'Located on the ancient King\'s Highway',
                    '140 km south of Amman'
                ],
                'key_sites': [
                    {'name': 'North Wall Galleries', 'slug': 'north-wall-galleries', 'description': 'Crusader arched halls on two levels', 'significance': 'Used for living, stables, and defense'},
                    {'name': 'Underground Passages', 'slug': 'underground-passages', 'description': 'Network of tunnels and rooms', 'significance': 'Includes marketplace, prison cells, and storage'},
                    {'name': 'Church and Mosque', 'slug': 'church-and-mosque', 'description': 'Religious structures from different periods', 'significance': 'Shows the castle\'s changing occupants'},
                    {'name': 'Museum', 'slug': 'museum', 'description': 'Displays artifacts and castle history', 'significance': 'Provides historical context'}
                ],
                'entrance_fees': '2 JOD (about $3 USD). Free with Jordan Pass.',
                'opening_hours': 'October-March: 8:00 AM to 4:00 PM; April-September: 8:00 AM to 7:00 PM',
                'best_time': 'Spring and fall for moderate temperatures',
                'how_to_get_there': 'Al-Karak is 140 km south of Amman on the ancient King\'s Highway, about 2 hours by car.',
                'what_to_wear': 'Comfortable walking shoes. The castle has many stairs and levels to explore.',
                'guided_tours': 'Local guides available. Exploring independently with a map is also possible.',
                'nearby_attractions': 'Dana Biosphere Reserve (40 km), Dead Sea (50 km), and Petra (100 km south).',
                'conservation': 'Ongoing preservation work by Jordanian authorities. The castle remains remarkably well-preserved.',
                'visitor_tips': [
                    'Allow 2-3 hours to properly explore all seven levels',
                    'Visit early to avoid midday heat',
                    'Bring a flashlight for darker underground areas',
                    'The castle offers great views of the surrounding landscape',
                    'Combine with King\'s Highway scenic route'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.1843° N, 35.7049° E',
                'climate': 'Mediterranean climate with cool winters and warm summers'
            },
            'dana-reserve': {
                'id': 'dana-reserve',
                'name': 'Dana Biosphere Reserve',
                'location': 'Tafilah Governorate, Jordan',
                'description': 'Jordan\'s largest nature reserve with diverse ecosystems and spectacular landscapes.',
                'long_description': 'Dana Biosphere Reserve is Jordan\'s largest nature reserve, comprising 308 square kilometers. Founded in 1989, it became Jordan\'s first biosphere reserve according to UNESCO classifications in 1998. The reserve drops from 1,500 meters on the Qadisiyah plateau to the low-lying Wadi Araba, encompassing four different bio-geographical zones.',
                'historical_significance': 'Human settlement in Dana dates back over 6,000 years, with archaeological discoveries suggesting Palaeolithic, Egyptian, Nabataean, and Roman settlement. The Dana village itself is a well-preserved 15th-century Ottoman stone village.',
                'facts': [
                    'Jordan\'s largest nature reserve at 308 square kilometers',
                    'Only reserve in Jordan with four bio-geographical zones',
                    'Home to 800 plant species',
                    '449 animal species recorded',
                    '25 endangered species including Sand Cat and Syrian Wolf',
                    'Largest breeding colony of Syrian serin',
                    'Human habitation for over 6,000 years'
                ],
                'key_sites': [
                    {'name': 'Dana Village', 'slug': 'dana-village', 'description': '15th-century Ottoman stone village', 'significance': 'Well-preserved historical village with traditional architecture'},
                    {'name': 'Wadi Dana Trail', 'slug': 'wadi-dana-trail', 'description': '14 km hiking trail through the reserve', 'significance': 'Descends through all four bio-geographical zones'},
                    {'name': 'Feynan Eco-lodge', 'slug': 'feynan-eco-lodge', 'description': 'Award-winning sustainable lodge', 'significance': 'First solar-powered lodge in the Middle East'},
                    {'name': 'Copper Mines', 'slug': 'copper-mines', 'description': 'Ancient copper mining sites', 'significance': 'Evidence of historical metal working'}
                ],
                'entrance_fees': 'Day visit: 7 JOD. Free with Jordan Pass. Hiking permits required for trails.',
                'opening_hours': 'Reserve accessible year-round. Visitor center: 8:00 AM to 3:00 PM',
                'best_time': 'Spring (March-May) and fall (September-November) for hiking',
                'how_to_get_there': 'Dana village is on the King\'s Highway between Tafilah and Shobak, about 220 km south of Amman.',
                'what_to_wear': 'Hiking boots, layered clothing, sun protection. Bring water for hikes.',
                'health_safety': 'Hire local guides for longer hikes. Some trails are strenuous. Stay on marked paths.',
                'guided_tours': 'Local Bedouin guides offer various hiking trails and camping experiences.',
                'nearby_attractions': 'Shobak Castle (30 km), Petra (60 km), and Wadi Feynan (within reserve).',
                'conservation': 'The reserve protects endangered species and supports sustainable tourism. Local communities are involved in conservation efforts.',
                'visitor_tips': [
                    'Book Feynan Eco-lodge in advance',
                    'Hire a local guide for the best experience',
                    'The Wadi Dana trail is strenuous but spectacular',
                    'Stay overnight to experience the reserve fully',
                    'Support local crafts made by Dana cooperative'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '30.6833° N, 35.6000° E',
                'area': '308 square kilometers',
                'climate': 'Varies by elevation: Mediterranean to desert climates'
            },
            'umm-qais': {
                'id': 'umm-qais',
                'name': 'Umm Qais (Gadara)',
                'location': 'Irbid Governorate, Jordan',
                'description': 'Ancient Decapolis city perched on a hilltop with stunning views over three countries.',
                'long_description': 'Umm Qais expanded from the ruins of ancient Gadara, located on a ridge 378 meters above sea level, overlooking the Sea of Tiberias, the Golan Heights, and the Yarmouk River gorge. Known in ancient times as Gadara, it was one of the cities of the Decapolis—a group of ten cities on the eastern frontier of the Roman Empire. Gadara was renowned as a cultural center and was once called "a new Athens" by a poet.',
                'historical_significance': 'Gadara was originally built by the Greeks in the 4th century BC. When Roman general Pompey conquered the region in 63 BC, he oversaw the rebuilding of Gadara and made it one of the semi-autonomous cities of the Roman Decapolis. It was the home of several classical poets and philosophers, including Theodorus, founder of a rhetorical school in Rome.',
                'architecture': 'The site features an impressive colonnaded street, a vaulted terrace, and the ruins of two theaters. One theater is unique in Jordan for its westward orientation and construction from basalt stone, holding up to 5,000 spectators with perfect acoustics.',
                'facts': [
                    'Gadara was the end point of the 170 km long Qanat Fir\'aun water system',
                    '106 km of the water system ran underground, the longest tunnel of antiquity',
                    'The site offers views over three countries: Jordan, Syria, and Israel',
                    'Named among the \'Best Tourism Villages 2022\' by UNWTO',
                    'The western theater is unique in Jordan for its basalt construction',
                    'Gadara was home to famous poets and philosophers in ancient times'
                ],
                'key_sites': [
                    {'name': 'West Theatre', 'slug': 'west-theatre', 'description': 'Unique basalt theater with 5,000-seat capacity', 'significance': 'Only westward-facing theater in Jordan with perfect acoustics'},
                    {'name': 'Colonnaded Street', 'slug': 'colonnaded-street', 'description': 'Impressive main street with columns', 'significance': 'Shows the grandeur of the Decapolis city'},
                    {'name': 'Ottoman Village', 'slug': 'ottoman-village', 'description': 'Well-preserved 19th-century Ottoman village', 'significance': 'Demonstrates later periods of habitation'},
                    {'name': 'Basilica Terrace', 'slug': 'basilica-terrace', 'description': 'Byzantine church complex', 'significance': 'Evidence of early Christian presence'}
                ],
                'entrance_fees': '3 JOD (about $4 USD). Free with Jordan Pass.',
                'opening_hours': 'Summer: 8:00 AM to 7:00 PM; Winter: 8:00 AM to 4:00 PM',
                'best_time': 'Spring for wildflowers and clear views',
                'how_to_get_there': 'Umm Qais is 120 km north of Amman, about 2 hours by car. Can be combined with Jerash and Ajloun.',
                'what_to_wear': 'Comfortable walking shoes, hat, sunglasses.',
                'guided_tours': 'Local guides available. Restaurant with panoramic terrace on site.',
                'nearby_attractions': 'Jerash (75 km), Ajloun Castle (50 km), and Yarmouk Forest Reserve.',
                'conservation': 'Ongoing preservation by Department of Antiquities. Recognition as UNWTO Best Tourism Village.',
                'visitor_tips': [
                    'Visit on a clear day for the best panoramic views',
                    'Have lunch at the restaurant with terrace overlooking three countries',
                    'Explore both the Greek-Roman ruins and Ottoman village',
                    'Allow 2-3 hours for full exploration',
                    'Combine with other northern Jordan sites'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '32.6539° N, 35.6828° E',
                'annual_visitors': 'Over 50,000',
                'climate': 'Mediterranean climate with mild winters'
            },
            'qasr-amra': {
                'id': 'qasr-amra',
                'name': 'Qasr Amra',
                'location': 'Zarqa Governorate, Jordan',
                'description': 'UNESCO World Heritage desert castle famous for its unique 8th-century frescoes.',
                'long_description': 'Qusayr Amra is the best-known of the desert castles in eastern Jordan. Built between 723-743 by Walid Ibn Yazid, the future Umayyad caliph Walid II, it is considered one of the most important examples of early Islamic art and architecture. The extensive fresco paintings are unique for Islamic architecture of the Umayyad period.',
                'historical_significance': 'This exceptionally well-preserved desert castle was both a fortress with a garrison and a residence of the Umayyad caliphs. The frescoes, painted around 730-740 AD, are an extremely rare example of the rich decorative culture of the Umayyads.',
                'cultural_impact': 'The castle was made a UNESCO World Heritage Site in 1985. The frescoes were restored in the 1970s and 1990s, revealing rich colors that had not been visible before.',
                'facts': [
                    'Built between 723-743 AD by future caliph Walid II',
                    'UNESCO World Heritage Site since 1985',
                    'Frescoes depict bathing scenes, hunting, crafts, and animals',
                    'Contains one of the earliest known celestial domes',
                    'Features completely nude figures, unusual for the period',
                    'The Painting of the Six Kings depicts rulers from different empires',
                    'Inscriptions in both Greek and Arabic'
                ],
                'key_sites': [
                    {'name': 'Reception Hall', 'slug': 'reception-hall', 'description': 'Main hall with extensive frescoes', 'significance': 'Contains the famous Painting of the Six Kings'},
                    {'name': 'Bath House', 'slug': 'bath-house', 'description': 'Three-room bathing complex', 'significance': 'Shows Umayyad bathing culture with unique frescoes'},
                    {'name': 'Caldarium Dome', 'slug': 'caldarium-dome', 'description': 'Hot room with zodiac ceiling', 'significance': 'One of earliest surviving celestial maps on a dome'},
                    {'name': 'Frescoed Walls', 'slug': 'frescoed-walls', 'description': 'Walls covered in 8th-century paintings', 'significance': 'Rare example of Umayyad decorative art'}
                ],
                'entrance_fees': '3 JOD (about $4 USD). Free with Jordan Pass.',
                'opening_hours': 'Summer: 8:00 AM to 6:00 PM; Winter: 8:00 AM to 4:00 PM',
                'best_time': 'Spring and fall for moderate temperatures',
                'how_to_get_there': 'About 85 km east of Amman on the highway to Azraq. Often part of "Desert Castles Loop" tour.',
                'what_to_wear': 'Sun protection, comfortable shoes. Modest clothing recommended.',
                'guided_tours': 'Guides available. Often combined with other desert castles like Qasr Kharana and Qasr Azraq.',
                'nearby_attractions': 'Qasr Kharana (15 km), Qasr Azraq (35 km), and Azraq Wetland Reserve.',
                'conservation': 'Restoration programs in 1970s and 1990s. Ongoing UNESCO protection.',
                'visitor_tips': [
                    'Visit as part of the Desert Castles Loop',
                    'Allow 45 minutes to 1 hour for visit',
                    'Photography allowed inside',
                    'Best light for photography in morning',
                    'Combine with Azraq Wetland Reserve visit'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.8017° N, 36.5842° E',
                'unesco_status': 'UNESCO World Heritage Site since 1985',
                'climate': 'Desert climate with hot summers and cool winters'
            },
            'azraq-wetland': {
                'id': 'azraq-wetland',
                'name': 'Azraq Wetland Reserve',
                'location': 'Zarqa Governorate, Jordan',
                'description': 'Unique desert oasis and migratory bird sanctuary in the heart of Jordan\'s eastern desert.',
                'long_description': 'The Azraq Wetland Reserve was established in 1978 and covers 12 square kilometers, serving as an oasis for migratory birds. The name "Azraq" means "blue" in Arabic, referring to the water that once filled this desert oasis. Located between a limestone desert and a basalt desert, it represents a crucial stopover for birds migrating between Africa, Asia, and Europe.',
                'historical_significance': 'The natural springs dried up in 1992 due to over-pumping for urban water supply. Through RSCN management, the wetlands have been partially restored to 10% of their original size, bringing back migratory species and creating opportunities for local communities.',
                'conservation': 'Artificial springs maintain the site today. The RSCN has successfully rehabilitated the oasis, resulting in the return of several migratory species including the hoopoe lark, Cetti\'s warbler, desert finch, and marsh harrier.',
                'facts': [
                    'Established as a reserve in 1978',
                    'Lost 99.6% of its water and plant cover by 1992',
                    'Now restored to 10% of original wetland',
                    'Home to the Azraq Killifish, Jordan\'s only endemic vertebrate',
                    '280 migratory bird species recorded',
                    'Migratory stopover for birds from three continents',
                    'Water pumping supplied 60 million cubic meters annually to cities'
                ],
                'key_sites': [
                    {'name': 'Boardwalk Trails', 'slug': 'boardwalk-trails', 'description': 'Elevated walkways through wetland', 'significance': 'Allow close observation of birds and fish'},
                    {'name': 'Observation Points', 'slug': 'observation-points', 'description': 'Bird watching platforms', 'significance': 'Best spots for viewing migratory species'},
                    {'name': 'Marshland Pools', 'slug': 'marshland-pools', 'description': 'Restored wetland areas', 'significance': 'Habitat for endemic Azraq Killifish'},
                    {'name': 'Visitor Center', 'slug': 'visitor-center', 'description': 'Educational facility with exhibits', 'significance': 'Explains wetland ecology and conservation'}
                ],
                'entrance_fees': '5 JOD (about $7 USD). Free with Jordan Pass.',
                'opening_hours': 'Summer: 8:00 AM to 6:00 PM; Winter: 8:00 AM to 4:00 PM',
                'best_time': 'Spring and fall for peak bird migration',
                'how_to_get_there': 'Located 100 km east of Amman near Azraq town. Accessible by car or as part of desert castles tour.',
                'what_to_wear': 'Comfortable walking shoes, sun protection. Bring binoculars for bird watching.',
                'health_safety': 'Stay on marked boardwalks. Bring water and sun protection.',
                'guided_tours': 'Guided walks available. Bird watching tours can be arranged.',
                'nearby_attractions': 'Qasr Azraq fortress (in Azraq town), Shaumari Wildlife Reserve (15 km), and desert castles.',
                'visitor_tips': [
                    'Visit early morning for best bird watching',
                    'Bring binoculars and camera with telephoto lens',
                    'Walk the full boardwalk circuit',
                    'Visit during migration seasons for maximum species',
                    'Allow 1-2 hours for visit'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.8211° N, 36.8211° E',
                'area': '12 square kilometers',
                'climate': 'Desert climate with hot summers and cool winters'
            },
            'wadi-mujib': {
                'id': 'wadi-mujib',
                'name': 'Wadi Mujib',
                'location': 'Karak and Madaba Governorates, Jordan',
                'description': 'Jordan\'s "Grand Canyon" - the lowest nature reserve in the world with spectacular canyoning adventures.',
                'long_description': 'The Mujib Biosphere Reserve is the lowest nature reserve in the world, located within the deep Wadi Mujib gorge, which enters the Dead Sea at 410 meters below sea level. The reserve extends to the Karak and Madaba mountains, reaching 900 meters above sea level, creating a dramatic 1,300-meter variation in elevation.',
                'historical_significance': 'The wadi has been a natural corridor for thousands of years. Its dramatic landscapes and year-round water flow have supported human activity since ancient times.',
                'facts': [
                    'Lowest nature reserve in the world at 410m below sea level',
                    '1,300-meter elevation variation from canyon to mountains',
                    'Often called Jordan\'s Grand Canyon',
                    'Features waterfalls, natural waterslides, and slot canyons',
                    'Home to Nubian ibex and striped hyenas',
                    'Open April to October for wet trails',
                    'Siq Trail is the most popular adventure route'
                ],
                'key_sites': [
                    {'name': 'Siq Trail', 'slug': 'siq-trail', 'description': 'River hike through slot canyon to waterfall', 'significance': 'Most popular 2-4 hour adventure with swimming and climbing'},
                    {'name': 'Malaqi Trail', 'slug': 'malaqi-trail', 'description': 'Longer route with waterfall rappelling', 'significance': 'Advanced canyoning experience requiring guides'},
                    {'name': 'Canyon Trail', 'slug': 'canyon-trail', 'description': 'Full-day canyon descent', 'significance': 'Technical route with multiple waterfalls'},
                    {'name': 'Ibex Trail', 'slug': 'ibex-trail', 'description': 'Dry hiking trail', 'significance': 'Only year-round trail, good for wildlife spotting'}
                ],
                'entrance_fees': 'Siq Trail: 21 JOD (about $30 USD). Other trails: 28-70 JOD. Not included in Jordan Pass.',
                'opening_hours': 'April to October: 8:00 AM to 4:00 PM for wet trails. Ibex Trail: Year-round',
                'best_time': 'April-May and September-October for ideal water temperatures',
                'how_to_get_there': 'Located on the Dead Sea Highway, about 90 km from Amman. Entrance is well-marked along the road.',
                'what_to_wear': 'Swimwear, water shoes with good grip, dry bag for valuables. Wetsuits available for rental.',
                'health_safety': 'Must be able to swim. Follow safety instructions. Trails can be physically demanding. Not recommended for young children.',
                'guided_tours': 'Guides mandatory for Malaqi and Canyon trails. Siq Trail can be done independently but guides recommended.',
                'nearby_attractions': 'Dead Sea resorts (15-30 km), Bethany Beyond the Jordan (40 km), and Mount Nebo (60 km).',
                'conservation': 'Protected biosphere reserve. Visitors must follow environmental guidelines. Flash flood monitoring in place.',
                'visitor_tips': [
                    'Book in advance during peak season',
                    'Start early to avoid crowds',
                    'Bring waterproof bag for phones and valuables',
                    'Wear shoes with good grip - surfaces are slippery',
                    'Check weather forecast - trails close during rain',
                    'Physical fitness required for all wet trails'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.4503° N, 35.5831° E',
                'area': 'Reserve extends over 212 square kilometers',
                'climate': 'Hot desert climate with year-round water flow'
            },
            'little-petra': {
                'id': 'little-petra',
                'name': 'Little Petra (Siq al-Barid)',
                'location': 'Ma\'an Governorate, Jordan',
                'description': 'Smaller Nabataean archaeological site featuring rare ancient frescoes and rock-cut architecture.',
                'long_description': 'Little Petra, also known as Siq al-Barid (meaning "the cold canyon"), is a Nabataean archaeological site located 8 kilometers north of Petra. Like its larger neighbor, it features buildings carved into sandstone canyon walls. The site consists of three wider areas connected by a 450-meter canyon and was likely a suburb of Petra meant to house visiting traders.',
                'historical_significance': 'Built during the height of Nabataean influence in the 1st century CE, Little Petra served as a commercial suburb of the capital. The site features the Painted Biclinium, the only known example of interior Nabataean figurative painting in situ, dated to 40 BCE-25 CE through radiocarbon analysis.',
                'cultural_impact': 'The Painted Biclinium represents a very rare large-scale example of Hellenistic painting, considered superior even to similar later Roman paintings at Herculaneum. The site is part of Petra\'s UNESCO World Heritage inscription.',
                'facts': [
                    'Located 8 km north of Petra',
                    'Connected by a 450-meter canyon',
                    'Built in the 1st century BCE',
                    'Houses the only known Nabataean interior figurative paintings',
                    'Frescoes dated to 40 BCE-25 CE',
                    'Free to visit and less crowded than Petra',
                    'Part of Petra UNESCO World Heritage Site'
                ],
                'key_sites': [
                    {'name': 'Painted Biclinium', 'slug': 'painted-biclinium', 'description': 'Rock-cut dining room with rare frescoes', 'significance': 'Only surviving example of Nabataean interior figurative painting'},
                    {'name': 'Rock-Cut Tombs', 'slug': 'rock-cut-tombs', 'description': 'Elaborate burial chambers', 'significance': 'Show Nabataean funerary architecture'},
                    {'name': 'Water Channels', 'slug': 'water-channels', 'description': 'Sophisticated water management system', 'significance': 'Demonstrates Nabataean engineering skills'},
                    {'name': 'Temple Facades', 'slug': 'temple-facades', 'description': 'Carved building fronts', 'significance': 'Smaller-scale versions of Petra\'s monuments'}
                ],
                'entrance_fees': 'Free admission',
                'opening_hours': '6:00 AM to 6:00 PM (similar to Petra)',
                'best_time': 'Morning or late afternoon for best light and fewer visitors',
                'how_to_get_there': 'Located 8 km north of Petra\'s visitor center. Accessible by car or taxi. Can also hike from Petra (5 km trail).',
                'what_to_wear': 'Comfortable walking shoes, sun protection, layers for temperature changes.',
                'guided_tours': 'Local guides available. Can be visited independently. Often combined with Petra visits.',
                'nearby_attractions': 'Petra (8 km), Al-Beidha Neolithic village (nearby), and Wadi Rum (80 km).',
                'conservation': 'Protected as part of Petra Archaeological Park. Ongoing preservation of the Painted Biclinium frescoes.',
                'visitor_tips': [
                    'Visit before or after Petra to avoid crowds',
                    'Free admission makes it great value',
                    'Allow 1-2 hours for exploration',
                    'Bring flashlight to see Painted Biclinium details',
                    'Less strenuous than Petra but still requires walking',
                    'Can hike to Petra from here via backdoor trail'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'
                ],
                'coordinates': '30.3667° N, 35.4667° E',
                'unesco_status': 'Part of Petra UNESCO World Heritage Site',
                'climate': 'Desert climate similar to Petra'
            },
            'shobak-castle': {
                'id': 'shobak-castle',
                'name': 'Shobak Castle (Montreal)',
                'location': 'Ma\'an Governorate, Jordan',
                'description': 'First Crusader castle in the region, dramatically perched on a conical mountain.',
                'long_description': 'Montreal, known in Arabic as Qal\'at ash-Shawbak, is a Crusader castle built on a conical mountain summit and later expanded by the Mamluks. The castle was built by King Baldwin I in 1115 CE with the dual purpose of extending Frankish settlement east of the Dead Sea and controlling the desert road used by caravans between Syria and Egypt.',
                'historical_significance': 'The first Crusader castle took only eighteen days to build. To commemorate the king\'s personal involvement, it was named "Mont Real" (Mount Royal). The castle was strategically important as it dominated the main passage from Egypt to Syria, allowing control of trade routes and taxation of pilgrims to Mecca and Medina.',
                'architecture': 'The castle solved its water shortage problem through a remarkable tunnel down the hill to two spring-fed cisterns, allowing defenders to retrieve water without exposure to attackers. The most significant Crusader remains include a curtain wall inside later Muslim additions and two chapels.',
                'facts': [
                    'Built by Baldwin I in 1115 CE in just 18 days',
                    'Named Mont Real (Mount Royal) after the king',
                    'First major Crusader fortress in the region',
                    'Besieged by Saladin for almost two years',
                    'Fell to Saladin in May 1189',
                    'Features 350-step tunnel to underground water source',
                    'Decorated with 14th-century Mamluk inscriptions'
                ],
                'key_sites': [
                    {'name': 'Water Tunnel', 'slug': 'water-tunnel', 'description': '350-step tunnel to cisterns', 'significance': 'Ingenious solution to water shortage problem'},
                    {'name': 'Crusader Chapels', 'slug': 'crusader-chapels', 'description': 'Two Christian chapels', 'significance': 'Best-preserved Crusader religious structures'},
                    {'name': 'Curtain Wall', 'slug': 'curtain-wall', 'description': 'Original Crusader defensive wall', 'significance': 'Shows medieval military architecture'},
                    {'name': 'Mamluk Towers', 'slug': 'mamluk-towers', 'description': 'Later Islamic additions with inscriptions', 'significance': '14th-century modifications and decorations'}
                ],
                'entrance_fees': '2 JOD (about $3 USD). Free with Jordan Pass.',
                'opening_hours': 'Summer: 8:00 AM to 6:00 PM; Winter: 8:00 AM to 4:00 PM',
                'best_time': 'Spring and fall for moderate temperatures',
                'how_to_get_there': 'Located 30 km north of Petra on the King\'s Highway. About 180 km south of Amman.',
                'what_to_wear': 'Sturdy shoes for exploring ruins and tunnel. Flashlight helpful for dark areas.',
                'health_safety': 'Tunnel descent is steep and can be slippery. Not suitable for those with mobility issues.',
                'guided_tours': 'Local guides available at entrance. Site can be explored independently.',
                'nearby_attractions': 'Petra (30 km), Dana Biosphere Reserve (30 km), and Wadi Musa.',
                'conservation': 'Ongoing preservation work. Site less visited than other castles, maintaining authentic atmosphere.',
                'visitor_tips': [
                    'Bring flashlight for exploring the water tunnel',
                    'Allow 1.5-2 hours for full exploration',
                    'Less crowded than Karak Castle',
                    'Combine with Dana Reserve or Petra visit',
                    'Stunning views from the ramparts',
                    'The tunnel descent is steep - wear good shoes'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '30.5333° N, 35.5667° E',
                'climate': 'Mediterranean climate with cooler temperatures at altitude'
            },
            'pella': {
                'id': 'pella',
                'name': 'Pella (Tabaqat Fahl)',
                'location': 'Irbid Governorate, Jordan',
                'description': 'Ancient Decapolis city with 8,000 years of continuous human occupation.',
                'long_description': 'Pella was an ancient city in northwest Jordan containing ruins from the Neolithic, Chalcolithic, Bronze Age, Iron Age, Canaanite, Hellenistic, and Islamic periods. Located near a rich water source in the Jordan Valley, the site has been continuously occupied for over 8,000 years, making it one of the oldest and most archaeologically significant sites in the Middle East.',
                'historical_significance': 'Over 45 years of excavations by the University of Sydney have unearthed Neolithic housing (ca. 6000 BCE), Early Bronze Age defensive platforms (ca. 3200 BCE), massive Middle Bronze Age city walls (ca. 1800 BCE), Late Bronze Age Egyptian governors\' residence with clay tablets (ca. 1350 BCE), and large areas of a Hellenistic city. In 2010, a city wall dating to 3400-3600 BCE was discovered.',
                'facts': [
                    'Over 8,000 years of continuous human occupation',
                    'Member of the Decapolis league of cities',
                    'Excavations reveal settlements from 6000 BCE',
                    'City walls discovered from 3600 BCE',
                    'Late Bronze Age Egyptian governors\' residence found',
                    'Rich water source in the Jordan Valley',
                    'Strategic location in fertile valley'
                ],
                'key_sites': [
                    {'name': 'Tell al-Husn', 'slug': 'tell-al-husn', 'description': 'Main archaeological mound with Byzantine fort', 'significance': 'Overlooks site with remains from multiple periods'},
                    {'name': 'Roman Civic Complex', 'slug': 'roman-civic-complex', 'description': 'Public buildings and forum area', 'significance': 'Shows city\'s importance in Roman period'},
                    {'name': 'Byzantine Churches', 'slug': 'byzantine-churches', 'description': 'Three excavated church complexes', 'significance': 'Evidence of early Christian community'},
                    {'name': 'Neolithic Settlement', 'slug': 'neolithic-settlement', 'description': 'Earliest housing remains', 'significance': 'Some of oldest permanent structures in region'}
                ],
                'entrance_fees': '3 JOD (about $4 USD). Free with Jordan Pass.',
                'opening_hours': 'Daily 8:00 AM to 5:00 PM',
                'best_time': 'Spring when valley is green and temperatures moderate',
                'how_to_get_there': 'Located 27 km south of the Sea of Galilee, 130 km north of Amman. About 30 km west of Irbid.',
                'what_to_wear': 'Comfortable walking shoes, sun protection. Valley can be hot in summer.',
                'guided_tours': 'Local guides available. Site requires walking across uneven terrain.',
                'nearby_attractions': 'Umm Qais (40 km), Jordan Valley sites, and Beit She\'an in Israel.',
                'conservation': 'Ongoing excavations and preservation. UNESCO tentative list site.',
                'visitor_tips': [
                    'Less visited than other sites - more authentic experience',
                    'Significant archaeological importance despite fewer standing structures',
                    'Best for history enthusiasts interested in ancient civilizations',
                    'Allow 2 hours for exploration',
                    'Combine with Umm Qais or northern Jordan sites',
                    'Fertile valley setting makes it scenic in spring'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '32.4419° N, 35.6117° E',
                'climate': 'Warm Mediterranean climate, can be hot in summer'
            },
            'rainbow-street': {
                'id': 'rainbow-street',
                'name': 'Rainbow Street',
                'location': 'Amman, Jordan',
                'description': 'Vibrant cultural hub in Amman with art galleries, cafes, and traditional Jordanian atmosphere.',
                'long_description': 'Rainbow Street is one of Amman\'s most vibrant and culturally rich streets, located in the heart of the city. This pedestrian-friendly street is lined with art galleries, independent cafes, restaurants, and boutiques. It represents modern Jordanian culture while maintaining traditional charm, making it a favorite gathering spot for locals and tourists alike.',
                'historical_significance': 'Rainbow Street has evolved from a quiet residential area into Amman\'s cultural and social hub. The street and surrounding Jabal Amman neighborhood represent the city\'s transformation while preserving its heritage character.',
                'cultural_impact': 'The street has become a symbol of Amman\'s contemporary urban culture. It showcases Jordan\'s modern creative scene with art galleries, live music venues, and innovative cafes while serving traditional Jordanian coffee and cuisine.',
                'facts': [
                    'Named after the colorful houses along the street',
                    'Center of Amman\'s contemporary cultural scene',
                    'Features mix of Ottoman and modern architecture',
                    'Popular with both locals and tourists',
                    'Home to independent art galleries and shops',
                    'Offers panoramic city views from various points',
                    'Walking street with pedestrian priority'
                ],
                'key_sites': [
                    {'name': 'Books@Cafe', 'slug': 'bookscafe', 'description': 'Popular bookstore cafe', 'significance': 'Cultural gathering spot with terrace views'},
                    {'name': 'Wild Jordan Center', 'slug': 'wild-jordan-center', 'description': 'RSCN cafe and visitor center', 'significance': 'Organic food and nature reserve information'},
                    {'name': 'Paris Circle', 'slug': 'paris-circle', 'description': 'Historic roundabout at street\'s top', 'significance': 'Starting point with city views'},
                    {'name': 'Independent Galleries', 'slug': 'independent-galleries', 'description': 'Art spaces and studios', 'significance': 'Showcase local Jordanian artists'}
                ],
                'entrance_fees': 'Free to walk. Individual cafes and shops have their own pricing.',
                'opening_hours': 'Street accessible 24/7. Most businesses open 9:00 AM to midnight',
                'best_time': 'Late afternoon to evening for atmosphere and cooler temperatures',
                'how_to_get_there': 'Located in Jabal Amman, downtown. Accessible by taxi or walking from downtown Amman.',
                'what_to_wear': 'Casual comfortable clothing. Street is pedestrian-friendly.',
                'guided_tours': 'Walking tours of Amman often include Rainbow Street. Can be explored independently.',
                'nearby_attractions': 'Amman Citadel (1 km), Roman Theatre (1.5 km), Duke\'s Diwan (on street), and Jordan Museum.',
                'visitor_tips': [
                    'Visit in late afternoon or evening for best atmosphere',
                    'Stop at rooftop cafes for sunset city views',
                    'Try traditional Jordanian coffee at local cafes',
                    'Browse local art galleries and craft shops',
                    'Perfect for people watching and experiencing local culture',
                    'Safe and walkable area'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.9539° N, 35.9246° E',
                'climate': 'Mediterranean climate, pleasant most of year'
            }
        },
        'egypt': {
            'pyramids-of-giza': {
                'id': 'pyramids-of-giza',
                'name': 'Pyramids of Giza & Sphinx',
                'location': 'Giza, Egypt',
                'description': 'Ancient architectural marvels and the only surviving Wonder of the Ancient World',
                'long_description': 'The Giza Pyramid Complex, located approximately 9 km west of the Nile River in Giza, Egypt, stands as one of humanity\'s greatest architectural achievements. Part of the UNESCO World Heritage Site "Memphis and its Necropolis," this ancient complex features the iconic Great Pyramid of Khufu, the Pyramid of Khafre, the Pyramid of Menkaure, and the enigmatic Great Sphinx. These monuments were constructed during the Fourth Dynasty of the Old Kingdom (c. 2600-2500 BC) and continue to captivate millions of visitors annually with their precision, scale, and enduring mystery.',
                'historical_significance': 'Built during Egypt\'s Fourth Dynasty Old Kingdom period, the pyramids served as elaborate tombs for pharaohs, designed to house their "ka" (spirit) and provide resources for the afterlife. The Great Pyramid of Khufu was constructed by an estimated workforce of 10,000 skilled laborers over approximately 30 years. Contrary to popular belief, these workers were not slaves but skilled craftsmen and laborers who lived in a workers\' village discovered near the pyramids. The pyramids were built using limestone from the Mokattam Formation and were precisely aligned to cardinal directions, suggesting advanced astronomical knowledge.',
                'cultural_impact': 'UNESCO World Heritage Site since 1979. As the only surviving Wonder of the Ancient World, the Pyramids of Giza attract millions of visitors annually and remain central to Egypt\'s cultural identity and tourism economy. The complex recently underwent a €17 million renovation to enhance visitor facilities and experience.',
                'best_time_to_visit': 'October to April when temperatures are cooler. Early morning visits (6-9 AM) offer the best light for photography and fewer crowds.',
                'how_to_get_there': 'Located 13 km southwest of Cairo city center. Accessible by taxi, Uber, or organized tour buses. The journey from central Cairo takes 30-45 minutes.',
                'entrance_fees': 'General admission approximately 200 EGP (Egyptian Pounds). Additional fees for entering the pyramids. Guided tours range from $50-150 USD.',
                'opening_hours': 'Open daily from 8:00 AM to 5:00 PM (winter) and 7:00 AM to 7:00 PM (summer). Seasonal variations apply.',
                'what_to_wear': 'Light, breathable clothing in summer; layers in winter. Comfortable walking shoes essential. Hat, sunglasses, and sunscreen recommended.',
                'guided_tours': 'Official guides available at entrance. Audio guides offered in multiple languages. Private tours provide deeper historical context and skip-the-line access.',
                'nearby_attractions': 'Grand Egyptian Museum (2 km), Memphis archaeological site, Saqqara Step Pyramid, Solar Boat Museum',
                'facts': [
                    'Only surviving Wonder of the Ancient World',
                    'Great Pyramid was world\'s tallest structure for 3,800 years',
                    'Built by skilled laborers, not slaves as commonly believed',
                    'Workers\' village discovered nearby housed pyramid builders',
                    'Pyramids precisely aligned to cardinal directions',
                    'Construction took approximately 30 years with 10,000 workers',
                    'Great Sphinx is 73 meters long and 20 meters high',
                    'Hosts occasional cultural events including concerts'
                ],
                'visitor_tips': [
                    'Visit early morning to avoid heat and crowds',
                    'Bring plenty of water and stay hydrated',
                    'Negotiate prices for camel rides beforehand',
                    'Beware of unofficial guides and touts',
                    'Allow 3-4 hours for comprehensive exploration',
                    'Consider visiting the Solar Boat Museum',
                    'New visitor center offers amenities and free Wi-Fi'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '29.9792° N, 31.1342° E',
                'unesco_status': 'UNESCO World Heritage Site (Memphis and its Necropolis) since 1979',
                'climate': 'Hot desert climate with very hot summers (40°C+) and mild winters (15-25°C)'
            },
            'grand-egyptian-museum': {
                'id': 'grand-egyptian-museum',
                'name': 'Grand Egyptian Museum',
                'location': 'Giza, Egypt',
                'description': 'World\'s largest museum dedicated to a single civilization',
                'long_description': 'The Grand Egyptian Museum (GEM), located just 2 kilometers from the Giza Pyramid Complex, stands as the world\'s largest archaeological museum dedicated to a single civilization. Designed by Dublin-based Heneghan Peng Architects and shaped like a chamfered triangle aligned with the Great Pyramid of Khufu, the museum houses over 100,000 artifacts spanning from the Predynastic Period to the Greco-Roman era. The building features translucent alabaster stone facades and represents a billion-dollar investment in preserving and showcasing Egypt\'s unparalleled archaeological heritage.',
                'historical_significance': 'First announced in 1992 with construction beginning in 2005, the Grand Egyptian Museum took nearly two decades to complete at a cost of $1 billion. The museum officially opened in 2023, offering partial public access to its treasures. The project represents Egypt\'s commitment to modern museology and cultural preservation, bringing together artifacts previously scattered across multiple facilities. Most notably, it houses the complete 5,398-piece King Tutankhamun collection, many items displayed publicly for the first time.',
                'cultural_impact': 'The Grand Egyptian Museum serves as an international center for museum communication and Egyptology. With 12 galleries arranged chronologically and thematically, the museum offers unprecedented access to Egypt\'s archaeological treasures. Official full opening scheduled for November 1, 2025. The facility includes a children\'s museum, conference center, conservation labs, and training facilities.',
                'best_time_to_visit': 'October to April for pleasant weather. Weekday mornings typically less crowded. Plan for 4-6 hours minimum.',
                'how_to_get_there': 'Located 2 km from Pyramids of Giza. Accessible by taxi, Uber, or organized tours. 20 km from central Cairo (45-minute drive).',
                'entrance_fees': 'Ticket prices vary by section. Full access approximately 500-1000 EGP. Special exhibitions may require additional fees.',
                'opening_hours': 'Daily 9:00 AM to 6:00 PM. Extended hours during peak season. Advance booking recommended.',
                'what_to_wear': 'Comfortable walking shoes for extensive galleries. Casual, modest clothing. Temperature-controlled interior.',
                'guided_tours': 'Professional guides available in multiple languages. Audio guides included with admission. Specialized tours for archaeology enthusiasts.',
                'nearby_attractions': 'Pyramids of Giza (2 km), Solar Boat Museum, Sound and Light Show at Pyramids, Memphis ruins',
                'facts': [
                    'World\'s largest museum dedicated to single civilization',
                    'Houses over 100,000 artifacts',
                    'Complete King Tutankhamun collection (5,398 pieces)',
                    'Construction cost exceeded $1 billion',
                    'Building covers 500,000 square meters',
                    'Facade aligned with Great Pyramid of Khufu',
                    'Features Khufu\'s second restored solar ship',
                    'Includes conservation laboratories and training facilities'
                ],
                'visitor_tips': [
                    'Book tickets online in advance to avoid queues',
                    'Allow minimum 4-6 hours for comprehensive visit',
                    'Start with King Tutankhamun galleries',
                    'Visit children\'s museum if traveling with family',
                    'Photography restrictions apply in certain areas',
                    'Museum restaurant offers Nile views',
                    'Combine visit with Pyramids of Giza for full day experience'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '29.9932° N, 31.1175° E',
                'unesco_status': 'Not a UNESCO site but houses UNESCO-recognized artifacts',
                'climate': 'Hot desert climate. Museum is fully climate-controlled year-round.'
            },
            'valley-of-the-kings': {
                'id': 'valley-of-the-kings',
                'name': 'Valley of the Kings',
                'location': 'Luxor, Egypt',
                'description': 'Ancient necropolis housing tombs of Egyptian pharaohs and nobles',
                'long_description': 'The Valley of the Kings, located on the west bank of the Nile near Luxor, served as Egypt\'s royal burial ground during the New Kingdom period (1539-1075 BC). This remarkable necropolis contains 65 known tombs and chambers carved into limestone cliffs, including the famous tomb of Tutankhamun (KV62) discovered by Howard Carter in 1922. The valley replaced earlier pyramid burials, with rock-cut tombs decorated with religious texts and scenes from Egyptian mythology designed to guide pharaohs through the afterlife.',
                'historical_significance': 'For nearly 500 years, the Valley of the Kings served as the primary burial site for pharaohs, queens, and powerful nobles during Egypt\'s New Kingdom period. The shift from pyramid tombs to hidden rock-cut chambers reflected efforts to prevent tomb robbery. Despite these precautions, most tombs were plundered in antiquity, making the discovery of Tutankhamun\'s nearly intact tomb in 1922 extraordinarily significant. The valley has been a major focus of Egyptological exploration for two centuries, providing invaluable insights into ancient Egyptian funerary practices, religious beliefs, and royal life.',
                'cultural_impact': 'UNESCO World Heritage Site since 1979 as part of "Ancient Thebes with its Necropolis." The valley receives 4,000-5,000 daily visitors and remains an active archaeological site with ongoing discoveries. Only 18 tombs occasionally open to public, with rotation to minimize damage from humidity and carbon dioxide.',
                'best_time_to_visit': 'October to April for cooler temperatures. Visit early morning (6-8 AM) to avoid extreme heat and crowds.',
                'how_to_get_there': 'Located 5 km west of Luxor across the Nile. Accessible by ferry and taxi, organized tours, or private car. Most visitors combine with other West Bank sites.',
                'entrance_fees': 'General admission approximately 240 EGP. Special tombs (including Tutankhamun) require additional tickets. Photography fees apply.',
                'opening_hours': 'Daily 6:00 AM to 5:00 PM (winter), 6:00 AM to 6:00 PM (summer). Last entry one hour before closing.',
                'what_to_wear': 'Light, breathable clothing. Comfortable walking shoes. Hat and sunglasses essential. Modest dress recommended.',
                'guided_tours': 'Highly recommended for historical context. Egyptologist-led tours provide detailed explanations of hieroglyphics and tomb significance.',
                'nearby_attractions': 'Hatshepsut Temple, Valley of the Queens, Tombs of the Nobles, Medinet Habu, Colossi of Memnon, Luxor Temple',
                'facts': [
                    'Contains 65 known tombs and chambers',
                    'Used for royal burials for nearly 500 years (1539-1075 BC)',
                    'Tutankhamun\'s tomb (KV62) discovered in 1922 nearly intact',
                    'UNESCO World Heritage Site since 1979',
                    'Most tombs robbed in antiquity',
                    'Carved over 1,000 feet of limestone and sedimentary rock',
                    'Receives 4,000-5,000 daily visitors',
                    'Only 18 tombs occasionally open to public'
                ],
                'visitor_tips': [
                    'Purchase combination ticket for multiple tombs',
                    'Visit Tutankhamun tomb early as crowds form quickly',
                    'Bring flashlight for darker tomb sections',
                    'Photography prohibited inside tombs (fees at entrance only)',
                    'Stay hydrated - limited shade available',
                    'Hire guide for maximum educational value',
                    'Allow 2-3 hours minimum for visit'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.7402° N, 32.6014° E',
                'unesco_status': 'UNESCO World Heritage Site (Ancient Thebes with its Necropolis) since 1979',
                'climate': 'Hot desert climate. Summer temperatures exceed 40°C. Winter mild (15-25°C).'
            },
            'karnak-temple': {
                'id': 'karnak-temple',
                'name': 'Karnak Temple Complex',
                'location': 'Luxor, Egypt',
                'description': 'Massive ancient temple complex and Egypt\'s second most-visited site',
                'long_description': 'The Karnak Temple Complex, located near Luxor in ancient Thebes, represents one of the largest religious complexes ever constructed. Known in ancient Egyptian as "The Most Select of Places," this vast site covers multiple precincts built over 2,000 years from the Middle Kingdom (c. 2000-1700 BC) through the Ptolemaic period (305-30 BC). The complex reached its zenith during the 18th Dynasty when Thebes became Egypt\'s capital. The magnificent Great Hypostyle Hall alone covers 5,000 square meters with 134 massive columns ranging from 10-21 meters tall, creating a forest of stone that continues to awe visitors.',
                'historical_significance': 'Construction at Karnak spanned over 2,000 years with contributions from approximately 30 pharaohs, making it a living chronicle of ancient Egyptian architectural evolution and religious practices. Dedicated primarily to Amun-Re, chief deity of the Theban Triad, the complex served as the most important religious center in ancient Egypt during the New Kingdom. The site demonstrates remarkable continuity of worship, with the complex later adapted for Coptic Christian use. The scale and ambition of Karnak reflects the power and resources of ancient Egyptian civilization at its height.',
                'cultural_impact': 'UNESCO World Heritage Site since 1979 as part of "Ancient Thebes with its Necropolis." Second most-visited historical site in Egypt after the Giza pyramids. Currently, only the Precinct of Amun-Re is open to the public, featuring an Open Air Museum.',
                'best_time_to_visit': 'October to April for pleasant weather. Late afternoon visits (3-5 PM) offer beautiful golden light. Sound and Light show available evening.',
                'how_to_get_there': 'Located 3 km north of Luxor city center. Easily accessible by taxi, Uber, or short walk from most Luxor hotels.',
                'entrance_fees': 'General admission approximately 200 EGP. Sound and Light show additional 300 EGP. Student discounts available.',
                'opening_hours': 'Daily 6:00 AM to 5:30 PM (winter), 6:00 AM to 6:30 PM (summer). Sound and Light shows at sunset.',
                'what_to_wear': 'Comfortable walking shoes essential. Light, modest clothing. Hat and sunscreen. Layers for evening shows.',
                'guided_tours': 'Highly recommended for understanding complex history. Audio guides available. Specialized Egyptologist tours offer deep insights.',
                'nearby_attractions': 'Luxor Temple (2.7 km via Avenue of Sphinxes), Luxor Museum, Mummification Museum, Valley of the Kings (across Nile)',
                'facts': [
                    'Construction spanned over 2,000 years',
                    'Approximately 30 pharaohs contributed to construction',
                    'Great Hypostyle Hall covers 5,000 square meters',
                    'Contains 134 massive columns (10-21 meters tall)',
                    'Houses one of Egypt\'s largest obelisks (328 tons, 29 meters)',
                    'UNESCO World Heritage Site since 1979',
                    'Second most-visited site in Egypt',
                    'Connected to Luxor Temple via 2.7 km Avenue of Sphinxes'
                ],
                'visitor_tips': [
                    'Visit early morning or late afternoon for best light',
                    'Allow minimum 2-3 hours for exploration',
                    'Combine visit with Luxor Temple via Avenue of Sphinxes',
                    'Attend evening Sound and Light show',
                    'Bring water - limited shade in complex',
                    'Hire qualified Egyptologist guide for rich historical context',
                    'Visit Open Air Museum for impressive artifacts'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.7188° N, 32.6573° E',
                'unesco_status': 'UNESCO World Heritage Site (Ancient Thebes with its Necropolis) since 1979',
                'climate': 'Hot desert climate. Summer extremely hot (40°C+). Winter pleasant (15-25°C).'
            },
            'luxor-temple': {
                'id': 'luxor-temple',
                'name': 'Luxor Temple',
                'location': 'Luxor, Egypt',
                'description': 'Ancient temple dedicated to kingship rejuvenation on Nile\'s east bank',
                'long_description': 'Luxor Temple, known in ancient Egyptian as "ipet resyt" (the southern sanctuary), stands majestically on the east bank of the Nile River in the heart of modern Luxor. Constructed around 1400 BCE using Nubian sandstone from Gebel el-Silsila, this architectural masterpiece was dedicated not to a specific cult god but to the rejuvenation of kingship. The temple features unique architectural illusions, grand colonnades, and multiple courtyards. Two original obelisks graced the entrance, though one now stands in Paris\'s Place de la Concorde. The temple represents over 3,400 years of continuous religious worship.',
                'historical_significance': 'Built primarily by Amenhotep III around 1400 BCE and later expanded by Tutankhamun and Ramesses II, Luxor Temple served as the focal point of the annual Opet Festival, celebrating the rejuvenation of the pharaoh\'s divine power. The temple was associated with the Theban Triad (Amun, Mut, and Khonsu) and potentially served as the symbolic coronation site for pharaohs. The complex experienced remarkable continuity through history - converted into a Roman legionary fortress, then later housing an active mosque (Abu Haggag Mosque) still functioning today within the ancient walls.',
                'cultural_impact': 'UNESCO World Heritage Site since 1979 as part of "Ancient Thebes with its Necropolis." Connected to Karnak Temple by the recently restored 2.7 km Avenue of Sphinxes, creating a monumental processional route. Extensive excavation beginning in 1884 revealed extraordinary preservation.',
                'best_time_to_visit': 'October to April for comfortable weather. Evening visits stunning when temple illuminated. Avoid midday summer heat.',
                'how_to_get_there': 'Located in central Luxor city on the Corniche. Walking distance from most Luxor hotels. 2.7 km south of Karnak Temple.',
                'entrance_fees': 'General admission approximately 160 EGP. Photography fees may apply. Combination tickets with other Luxor sites available.',
                'opening_hours': 'Daily 6:00 AM to 9:00 PM. Extended evening hours allow atmospheric illuminated visits.',
                'what_to_wear': 'Modest, comfortable clothing. Walking shoes recommended. Evening visits may require light jacket in winter.',
                'guided_tours': 'Professional guides offer insights into architectural illusions and hieroglyphic meanings. Audio guides available in multiple languages.',
                'nearby_attractions': 'Karnak Temple (2.7 km), Luxor Museum, Avenue of Sphinxes, Mummification Museum, Winter Palace Hotel',
                'facts': [
                    'Built around 1400 BCE using Nubian sandstone',
                    'Dedicated to kingship rejuvenation, not specific deity',
                    'One original obelisk now in Paris (Place de la Concorde)',
                    'Connected to Karnak via 2.7 km Avenue of Sphinxes',
                    'Contains functioning mosque (Abu Haggag) within ancient walls',
                    'Represents 3,400+ years continuous religious worship',
                    'UNESCO World Heritage Site since 1979',
                    'Features unique architectural "illusionism" techniques'
                ],
                'visitor_tips': [
                    'Visit at sunset for spectacular illumination',
                    'Walk Avenue of Sphinxes to/from Karnak Temple',
                    'Allow 1.5-2 hours for thorough exploration',
                    'Evening visits cooler and beautifully lit',
                    'Respect active Abu Haggag Mosque within complex',
                    'Photography excellent in golden hour',
                    'Combine with Luxor Museum visit'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.6990° N, 32.6390° E',
                'unesco_status': 'UNESCO World Heritage Site (Ancient Thebes with its Necropolis) since 1979',
                'climate': 'Hot desert climate. Summer very hot (40°C+). Winter mild and pleasant (15-25°C).'
            },
            'abu-simbel': {
                'id': 'abu-simbel',
                'name': 'Abu Simbel Temples',
                'location': 'Aswan Governorate, Egypt',
                'description': 'Colossal rock-cut temples relocated to save them from flooding',
                'long_description': 'The Abu Simbel Temples, located near Egypt\'s border with Sudan in Aswan Governorate, represent one of ancient Egypt\'s most spectacular monuments and modern archaeology\'s greatest rescue operations. Built by Ramesses II around 1264 BC, these two massive rock-cut temples were carved directly into a mountainside. The Great Temple features four colossal 20-meter statues of Ramesses II guarding the entrance, while the Small Temple honors Queen Nefertari and the goddess Hathor. In an unprecedented engineering feat, the entire complex was relocated in 1968, cut into 1,036 blocks and reassembled 208 meters inland to prevent submersion by Lake Nasser.',
                'historical_significance': 'Commissioned by Ramesses II during the 13th century BC, the Great Temple was dedicated to the gods Ra-Horakhty, Ptah, Amun, and the deified Ramesses himself. The temples feature intricate bas-reliefs depicting Ramesses II\'s military campaigns, particularly the Battle of Kadesh. The Small Temple is remarkable for depicting Queen Nefertari with statues equal in size to the pharaoh, extremely rare in Egyptian history. The temples demonstrate the pinnacle of New Kingdom architectural ambition and the pharaoh\'s determination to assert Egyptian power in Nubia.',
                'cultural_impact': 'UNESCO World Heritage Site. The 1960s relocation involved a $41.7 million international UNESCO campaign funded by 48 countries, representing one of archaeology\'s greatest achievements. The temples feature remarkable solar alignment - twice yearly, sunlight penetrates the inner sanctuary to illuminate specific statues.',
                'best_time_to_visit': 'October to April for moderate temperatures. February 22 and October 22 for solar alignment phenomenon (sun festival).',
                'how_to_get_there': 'Located 280 km south of Aswan. Accessible by 3-hour bus/car journey, domestic flights to Abu Simbel Airport, or Lake Nasser cruise.',
                'entrance_fees': 'General admission approximately 240 EGP. Sound and Light show additional fee. Early morning flights from Aswan often include entrance.',
                'opening_hours': 'Daily 5:00 AM to 6:00 PM. Sound and Light shows evening (weather permitting).',
                'what_to_wear': 'Light, breathable clothing. Comfortable walking shoes. Sun protection essential. Early morning visits may require light jacket.',
                'guided_tours': 'Organized day trips from Aswan include transport, guide, and entrance fees. Egyptologist guides enhance understanding of relocation and history.',
                'nearby_attractions': 'Lake Nasser, Nubian villages, Aswan High Dam, Kalabsha Temple (on Lake Nasser), Sudan border region',
                'facts': [
                    'Built by Ramesses II around 1264 BC',
                    'Four colossal 20-meter statues guard Great Temple entrance',
                    'Relocated in 1968 using 1,036 individual blocks',
                    'Moved 208 meters inland to prevent Lake Nasser flooding',
                    'Relocation cost $41.7 million funded by 48 countries',
                    'Solar alignment illuminates inner sanctuary twice yearly',
                    'Small Temple rare example of queen equal-sized to pharaoh',
                    'UNESCO World Heritage Site'
                ],
                'visitor_tips': [
                    'Book early morning flight from Aswan for day trip',
                    'Visit during sun festival (Feb 22, Oct 22) for solar alignment',
                    'Allow 2-3 hours for both temples',
                    'Bring water and snacks - limited facilities',
                    'Photography allowed but tripods prohibited',
                    'Sound and Light show worth attending',
                    'Consider Lake Nasser cruise for leisurely visit'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '22.3372° N, 31.6258° E',
                'unesco_status': 'UNESCO World Heritage Site (Nubian Monuments from Abu Simbel to Philae)',
                'climate': 'Hot desert climate. Extremely hot summers (45°C+). Mild winters (15-25°C).'
            },
            'philae-temple': {
                'id': 'philae-temple',
                'name': 'Philae Temple',
                'location': 'Aswan, Egypt',
                'description': 'Sacred island temple complex dedicated to goddess Isis, relocated to Agilkia Island',
                'long_description': 'The Philae Temple Complex, originally located on Philae Island near the First Cataract of the Nile, served as one of ancient Egypt\'s most sacred sites dedicated to the goddess Isis. This remarkable complex existed from the 7th/6th century BC to the 6th century AD, functioning as an important religious and cultural center for Egyptians, Nubians, and Mediterranean pilgrims. The temples feature stunning Ptolemaic and Roman-era architecture with intricate hieroglyphic reliefs. Threatened by flooding from both the Aswan Low Dam and High Dam, UNESCO orchestrated a heroic rescue operation between 1977-1980, carefully dismantling 40,000 individual pieces and reconstructing the entire complex on nearby Agilkia Island.',
                'historical_significance': 'Philae\'s oldest known structure dates to the reign of Pharaoh Taharqa (7th century BC), though most surviving buildings were constructed during the Ptolemaic and Roman periods. The temple served as one of the last strongholds of ancient Egyptian religion, with the last known hieroglyphic inscription dated 394 AD carved here. The complex functioned as a pagan religious site until officially closed in 537 AD by Byzantine emperor Justinian I, after which it transitioned to Christian use. This long history represents over 1,200 years of continuous religious worship.',
                'cultural_impact': 'UNESCO World Heritage Site since 1979 as part of "Nubian Monuments from Abu Simbel to Philae." The temple\'s successful relocation set precedent for preserving endangered archaeological sites worldwide. Evening Sound and Light shows illuminate the complex\'s history.',
                'best_time_to_visit': 'October to April for pleasant weather. Evening Sound and Light shows particularly atmospheric. Avoid summer heat.',
                'how_to_get_there': 'Located 12 km south of Aswan. Accessible only by motorboat from Shellal marina. Most visitors join organized tours from Aswan.',
                'entrance_fees': 'General admission approximately 140 EGP. Boat transfer additional 30-50 EGP. Sound and Light show extra fee.',
                'opening_hours': 'Daily 7:00 AM to 5:00 PM (winter), 7:00 AM to 6:00 PM (summer). Sound and Light shows at sunset.',
                'what_to_wear': 'Comfortable walking shoes for island exploration. Modest clothing. Sun protection. Light layers for boat ride.',
                'guided_tours': 'Organized tours from Aswan include boat transfer and guided tour. Audio guides available. Egyptologist tours offer deeper historical context.',
                'nearby_attractions': 'Aswan High Dam, Unfinished Obelisk, Nubian villages, Elephantine Island, Aswan Museum, Abu Simbel Temples',
                'facts': [
                    'Dedicated primarily to goddess Isis',
                    'Existed from 7th/6th century BC to 6th century AD',
                    'Last known hieroglyphic inscription (394 AD) carved here',
                    'Relocated 1977-1980 using 40,000 individual pieces',
                    'Moved from Philae Island to Agilkia Island',
                    'Closed as pagan site in 537 AD by Justinian I',
                    'UNESCO World Heritage Site since 1979',
                    'Accessible only by boat from mainland'
                ],
                'visitor_tips': [
                    'Combine visit with Aswan High Dam and Unfinished Obelisk',
                    'Attend evening Sound and Light show',
                    'Negotiate boat fare before departure',
                    'Allow 2-3 hours for island exploration',
                    'Bring water - limited facilities on island',
                    'Morning visits offer better photography light',
                    'Wear comfortable shoes for temple walkways'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '24.0207° N, 32.8845° E',
                'unesco_status': 'UNESCO World Heritage Site (Nubian Monuments from Abu Simbel to Philae) since 1979',
                'climate': 'Hot desert climate. Very hot summers (40°C+). Mild, pleasant winters (15-25°C).'
            },
            'egyptian-museum': {
                'id': 'egyptian-museum',
                'name': 'Egyptian Museum Cairo',
                'location': 'Cairo, Egypt',
                'description': 'World\'s largest collection of Egyptian antiquities in iconic Tahrir Square building',
                'long_description': 'The Egyptian Museum, located in Cairo\'s historic Tahrir Square, houses the world\'s largest collection of Egyptian antiquities with over 120,000 items spanning prehistoric to Roman periods. Established in 1835 and housed in its current iconic building since 1902, this pink neoclassical palace designed by French architect Marcel Dourgnon has served as the primary repository of Egypt\'s archaeological treasures for over a century. The museum\'s most famous collection is the treasure of Tutankhamun, including his iconic gold burial mask, alongside countless mummies, statues, jewelry, and artifacts that chronicle ancient Egyptian civilization.',
                'historical_significance': 'The Egyptian Museum represents the world\'s first national museum dedicated to a single civilization. Founded in 1835, it moved through several locations before settling in its current purpose-built structure in 1902. The museum has witnessed Egypt\'s modern history, including damage during the 2011 Revolution when looters stole and damaged artifacts. In 2021, 22 royal mummies were transferred in a spectacular "Pharaohs\' Golden Parade" to the new National Museum of Egyptian Civilization, marking the beginning of a transition as some collections move to the new Grand Egyptian Museum.',
                'cultural_impact': 'Considered Africa\'s largest museum and one of the world\'s most important Egyptological institutions. Contains invaluable research materials and a library with over 50,000 volumes on Egyptian antiquities. The museum underwent major renovations in 2016 to improve facilities and conservation.',
                'best_time_to_visit': 'October to April for pleasant weather. Weekday mornings (9-11 AM) typically less crowded. Allow 3-4 hours minimum.',
                'how_to_get_there': 'Located at Tahrir Square in central Cairo. Accessible by Cairo Metro (Sadat Station), taxi, or Uber. Walking distance from Nile Corniche hotels.',
                'entrance_fees': 'General admission approximately 200 EGP. Additional fee for Royal Mummy Room. Photography fees 50 EGP. Student discounts available.',
                'opening_hours': 'Daily 9:00 AM to 7:00 PM. Extended hours during peak season. Closed on major holidays.',
                'what_to_wear': 'Comfortable walking shoes essential. Modest, casual clothing. Museum is climate-controlled but can be warm.',
                'guided_tours': 'Professional Egyptologist guides highly recommended. Audio guides available in multiple languages. Specialized tours for specific collections offered.',
                'nearby_attractions': 'Tahrir Square, Nile River Corniche, Cairo Tower, Downtown Cairo, Khan el-Khalili Bazaar (4 km), Islamic Cairo',
                'facts': [
                    'Houses over 120,000 Egyptian antiquities',
                    'Established in 1835, current building opened 1902',
                    'Contains Tutankhamun\'s gold burial mask',
                    'Designed by French architect Marcel Dourgnon',
                    'Library holds over 50,000 volumes',
                    'Considered Africa\'s largest museum',
                    'Experienced artifact damage during 2011 Revolution',
                    '22 royal mummies transferred to new museum in 2021'
                ],
                'visitor_tips': [
                    'Visit early to avoid crowds, especially for Tutankhamun galleries',
                    'Hire Egyptologist guide for maximum educational value',
                    'Allow minimum 3-4 hours for comprehensive visit',
                    'Pay extra for Royal Mummy Room - worth it',
                    'Photography allowed in most areas (50 EGP fee)',
                    'Museum shop offers quality replicas and books',
                    'Combine with Tahrir Square and downtown Cairo exploration'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '30.0478° N, 31.2336° E',
                'unesco_status': 'Not a UNESCO site but houses UNESCO-recognized artifacts',
                'climate': 'Hot desert climate. Museum climate-controlled year-round. Visit October-April for pleasant outdoor weather.'
            },
            'islamic-cairo': {
                'id': 'islamic-cairo',
                'name': 'Islamic Cairo',
                'location': 'Cairo, Egypt',
                'description': 'Historic medieval district with hundreds of mosques, markets, and Islamic monuments',
                'long_description': 'Islamic Cairo, founded in 969 CE by the Fatimid Caliphate, encompasses one of the world\'s oldest and most concentrated collections of Islamic architecture and monuments. This historic district served as Egypt\'s royal city and administrative capital through multiple ruling dynasties including the Fatimids, Ayyubids, Mamluks, Ottomans, and Muhammad Ali\'s dynasty. The area features hundreds of historic mosques, madrasas, mausoleums, gates, walls, and the famous Khan el-Khalili bazaar. Notable landmarks include Al-Azhar Mosque, Ibn Tulun Mosque, the Citadel, and the vibrant Al-Mu\'izz Street, creating a living museum of Islamic civilization spanning over a millennium.',
                'historical_significance': 'Islamic Cairo represents over 1,000 years of continuous Islamic civilization and architectural evolution. Founded as Al-Qahira (The Victorious) by the Fatimids, the district became the political and cultural heart of medieval Islamic Egypt. The area preserves extraordinary examples of Fatimid, Ayyubid, Mamluk, and Ottoman architecture. Al-Azhar Mosque, founded in 970 CE, became one of Islam\'s oldest universities and remains a premier center of Islamic learning. The historic street Al-Mu\'izz li-Din Allah contains the greatest concentration of medieval architectural treasures in the Islamic world.',
                'cultural_impact': 'UNESCO World Heritage Site since 1979, recognized as "one of the world\'s oldest Islamic cities" covering 523.66 hectares. The area suffers from neglect and decay but ongoing restoration efforts by government and international organizations work to preserve this irreplaceable heritage. Khan el-Khalili bazaar remains a vibrant commercial center.',
                'best_time_to_visit': 'October to April for comfortable weather. Early morning or late afternoon for exploring markets. Friday mornings busy with prayers.',
                'how_to_get_there': 'Central Cairo location accessible by taxi, Uber, or Cairo Metro. Walking distance from Downtown Cairo. Many hotels in proximity.',
                'entrance_fees': 'Individual monuments charge separate fees (typically 60-100 EGP each). Combination tickets available. Bazaar free to explore.',
                'opening_hours': 'Varies by site. Mosques generally 9:00 AM to 5:00 PM (closed during prayers). Bazaar opens morning to late evening.',
                'what_to_wear': 'Modest clothing essential. Women should cover shoulders and knees. Headscarf recommended for mosque visits. Comfortable walking shoes.',
                'guided_tours': 'Professional guides recommended for navigating complex history and architecture. Walking tours of Al-Mu\'izz Street popular. Specialized Islamic architecture tours available.',
                'nearby_attractions': 'Khan el-Khalili Bazaar, Al-Azhar Mosque, Citadel of Cairo, Ibn Tulun Mosque, Egyptian Museum (4 km), Nile River',
                'facts': [
                    'Founded in 969 CE by Fatimid Caliphate',
                    'UNESCO World Heritage Site since 1979',
                    'Covers 523.66 hectares',
                    'Al-Azhar University founded 970 CE (oldest in Islam)',
                    'Al-Mu\'izz Street: greatest concentration of medieval Islamic monuments',
                    'Includes hundreds of historic mosques and monuments',
                    'Spans Fatimid, Ayyubid, Mamluk, Ottoman periods',
                    'Khan el-Khalili bazaar dates to 14th century'
                ],
                'visitor_tips': [
                    'Hire knowledgeable guide for historical context',
                    'Start early to avoid heat and crowds',
                    'Allow full day for comprehensive exploration',
                    'Dress modestly - required for mosque entry',
                    'Bargain in Khan el-Khalili bazaar (start at 50% asking price)',
                    'Visit Al-Mu\'izz Street pedestrian area',
                    'Try traditional Egyptian coffee at historic cafes'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '30.0489° N, 31.2622° E',
                'unesco_status': 'UNESCO World Heritage Site (Historic Cairo) since 1979',
                'climate': 'Hot desert climate. Very hot summers (35-40°C). Mild winters (15-25°C). Best October-April.'
            },
            'muhammad-ali-mosque': {
                'id': 'muhammad-ali-mosque',
                'name': 'Muhammad Ali Mosque',
                'location': 'Cairo, Egypt',
                'description': 'Ottoman-style alabaster mosque crowning Cairo\'s historic Citadel',
                'long_description': 'The Muhammad Ali Mosque, also known as the Alabaster Mosque, dominates Cairo\'s skyline from its commanding position within the Cairo Citadel. Commissioned by Muhammad Ali Pasha, an Ottoman governor who modernized Egypt, construction began in 1830 and was completed in 1857. This magnificent Ottoman-style mosque, designed with European influences, features extensive alabaster facing that gives it its nickname. The mosque showcases a central dome 21 meters in diameter reaching 52 meters high, flanked by two soaring 82-meter cylindrical minarets. The rectangular courtyard measures 55 by 57 meters, and the mosque can accommodate approximately 10,000 worshippers.',
                'historical_significance': 'Muhammad Ali Pasha commissioned this mosque to symbolize his break from Istanbul and establish his dynasty\'s legitimacy. The design intentionally departed from traditional Cairene architectural styles, instead drawing inspiration from Istanbul\'s Blue Mosque and Hagia Sophia. This represented Muhammad Ali\'s modernization efforts and political independence from the Ottoman capital. The mosque contains Muhammad Ali\'s tomb in the western corner of the prayer hall. A monumental clock tower, gifted by French King Louis Philippe in exchange for the Luxor Obelisk, stands in the courtyard though it never functioned properly.',
                'cultural_impact': 'One of Cairo\'s most prominent landmarks, visible across the city. Represents a radical architectural departure from traditional Islamic Cairo. The mosque symbolizes 19th-century Egypt\'s cultural and political transformations under Muhammad Ali\'s modernizing rule.',
                'best_time_to_visit': 'October to April for pleasant weather. Early morning or late afternoon for best light. Sunset views of Cairo spectacular.',
                'how_to_get_there': 'Located within Cairo Citadel in southern Cairo. Accessible by taxi or Uber. 15-20 minutes from Downtown Cairo.',
                'entrance_fees': 'Citadel entrance approximately 200 EGP (includes mosque and other Citadel sites). Photography permitted.',
                'opening_hours': 'Daily 8:00 AM to 5:00 PM. Closed to tourists during prayer times (approximately 15 minutes five times daily).',
                'what_to_wear': 'Modest clothing required. Women must cover hair, shoulders, and knees. Headscarves provided if needed. Remove shoes before entering.',
                'guided_tours': 'Included in most Citadel tours. Audio guides available. Egyptologist tours provide historical and architectural context.',
                'nearby_attractions': 'Cairo Citadel, Sultan Hassan Mosque, Al-Rifai Mosque, Islamic Cairo, Ibn Tulun Mosque, Gayer-Anderson Museum',
                'facts': [
                    'Commissioned by Muhammad Ali Pasha in 1830',
                    'Completed in 1857 after 27 years construction',
                    'Known as "Alabaster Mosque" for extensive alabaster facing',
                    'Central dome 21 meters diameter, 52 meters high',
                    'Two 82-meter tall minarets',
                    'Capacity approximately 10,000 people',
                    'Contains Muhammad Ali\'s tomb',
                    'French clock tower gift never functioned properly'
                ],
                'visitor_tips': [
                    'Visit in morning for fewer crowds',
                    'Combine with other Citadel attractions',
                    'Panoramic Cairo views from Citadel walls',
                    'Respect prayer times - mosque temporarily closes',
                    'Photography allowed inside with restrictions',
                    'Shoes removed and stored at entrance',
                    'Allow 45-60 minutes for mosque visit'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '30.0288° N, 31.2602° E',
                'unesco_status': 'Part of Historic Cairo UNESCO World Heritage Site',
                'climate': 'Hot desert climate. Very hot summers (35-40°C). Mild winters (15-25°C). Best October-April.'
            },
            'hurghada': {
                'id': 'hurghada',
                'name': 'Hurghada',
                'location': 'Red Sea, Egypt',
                'description': 'Premier Red Sea resort destination famous for diving, beaches, and watersports',
                'long_description': 'Hurghada, the capital of Egypt\'s Red Sea Governorate, has transformed from a small fishing village founded in 1905 into one of the world\'s premier resort destinations. This coastal city extends approximately 36 kilometers along the Red Sea coast and attracts over 1 million visitors annually. Known for crystal-clear waters, vibrant coral reefs, diverse marine life, and year-round warm climate, Hurghada offers world-class diving, snorkeling, windsurfing, and kitesurfing. The city features numerous beach resorts, the Hurghada Grand Aquarium, Hurghada Museum, and serves as a gateway for day trips to Luxor and Cairo.',
                'historical_significance': 'While Hurghada itself is relatively modern (founded 1905), the region has ancient roots with Roman settlements nearby dating to the 4th century. The city\'s rapid transformation began in the 1980s when it emerged as Egypt\'s primary Red Sea resort destination. Hurghada\'s development represents Egypt\'s modern tourism industry evolution, with the city becoming home to a large Russian expatriate community and international resort infrastructure. The Hurghada Museum, opened recently, showcases artifacts from across Egyptian history.',
                'cultural_impact': 'Hurghada serves as Egypt\'s primary Red Sea resort, attracting over 1 million annual visitors. The city is served by Hurghada International Airport, Egypt\'s second-busiest airport. Hurghada has become a major center for Red Sea diving tourism and marine conservation efforts.',
                'best_time_to_visit': 'September to November and March to May for ideal weather. Year-round diving possible. Summer (June-August) very hot but water activities remain popular.',
                'how_to_get_there': 'Hurghada International Airport receives international and domestic flights. 450 km from Cairo (5-hour drive). Regular bus services from Cairo and Luxor.',
                'entrance_fees': 'City access free. Individual attractions charge separate fees: Hurghada Grand Aquarium (approximately 200 EGP), Hurghada Museum (100 EGP).',
                'opening_hours': 'City operates 24/7. Museums and aquarium typically 9:00 AM to 5:00 PM. Dive centers operate dawn to dusk.',
                'what_to_wear': 'Beach and resort casual. Swimwear for beaches and pools. Modest clothing for venturing into town. Sun protection essential.',
                'guided_tours': 'Numerous diving centers offer PADI courses and guided dives. Day trips to Luxor, Cairo, and Giftun Islands widely available. Desert safari tours popular.',
                'nearby_attractions': 'Giftun Islands, Mahmya Island, Makadi Bay, Sahl Hasheesh, El Gouna, Luxor (300 km), Cairo (450 km)',
                'facts': [
                    'Founded in 1905 as fishing village',
                    'Over 1 million annual visitors',
                    'Extends 36 kilometers along Red Sea coast',
                    'Second busiest airport in Egypt',
                    'Average annual sea temperature 24°C',
                    'Population 214,247 (2023)',
                    'Large Russian expatriate community',
                    'Major center for Red Sea diving tourism'
                ],
                'visitor_tips': [
                    'Book diving trips through reputable PADI-certified centers',
                    'Giftun Islands day trips excellent for snorkeling',
                    'Negotiate prices for watersports and excursions',
                    'Many resorts offer all-inclusive packages',
                    'Visit Hurghada Grand Aquarium on hot days',
                    'Day trips to Luxor best booked through hotel',
                    'Stay hydrated in summer heat'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1583037189850-1921ae7c6c22?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1559827260-dc66d52bef19?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1559827260-dc66d52bef19?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '27.2579° N, 33.8116° E',
                'unesco_status': 'Not a UNESCO site but gateway to marine protected areas',
                'climate': 'Subtropical desert climate. Very hot summers (up to 46°C). Mild winters. Average sea temperature 24°C year-round.'
            },
            'sharm-el-sheikh': {
                'id': 'sharm-el-sheikh',
                'name': 'Sharm El-Sheikh',
                'location': 'Sinai Peninsula, Egypt',
                'description': 'World-class diving resort at Sinai\'s southern tip, the "City of Peace"',
                'long_description': 'Sharm El-Sheikh, located on the southern tip of Egypt\'s Sinai Peninsula along the Red Sea coast, has evolved from a small fishing village and military base into one of the world\'s premier resort destinations. Developed initially by Israel beginning in 1968 and returned to Egypt in 1982 following the Camp David Accords, the city is nicknamed the "City of Peace" for hosting numerous international peace conferences. Home to 91 resorts, Sharm El-Sheikh is renowned for year-round dry climate, crystal-clear calm waters, exceptional scuba diving and snorkeling around Ras Muhammad National Park, with 250 types of coral reefs and 1,000 fish species.',
                'historical_significance': 'Originally a small fishing village and military base, Sharm El-Sheikh\'s modern development began in 1968 during Israeli occupation. The city was returned to Egypt in 1982 under the Camp David Accords and has since grown into Egypt\'s premier Sinai resort. The nickname "City of Peace" reflects its role hosting international conferences including Middle East peace summits. In 2022, Sharm El-Sheikh hosted the COP27 climate conference, demonstrating its evolution into an international diplomatic venue alongside its tourism role.',
                'cultural_impact': 'Major international resort destination with world-class diving facilities. Hosted COP27 climate conference in 2022. Ras Muhammad National Park (established 1983) protects unique marine ecosystems. Sharm El-Sheikh serves as a model for sustainable Red Sea tourism development.',
                'best_time_to_visit': 'September to November and March to May for ideal conditions. Year-round diving excellent. Winter (December-February) mild and pleasant.',
                'how_to_get_there': 'Sharm El-Sheikh International Airport receives international and domestic flights. Regular coach services from Cairo (6-7 hours). Marina accommodates cruise ships and private yachts.',
                'entrance_fees': 'City access free. Ras Muhammad National Park entrance approximately 100 EGP. Individual dive trips and excursions priced separately.',
                'opening_hours': 'City operates 24/7. Ras Muhammad National Park 8:00 AM to 5:00 PM. Dive centers operate dawn to dusk.',
                'what_to_wear': 'Beach resort casual. Swimwear for beaches and watersports. Modest clothing for town areas. Sun protection essential year-round.',
                'guided_tours': 'Numerous PADI diving centers offer courses and guided dives. Desert safari tours, Mount Sinai sunrise treks, St. Catherine\'s Monastery visits popular.',
                'nearby_attractions': 'Ras Muhammad National Park, Naama Bay, Shark Reef, Yolanda Reef, Mount Sinai, St. Catherine\'s Monastery, Dahab (90 km)',
                'facts': [
                    'Located at southern tip of Sinai Peninsula',
                    'Nicknamed "City of Peace" for hosting peace conferences',
                    'Home to 91 resorts (as of 2000)',
                    'Red Sea temperatures 21-28°C year-round',
                    '250 coral reef types, 1,000 fish species',
                    'Ras Muhammad National Park established 1983',
                    'Hosted COP27 climate conference 2022',
                    'Returned to Egypt 1982 after Camp David Accords'
                ],
                'visitor_tips': [
                    'Book diving trips through reputable PADI centers',
                    'Visit Ras Muhammad National Park for best diving',
                    'Naama Bay offers restaurants and nightlife',
                    'Mount Sinai sunrise trek unforgettable experience',
                    'All-inclusive resorts offer excellent value',
                    'Respect marine life - no touching coral',
                    'Airport transfers typically included in resort packages'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1583037189850-1921ae7c6c22?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1559827260-dc66d52bef19?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1559827260-dc66d52bef19?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '27.9158° N, 34.3300° E',
                'unesco_status': 'Ras Muhammad National Park (nearby) internationally protected marine area',
                'climate': 'Subtropical arid climate. Temperatures 18-23°C (January) to 33-37°C (August). Very low precipitation.'
            },
            'bibliotheca-alexandrina': {
                'id': 'bibliotheca-alexandrina',
                'name': 'Bibliotheca Alexandrina',
                'location': 'Alexandria, Egypt',
                'description': 'Modern revival of the ancient Library of Alexandria, major cultural center',
                'long_description': 'The Bibliotheca Alexandrina, officially inaugurated on October 16, 2002, commemorates and revives the legendary ancient Library of Alexandria on the Mediterranean Sea coastline. Designed by Norwegian architectural firm Snøhetta (selected from 524 international competition entries), this US$220 million cultural complex features a distinctive tilted cylindrical form with a 32-meter-high glass-paneled roof resembling a sundial. The main reading room spans 20,000 square meters with shelf space for 8 million books. The complex includes specialized libraries, four museums, four art galleries, 15 permanent exhibitions, a planetarium, conference center, and manuscript restoration laboratory.',
                'historical_significance': 'The Bibliotheca Alexandrina represents Egypt and UNESCO\'s effort to revive the spirit of the ancient Library of Alexandria, one of antiquity\'s greatest centers of learning destroyed centuries ago. The modern library received a 500,000-book donation from France\'s Bibliothèque nationale in 2009 and a $5 million donation plus 10 billion archived web pages from the Internet Archive. During Egypt\'s 2011 Revolution, the library was protected by citizens forming human chains, demonstrating its cultural importance. The library houses collections in classical Arabic, English, and French, plus the Nobel Prize Laureates in Literature collection.',
                'cultural_impact': 'Major cultural and educational landmark for Egypt and the Mediterranean region. Houses extensive digital archives and serves as regional hub for Internet Archive. The library survived and was protected during 2011 Revolution. Serves as international conference center and educational institution.',
                'best_time_to_visit': 'October to April for pleasant Mediterranean weather. Library less crowded weekday mornings. Allow 3-4 hours for comprehensive visit.',
                'how_to_get_there': 'Located in Alexandria\'s Eastern Harbor area. Accessible by taxi, tram, or bus from central Alexandria. 220 km from Cairo (3-hour drive).',
                'entrance_fees': 'General admission approximately 70 EGP. Additional fees for planetarium and special exhibitions. Photography fees apply.',
                'opening_hours': 'Daily 10:00 AM to 7:00 PM. Closed Fridays and public holidays. Reduced summer hours during Ramadan.',
                'what_to_wear': 'Casual, modest clothing. Comfortable shoes for exploring multiple levels. Library climate-controlled.',
                'guided_tours': 'Professional guided tours available in multiple languages. Specialized architectural tours offered. Educational programs for students and researchers.',
                'nearby_attractions': 'Citadel of Qaitbay (3 km), Alexandria Corniche, Catacombs of Kom El Shoqafa, Montaza Palace, Roman Amphitheater',
                'facts': [
                    'Inaugurated October 16, 2002',
                    'Construction cost US$220 million',
                    'Shelf space for 8 million books',
                    'Main reading room 20,000 square meters',
                    'Designed by Norwegian firm Snøhetta',
                    'Selected from 524 competition entries',
                    'Walls carved with 120 different scripts',
                    'Internet Archive donated $5 million and 10 billion web pages'
                ],
                'visitor_tips': [
                    'Allow 3-4 hours for comprehensive visit',
                    'Visit planetarium show (additional ticket)',
                    'Explore specialized libraries and exhibitions',
                    'Library cafe offers Mediterranean views',
                    'Photography permitted (fee required)',
                    'Combine with Alexandria Corniche walk',
                    'Research facilities available for scholars'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.2089° N, 29.9097° E',
                'unesco_status': 'Not a UNESCO site but UNESCO-supported project',
                'climate': 'Mediterranean climate. Mild winters (10-18°C). Warm summers (25-30°C). Best October-April.'
            },
            'citadel-qaitbay': {
                'id': 'citadel-qaitbay',
                'name': 'Citadel of Qaitbay',
                'location': 'Alexandria, Egypt',
                'description': 'Medieval fortress built on ancient Lighthouse of Alexandria foundations',
                'long_description': 'The Citadel of Qaitbay, standing 17 meters high on Alexandria\'s Mediterranean coast, represents one of Egypt\'s most important defensive fortifications. Built between 1477-1479 AD by Mamluk Sultan Al-Ashraf Sayf al-Din Qa\'it Bay, this fortress was constructed on the exact site of the legendary Lighthouse of Alexandria (Pharos), one of the Seven Wonders of the Ancient World. The citadel\'s builders incorporated stones from the lighthouse ruins into the fortress walls. The site served critical defensive roles during the Mamluk period, protecting Alexandria against potential Ottoman threats, and now functions as a Maritime Museum.',
                'historical_significance': 'Built on the site of the ancient Pharos Lighthouse (one of the Seven Wonders of the Ancient World), the Citadel of Qaitbay incorporated stones from the lighthouse ruins destroyed by earthquakes. Constructed during the Mamluk period to defend against Ottoman expansion, the fortress represents Mamluk military architecture. The citadel suffered damage during the British bombardment of Alexandria in 1882 during the Urabi Revolt. Muhammad Ali Pasha renovated the structure in 1805, and the Egyptian Antiquities Organization restored it in 1984. The citadel has witnessed Alexandria\'s transitions through Mamluk, Ottoman, and modern Egyptian periods.',
                'cultural_impact': 'Considered "one of the most important defensive strongholds" along the Mediterranean coast during the Mamluk period. Now functions as Maritime Museum. Popular tourist attraction offering Mediterranean views and connection to ancient Alexandria.',
                'best_time_to_visit': 'October to April for pleasant Mediterranean weather. Sunset visits particularly scenic. Combine with Alexandria Corniche walk.',
                'how_to_get_there': 'Located at eastern tip of Pharos Island in Alexandria. Accessible by taxi or tram from central Alexandria. Walking distance from Alexandria Corniche.',
                'entrance_fees': 'General admission approximately 60 EGP. Additional fee for Maritime Museum. Photography permitted.',
                'opening_hours': 'Daily 9:00 AM to 5:00 PM (winter), 9:00 AM to 6:00 PM (summer). Friday mornings may have restrictions.',
                'what_to_wear': 'Comfortable walking shoes for fortress exploration. Casual, modest clothing. Sun protection recommended.',
                'guided_tours': 'Professional guides available explaining Mamluk architecture and Pharos Lighthouse history. Audio guides in multiple languages.',
                'nearby_attractions': 'Bibliotheca Alexandrina (3 km), Alexandria Corniche, Montaza Palace, Catacombs of Kom El Shoqafa, Pompey\'s Pillar',
                'facts': [
                    'Built 1477-1479 AD by Sultan Qa\'it Bay',
                    'Constructed on site of ancient Pharos Lighthouse',
                    'Incorporates stones from lighthouse ruins',
                    'Height 17 meters',
                    'Damaged in British bombardment of 1882',
                    'Renovated by Muhammad Ali Pasha in 1805',
                    'Restored by Egyptian Antiquities Organization in 1984',
                    'Now functions as Maritime Museum'
                ],
                'visitor_tips': [
                    'Visit at sunset for spectacular Mediterranean views',
                    'Explore Maritime Museum inside fortress',
                    'Combine with Bibliotheca Alexandrina visit',
                    'Walk Alexandria Corniche to/from citadel',
                    'Allow 1-2 hours for exploration',
                    'Fortress offers excellent photo opportunities',
                    'Learn about ancient Pharos Lighthouse from guides'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.2138° N, 29.8856° E',
                'unesco_status': 'Not a UNESCO site but built on former Wonder of the World location',
                'climate': 'Mediterranean climate. Mild winters (10-18°C). Warm summers (25-30°C). Sea breezes moderate temperatures.'
            },
            'aswan-high-dam': {
                'id': 'aswan-high-dam',
                'name': 'Aswan High Dam',
                'location': 'Aswan, Egypt',
                'description': 'Massive engineering marvel controlling Nile floods and generating hydroelectric power',
                'long_description': 'The Aswan High Dam, one of the world\'s largest embankment dams, stands as a monument to modern engineering and Egypt\'s 20th-century development ambitions. Constructed between 1960-1970 and designed by Nikolai Aleksandrovich Malyshev from Moscow\'s Hydroproject Institute, the dam measures 3,830 meters long, 980 meters wide at the base, and 111 meters high. The project created Lake Nasser, a massive 500-kilometer-long reservoir with capacity for 132 cubic kilometers of water. Built primarily with Soviet funding after the United States and UK withdrew support, 25,000 Egyptian engineers and workers contributed to this transformative project.',
                'historical_significance': 'The Aswan High Dam represented Egypt\'s modernization under President Gamal Abdel Nasser and a major Cold War-era infrastructure project symbolizing Soviet-Egyptian cooperation. The dam mitigated periodic floods and droughts that had plagued Egypt for millennia, increased irrigated land by one-third, enabled two crop cycles annually, and reclaimed approximately 840,000 hectares of land. Twelve generators produce 2.1 gigawatts of power, bringing electricity to many Egyptian villages for the first time. However, the project displaced over 100,000 Nubian people and submerged archaeological sites, prompting the famous UNESCO campaign to relocate Abu Simbel and other monuments.',
                'cultural_impact': 'Symbolized Egypt\'s modernization and technological ambition under Nasser. Required displacement of 100,000+ Nubians and submersion of archaeological sites. Prompted UNESCO\'s largest archaeological rescue operation (relocating Abu Simbel, Philae, and other monuments). Changed Nile ecology and Mediterranean fisheries.',
                'best_time_to_visit': 'October to April for pleasant weather. Early morning visits offer cooler temperatures and clearer views. Combine with Philae Temple visit.',
                'how_to_get_there': 'Located 13 km south of Aswan. Accessible by taxi or organized tours from Aswan. Often combined with Philae Temple and Unfinished Obelisk tours.',
                'entrance_fees': 'General admission approximately 75 EGP. Photography permitted. Guided tours available.',
                'opening_hours': 'Daily 7:00 AM to 5:00 PM. Security checkpoints at entrance. Photography restrictions in certain areas.',
                'what_to_wear': 'Comfortable walking shoes. Sun protection essential. Modest clothing. Windy conditions possible near dam.',
                'guided_tours': 'Tours from Aswan hotels include dam visit, Philae Temple, and Unfinished Obelisk. Guides explain engineering and historical significance.',
                'nearby_attractions': 'Philae Temple, Unfinished Obelisk, Lake Nasser, Kalabsha Temple, Abu Simbel Temples (280 km south), Nubian villages',
                'facts': [
                    'Constructed 1960-1970',
                    'Length 3,830 meters, height 111 meters',
                    'Created Lake Nasser (500 km long)',
                    'Reservoir capacity 132 cubic kilometers',
                    '12 generators produce 2.1 gigawatts',
                    'Displaced 100,000+ Nubian people',
                    'Increased irrigated land by one-third',
                    'Built with Soviet funding and Egyptian labor'
                ],
                'visitor_tips': [
                    'Visit morning for best views and cooler weather',
                    'Combine with Philae Temple and Unfinished Obelisk',
                    'Allow 45-60 minutes for visit',
                    'Bring ID - security checkpoints present',
                    'Photography restricted in certain areas',
                    'Panoramic Lake Nasser views from dam top',
                    'Learn about Nubian displacement from guides'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '23.9703° N, 32.8773° E',
                'unesco_status': 'Not a UNESCO site but prompted major UNESCO archaeological rescue campaign',
                'climate': 'Hot desert climate. Extremely hot summers (40°C+). Mild winters (15-25°C). Best October-April.'
            },
            'siwa-oasis': {
                'id': 'siwa-oasis',
                'name': 'Siwa Oasis',
                'location': 'Western Desert, Egypt',
                'description': 'Remote desert oasis famous for Oracle of Amun, visited by Alexander the Great',
                'long_description': 'Siwa Oasis, located in Egypt\'s Western Desert approximately 560 km from Cairo, sits between the Qattara Depression and the Great Sand Sea at 19 meters below sea level. This remarkable oasis covers about 80 km in length and 20 km in width, featuring around 200 natural springs that have sustained settlement since at least the 10th millennium BCE. Known in ancient Egypt as the "Field of Trees," Siwa gained fame for its Oracle of Amun, which Alexander the Great visited in 331 BCE. The predominantly Berber population of around 30,000 people speaks the Siwi language and maintains unique cultural traditions including distinctive silver jewelry and the Siyaha Festival.',
                'historical_significance': 'Siwa has been continuously inhabited since at least the 10th millennium BCE. The Oracle of Amun at Siwa was one of the ancient world\'s most famous oracles, consulted by Alexander the Great in 331 BCE who traveled here to legitimize his rule as pharaoh. The oasis was relatively isolated until annexed by Muhammad Ali of Egypt in 1820. During World Wars I and II, the region experienced significant military activity due to its strategic location. The ancient fortress of Shali Ghadi and the Mountain of the Dead (Gebel al Mawta) containing ancient tombs testify to Siwa\'s long history.',
                'cultural_impact': 'Siwa\'s Berber culture remains distinct from mainstream Egyptian culture. The oasis is famous for unique cultural traditions, handicrafts, and the natural spring known as "Cleopatra\'s Bath." Growing tourism sector brings economic opportunity while challenging cultural preservation.',
                'best_time_to_visit': 'October to April for moderate temperatures. Summer extremely hot (up to 48°C). October Siyaha Festival offers cultural immersion.',
                'how_to_get_there': 'Located 560 km from Cairo. Accessible by 8-10 hour bus journey from Cairo or Marsa Matrouh. 4WD vehicles recommended for desert exploration.',
                'entrance_fees': 'Oasis access free. Individual sites charge fees: Oracle Temple (approximately 30 EGP), Mountain of the Dead (30 EGP).',
                'opening_hours': 'Oasis operates 24/7. Archaeological sites typically 8:00 AM to 5:00 PM. Natural springs accessible dawn to dusk.',
                'what_to_wear': 'Modest clothing respecting conservative local culture. Comfortable shoes for oasis exploration. Sun protection essential. Layers for temperature variations.',
                'guided_tours': 'Organized tours from Cairo include transport and accommodation. Local guides offer desert safaris and cultural tours. Multi-day trips recommended.',
                'nearby_attractions': 'Oracle Temple of Amun, Shali Ghadi fortress, Gebel al Mawta (Mountain of the Dead), Cleopatra\'s Bath spring, Great Sand Sea',
                'facts': [
                    'Located 560 km from Cairo, 19 meters below sea level',
                    'Settled since 10th millennium BCE',
                    'Oracle of Amun visited by Alexander the Great (331 BCE)',
                    'Around 200 natural springs',
                    'Covers 80 km length, 20 km width',
                    'Population approximately 30,000 Berber people',
                    'Speaks unique Siwi language',
                    'Summer temperatures reach 48°C'
                ],
                'visitor_tips': [
                    'Plan minimum 2-3 days to experience oasis properly',
                    'Dress modestly - conservative Berber community',
                    'Book accommodation in advance (limited options)',
                    'Try dates and olives - primary local crops',
                    'Visit natural springs for refreshing swim',
                    'Explore Shali Ghadi fortress at sunset',
                    'Hire local guide for desert safaris'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '29.2028° N, 25.5194° E',
                'unesco_status': 'Not formally UNESCO listed but culturally significant',
                'climate': 'Hot desert climate. Extremely hot summers (up to 48°C). Mild winters. Very low precipitation.'
            },
            'hatshepsut-temple': {
                'id': 'hatshepsut-temple',
                'name': 'Hatshepsut Temple',
                'location': 'Luxor, Egypt',
                'description': 'Spectacular mortuary temple of Egypt\'s female pharaoh carved into cliff face',
                'long_description': 'The Mortuary Temple of Hatshepsut at Deir el-Bahari, located opposite Luxor, stands as one of ancient Egypt\'s greatest architectural wonders. Built during Hatshepsut\'s reign in the 15th century BC, this spectacular temple features three massive terraces rising into limestone cliff faces, constructed with limestone, sandstone, and granite. Inspired by the adjacent Temple of Mentuhotep II, the complex includes shrines to Hathor, Anubis, and Amun, with unique porticoes featuring remarkable relief artwork depicting Hatshepsut\'s expedition to Punt and her divine birth. The temple was aligned with Karnak Temple across the Nile and served the mortuary cults of Hatshepsut and her father Thutmose I.',
                'historical_significance': 'Built by Egypt\'s most successful female pharaoh Hatshepsut in the 15th century BC, the temple demonstrated her architectural and political ambitions. The temple served as the endpoint of the annual Beautiful Festival of the Valley procession from Karnak. After Hatshepsut\'s death, her successor Thutmose III systematically defaced her images and cartouches in an attempt to erase her from history. The temple suffered further damage during the Amarna Period and from earthquakes in the Third Intermediate Period. Extensively excavated between 1893-1936, ongoing Polish archaeological missions continue restoration work. The temple partially opened to tourists in 2000 and fully reopened in March 2023.',
                'cultural_impact': 'Considered "one of the great architectural wonders of the ancient world." Represents rare example of female pharaoh\'s monumental architecture. Extensive excavation and restoration by Polish missions since 1960s. Fully reopened to public in March 2023.',
                'best_time_to_visit': 'October to April for comfortable weather. Early morning visits (6-8 AM) avoid extreme heat and crowds. Combine with Valley of the Kings.',
                'how_to_get_there': 'Located on Luxor\'s West Bank in Deir el-Bahari. Accessible by ferry from East Bank, then taxi or tour bus. Often combined with Valley of the Kings.',
                'entrance_fees': 'General admission approximately 140 EGP. Combination tickets with other West Bank sites available. Photography permitted.',
                'opening_hours': 'Daily 6:00 AM to 5:00 PM (winter), 6:00 AM to 6:00 PM (summer). Last entry one hour before closing.',
                'what_to_wear': 'Comfortable walking shoes for temple terraces. Light, breathable clothing. Hat and sun protection essential. Modest dress recommended.',
                'guided_tours': 'Egyptologist-led tours highly recommended for understanding Hatshepsut\'s history and temple symbolism. Audio guides available.',
                'nearby_attractions': 'Valley of the Kings, Valley of the Queens, Medinet Habu, Colossi of Memnon, Tombs of the Nobles, Ramesseum',
                'facts': [
                    'Built in 15th century BC by female pharaoh Hatshepsut',
                    'Considered "one of great architectural wonders of ancient world"',
                    'Features three massive terraces rising into cliffs',
                    'Aligned with Karnak Temple across Nile',
                    'Defaced by Thutmose III after Hatshepsut\'s death',
                    'Excavated extensively 1893-1936',
                    'Ongoing Polish restoration since 1960s',
                    'Fully reopened March 2023 after restoration'
                ],
                'visitor_tips': [
                    'Visit early morning to avoid heat',
                    'Combine with Valley of the Kings (nearby)',
                    'Allow 1.5-2 hours for exploration',
                    'Climb all three terraces for full experience',
                    'Study Punt expedition reliefs - historically significant',
                    'Photography excellent in morning light',
                    'Hire Egyptologist guide for Hatshepsut\'s fascinating story'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.7380° N, 32.6065° E',
                'unesco_status': 'UNESCO World Heritage Site (Ancient Thebes with its Necropolis) since 1979',
                'climate': 'Hot desert climate. Summer extremely hot (40°C+). Winter pleasant (15-25°C). Best October-April.'
            },
            'dahab': {
                'id': 'dahab',
                'name': 'Dahab',
                'location': 'Sinai Peninsula, Egypt',
                'description': 'Laid-back Bedouin beach town famous for world-class windsurfing and diving',
                'long_description': 'Dahab, located on the southeast coast of Egypt\'s Sinai Peninsula approximately 80 km northeast of Sharm el-Sheikh, has evolved from a small Bedouin fishing village into a world-renowned destination for windsurfing, diving, and alternative tourism. Situated at 21 meters above sea level, the town is divided into three main parts: Masbat (including the Bedouin village Asalah with its beachfront cafes), Mashraba, and Medina. Dahab offers a more relaxed, bohemian atmosphere than Sharm el-Sheikh, with beach cafes, budget accommodations, and some of the Red Sea\'s best diving sites. The town features Neoproterozoic rock formations and mineral deposits including rutile, zircon, and gold.',
                'historical_significance': 'Dahab is mentioned in biblical texts (Deuteronomy) as "דִ֥י זָהָֽב" (dî zāhāḇ). During the Six-Day War in 1967, it was occupied by Israel and known as Di-Zahav, serving as a small military outpost and beginning its transformation into a tourist destination. The town was returned to Egyptian control in 1982 under the Egypt-Israel peace treaty. Since then, Dahab has developed its reputation as a windsurfing and diving destination while maintaining its laid-back Bedouin character. The town remains less developed and more authentic than nearby Sharm el-Sheikh.',
                'cultural_impact': 'World-renowned for windsurfing and kitesurfing, attracting international enthusiasts. Known for relaxed, bohemian atmosphere and Bedouin cultural influence. Popular budget alternative to Sharm el-Sheikh. Part of Red Sea Riviera tourism region.',
                'best_time_to_visit': 'March to May and September to November for ideal conditions. Year-round windsurfing excellent. Winter (December-February) cooler but still pleasant.',
                'how_to_get_there': 'Located 80 km northeast of Sharm el-Sheikh. Accessible by bus or shared taxi from Sharm, Cairo, or Nuweiba. Sharm el-Sheikh Airport nearest international airport.',
                'entrance_fees': 'Town access free. Individual dive sites and activities priced separately. Beach cafes typically free with food/drink purchase.',
                'opening_hours': 'Town operates 24/7. Beach cafes open dawn to late night. Dive centers operate 7:00 AM to 6:00 PM.',
                'what_to_wear': 'Beach casual and bohemian style common. Modest clothing for venturing beyond beach areas. Wetsuit for diving. Sun protection essential.',
                'guided_tours': 'Numerous dive centers offer PADI courses and guided dives. Windsurfing and kitesurfing instruction available. Bedouin desert safari tours popular.',
                'nearby_attractions': 'Blue Hole dive site, Lighthouse dive site, Ras Abu Gallum nature reserve, Mount Sinai, Colored Canyon, St. Catherine\'s Monastery',
                'facts': [
                    'Located 80 km northeast of Sharm el-Sheikh',
                    'Population approximately 3,169 (2023)',
                    'World-renowned for windsurfing and kitesurfing',
                    'Mentioned in biblical Deuteronomy',
                    'Occupied by Israel 1967-1982',
                    'Hot desert climate (Köppen: BWh)',
                    'Elevation 21 meters above sea level',
                    'Contains mineral deposits including gold'
                ],
                'visitor_tips': [
                    'Blue Hole dive site world-famous but challenging',
                    'Beach cafes offer cushioned seating and shisha',
                    'Negotiate accommodation prices - many budget options',
                    'Respect Bedouin culture and traditions',
                    'Try camel treks to Ras Abu Gallum',
                    'More laid-back atmosphere than Sharm el-Sheikh',
                    'Local Bedouin children often sell handmade crafts'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1583037189850-1921ae7c6c22?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1559827260-dc66d52bef19?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '28.4928° N, 34.5044° E',
                'unesco_status': 'Not a UNESCO site but near protected areas',
                'climate': 'Hot desert climate. Extremely hot summer days/nights. Warm winter days, mild nights. Minimal precipitation.'
            },
            'marsa-alam': {
                'id': 'marsa-alam',
                'name': 'Marsa Alam',
                'location': 'Red Sea, Egypt',
                'description': 'Emerging Red Sea resort known as "Egyptian Maldives" for pristine beaches and marine life',
                'long_description': 'Marsa Alam, located in southeastern Egypt on the Red Sea\'s western shore, sits 274 km south of Hurghada and 134 km south of Qusayr. This relatively new resort town, with development beginning in 1995 by Kuwait\'s Al-Kharafi Group, covers 38,433 square kilometers at approximately 60 meters elevation. Known as the "Egyptian Maldives" for its crystal-clear water and white sandy beaches, Marsa Alam offers exceptional underwater diving, kitesurfing, and safaris. The region features Wadi El Gemal National Park with diverse wildlife including mountain goats, gazelles, dugongs, green turtles, and whale sharks. The area also provides access to historic emerald mines and the Temple of Seti I at Khanais.',
                'historical_significance': 'While Marsa Alam itself is modern (development from 1995), the region has ancient significance with historic emerald mines that supplied the Roman Empire and the Temple of Seti I at nearby Khanais dating to the 19th Dynasty. The town\'s growth accelerated with the opening of Marsa Alam International Airport in 2003, transforming it from a small fishing village into an international resort destination. The establishment of Wadi El Gemal National Park protects the region\'s unique desert and marine ecosystems. Marsa Alam represents Egypt\'s effort to develop sustainable Red Sea tourism south of traditional centers like Hurghada.',
                'cultural_impact': 'Nicknamed "Egyptian Maldives" for pristine beaches and marine life. Wadi El Gemal National Park protects unique ecosystems including dugongs, whale sharks, and mangroves. Growing reputation for eco-tourism and sustainable diving. Port Ghalib Marina developed for yacht tourism.',
                'best_time_to_visit': 'September to November and March to May for ideal weather. Year-round diving excellent. Red Sea water temperatures 22-29°C.',
                'how_to_get_there': 'Marsa Alam International Airport receives international and domestic flights. Located 274 km south of Hurghada (4-hour drive). Road access from Cairo and Luxor.',
                'entrance_fees': 'Town access free. Wadi El Gemal National Park entrance approximately 100 EGP. Individual dive trips priced separately.',
                'opening_hours': 'Town operates 24/7. Wadi El Gemal National Park 8:00 AM to 5:00 PM. Dive centers operate dawn to dusk.',
                'what_to_wear': 'Beach resort casual. Swimwear for beaches and watersports. Modest clothing for town areas. Sun protection essential year-round.',
                'guided_tours': 'PADI diving centers offer courses and guided dives to pristine reefs. Desert safaris to historic emerald mines popular. Dolphin and dugong watching tours available.',
                'nearby_attractions': 'Wadi El Gemal National Park, Port Ghalib, Temple of Seti I at Khanais, historic emerald mines, Hamata Islands, Luxor (300 km)',
                'facts': [
                    'Development began 1995 by Kuwaiti Al-Kharafi Group',
                    'Known as "Egyptian Maldives"',
                    'Covers 38,433 square kilometers',
                    'Marsa Alam Airport opened 2003',
                    'Red Sea temperatures 22-29°C',
                    'January temperatures 22-25°C, August 33-40°C',
                    'Wadi El Gemal National Park protects dugongs, whale sharks',
                    'Historic emerald mines supplied Roman Empire'
                ],
                'visitor_tips': [
                    'Less crowded alternative to Hurghada',
                    'Excellent for spotting dugongs and dolphins',
                    'Visit Wadi El Gemal National Park for wildlife',
                    'Pristine reefs less damaged than northern Red Sea',
                    'Port Ghalib offers upscale marina and shopping',
                    'Consider day trip to historic emerald mines',
                    'Book diving trips through reputable PADI centers'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1559827260-dc66d52bef19?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1583037189850-1921ae7c6c22?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.0631° N, 34.8914° E',
                'unesco_status': 'Wadi El Gemal National Park (nearby) nationally protected area',
                'climate': 'Hot desert climate. Minimal rainfall. January 22-25°C, August 33-40°C. Red Sea water 22-29°C year-round.'
            },
            'catacombs-kom-el-shoqafa': {
                'id': 'catacombs-kom-el-shoqafa',
                'name': 'Catacombs of Kom El Shoqafa',
                'location': 'Alexandria, Egypt',
                'description': 'Underground necropolis blending Egyptian, Greek, and Roman cultural elements',
                'long_description': 'The Catacombs of Kom El Shoqafa, located in Alexandria, represent one of the "Seven Wonders of the Middle Ages" and one of the largest Roman-period burial sites in Egypt. Established in the 2nd century CE during the Antonine emperors\' period, this remarkable underground complex consists of three levels cut through solid rock, featuring a six-pillared central shaft and circular staircase for transporting deceased bodies. The catacombs demonstrate a unique fusion of Roman, Greek, and Egyptian cultural attributes, with statues and artwork displaying Egyptian-style sculptures bearing Roman clothes and hairstyles. The site was rediscovered in 1900 when a donkey accidentally fell into the access shaft.',
                'historical_significance': 'Built in the 2nd century CE and used through the 4th century CE, the Catacombs of Kom El Shoqafa represent the cultural melting pot of Greco-Roman Alexandria. Originally believed to be intended for a single family, the complex expanded to accommodate multiple burials. The catacombs feature a triclinium (funeral banquet hall) where families gathered to honor the deceased, three large stone sarcophagi with intricate decorations, and the "Hall of Caracalla" containing horse bones from young men supposedly killed by Emperor Caracalla. The site\'s name "Kom El Shoqafa" (Mound of Shards) derives from broken pottery left by visitors bringing food offerings.',
                'cultural_impact': 'Considered one of the "Seven Wonders of the Middle Ages." Represents unique blend of Egyptian, Greek, and Roman funerary traditions. Rediscovered accidentally in 1900. Depth reaches approximately 100 feet underground.',
                'best_time_to_visit': 'October to April for pleasant Alexandria weather. Underground temperature constant year-round. Allow 1-1.5 hours for visit.',
                'how_to_get_there': 'Located in Alexandria\'s Karmouz district. Accessible by taxi or tram from central Alexandria. 3-4 km from Alexandria Corniche.',
                'entrance_fees': 'General admission approximately 80 EGP. Student discounts available. Photography fees may apply.',
                'opening_hours': 'Daily 9:00 AM to 5:00 PM. Last entry 4:30 PM. May close early on Fridays.',
                'what_to_wear': 'Comfortable walking shoes for underground stairs and passages. Modest clothing. Temperature cool underground - light jacket recommended.',
                'guided_tours': 'Professional guides available explaining Greco-Roman funerary practices and architectural symbolism. Audio guides in multiple languages.',
                'nearby_attractions': 'Pompey\'s Pillar (nearby), Citadel of Qaitbay, Bibliotheca Alexandrina, Alexandria Corniche, Roman Amphitheater, Alexandria National Museum',
                'facts': [
                    'Established 2nd century CE',
                    'Considered "Seven Wonders of the Middle Ages"',
                    'Rediscovered 1900 when donkey fell into shaft',
                    'Three underground levels cut through solid rock',
                    'Blends Egyptian, Greek, and Roman cultural elements',
                    'Used for burials 2nd-4th centuries CE',
                    'Depth approximately 100 feet underground',
                    '"Hall of Caracalla" contains horse bones'
                ],
                'visitor_tips': [
                    'Bring light jacket - cool underground',
                    'Watch your step on circular staircase',
                    'Hire guide for understanding cultural fusion',
                    'Combine with Pompey\'s Pillar (nearby)',
                    'Photography restrictions may apply',
                    'Allow 1-1.5 hours for exploration',
                    'Study statues showing cultural blend'
                ],
                'photos': [
                    'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1568322445389-f64ac2515020?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
                    'https://images.unsplash.com/photo-1539768942893-daf53e448371?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '31.1781° N, 29.8925° E',
                'unesco_status': 'Not formally UNESCO listed but historically significant',
                'climate': 'Mediterranean climate above ground. Underground temperature constant and cool year-round. Best October-April.'
            }
        },
        'uae': {
            'burj-khalifa': {
                'id': 'burj-khalifa',
                'name': 'Burj Khalifa',
                'location': 'Dubai, UAE',
                'description': 'The world\'s tallest building standing at 828 meters with 163 floors and panoramic observation decks.',
                'long_description': 'Burj Khalifa stands as the world\'s tallest building at over 828 meters with 163 floors, receiving 6 million visitors annually. This architectural marvel dominates Dubai\'s skyline and offers unparalleled panoramic views of the city, desert, and ocean from its observation decks on the 124th, 125th, and 148th floors.',
                'historical_significance': 'Completed in 2010, Burj Khalifa was designed by Adrian Smith of Skidmore, Owings & Merrill. The tower broke numerous height records and remains the tallest free-standing structure in the world. Its construction represented Dubai\'s emergence as a global city.',
                'architecture': 'The building\'s Y-shaped floor plan is designed to maximize views of the Arabian Gulf. The structure is built using over 330,000 cubic meters of concrete and 39,000 tonnes of steel. The exterior cladding consists of reflective glazing and aluminum panels.',
                'discovery': 'Burj Khalifa emerged as a symbol of Dubai\'s ambition during the global financial crisis. The project continued despite economic challenges, representing resilience and vision. The tower\'s design evolved through multiple iterations, with the final Y-shaped plan chosen for structural stability and aesthetic appeal. Its completion in 2010 marked a new era in skyscraper construction.',
                'cultural_impact': 'Burj Khalifa has become an iconic symbol of modern Dubai and the UAE\'s emergence as a global destination. The tower appears in countless photographs, films, and media representations of the city. It has inspired architectural innovation worldwide and represents the UAE\'s blend of traditional Islamic design principles with cutting-edge engineering. The building hosts cultural events and exhibitions, contributing to Dubai\'s cultural landscape.',
                'conservation': 'Burj Khalifa incorporates sustainable design features including high-performance glazing, efficient lighting systems, and advanced building management technology. The tower uses recycled water for landscaping and implements energy-efficient systems throughout. Regular maintenance and structural monitoring ensure the building\'s longevity and safety. The development includes green spaces and pedestrian-friendly areas around the base.',
                'health_safety': 'The tower features advanced safety systems including earthquake-resistant design, fire suppression systems, and emergency evacuation procedures. Observation decks have capacity limits and safety barriers. Visitors should wear comfortable shoes for extensive walking and queuing. The building provides accessibility features for visitors with disabilities. Medical facilities are available in the surrounding Dubai Mall.',
                'guided_tours': 'Official guided tours are available through the Burj Khalifa website and authorized operators. Audio guides in multiple languages provide detailed information about the building\'s construction and history. VIP tours offer exclusive access to restricted areas. Photography tours and architectural walking tours are available for special interest groups. Educational programs for students focus on engineering and design principles.',
                'facts': [
                    'World\'s tallest building at 828 meters',
                    'Has 163 floors above ground',
                    'Receives 6 million visitors annually',
                    'Observation decks on 124th, 125th, and 148th floors',
                    'Contains 57 elevators and 8 escalators',
                    'The building sways up to 1.5 meters at the top during high winds',
                    'Construction took 6 years from 2004-2010'
                ],
                'key_sites': [
                    {'name': 'At The Top (Level 124-125)', 'slug': 'at-the-top-level-124-125', 'description': 'Observation deck at 452-456 meters', 'significance': 'Standard observation experience with 360-degree views'},
                    {'name': 'At The Top SKY (Level 148)', 'slug': 'at-the-top-sky-level-148', 'description': 'Highest observation deck at 555 meters', 'significance': 'Premium experience with highest outdoor terrace in the world'},
                    {'name': 'The Lounge', 'slug': 'the-lounge', 'description': 'Luxury lounge on levels 152-154', 'significance': 'Exclusive refreshments with stunning views'},
                    {'name': 'Armani Hotel', 'slug': 'armani-hotel', 'description': 'Hotel occupying floors 1-8 and 38-39', 'significance': 'World\'s first Armani Hotel designed by Giorgio Armani'}
                ],
                'entrance_fees': 'At The Top: 149-189 AED. At The Top SKY: 378-533 AED. Prices vary by time slot.',
                'opening_hours': '8:30 AM to 11:00 PM daily. Last entry at 10:00 PM.',
                'best_time': 'Sunset hours (around 6-7 PM) for spectacular views. Book in advance.',
                'how_to_get_there': 'Located in Downtown Dubai. Metro: Dubai Mall/Burj Khalifa Station. Taxi and private car access available.',
                'what_to_wear': 'Casual smart attire. Comfortable shoes for queues.',
                'visitor_tips': [
                    'Book tickets online in advance to skip queues',
                    'Visit at sunset for day and night views',
                    'Non-prime hours (early morning) have lower prices',
                    'Dubai Fountain show visible from base every 30 minutes',
                    'Photography allowed on all observation decks',
                    'Allow 2-3 hours for complete experience'
                ],
                'nearby_attractions': 'Dubai Mall (adjacent), Dubai Fountain (base), Souk Al Bahar (500m), Dubai Opera (1km).',
                'photos': [
                    'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.1972° N, 55.2744° E',
                'annual_visitors': '6 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'sheikh-zayed-mosque': {
                'id': 'sheikh-zayed-mosque',
                'name': 'Sheikh Zayed Grand Mosque',
                'location': 'Abu Dhabi, UAE',
                'description': 'One of the largest mosques in the world with capacity for 41,000 worshippers, featuring stunning white marble architecture.',
                'long_description': 'The Sheikh Zayed Grand Mosque is one of the largest mosques ever built with capacity for 41,000 worshippers. This architectural masterpiece features 82 domes, over 1,000 columns, 24-carat gold gilded chandeliers, and the world\'s largest hand-knotted carpet. Visiting the mosque is free of charge.',
                'historical_significance': 'Named after Sheikh Zayed bin Sultan Al Nahyan, the founder and first president of the UAE. Construction began in 1996 and was completed in 2007. The mosque represents the late president\'s vision of cultural diversity and tolerance.',
                'architecture': 'The mosque combines architectural styles from different Muslim civilizations. It features 82 domes of seven different sizes, over 1,000 columns, and is adorned with semi-precious stones including lapis lazuli, red agate, amethyst, and mother of pearl.',
                'discovery': 'The Sheikh Zayed Grand Mosque was commissioned by the late Sheikh Zayed bin Sultan Al Nahyan as a symbol of Islamic civilization and cultural diversity. The mosque was designed to showcase the best of Islamic architecture while welcoming people of all faiths. Its construction involved artisans from around the world, creating a masterpiece that represents unity and peace.',
                'cultural_impact': 'The mosque has become a symbol of Abu Dhabi\'s cultural heritage and Islamic architectural excellence. It serves as an educational center, hosting interfaith dialogues and cultural events. The mosque\'s design influences modern Islamic architecture worldwide and represents the UAE\'s commitment to cultural preservation and religious tolerance.',
                'health_safety': 'The mosque provides a safe and respectful environment for visitors. Modest dress is required, with abayas and headscarves provided for women. Wheelchair accessibility is available throughout the complex. Medical facilities are on-site, and security measures ensure visitor safety. Respectful behavior is essential in this sacred space.',
                'facts': [
                    'Capacity for 41,000 worshippers',
                    '82 domes of varying sizes',
                    'Over 1,000 columns inlaid with semi-precious stones',
                    'World\'s largest hand-knotted carpet (5,627 square meters)',
                    'Seven crystal chandeliers, the largest weighing 12 tonnes',
                    'Construction took 11 years (1996-2007)',
                    'Free entry for all visitors'
                ],
                'key_sites': [
                    {'name': 'Main Prayer Hall', 'slug': 'main-prayer-hall', 'description': 'Massive hall with world\'s largest carpet', 'significance': 'Features Swarovski crystal chandeliers and holds 7,000 worshippers'},
                    {'name': 'Courtyard', 'slug': 'courtyard', 'description': 'Marble courtyard with floral mosaic', 'significance': 'World\'s largest marble mosaic covering 17,000 square meters'},
                    {'name': 'Reflective Pools', 'slug': 'reflective-pools', 'description': 'Surrounding pools that mirror the mosque', 'significance': 'Create stunning visual effects especially at night'},
                    {'name': 'Minarets', 'slug': 'minarets', 'description': 'Four 107-meter tall minarets', 'significance': 'Mark the four corners of the mosque'}
                ],
                'entrance_fees': 'Free admission',
                'opening_hours': 'Saturday-Thursday: 9:00 AM - 10:00 PM (last tour 9:30 PM). Friday: 4:30 PM - 10:00 PM. Closed to visitors during prayer times.',
                'best_time': 'Late afternoon for daylight and evening illumination. Avoid Friday mornings.',
                'how_to_get_there': 'Located on Sheikh Rashid Bin Saeed Street, Abu Dhabi. Free shuttle from Abu Dhabi Bus Station. Taxi and private car access available.',
                'what_to_wear': 'Modest clothing mandatory. Women must wear abaya and headscarf (provided free at entrance). Men: long trousers and shirts with sleeves. Remove shoes before entering.',
                'guided_tours': 'Free guided tours available daily. Audio guides in multiple languages. Tours last approximately 45 minutes.',
                'visitor_tips': [
                    'Dress modestly - abayas and headscarves provided for women',
                    'Visit at sunset for beautiful lighting',
                    'Photography allowed but respect prayer areas',
                    'Free guided tours highly recommended',
                    'Closed during prayer times - check schedule',
                    'Allow 1.5-2 hours for visit'
                ],
                'nearby_attractions': 'Louvre Abu Dhabi (15 km), Emirates Palace (10 km), Wahat Al Karama memorial (5 km).',
                'conservation': 'Regular maintenance and restoration to preserve the intricate details and precious materials.',
                'photos': [
                    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '24.4128° N, 54.4747° E',
                'annual_visitors': 'Over 5 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'palm-jumeirah': {
                'id': 'palm-jumeirah',
                'name': 'Palm Jumeirah',
                'location': 'Dubai, UAE',
                'description': 'Artificial island shaped like a palm tree, featuring luxury resorts, private beaches, and world-class entertainment.',
                'long_description': 'Palm Jumeirah is the world\'s largest artificial island, shaped like a palm tree and extending 5 km into the Persian Gulf. This engineering marvel features luxury resorts, private villas, pristine beaches, and world-class entertainment venues. The island is connected to the mainland by a 300-meter-long causeway.',
                'historical_significance': 'Construction began in 2001 and was completed in 2006. Palm Jumeirah was the first of three planned palm-shaped islands (Palm Jebel Ali and Palm Deira were later developed). The project represented Dubai\'s ambitious vision to create new land for tourism and real estate development.',
                'architecture': 'The island consists of a trunk, 16 fronds, and a surrounding crescent. The trunk houses luxury hotels and apartments, while the fronds feature private villas and beachfront properties. The crescent contains the famous Atlantis The Palm resort and marina.',
                'discovery': 'Palm Jumeirah was conceived as part of Dubai\'s vision to create artificial islands that would add valuable coastline to the city. The project began with feasibility studies in the late 1990s, with construction starting in 2001. The palm-shaped design was chosen to maximize beachfront property while creating a distinctive landmark visible from space.',
                'cultural_impact': 'Palm Jumeirah has become a symbol of Dubai\'s engineering prowess and transformed the city\'s skyline. It represents the UAE\'s ability to reshape its geography and create new possibilities for tourism and real estate. The island has influenced similar projects worldwide and showcases Arabian innovation in modern architecture.',
                'health_safety': 'The island features extensive safety measures including 24/7 security, lifeguard services at beaches, and emergency medical facilities. Monorail and pedestrian bridges ensure safe transportation. Visitors should follow local guidelines, stay hydrated, and avoid swimming in unauthorized areas. The development includes shaded walkways and cooling stations.',
                'guided_tours': 'Official guided tours are available through Dubai Tourism and Atlantis The Palm. Walking tours explore the island\'s architecture and history, while boat tours provide water-level perspectives. Photography tours capture the island\'s unique features, and VIP experiences include private access to exclusive areas.',
                'facts': [
                    'World\'s largest artificial island at 5.6 km²',
                    'Took 6 years to construct (2001-2006)',
                    'Used 94 million cubic meters of sand and 5.5 million tonnes of rock',
                    'Features 1,400 luxury villas and apartments',
                    'Home to Atlantis The Palm, one of Dubai\'s most luxurious resorts',
                    'Connected to mainland by 300-meter causeway',
                    'Part of larger Palm Islands development project'
                ],
                'key_sites': [
                    {'name': 'Atlantis The Palm', 'slug': 'atlantis-the-palm', 'description': 'Iconic luxury resort with water park and aquarium', 'significance': 'World-famous hotel with underwater dining and marine attractions'},
                    {'name': 'The Pointe', 'slug': 'the-pointe', 'description': 'Shopping and entertainment complex at the island\'s tip', 'significance': 'Features restaurants, bars, and panoramic views'},
                    {'name': 'Golden Mile', 'slug': 'golden-mile', 'description': 'Beachfront promenade with luxury hotels', 'significance': 'Home to prestigious hotels like Jumeirah Zabeel Saray'},
                    {'name': 'Trunk Road', 'slug': 'trunk-road', 'description': 'Main artery connecting the island', 'significance': 'Features luxury shopping and dining options'}
                ],
                'entrance_fees': 'Free to visit the island. Individual attractions have their own fees.',
                'opening_hours': '24/7 access. Individual venues have varying hours.',
                'best_time': 'Evening for illuminated views and cooler temperatures.',
                'how_to_get_there': 'Located off Dubai\'s coast. Taxi, private car, or monorail from Dubai Marina. Water taxi available.',
                'what_to_wear': 'Beachwear for resorts, smart casual for dining and entertainment.',
                'visitor_tips': [
                    'Visit Atlantis The Palm for world-class entertainment',
                    'Take the monorail for scenic views of the island',
                    'Book water taxi for romantic approach to resorts',
                    'Explore the fronds for stunning sunset views',
                    'Visit during Dubai Summer Surprises for discounted rates',
                    'Allow 2-3 hours to explore the main attractions'
                ],
                'nearby_attractions': 'Dubai Marina (adjacent), Jumeirah Beach Residence (1 km), Mall of the Emirates (5 km).',
                'conservation': 'Ongoing maintenance to protect the artificial island structure and marine environment.',
                'photos': [
                    'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.1124° N, 55.1390° E',
                'annual_visitors': 'Over 10 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'dubai-mall': {
                'id': 'dubai-mall',
                'name': 'Dubai Mall',
                'location': 'Dubai, UAE',
                'description': 'World\'s largest shopping and entertainment complex featuring over 1,200 stores, aquarium, and ice rink.',
                'long_description': 'Dubai Mall is the world\'s largest shopping and entertainment complex, spanning 1.1 million square meters. Connected to the Burj Khalifa, it features over 1,200 retail outlets, a massive aquarium, indoor ice rink, and numerous dining and entertainment options. The mall receives over 80 million visitors annually.',
                'historical_significance': 'Opened in 2008 alongside the Burj Khalifa, Dubai Mall represents Dubai\'s transformation into a global shopping and tourism destination. It was designed to complement the world\'s tallest building and create an integrated entertainment district.',
                'architecture': 'The mall features a modern design with glass facades and spacious interiors. It includes the Dubai Aquarium & Underwater Zoo, VR Park, and KidZania educational entertainment center. The mall\'s design emphasizes luxury shopping and family entertainment.',
                'facts': [
                    'World\'s largest shopping mall at 1.1 million square meters',
                    'Over 1,200 retail stores and outlets',
                    'Receives 80 million visitors annually',
                    'Features world\'s largest acrylic panel aquarium tunnel',
                    'Home to Dubai Ice Rink and VR Park',
                    'Contains over 200 food and beverage outlets',
                    'Connected directly to Burj Khalifa'
                ],
                'key_sites': [
                    {'name': 'Dubai Aquarium & Underwater Zoo', 'slug': 'dubai-aquarium-underwater-zoo', 'description': 'World\'s largest acrylic panel tunnel with marine life', 'significance': 'Features sharks, rays, and underwater viewing experiences'},
                    {'name': 'Dubai Ice Rink', 'slug': 'dubai-ice-rink', 'description': 'Olympic-sized ice skating rink', 'significance': 'Year-round skating in desert climate'},
                    {'name': 'Fashion Avenue', 'slug': 'fashion-avenue', 'description': 'Luxury shopping district with high-end brands', 'significance': 'Features flagship stores of international designers'},
                    {'name': 'KidZania', 'slug': 'kidzania', 'description': 'Educational entertainment center for children', 'significance': 'Interactive learning through role-playing activities'}
                ],
                'entrance_fees': 'Free entry to mall. Individual attractions: Aquarium (95-140 AED), Ice Rink (50-80 AED), VR Park (95 AED).',
                'opening_hours': '10:00 AM to 10:00 PM Sunday-Wednesday, 10:00 AM to 11:00 PM Thursday-Saturday.',
                'best_time': 'Evening for shopping and entertainment. Weekends are busiest.',
                'how_to_get_there': 'Connected to Burj Khalifa. Metro: Dubai Mall Station. Multiple parking levels available.',
                'what_to_wear': 'Smart casual attire. Comfortable shoes for extensive walking.',
                'visitor_tips': [
                    'Visit early morning or late evening to avoid crowds',
                    'Download mall app for navigation and offers',
                    'Book aquarium and VR experiences in advance',
                    'Take advantage of free shuttle to Burj Khalifa',
                    'Explore the outdoor terraces for Burj Khalifa views',
                    'Allow 3-4 hours for comprehensive visit'
                ],
                'nearby_attractions': 'Burj Khalifa (connected), Dubai Fountain (adjacent), Souk Al Bahar (adjacent).',
                'conservation': 'Modern facility with sustainable design features and waste management systems.',
                'discovery': 'Dubai Mall emerged as a visionary project to create the world\'s largest shopping and entertainment destination. The mall was conceived as an integral part of the Burj Khalifa development, designed to complement the world\'s tallest building and establish Dubai as a global shopping capital. Its discovery represents Dubai\'s transformation from traditional trading to modern retail excellence.',
                'architecture': 'Dubai Mall showcases contemporary architectural excellence with its expansive glass facades, soaring atriums, and integrated design that seamlessly connects indoor and outdoor spaces. The mall\'s architecture incorporates sustainable design elements including energy-efficient lighting, advanced HVAC systems, and water recycling facilities. The structure features multiple levels of retail space, entertainment zones, and public areas that create an immersive shopping experience.',
                'cultural_impact': 'Dubai Mall has redefined shopping culture in the Middle East, introducing world-class retail experiences and entertainment options that blend international brands with local hospitality. The mall has become a social hub where diverse cultures converge, fostering community events, cultural exhibitions, and family-oriented entertainment. It represents Dubai\'s ability to preserve traditional values while embracing global consumerism.',
                'health_safety': 'The mall maintains strict health and safety standards with comprehensive security systems, emergency protocols, and regular safety inspections. Temperature-controlled environments provide comfort throughout the year. Medical facilities and first aid stations are available, along with accessibility features for visitors with disabilities. Security personnel and CCTV monitoring ensure a safe shopping environment.',
                'guided_tours': 'Official guided tours are available through the Dubai Tourism Department, offering insights into the mall\'s architecture, history, and attractions. Specialized tours focus on the aquarium, VR experiences, and shopping districts. Audio guides in multiple languages provide self-guided exploration options. Group tours can be arranged for educational and corporate visits.',
                'photos': [
                    'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.1972° N, 55.2791° E',
                'annual_visitors': '80 million',
                'climate': 'Air-conditioned indoor environment.'
            },
            'dubai-desert-safari': {
                'id': 'dubai-desert-safari',
                'name': 'Dubai Desert Safari',
                'location': 'Dubai Desert, UAE',
                'description': 'Thrilling desert adventure combining dune bashing, camel riding, falconry shows, and traditional Bedouin hospitality.',
                'long_description': 'Dubai Desert Safari offers an authentic Arabian desert experience just minutes from the city. This adventure combines high-speed dune bashing in 4x4 vehicles, camel riding, traditional Bedouin camp entertainment, and stunning desert landscapes. The safari provides a glimpse into traditional Emirati culture and the natural beauty of the Arabian Desert.',
                'historical_significance': 'The desert safari experience draws from centuries-old Bedouin traditions of desert travel and hospitality. The activity has become a cornerstone of Dubai\'s tourism industry, showcasing the country\'s heritage while providing modern adventure experiences.',
                'facts': [
                    'Covers over 600 square kilometers of desert',
                    'Features 100-meter high sand dunes',
                    'Includes traditional Bedouin camp with entertainment',
                    'Camel riding and falconry demonstrations',
                    'Tanoura dance and belly dancing performances',
                    'Arabic coffee and dates served in traditional style',
                    'Sunset views over Dubai skyline from desert'
                ],
                'key_sites': [
                    {'name': 'Sand Dunes', 'slug': 'sand-dunes', 'description': 'Massive red sand dunes for 4x4 adventures', 'significance': 'Thrilling dune bashing experiences with professional drivers'},
                    {'name': 'Bedouin Camp', 'slug': 'bedouin-camp', 'description': 'Traditional desert camp with entertainment', 'significance': 'Authentic Arabian hospitality and cultural performances'},
                    {'name': 'Camel Farm', 'slug': 'camel-farm', 'description': 'Camel riding and interaction area', 'significance': 'Experience traditional desert transportation'},
                    {'name': 'Falconry Display', 'slug': 'falconry-display', 'description': 'Traditional Emirati falconry demonstration', 'significance': 'Showcases ancient Arabian hunting tradition'}
                ],
                'entrance_fees': 'Standard safari: 150-250 AED. Premium options: 300-500 AED. Prices vary by package.',
                'opening_hours': 'Sunset safaris depart 3:00-4:00 PM. Evening safaris 7:00-8:00 PM.',
                'best_time': 'Winter months (November-March) for cooler temperatures.',
                'how_to_get_there': 'Pickup from major Dubai hotels. Desert location is 45-60 minutes from city center.',
                'what_to_wear': 'Comfortable clothing, closed-toe shoes, light jacket for evening. Scarf for face protection.',
                'visitor_tips': [
                    'Book in advance, especially during peak season',
                    'Choose morning pickup for better dune conditions',
                    'Stay seated during dune bashing for safety',
                    'Try traditional Arabic food at the camp',
                    'Photography opportunities throughout the experience',
                    'Allow 4-5 hours for complete safari experience'
                ],
                'nearby_attractions': 'Al Ain Oasis (90 km), Hatta Mountain Pools (60 km), Dubai city center (45 km).',
                'conservation': 'Operates under environmental guidelines to protect desert ecosystem.',
                'discovery': 'Dubai Desert Safari emerged as a pioneering tourism concept that transformed desert exploration into a structured adventure experience. The safari concept was developed to showcase the natural beauty of the Arabian Desert while providing authentic cultural encounters. It became a cornerstone of Dubai\'s tourism industry, blending traditional Bedouin hospitality with modern adventure tourism.',
                'architecture': 'The desert safari experience features specially designed 4x4 vehicles equipped for extreme terrain, traditional Bedouin-style camps with climate-controlled tents, and open-air dining pavilions. The camps incorporate authentic Arabian architectural elements with modern safety features, creating immersive environments that transport visitors to traditional desert life while ensuring comfort and security.',
                'cultural_impact': 'Dubai Desert Safari has become a cultural bridge, introducing millions of visitors to traditional Emirati customs, Bedouin hospitality, and desert heritage. The experience has preserved and promoted authentic cultural practices while creating economic opportunities for local communities. It represents Dubai\'s ability to maintain cultural authenticity while embracing global tourism trends.',
                'health_safety': 'All safaris operate with professional drivers trained in desert navigation and emergency procedures. Vehicles are equipped with communication devices, first aid kits, and GPS tracking. Passengers receive safety briefings and are required to wear seatbelts during dune bashing. Medical facilities are available at camp locations, and all activities follow strict safety protocols.',
                'guided_tours': 'Professional guides provide historical context and cultural insights throughout the safari experience. Multilingual guides explain desert ecology, traditional Bedouin life, and local customs. Specialized photography tours and cultural immersion experiences are available. Group tours can be customized for educational institutions and corporate events.',
                'photos': [
                    'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '24.9167° N, 55.2833° E',
                'annual_visitors': 'Over 2 million',
                'climate': 'Desert climate. Best experienced November-March.'
            },
            'dubai-marina': {
                'id': 'dubai-marina',
                'name': 'Dubai Marina',
                'location': 'Dubai, UAE',
                'description': 'Modern waterfront district featuring luxury yachts, high-rise towers, and vibrant dining and entertainment scene.',
                'long_description': 'Dubai Marina is a modern waterfront development featuring luxury residential towers, a man-made marina, and vibrant lifestyle amenities. The district offers stunning views of the Persian Gulf, world-class dining, shopping, and entertainment options. It\'s home to over 150 restaurants and the famous Dubai Marina Mall.',
                'historical_significance': 'Developed in the early 2000s as part of Dubai\'s expansion, Dubai Marina represents the city\'s transformation from oil-dependent economy to tourism and real estate hub. The marina was designed to create a European-style waterfront lifestyle in the desert.',
                'architecture': 'The district features over 200 residential towers, many over 50 stories high. The marina can accommodate over 3,000 yachts and features a promenade with palm-lined walkways, fountains, and modern sculptures.',
                'facts': [
                    'Home to over 120,000 residents',
                    'Features 3,000+ yacht berths in the marina',
                    'Over 200 residential and commercial towers',
                    'Contains Dubai Marina Mall with 160 stores',
                    '150+ restaurants and cafes',
                    'JBR Beach and promenade stretching 3 km',
                    'Average tower height of 50+ stories'
                ],
                'key_sites': [
                    {'name': 'Dubai Marina Mall', 'slug': 'dubai-marina-mall', 'description': 'Modern shopping and entertainment complex', 'significance': 'Features cinema, bowling, and diverse dining options'},
                    {'name': 'JBR Beach', 'slug': 'jbr-beach', 'description': 'Artificial beach with promenade and water activities', 'significance': 'Popular recreational area with beach volleyball and dining'},
                    {'name': 'Marina Walk', 'slug': 'marina-walk', 'description': 'Waterfront promenade with restaurants and shops', 'significance': 'Scenic walking path with views of yachts and towers'},
                    {'name': 'Pier 7', 'slug': 'pier-7', 'description': 'Entertainment complex with bars and restaurants', 'significance': 'Vibrant nightlife and dining destination'}
                ],
                'entrance_fees': 'Free access to public areas. Individual venues have their own fees.',
                'opening_hours': '24/7 access to marina. Shops and restaurants vary.',
                'best_time': 'Evening for dining and entertainment. Cooler months for outdoor activities.',
                'how_to_get_there': 'Located between Jumeirah Beach Residence and Palm Jumeirah. Metro: Dubai Marina Station.',
                'what_to_wear': 'Casual attire for daytime, smart casual for evening dining.',
                'visitor_tips': [
                    'Visit Marina Mall for shopping and entertainment',
                    'Walk the JBR promenade for people-watching',
                    'Try waterfront dining with yacht views',
                    'Take a yacht tour of the marina',
                    'Visit during Dubai Summer Surprises for deals',
                    'Allow 2-3 hours to explore the district'
                ],
                'nearby_attractions': 'Palm Jumeirah (adjacent), Jumeirah Beach Residence (adjacent), Mall of the Emirates (3 km).',
                'conservation': 'Modern development with sustainable design features.',
                'discovery': 'Dubai Marina emerged as a visionary waterfront development project that transformed Dubai\'s coastline into a modern lifestyle destination. The marina concept was pioneered in the early 2000s, creating the first man-made marina in the Middle East and establishing a new paradigm for urban waterfront living. It became a catalyst for Dubai\'s transformation from traditional trading hub to global lifestyle destination.',
                'architecture': 'Dubai Marina showcases innovative architectural design with over 200 high-rise residential towers featuring contemporary aesthetics and functional layouts. The marina incorporates advanced engineering with a 3,000-berth harbor, pedestrian promenades, and integrated retail and entertainment spaces. The development blends modern skyscrapers with traditional Arabian design elements, creating a harmonious urban landscape.',
                'cultural_impact': 'Dubai Marina has redefined urban living in the UAE, introducing cosmopolitan lifestyle concepts and creating a melting pot of international cultures. The development has fostered community building through waterfront events, international cuisine, and diverse entertainment options. It represents Dubai\'s evolution from traditional society to modern multicultural metropolis while maintaining cultural authenticity.',
                'health_safety': 'The marina district maintains comprehensive security systems with 24/7 surveillance, professional security personnel, and emergency response protocols. All buildings meet international safety standards with fire prevention systems and accessibility features. Water safety measures are implemented throughout the marina area, and medical facilities are readily available in the vicinity.',
                'guided_tours': 'Official guided tours are available through Dubai Tourism, offering architectural insights and historical context about the marina\'s development. Yacht tours provide unique perspectives of the waterfront, while walking tours explore the promenade and key attractions. Specialized photography tours capture the marina\'s skyline and architectural highlights.',
                'photos': [
                    'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.0783° N, 55.1403° E',
                'annual_visitors': 'Over 15 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'burj-al-arab': {
                'id': 'burj-al-arab',
                'name': 'Burj Al Arab',
                'location': 'Dubai, UAE',
                'description': 'Iconic luxury hotel shaped like a sail, featuring seven-star service and the world\'s highest atrium lounge.',
                'long_description': 'Burj Al Arab is a luxury hotel located in Dubai, United Arab Emirates. At 321 meters (1,053 ft), it is the fourth tallest hotel in the world. The hotel is the first and only hotel to be awarded a seven-star rating by its creator, and is often described as "the world\'s most luxurious hotel".',
                'historical_significance': 'Opened in 1999, Burj Al Arab was built to showcase Dubai\'s emergence as a luxury tourism destination. The hotel was designed to resemble the sail of a dhow, traditional Arabian boat, and became an instant icon of modern Dubai.',
                'architecture': 'The hotel features a distinctive sail-shaped silhouette and is built on an artificial island 280 meters offshore. It includes the world\'s highest atrium lounge, a helipad on the 28th floor, and luxury suites with panoramic views.',
                'facts': [
                    'World\'s first seven-star hotel',
                    '321 meters tall (1,053 feet)',
                    'Built on artificial island 280 meters offshore',
                    'Features world\'s highest atrium lounge',
                    'Helipad on the 28th floor',
                    'Suites start at 170 square meters',
                    'Construction cost $650 million'
                ],
                'key_sites': [
                    {'name': 'Atrium Lounge', 'slug': 'atrium-lounge', 'description': 'World\'s highest atrium lounge at 200 meters', 'significance': 'Panoramic views and afternoon tea experience'},
                    {'name': 'Gold Leaf Restaurant', 'slug': 'gold-leaf-restaurant', 'description': 'Signature restaurant with gold leaf decor', 'significance': 'Fine dining with views of Dubai Fountain'},
                    {'name': 'Royal Suite', 'slug': 'royal-suite', 'description': 'Presidential suite spanning 780 square meters', 'significance': 'Most luxurious accommodation in Dubai'},
                    {'name': 'Private Beach', 'slug': 'private-beach', 'description': 'Exclusive beach with cabana services', 'significance': 'Secluded relaxation area with luxury amenities'}
                ],
                'entrance_fees': 'Public areas accessible. Restaurant reservations required. Day passes available for some facilities.',
                'opening_hours': '24/7 hotel operations. Public areas accessible during business hours.',
                'best_time': 'Evening for illuminated views and sunset dining.',
                'how_to_get_there': 'Located on Jumeirah Beach. Taxi or private car recommended.',
                'what_to_wear': 'Smart casual for public areas, formal for fine dining.',
                'visitor_tips': [
                    'Book afternoon tea at the Atrium Lounge in advance',
                    'Visit at sunset for spectacular views',
                    'Experience the helipad arrival (by arrangement)',
                    'Try the signature Gold Leaf restaurant',
                    'Photography allowed in public areas',
                    'Allow 2-3 hours for complete experience'
                ],
                'nearby_attractions': 'Dubai Fountain (adjacent), Wild Wadi Water Park (adjacent), Jumeirah Beach (adjacent).',
                'conservation': 'Modern luxury facility with sustainable design features.',
                'discovery': 'Burj Al Arab emerged as a revolutionary concept in luxury hospitality, introducing seven-star service standards and redefining the boundaries of luxury accommodation. The hotel was conceived as a symbol of Dubai\'s emergence as a global luxury destination, combining traditional Arabian hospitality with world-class service excellence. Its discovery marked a new era in Middle Eastern tourism and hospitality.',
                'architecture': 'Burj Al Arab showcases distinctive architectural innovation with its sail-shaped silhouette inspired by traditional Arabian dhow boats. The hotel features advanced engineering including a helipad, atrium lounge, and artificial island construction. The interior design incorporates gold leaf accents, marble finishes, and contemporary Arabian motifs, creating an opulent yet functional luxury environment.',
                'cultural_impact': 'Burj Al Arab has become an iconic symbol of modern Dubai, representing the city\'s transformation from traditional trading hub to luxury tourism destination. The hotel has influenced global hospitality standards and inspired similar luxury developments worldwide. It serves as a cultural bridge, blending traditional Emirati values with international luxury expectations.',
                'health_safety': 'The hotel maintains the highest standards of health and safety with comprehensive security systems, emergency protocols, and medical facilities on-site. All areas are monitored 24/7, and the hotel follows international hygiene and safety standards. Private security personnel and advanced surveillance systems ensure guest safety throughout the property.',
                'guided_tours': 'Official guided tours are available through the hotel\'s concierge services, offering insights into the architectural design, historical significance, and luxury amenities. Specialized tours include helipad experiences, suite previews, and behind-the-scenes access to service areas. Private tours can be arranged for VIP guests and special occasions.',
                'photos': [
                    'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.1412° N, 55.1853° E',
                'annual_visitors': 'Over 1 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'dubai-fountain': {
                'id': 'dubai-fountain',
                'name': 'Dubai Fountain',
                'location': 'Dubai, UAE',
                'description': 'World\'s largest choreographed fountain system performing to music with water jets reaching 150 meters.',
                'long_description': 'Dubai Fountain is a choreographed fountain system located at the base of the Burj Khalifa. It is the world\'s largest fountain system, with water jets reaching 150 meters into the air, accompanied by colored lights and music. The fountain performs every 30 minutes from 6:00 PM to 11:00 PM.',
                'historical_significance': 'Opened in 2009, Dubai Fountain was created to complement the Burj Khalifa and enhance Dubai\'s reputation as an entertainment destination. It represents Dubai\'s investment in world-class attractions and technological innovation.',
                'facts': [
                    'World\'s largest choreographed fountain',
                    'Water jets reach 150 meters (492 feet)',
                    'Contains 6,600 lights and 25 colored projectors',
                    'Uses 83,000 liters of water per show',
                    'Performs to 6 different musical pieces',
                    'Shows every 30 minutes from 6 PM to 11 PM',
                    'Cost $218 million to build'
                ],
                'key_sites': [
                    {'name': 'Main Fountain Basin', 'slug': 'main-fountain-basin', 'description': '660-foot long lake with fountain system', 'significance': 'Features the world\'s largest fountain display'},
                    {'name': 'Burj Khalifa View', 'slug': 'burj-khalifa-view', 'description': 'Fountain viewed against the world\'s tallest building', 'significance': 'Creates spectacular visual contrast'},
                    {'name': 'Surrounding Walkways', 'slug': 'surrounding-walkways', 'description': 'Pedestrian paths around the fountain', 'significance': 'Best viewing locations for the shows'}
                ],
                'entrance_fees': 'Free to view from surrounding areas. Premium viewing areas may have fees.',
                'opening_hours': 'Shows every 30 minutes from 6:00 PM to 11:00 PM daily.',
                'best_time': 'Evening shows for full illumination and cooler temperatures.',
                'how_to_get_there': 'Located at Burj Khalifa base. Metro: Dubai Mall Station.',
                'what_to_wear': 'Comfortable clothing for evening viewing.',
                'visitor_tips': [
                    'Arrive 30 minutes early for good viewing spots',
                    'Visit during weekends for larger crowds',
                    'Combine with Burj Khalifa visit',
                    'Best viewed from Dubai Mall terrace or bridge',
                    'Shows are synchronized to music',
                    'Photography encouraged'
                ],
                'discovery': 'Dubai Fountain was inaugurated in 2009 as part of the Burj Khalifa development project. The fountain system was designed by WET Design, the same company that created the Bellagio fountains in Las Vegas. The project involved extensive engineering to create a fountain system that could operate in Dubai\'s desert climate while providing spectacular water displays.',
                'architecture': 'The fountain spans 275 meters in length and features 6,600 lights and 50 colored projectors. The system uses 83,000 liters of water per show, propelled by 5,000 nozzles that can shoot water up to 150 meters high. The engineering includes advanced computer systems that synchronize the water jets, lights, and music for precise performances.',
                'cultural_impact': 'Dubai Fountain has become an iconic symbol of Dubai\'s modern identity, representing the city\'s technological innovation and entertainment excellence. It has transformed Dubai into a global entertainment destination and inspired similar projects worldwide. The fountain has become a cultural landmark that showcases Dubai\'s ability to blend tradition with cutting-edge technology.',
                'conservation': 'The fountain uses recycled water from Burj Khalifa\'s air conditioning system, making it an environmentally conscious attraction. Advanced filtration systems ensure water quality, and energy-efficient LED lighting reduces power consumption. Regular maintenance programs preserve the fountain\'s performance and visual impact.',
                'health_safety': 'The fountain area is monitored by security personnel and features clear pathways for visitors. During hot weather, stay hydrated and seek shade when not viewing shows. Some areas may be slippery near water features. Follow local guidelines and maintain safe distances from the water displays.',
                'guided_tours': 'Official guided tours are available through Dubai Tourism, providing insights into the fountain\'s engineering and history. Audio guides in multiple languages offer self-paced exploration. Special VIP experiences include behind-the-scenes access and premium viewing areas during shows.',
                'nearby_attractions': 'Burj Khalifa (adjacent), Dubai Mall (adjacent), Souk Al Bahar (adjacent).',
                'conservation': 'Uses recycled water and energy-efficient lighting systems.',
                'photos': [
                    'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.1972° N, 55.2744° E',
                'annual_visitors': 'Over 10 million',
                'climate': 'Desert climate. Shows run year-round.'
            },
            'louvre-abu-dhabi': {
                'id': 'louvre-abu-dhabi',
                'name': 'Louvre Abu Dhabi',
                'location': 'Abu Dhabi, UAE',
                'description': 'World-class art museum featuring masterpieces from around the world in a stunning desert location.',
                'long_description': 'Louvre Abu Dhabi is a world-class art museum located on Saadiyat Island in Abu Dhabi. The museum houses over 600 artworks from around the world, spanning 3,000 years of human creativity. The building features a distinctive dome with 7,850 stars that filter light into the galleries below.',
                'historical_significance': 'Opened in 2017, Louvre Abu Dhabi represents the first Louvre museum outside France. The museum\'s collection includes works from the Louvre in Paris and other prestigious institutions, showcasing universal art and culture.',
                'architecture': 'Designed by Jean Nouvel, the museum features a large dome with intricate star-shaped perforations that create a "rain of light" effect. The building is surrounded by water and integrates traditional Islamic architectural elements with modern design.',
                'facts': [
                    'First Louvre museum outside France',
                    'Houses over 600 artworks from 3,000 years',
                    'Dome features 7,850 stars filtering light',
                    'Collection includes works from Louvre Paris',
                    'Features universal museum concept',
                    'Cost $653 million to build',
                    'Spans 24,000 square meters'
                ],
                'key_sites': [
                    {'name': 'Main Dome', 'slug': 'main-dome', 'description': 'Iconic dome with star-shaped perforations', 'significance': 'Creates "rain of light" effect in galleries'},
                    {'name': 'Pavilion of Islamic Art', 'slug': 'pavilion-of-islamic-art', 'description': 'Dedicated gallery for Islamic masterpieces', 'significance': 'Showcases Islamic art and artifacts'},
                    {'name': 'Modern Art Gallery', 'slug': 'modern-art-gallery', 'description': 'Contemporary art collection', 'significance': 'Features works from 20th and 21st centuries'},
                    {'name': 'Ancient Civilizations', 'slug': 'ancient-civilizations', 'description': 'Artifacts from ancient cultures', 'significance': 'Includes Egyptian, Greek, and Roman works'}
                ],
                'entrance_fees': '63 AED for adults. Free for children under 13.',
                'opening_hours': '10:00 AM to 8:00 PM Saturday-Wednesday, 10:00 AM to 10:00 PM Thursday-Friday.',
                'best_time': 'Evening for cooler temperatures and illuminated dome.',
                'how_to_get_there': 'Located on Saadiyat Island. Free shuttle from Abu Dhabi Mall.',
                'what_to_wear': 'Modest attire. Comfortable shoes for extensive walking.',
                'visitor_tips': [
                    'Book tickets online to avoid queues',
                    'Allow 3-4 hours for comprehensive visit',
                    'Audio guide enhances the experience',
                    'Visit during special exhibitions',
                    'Photography allowed in most areas',
                    'Take the free shuttle from city center'
                ],
                'discovery': 'The Louvre Abu Dhabi project was conceived in 2007 as part of Abu Dhabi\'s cultural development initiative. The museum represents the first Louvre outside France and was designed to showcase universal art and culture. The architectural concept was developed by French architect Jean Nouvel, who created the distinctive dome with 7,850 stars that filter desert light into the galleries.',
                'cultural_impact': 'Louvre Abu Dhabi has transformed Abu Dhabi into a global cultural destination, attracting millions of visitors annually. The museum promotes cultural exchange between East and West, featuring artworks from diverse civilizations. It has inspired similar cultural initiatives across the UAE and positioned Abu Dhabi as a center for arts and heritage preservation.',
                'conservation': 'The museum employs state-of-the-art climate control systems to protect priceless artworks from the desert environment. Advanced security measures and conservation laboratories ensure the preservation of the collection. The dome\'s innovative design filters harmful UV rays while allowing natural light to illuminate the galleries.',
                'health_safety': 'The museum maintains comfortable indoor temperatures year-round. Wheelchair accessibility is available throughout, and audio guides in multiple languages assist visitors. Security measures ensure a safe environment, and medical facilities are available on-site. Visitors should wear comfortable shoes for extensive walking.',
                'guided_tours': 'Official guided tours are available in multiple languages, providing historical and artistic context for the collections. Audio guides offer self-paced exploration with detailed information about artworks. Special themed tours focus on Islamic art, modern collections, and architectural features.',
                'nearby_attractions': 'Ferrari World (adjacent), Yas Island (5 km), Abu Dhabi city center (15 km).',
                'conservation': 'State-of-the-art climate control and security systems protect artworks.',
                'photos': [
                    'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '24.5333° N, 54.4000° E',
                'annual_visitors': 'Over 2 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'dubai-creek': {
                'id': 'dubai-creek',
                'name': 'Dubai Creek',
                'location': 'Dubai, UAE',
                'description': 'Historic waterway that has shaped Dubai\'s development, offering traditional dhow rides and cultural experiences.',
                'long_description': 'Dubai Creek is a saltwater creek that has played a pivotal role in Dubai\'s history and development. This natural inlet from the Arabian Gulf has served as a natural harbor for centuries, facilitating trade and transportation. Today, it divides the city into two parts - Deira and Bur Dubai - and offers visitors a glimpse into Dubai\'s maritime heritage with traditional wooden dhow boats, bustling souks, and waterfront promenades.',
                'historical_significance': 'Dubai Creek has been Dubai\'s lifeline since the 19th century when the Bani Yas tribe settled along its banks. The creek enabled Dubai to become a major trading hub for pearls, spices, and textiles. The discovery of oil in 1966 transformed Dubai, but the creek remains a symbol of the city\'s maritime heritage and traditional way of life. The creek has witnessed Dubai\'s transformation from a small fishing village to a global metropolis.',
                'discovery': 'Dubai Creek was first documented by British explorers in the early 19th century. The creek\'s strategic location made it a natural choice for settlement, with evidence of human habitation dating back thousands of years. The creek became internationally famous during Dubai\'s oil boom in the 1960s and 1970s, when it served as the primary transportation route for goods and people.',
                'architecture': 'The creek features traditional wind-tower houses (barjeel) that were designed to provide natural cooling through wind catchers. The Dhow Wharfage showcases Dubai\'s maritime architecture with traditional wooden boat building yards. Modern developments along the creek include contemporary bridges and waterfront promenades that blend traditional and modern architectural styles.',
                'cultural_impact': 'Dubai Creek represents the heart of traditional Emirati culture and maritime heritage. It has inspired numerous works of art, literature, and photography showcasing Dubai\'s transformation. The creek continues to be a gathering place for locals and tourists, preserving traditional practices while embracing modernity. It has become a symbol of Dubai\'s ability to maintain its cultural roots while embracing global change.',
                'facts': [
                    'Natural saltwater creek extending 14 km inland',
                    'Divides Dubai into Deira and Bur Dubai districts',
                    'Traditional dhow harbor with over 200 wooden boats',
                    'Historic trading center since the 19th century',
                    'Features the world\'s largest wooden dhow building yard',
                    'Home to Dubai Creek Park and promenade',
                    'UNESCO tentative World Heritage Site',
                    'Hosts the annual Dubai Creek Festival'
                ],
                'key_sites': [
                    {'name': 'Dhow Wharfage', 'slug': 'dhow-wharfage', 'description': 'Traditional wooden boat harbor and repair area', 'significance': 'Showcases Dubai\'s maritime heritage and boat-building tradition'},
                    {'name': 'Dubai Creek Park', 'slug': 'dubai-creek-park', 'description': 'Riverside park with walking paths and picnic areas', 'significance': 'Popular recreational area with views of the creek and city skyline'},
                    {'name': 'Al Seef', 'slug': 'al-seef', 'description': 'Heritage district with restored traditional buildings', 'significance': 'Preserves Dubai\'s architectural heritage from the 19th and 20th centuries'},
                    {'name': 'Creek Side Promenade', 'slug': 'creek-side-promenade', 'description': 'Waterfront walkway connecting Deira and Bur Dubai', 'significance': 'Offers scenic views and connects historic districts'}
                ],
                'entrance_fees': 'Free access to public areas. Abra rides: 1 AED per person.',
                'opening_hours': '24/7 access to public areas. Abra rides: 6:00 AM to 10:00 PM.',
                'best_time': 'Early morning or evening for cooler temperatures and fewer crowds.',
                'how_to_get_there': 'Located in central Dubai. Metro: Al Ras or Deira City Centre stations.',
                'what_to_wear': 'Comfortable clothing and shoes. Modest attire recommended.',
                'visitor_tips': [
                    'Take an abra ride across the creek for authentic experience',
                    'Visit during Dubai Creek Festival for special events',
                    'Explore the souks on both sides of the creek',
                    'Try traditional Emirati food at waterfront restaurants',
                    'Visit early morning to see fishermen and boat activity',
                    'Allow 2-3 hours to explore both sides'
                ],
                'nearby_attractions': 'Dubai Museum (adjacent), Al Fahidi Historical Neighbourhood (nearby), Gold Souk (walking distance).',
                'conservation': 'Dubai Creek is undergoing preservation efforts to maintain its cultural and environmental significance. The Dubai Future Foundation works to protect the creek\'s heritage while promoting sustainable development. Traditional boat building techniques are being preserved, and environmental monitoring ensures water quality is maintained.',
                'health_safety': 'Stay hydrated, especially during summer visits. Some areas may be slippery near water. Follow local guidelines and respect cultural sites. Avoid swimming in the creek due to strong currents and water quality concerns.',
                'guided_tours': 'Official guided tours are available through the Dubai Tourism Department. Local guides provide historical context and cultural insights. Boat tours offer unique perspectives of the creek and surrounding areas.',
                'photos': [
                    'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.2631° N, 55.3103° E',
                'annual_visitors': 'Over 5 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'jumeirah-beach': {
                'id': 'jumeirah-beach',
                'name': 'Jumeirah Beach',
                'location': 'Dubai, UAE',
                'description': 'Pristine beach along Dubai\'s coastline featuring luxury resorts, water sports, and stunning Arabian Gulf views.',
                'long_description': 'Jumeirah Beach is one of Dubai\'s most popular beaches, stretching along the Arabian Gulf coastline. This pristine sandy beach offers crystal-clear waters, luxury beach clubs, and a wide range of water sports activities. The beach is lined with some of Dubai\'s most iconic hotels and resorts, creating a perfect blend of relaxation and entertainment.',
                'facts': [
                    'Stretches over 7 km along Dubai\'s coastline',
                    'Features fine white sand and clear turquoise waters',
                    'Home to luxury beach clubs and resorts',
                    'Offers various water sports including jet skiing and parasailing',
                    'Part of Dubai\'s extensive beach network',
                    'Popular for sunset views and evening strolls',
                    'Accessible public areas with facilities',
                    'Temperature-controlled swimming pools available'
                ],
                'key_sites': [
                    {'name': 'Jumeirah Beach Park', 'slug': 'jumeirah-beach-park', 'description': 'Public beach area with facilities and activities', 'significance': 'Free public access with beach volleyball and picnic areas'},
                    {'name': 'Burj Al Arab Beach', 'slug': 'burj-al-arab-beach', 'description': 'Private beach area for Burj Al Arab guests', 'significance': 'Exclusive luxury beach experience'},
                    {'name': 'Wild Wadi Beach', 'slug': 'wild-wadi-beach', 'description': 'Beach area adjacent to the water park', 'significance': 'Family-friendly beach with water park access'},
                    {'name': 'Jumeirah Beach Residence Beach', 'slug': 'jumeirah-beach-residence-beach', 'description': 'Beachfront promenade with restaurants', 'significance': 'Modern beach area with dining and shopping'}
                ],
                'entrance_fees': 'Free public access. Beach clubs charge 50-200 AED for day passes.',
                'opening_hours': '24/7 access. Beach clubs: 10:00 AM to sunset.',
                'best_time': 'October to April for comfortable swimming temperatures.',
                'how_to_get_there': 'Located along Jumeirah Road. Taxi or private car recommended.',
                'what_to_wear': 'Swimwear at beach clubs. Modest attire in public areas.',
                'visitor_tips': [
                    'Visit beach clubs for premium facilities and service',
                    'Try water sports like jet skiing and parasailing',
                    'Bring sunscreen and stay hydrated',
                    'Visit during weekdays to avoid crowds',
                    'Enjoy sunset views from the beach',
                    'Check water quality and safety flags'
                ],
                'discovery': 'Jumeirah Beach was developed as part of Dubai\'s coastal reclamation and tourism development in the 1990s. The beach emerged as a premier recreational destination following the construction of luxury hotels and resorts along the shoreline. Its pristine white sand and clear waters quickly made it a favorite among locals and international visitors.',
                'architecture': 'The beach features modern beachfront architecture with luxury hotels and resorts designed to complement the natural coastal environment. Beach clubs incorporate contemporary design elements with traditional Arabian architectural influences. The promenade areas feature shaded walkways and recreational facilities integrated with the natural landscape.',
                'cultural_impact': 'Jumeirah Beach has become a cultural melting pot where traditional Emirati hospitality meets international tourism. It represents Dubai\'s transformation into a global beach destination and has influenced the development of similar coastal resorts across the UAE. The beach has become a symbol of Dubai\'s modern lifestyle and recreational excellence.',
                'conservation': 'Jumeirah Beach maintains strict environmental standards with regular water quality monitoring and beach cleaning programs. Sustainable practices include energy-efficient lighting for beach facilities and eco-friendly waste management. The beach supports marine conservation efforts and maintains natural dune ecosystems.',
                'health_safety': 'The beach has designated swimming areas with lifeguard supervision during operating hours. Safety flags indicate water conditions, and medical facilities are available at nearby resorts. Visitors should stay hydrated, use sunscreen, and follow local beach guidelines. Some areas may have strong currents.',
                'guided_tours': 'Beach resort tours are available through luxury hotels, offering insights into marine life and coastal ecosystems. Water sports operators provide guided activities with certified instructors. Cultural tours highlight the beach\'s role in Dubai\'s tourism development and traditional maritime activities.',
                'nearby_attractions': 'Burj Al Arab (adjacent), Wild Wadi Water Park (adjacent), Dubai Marina (2 km).',
                'photos': [
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.2333° N, 55.2667° E',
                'annual_visitors': 'Over 3 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'dubai-museum': {
                'id': 'dubai-museum',
                'name': 'Dubai Museum',
                'location': 'Dubai, UAE',
                'description': 'Located in Al Fahidi Fort, this museum chronicles Dubai\'s history from ancient times to modern development.',
                'long_description': 'Dubai Museum, housed in the restored Al Fahidi Fort, offers a comprehensive journey through Dubai\'s rich history. Built in 1787, the fort served as a defensive structure and government headquarters. The museum features archaeological artifacts, traditional exhibits, and interactive displays that showcase Dubai\'s transformation from a small fishing village to a global metropolis.',
                'historical_significance': 'Al Fahidi Fort was constructed in 1787 by order of Sheikh Maktoum bin Butti, founder of the Al Maktoum dynasty. It served as a defensive fortification, residence for rulers, and administrative center. The fort witnessed key events in Dubai\'s history and now preserves the city\'s heritage for future generations.',
                'facts': [
                    'Located in Dubai\'s oldest building, Al Fahidi Fort (1787)',
                    'Features archaeological finds from ancient settlements',
                    'Interactive exhibits on Bedouin life and pearl diving',
                    'Shows Dubai\'s transformation from fishing village to city',
                    'Includes traditional souk and wind tower house exhibits',
                    'Underground galleries with artifacts from 3,000 BCE',
                    'Multimedia presentations on modern Dubai',
                    'Regular cultural events and exhibitions'
                ],
                'key_sites': [
                    {'name': 'Archaeological Gallery', 'slug': 'archaeological-gallery', 'description': 'Underground exhibits of ancient artifacts', 'significance': 'Showcases finds from Dubai\'s earliest settlements'},
                    {'name': 'Traditional Life Gallery', 'slug': 'traditional-life-gallery', 'description': 'Reconstructed souk and traditional house', 'significance': 'Demonstrates pre-oil Dubai lifestyle'},
                    {'name': 'Pearl Diving Exhibit', 'slug': 'pearl-diving-exhibit', 'description': 'Interactive display on pearl diving industry', 'significance': 'Highlights Dubai\'s maritime heritage'},
                    {'name': 'Modern Dubai Gallery', 'slug': 'modern-dubai-gallery', 'description': 'Multimedia presentation of city\'s development', 'significance': 'Shows Dubai\'s rapid modernization'}
                ],
                'entrance_fees': '5 AED for adults. Free for children under 6.',
                'opening_hours': '8:30 AM to 8:30 PM Saturday-Thursday, 2:30 PM to 8:30 PM Friday.',
                'best_time': 'Early morning or late afternoon to avoid midday heat.',
                'how_to_get_there': 'Located near Dubai Creek. Walking distance from Abra station.',
                'what_to_wear': 'Comfortable clothing. Modest attire recommended.',
                'visitor_tips': [
                    'Start with the archaeological galleries',
                    'Allow 1-2 hours for complete visit',
                    'Audio guide available in multiple languages',
                    'Visit during cultural events for special programs',
                    'Combine with Al Fahidi Historical Neighbourhood',
                    'Photography allowed in most areas'
                ],
                'discovery': 'Dubai Museum was established in 1971 in the historic Al Fahidi Fort, making it one of the oldest museums in the UAE. The fort itself dates back to 1787 and served as a defensive structure during Dubai\'s early history. The museum was created to preserve and showcase Dubai\'s cultural heritage and archaeological finds.',
                'architecture': 'The museum is housed in the restored Al Fahidi Fort, featuring traditional Gulf architecture with wind towers for natural cooling. The fort\'s design includes thick walls, strategic defensive positions, and traditional construction methods. Modern museum facilities have been integrated while preserving the historic structure.',
                'cultural_impact': 'Dubai Museum plays a crucial role in preserving Emirati cultural heritage and educating visitors about the UAE\'s history. It has become a cornerstone of Dubai\'s cultural tourism, attracting visitors from around the world. The museum has inspired similar cultural preservation efforts across the UAE and contributed to national identity.',
                'conservation': 'The museum employs advanced conservation techniques to protect archaeological artifacts and maintain the historic fort structure. Climate-controlled environments preserve delicate items, and restoration work continues to maintain the building\'s architectural integrity. Educational programs promote cultural preservation awareness.',
                'health_safety': 'The museum maintains comfortable indoor temperatures with air conditioning. Wheelchair accessibility is available throughout the main areas. Security measures ensure visitor safety, and medical facilities are nearby. The museum recommends comfortable walking shoes due to extensive exploration.',
                'guided_tours': 'Official guided tours are available in multiple languages, providing historical context and detailed explanations of exhibits. Audio guides offer self-paced exploration with comprehensive information. Special themed tours focus on specific aspects of Dubai\'s history and culture.',
                'nearby_attractions': 'Al Fahidi Historical Neighbourhood (adjacent), Dubai Creek (walking distance), Gold Souk (nearby).',
                'photos': [
                    'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.2639° N, 55.2978° E',
                'annual_visitors': 'Over 500,000',
                'climate': 'Air-conditioned museum.'
            },
            'al-fahidi-historical': {
                'id': 'al-fahidi-historical',
                'name': 'Al Fahidi Historical Neighbourhood',
                'location': 'Dubai, UAE',
                'description': 'Dubai\'s oldest district featuring restored wind-tower houses, museums, and traditional architecture.',
                'long_description': 'Al Fahidi Historical Neighbourhood, also known as Bastakiya, is Dubai\'s oldest district and a UNESCO tentative World Heritage Site. This restored area features traditional wind-tower houses, narrow alleyways, and cultural institutions. The neighbourhood showcases Dubai\'s architectural heritage and serves as a cultural hub with art galleries, museums, and traditional crafts.',
                'historical_significance': 'Bastakiya was settled by Iranian merchants in the late 19th century. The distinctive wind-tower houses were designed to provide natural cooling through wind catchers. The area declined after the 1970s but was restored in the 1990s to preserve Dubai\'s cultural heritage.',
                'facts': [
                    'Dubai\'s oldest residential district',
                    'Features over 50 restored wind-tower houses',
                    'UNESCO tentative World Heritage Site',
                    'Traditional Iranian-influenced architecture',
                    'Wind towers provide natural air conditioning',
                    'Home to art galleries and cultural institutions',
                    'Features narrow alleyways and courtyards',
                    'Preserves pre-oil Dubai architecture'
                ],
                'key_sites': [
                    {'name': 'Wind Tower Houses', 'slug': 'wind-tower-houses', 'description': 'Traditional houses with distinctive wind catchers', 'significance': 'Showcase Persian Gulf architectural heritage'},
                    {'name': 'Majlis Gallery', 'slug': 'majlis-gallery', 'description': 'Contemporary art gallery in restored house', 'significance': 'Features rotating exhibitions of local and international artists'},
                    {'name': 'Bastakiya Art Fair', 'slug': 'bastakiya-art-fair', 'description': 'Annual art event in the neighbourhood', 'significance': 'Showcases contemporary art in historic setting'},
                    {'name': 'Traditional Courtyards', 'slug': 'traditional-courtyards', 'description': 'Restored open spaces with fountains', 'significance': 'Provide respite from heat and social gathering spaces'}
                ],
                'entrance_fees': 'Free access to public areas. Museum fees vary.',
                'opening_hours': 'Galleries typically 10:00 AM to 6:00 PM.',
                'best_time': 'Early morning or evening for cooler exploration.',
                'how_to_get_there': 'Near Dubai Creek. Walking distance from Dubai Museum.',
                'what_to_wear': 'Comfortable walking shoes. Modest attire.',
                'visitor_tips': [
                    'Explore the narrow alleyways on foot',
                    'Visit art galleries for contemporary exhibits',
                    'Try traditional Arabic coffee at local cafes',
                    'Attend Bastakiya Art Fair when in season',
                    'Combine with Dubai Museum visit',
                    'Allow 1-2 hours to explore thoroughly'
                ],
                'discovery': 'Al Fahidi Historical Neighbourhood was rediscovered in the 1990s when Dubai began its cultural preservation efforts. The area, originally settled by Iranian merchants in the late 19th century, had fallen into disrepair but was restored to preserve Dubai\'s architectural heritage. The restoration project transformed the neighbourhood into a living museum showcasing traditional Gulf architecture.',
                'architecture': 'The neighbourhood features distinctive wind-tower houses (barjeel) with traditional Persian Gulf architectural elements. The wind towers provide natural air conditioning through wind catchers, while the narrow alleyways and courtyards create shaded, comfortable spaces. Modern restoration has preserved the original construction methods while adding contemporary amenities.',
                'cultural_impact': 'Bastakiya has become a symbol of Dubai\'s commitment to cultural preservation amidst rapid modernization. It hosts art galleries, cultural events, and traditional crafts, serving as a bridge between Dubai\'s past and present. The neighbourhood has inspired similar preservation projects across the UAE and contributes to national cultural identity.',
                'conservation': 'Ongoing conservation efforts maintain the architectural integrity of the wind-tower houses and traditional structures. The Dubai Future Foundation supports preservation programs that balance tourism needs with cultural authenticity. Environmental monitoring ensures the neighbourhood remains a sustainable cultural destination.',
                'health_safety': 'The neighbourhood features shaded alleyways and courtyards that provide respite from heat. Security measures ensure visitor safety, and medical facilities are nearby. Visitors should wear comfortable walking shoes for the uneven traditional pathways and stay hydrated during exploration.',
                'guided_tours': 'Official guided tours are available through the Dubai Tourism Department, providing historical context and architectural insights. Local guides offer cultural experiences including traditional coffee ceremonies. Art gallery tours showcase contemporary Emirati artists and their work in historic settings.',
                'nearby_attractions': 'Dubai Museum (adjacent), Dubai Creek (walking distance), Gold Souk (nearby).',
                'photos': [
                    'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.2647° N, 55.2994° E',
                'annual_visitors': 'Over 1 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'dubai-frame': {
                'id': 'dubai-frame',
                'name': 'Dubai Frame',
                'location': 'Dubai, UAE',
                'description': 'Massive picture frame structure offering panoramic views of old and new Dubai from elevated platforms.',
                'long_description': 'Dubai Frame is a massive architectural structure designed as a giant picture frame, symbolizing Dubai\'s journey from past to present. Standing 150 meters tall, this modern monument offers visitors panoramic views of Dubai\'s historic and contemporary landscapes from its elevated observation platforms. The structure represents the frame of a picture, with old Dubai on one side and new Dubai on the other.',
                'historical_significance': 'Dubai Frame was inaugurated in 2018 as part of Dubai\'s 2020 urban regeneration project. The structure symbolizes Dubai\'s transformation from a small fishing village to a global metropolis. It represents the "frame" that connects Dubai\'s rich heritage with its futuristic vision.',
                'facts': [
                    '150 meters tall (equivalent to 50-story building)',
                    'Designed as a giant picture frame',
                    'Two observation decks at different heights',
                    'Bridges connect old and new Dubai symbolically',
                    'Features multimedia exhibits on Dubai\'s history',
                    'Night illumination creates stunning visual effects',
                    'Part of Dubai 2040 Urban Master Plan',
                    'Cost 170 million AED to construct'
                ],
                'key_sites': [
                    {'name': 'Upper Observation Deck', 'slug': 'upper-observation-deck', 'description': '360-degree views at 150 meters', 'significance': 'Highest public viewpoint in Dubai Frame'},
                    {'name': 'Lower Observation Deck', 'slug': 'lower-observation-deck', 'description': 'Views at 93 meters with glass floor', 'significance': 'Offers different perspective with transparent floor'},
                    {'name': 'Multimedia Gallery', 'slug': 'multimedia-gallery', 'description': 'Interactive exhibits on Dubai\'s history', 'significance': 'Educational displays on city\'s development'},
                    {'name': 'Bridge of Progress', 'slug': 'bridge-of-progress', 'description': 'Connecting bridge between platforms', 'significance': 'Symbolizes connection between past and future'}
                ],
                'entrance_fees': '50 AED for adults. Free for children under 6.',
                'opening_hours': '9:00 AM to 9:00 PM daily.',
                'best_time': 'Evening for illuminated views and cooler temperatures.',
                'how_to_get_there': 'Located in Zabeel Park. Metro: Dubai Frame station.',
                'what_to_wear': 'Comfortable clothing and shoes.',
                'visitor_tips': [
                    'Book tickets online to skip queues',
                    'Visit at sunset for spectacular views',
                    'Experience the glass floor on lower deck',
                    'Allow 1-2 hours for complete visit',
                    'Night visits offer illuminated city views',
                    'Photography encouraged from observation decks'
                ],
                'discovery': 'Dubai Frame was conceived as part of Dubai\'s urban regeneration project in 2018, symbolizing the city\'s transformation from traditional to modern. The structure represents a "frame" that captures both Dubai\'s heritage and its futuristic vision, offering visitors a unique perspective on the city\'s evolution through contrasting viewpoints of old and new Dubai.',
                'architecture': 'The 150-meter-tall structure is designed as a massive picture frame with two observation decks at different heights. The upper deck provides panoramic views at 150 meters, while the lower deck features a glass floor for a thrilling transparent experience. The design incorporates modern engineering with symbolic elements representing Dubai\'s journey from past to present.',
                'cultural_impact': 'Dubai Frame has become an iconic symbol of Dubai\'s modern identity, representing the city\'s ability to preserve heritage while embracing innovation. It serves as a cultural bridge between traditional and contemporary Dubai, attracting visitors from around the world and contributing to the city\'s global image as a destination that honors both history and progress.',
                'conservation': 'The structure incorporates sustainable design elements including energy-efficient lighting and materials. As part of Dubai\'s broader conservation efforts, Dubai Frame promotes environmental awareness through its exhibits on urban regeneration and sustainable development. The surrounding Zabeel Park contributes to green space preservation in the city.',
                'health_safety': 'The attraction features multiple safety measures including secure access controls, emergency evacuation procedures, and medical facilities nearby. Visitors should wear comfortable shoes for extended standing on observation decks and stay hydrated. The glass floor area has safety barriers, and staff monitor visitor capacity to ensure comfortable viewing conditions.',
                'guided_tours': 'Official guided tours are available in multiple languages, providing historical context about Dubai\'s development and architectural significance. Audio guides offer self-paced exploration with detailed information about the city\'s transformation. Special evening tours showcase the illuminated structure and night-time city views.',
                'nearby_attractions': 'Zabeel Park (surrounding), Dubai Miracle Garden (nearby), Dubai Safari Park (adjacent).',
                'photos': [
                    'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.2367° N, 55.3028° E',
                'annual_visitors': 'Over 2 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'dubai-miracle-garden': {
                'id': 'dubai-miracle-garden',
                'name': 'Dubai Miracle Garden',
                'location': 'Dubai, UAE',
                'description': 'World\'s largest flower garden featuring millions of flowers arranged in spectacular displays and sculptures.',
                'long_description': 'Dubai Miracle Garden is the world\'s largest flower garden, spanning 72,000 square meters and featuring over 150 million flowers. This floral paradise showcases spectacular displays including the world\'s largest flower sculpture, heart-shaped installations, and themed gardens. The garden represents Dubai\'s commitment to creating world-class attractions that celebrate nature and beauty.',
                'facts': [
                    'World\'s largest flower garden at 72,000 square meters',
                    'Features over 150 million flowers',
                    'World\'s largest flower sculpture (15 meters tall)',
                    'Over 250 varieties of flowers and plants',
                    'Heart-shaped installations and photo opportunities',
                    'Butterfly garden and children\'s play areas',
                    'Seasonal flower displays and themed gardens',
                    'Sustainable irrigation systems used throughout'
                ],
                'key_sites': [
                    {'name': 'World\'s Largest Flower Sculpture', 'description': '15-meter tall floral structure', 'significance': 'Guinness World Record holder and iconic photo spot'},
                    {'name': 'Heart of Love', 'slug': 'heart-of-love', 'description': 'Massive heart-shaped flower installation', 'significance': 'Popular romantic photo location'},
                    {'name': 'Butterfly Garden', 'slug': 'butterfly-garden', 'description': 'Enclosed garden with butterflies and flowers', 'significance': 'Interactive nature experience'},
                    {'name': 'Seasonal Gardens', 'slug': 'seasonal-gardens', 'description': 'Themed floral displays that change with seasons', 'significance': 'Showcases different flower varieties throughout year'}
                ],
                'entrance_fees': '60 AED for adults. 30 AED for children 3-12.',
                'opening_hours': '9:00 AM to 9:00 PM daily.',
                'best_time': 'Early morning or late afternoon. Cooler months October-April.',
                'how_to_get_there': 'Located in Al Barsha South. Taxi or private car recommended.',
                'what_to_wear': 'Comfortable walking shoes. Light clothing.',
                'visitor_tips': [
                    'Visit early morning to avoid heat and crowds',
                    'Bring water and stay hydrated',
                    'Allow 2-3 hours to explore all areas',
                    'Best photographed during golden hour',
                    'Wheelchair accessible throughout',
                    'Photography encouraged in all areas'
                ],
                'discovery': 'Dubai Miracle Garden was established in 2013 as part of Dubai\'s initiative to create world-class floral attractions. The garden emerged from Dubai\'s vision to transform desert landscapes into spectacular displays of nature and beauty, showcasing innovative horticulture in the Middle East. It represents Dubai\'s commitment to sustainable tourism and floral excellence.',
                'architecture': 'The garden spans 72,000 square meters with meticulously planned floral arrangements and sculptures. The design incorporates sustainable irrigation systems, shaded walkways, and themed areas that create immersive experiences. The world\'s largest flower sculpture and heart installations demonstrate advanced floral engineering and artistic design in a desert environment.',
                'cultural_impact': 'Dubai Miracle Garden has become a symbol of Dubai\'s ability to create beauty from barren landscapes, inspiring similar projects across the UAE and Middle East. It promotes environmental awareness and showcases sustainable horticulture practices. The garden has become a popular destination for families, couples, and tourists seeking natural beauty in an urban setting.',
                'conservation': 'The garden implements advanced water conservation techniques and sustainable horticulture practices. It uses recycled water systems and energy-efficient operations to minimize environmental impact. Conservation programs educate visitors about desert agriculture and floral biodiversity, contributing to broader environmental awareness in the region.',
                'health_safety': 'The garden features shaded walkways and covered areas to protect visitors from heat. Medical facilities are available on-site, and staff monitor visitor safety throughout the park. Wheelchair accessibility ensures inclusive access for all visitors, with smooth pathways and ramps throughout the garden.',
                'guided_tours': 'Official guided tours provide insights into the garden\'s horticulture and floral arrangements. Photography tours help visitors capture the best shots of the flower displays. Family-oriented tours include interactive elements and educational content about plants and sustainability.',
                'nearby_attractions': 'Dubai Butterfly Garden (adjacent), Dubai Frame (nearby), Mall of Emirates (5 km).',
                'photos': [
                    'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.0667° N, 55.2333° E',
                'annual_visitors': 'Over 1.5 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'global-village-dubai': {
                'id': 'global-village-dubai',
                'name': 'Global Village Dubai',
                'description': 'Cultural theme park showcasing pavilions from around the world with food, entertainment, and shopping.',
                'long_description': 'Global Village Dubai is a cultural theme park that brings the world to Dubai through authentic reproductions of famous landmarks and cultural pavilions. Featuring over 30 international pavilions, the park offers visitors a journey through global cultures with traditional food, shopping, entertainment, and architectural displays. It\'s one of Dubai\'s most popular seasonal attractions.',
                'facts': [
                    'Spans 17.5 million square feet (1.6 million square meters)',
                    'Features over 30 international pavilions',
                    'Authentic reproductions of world landmarks',
                    'Over 100 restaurants serving international cuisine',
                    'Daily cultural performances and shows',
                    'Seasonal attraction open October-April',
                    'Features shopping, entertainment, and dining',
                    'Accommodates up to 30,000 visitors daily'
                ],
                'key_sites': [
                    {'name': 'International Pavilions', 'slug': 'international-pavilions', 'description': 'Authentic reproductions of world landmarks', 'significance': 'Showcase architecture and culture from different countries'},
                    {'name': 'Cultural Shows', 'slug': 'cultural-shows', 'description': 'Daily performances of traditional dances and music', 'significance': 'Entertainment featuring artists from around the world'},
                    {'name': 'Food Court', 'slug': 'food-court', 'description': 'Diverse international cuisine options', 'significance': 'Culinary journey through global flavors'},
                    {'name': 'Shopping Areas', 'slug': 'shopping-areas', 'description': 'Traditional crafts and souvenirs', 'significance': 'Authentic handicrafts from different cultures'}
                ],
                'entrance_fees': '15 AED for adults. Free for children under 3.',
                'opening_hours': '4:00 PM to 12:00 AM daily (seasonal).',
                'best_time': 'Evening for cooler temperatures and night shows.',
                'how_to_get_there': 'Located in Dubai Festival City. Free shuttle from nearby malls.',
                'what_to_wear': 'Comfortable casual attire.',
                'visitor_tips': [
                    'Visit in the evening for cooler weather',
                    'Try food from different country pavilions',
                    'Watch cultural performances at designated times',
                    'Allow 3-4 hours to explore thoroughly',
                    'Free parking and shuttle services available',
                    'Best experienced with family or groups'
                ],
                'discovery': 'Global Village Dubai opened in 1997 as Dubai\'s first cultural theme park, evolving from a small seasonal market to a major international attraction. The park was created to bring world cultures to Dubai residents and visitors, fostering cultural exchange and understanding. It has grown to become one of the largest seasonal attractions in the Middle East.',
                'architecture': 'The park features authentic reproductions of iconic world landmarks and cultural buildings from different countries. Each pavilion showcases traditional architectural styles and designs, from European castles to Asian temples. The layout creates a global journey through diverse architectural traditions, with themed entertainment areas and cultural displays.',
                'cultural_impact': 'Global Village has become a bridge between cultures, promoting understanding and appreciation of global diversity. It serves as an educational platform for cultural exchange and has influenced similar cultural attractions across the UAE. The park contributes to Dubai\'s image as a cosmopolitan city that celebrates international cultures.',
                'conservation': 'The park incorporates sustainable practices in its seasonal operations, including energy-efficient lighting and waste management systems. Cultural preservation efforts ensure authentic representations of world landmarks and traditions. Environmental initiatives include green spaces and water conservation measures throughout the park.',
                'health_safety': 'The park maintains high safety standards with security personnel, emergency medical services, and crowd management systems. Shaded areas and covered walkways provide protection from weather. Accessibility features ensure inclusive access for visitors with disabilities, with ramps and accessible facilities throughout.',
                'guided_tours': 'Cultural guided tours explore different country pavilions with historical and cultural context. Family tours include interactive elements and cultural performances. Photography tours help visitors capture the best views of the international landmarks and cultural displays.',
                'nearby_attractions': 'Dubai Festival City (adjacent), Dubai Miracle Garden (nearby), Dubai Frame (5 km).',
                'photos': [
                    'https://images.unsplash.com/photo-1542204165-65bf26472b9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.0667° N, 55.3000° E',
                'annual_visitors': 'Over 5 million',
                'climate': 'Desert climate. Seasonal attraction.'
            },
            'ferrari-world-abu-dhabi': {
                'id': 'ferrari-world-abu-dhabi',
                'name': 'Ferrari World Abu Dhabi',
                'location': 'Abu Dhabi, UAE',
                'description': 'High-speed racing theme park featuring the world\'s fastest roller coaster and Ferrari experiences.',
                'long_description': 'Ferrari World Abu Dhabi is a racing-themed amusement park located on Yas Island. This Ferrari-branded attraction features the world\'s fastest roller coaster, interactive racing experiences, and exhibits showcasing Ferrari\'s racing heritage. The park offers a complete Ferrari experience with rides, shows, and merchandise.',
                'facts': [
                    'World\'s first Ferrari-themed amusement park',
                    'Features Formula Rossa, world\'s fastest roller coaster (240 km/h)',
                    'Spans 200,000 square meters',
                    'Over 20 rides and attractions',
                    'Interactive racing simulators and go-kart tracks',
                    'Ferrari merchandise and memorabilia',
                    'Multiple restaurants and food outlets',
                    'Capacity for 30,000 visitors daily'
                ],
                'key_sites': [
                    {'name': 'Formula Rossa', 'slug': 'formula-rossa', 'description': 'World\'s fastest roller coaster reaching 240 km/h', 'significance': 'Guinness World Record holder and park\'s signature ride'},
                    {'name': 'Racing Legends', 'slug': 'racing-legends', 'description': 'Interactive exhibit on Ferrari\'s racing history', 'significance': 'Showcases Ferrari\'s championship-winning cars'},
                    {'name': 'Junior GP Karting', 'slug': 'junior-gp-karting', 'description': 'Go-kart track for children and families', 'significance': 'Safe racing experience for younger visitors'},
                    {'name': 'Ferrari Racing Academy', 'slug': 'ferrari-racing-academy', 'description': 'Professional racing simulators', 'significance': 'High-tech racing experience with real F1 cars'}
                ],
                'entrance_fees': '295 AED for adults. 255 AED for children 3-12.',
                'opening_hours': '11:00 AM to 8:00 PM Saturday-Wednesday, 11:00 AM to 10:00 PM Thursday-Friday.',
                'best_time': 'Early morning or evening to avoid peak heat.',
                'how_to_get_there': 'Located on Yas Island. Free shuttle from Yas Mall.',
                'what_to_wear': 'Comfortable clothing and closed-toe shoes.',
                'visitor_tips': [
                    'Book tickets online for faster entry',
                    'Ride Formula Rossa first before lines get long',
                    'Stay hydrated and use sunscreen',
                    'Allow 4-6 hours for full park experience',
                    'Wheelchair accessible throughout',
                    'Photography allowed in most areas'
                ],
                'discovery': 'Ferrari World Abu Dhabi opened in 2010 as the world\'s first Ferrari-themed amusement park, built on Yas Island. The park emerged from Abu Dhabi\'s vision to create world-class entertainment attractions and celebrate automotive excellence. It represents the partnership between Italian automotive heritage and Emirati hospitality.',
                'architecture': 'The park\'s design incorporates Ferrari\'s racing heritage with modern amusement park architecture. The signature red structures and racing-themed buildings create an immersive Ferrari experience. The layout includes high-speed roller coaster tracks, interactive exhibit halls, and themed entertainment areas that showcase automotive engineering.',
                'cultural_impact': 'Ferrari World has become a symbol of Abu Dhabi\'s emergence as a global entertainment destination, blending Italian racing culture with Emirati values. It has influenced motorsport tourism in the UAE and contributed to the development of Yas Island as an entertainment hub. The park promotes automotive heritage and engineering excellence.',
                'conservation': 'The park implements energy-efficient systems and sustainable practices in its operations. Water conservation measures and waste management systems minimize environmental impact. Ferrari World supports conservation education through exhibits on automotive technology and sustainable racing practices.',
                'health_safety': 'Comprehensive safety measures include trained staff, emergency response systems, and medical facilities. Ride safety protocols ensure visitor security on high-speed attractions. Heat protection measures and hydration stations address desert climate challenges, with shaded areas throughout the park.',
                'guided_tours': 'Racing heritage tours provide insights into Ferrari\'s history and Abu Dhabi\'s motorsport legacy. VIP tours offer exclusive access to exhibits and behind-the-scenes areas. Family tours include interactive elements and educational content about automotive engineering.',
                'nearby_attractions': 'Yas Marina Circuit (adjacent), Yas Waterworld (nearby), Louvre Abu Dhabi (10 km).',
                'photos': [
                    'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '24.4833° N, 54.6167° E',
                'annual_visitors': 'Over 2 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'yas-marina-circuit': {
                'id': 'yas-marina-circuit',
                'name': 'Yas Marina Circuit',
                'location': 'Abu Dhabi, UAE',
                'description': 'F1 race track and entertainment complex hosting the Abu Dhabi Grand Prix and various events.',
                'long_description': 'Yas Marina Circuit is a motor racing circuit on Yas Island, Abu Dhabi. The track hosts the Abu Dhabi Grand Prix, the final race of the Formula One World Championship. Beyond racing, the circuit features entertainment venues, restaurants, and attractions that operate year-round, making it a major tourist destination.',
                'facts': [
                    'Hosts Abu Dhabi Grand Prix, final F1 race of season',
                    'Track length of 5.554 km (3.451 miles)',
                    'Features Yas Marina Hotel built into the circuit',
                    'Capacity for 60,000 spectators',
                    'Year-round entertainment and dining venues',
                    'Home to Ferrari World Abu Dhabi',
                    'Features the world\'s first circuit hotel',
                    'Hosts various motorsport and entertainment events'
                ],
                'key_sites': [
                    {'name': 'F1 Race Track', 'slug': 'f1-race-track', 'description': 'Professional Formula One circuit', 'significance': 'Hosts Abu Dhabi Grand Prix and other racing events'},
                    {'name': 'Yas Marina Hotel', 'slug': 'yas-marina-hotel', 'description': 'Hotel built into the circuit with track views', 'significance': 'Unique accommodation with F1 racing views'},
                    {'name': 'Entertainment Venues', 'slug': 'entertainment-venues', 'description': 'Restaurants, bars, and entertainment complexes', 'significance': 'Year-round dining and entertainment options'},
                    {'name': 'VIP Areas', 'slug': 'vip-areas', 'description': 'Premium viewing and hospitality areas', 'significance': 'Exclusive experiences during race weekends'}
                ],
                'entrance_fees': 'Varies by event. Circuit tours available when no events.',
                'opening_hours': 'Varies by events. Entertainment areas open daily.',
                'best_time': 'During Abu Dhabi Grand Prix (December) or other events.',
                'how_to_get_there': 'Located on Yas Island. Taxi or private car recommended.',
                'what_to_wear': 'Casual attire for entertainment, smart casual for events.',
                'visitor_tips': [
                    'Book Grand Prix tickets well in advance',
                    'Visit Ferrari World while at the circuit',
                    'Explore dining options in entertainment areas',
                    'Take circuit tours when available',
                    'Best experienced during race weekends',
                    'Allow time for traffic during events'
                ],
                'discovery': 'Yas Marina Circuit was inaugurated in 2009 as the venue for the Abu Dhabi Grand Prix, the final race of the Formula One World Championship. The circuit was built on Yas Island as part of Abu Dhabi\'s strategy to become a global motorsport destination. It represents the emirate\'s investment in world-class sporting infrastructure.',
                'architecture': 'The circuit features a unique design with the Yas Marina Hotel built directly over the track, creating a one-of-a-kind architectural landmark. The track layout incorporates challenging corners and high-speed straights, with the iconic hotel providing a stunning backdrop. Modern engineering ensures safety and performance for both racing and entertainment.',
                'cultural_impact': 'Yas Marina Circuit has elevated Abu Dhabi\'s global profile as a premier motorsport destination and contributed to the development of Yas Island as an entertainment complex. It has inspired motorsport tourism across the UAE and fostered international sporting events. The circuit represents Abu Dhabi\'s commitment to excellence in sports and entertainment.',
                'conservation': 'The circuit incorporates sustainable design elements including energy-efficient lighting and water conservation systems. Environmental monitoring ensures minimal impact on the surrounding marine ecosystem. The venue supports conservation through educational programs about motorsport and environmental stewardship.',
                'health_safety': 'Comprehensive safety protocols include advanced track security systems, emergency medical services, and crowd management during events. The circuit maintains high safety standards for both race weekends and public visits. Medical facilities and security personnel ensure visitor safety throughout the venue.',
                'guided_tours': 'Circuit tours provide behind-the-scenes access to the track and pit areas. Grand Prix experience tours offer insights into Formula One racing. VIP tours include access to the Yas Marina Hotel and exclusive viewing areas during events.',
                'nearby_attractions': 'Ferrari World Abu Dhabi (adjacent), Yas Waterworld (nearby), Louvre Abu Dhabi (10 km).',
                'photos': [
                    'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '24.4833° N, 54.6167° E',
                'annual_visitors': 'Over 3 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'abu-dhabi-corniche': {
                'id': 'abu-dhabi-corniche',
                'name': 'Abu Dhabi Corniche',
                'description': 'Scenic waterfront promenade featuring beaches, parks, luxury hotels, and stunning Arabian Gulf views.',
                'long_description': 'Abu Dhabi Corniche is a stunning waterfront promenade that stretches along the Arabian Gulf coastline. This scenic area features pristine beaches, lush parks, luxury hotels, and modern architecture. It serves as Abu Dhabi\'s premier recreational area, offering residents and visitors a perfect blend of relaxation, entertainment, and cultural experiences.',
                'facts': [
                    'Stretches 7 km along Abu Dhabi\'s coastline',
                    'Features pristine beaches and waterfront promenade',
                    'Home to luxury hotels and modern architecture',
                    'Multiple parks and recreational areas',
                    'Popular for jogging, cycling, and picnics',
                    'Features the iconic Abu Dhabi skyline views',
                    'Evening entertainment with fountains and lights',
                    'Cultural events and festivals held regularly'
                ],
                'key_sites': [
                    {'name': 'Corniche Beach', 'slug': 'corniche-beach', 'description': 'Pristine sandy beach with facilities', 'significance': 'Popular swimming and relaxation area'},
                    {'name': 'Emirates Palace Hotel', 'slug': 'emirates-palace-hotel', 'description': 'Luxury hotel with corniche views', 'significance': 'Iconic landmark and hospitality venue'},
                    {'name': 'Corniche Park', 'slug': 'corniche-park', 'description': 'Green spaces with walking paths', 'significance': 'Recreational area for outdoor activities'},
                    {'name': 'Waterfront Promenade', 'slug': 'waterfront-promenade', 'description': 'Scenic walkway with shops and cafes', 'significance': 'Popular for evening strolls and dining'}
                ],
                'entrance_fees': 'Free access to public areas.',
                'opening_hours': '24/7 access to promenade.',
                'best_time': 'Evening for cooler temperatures and illuminated views.',
                'how_to_get_there': 'Central Abu Dhabi location. Walking distance from many hotels.',
                'what_to_wear': 'Casual attire. Swimwear at designated beach areas.',
                'visitor_tips': [
                    'Visit during evening for spectacular views',
                    'Rent bikes for scenic rides along the promenade',
                    'Try waterfront dining at beach clubs',
                    'Watch the sunset from the corniche',
                    'Join locals for evening walks',
                    'Allow 2-3 hours to explore the full length'
                ],
                'discovery': 'Abu Dhabi Corniche was developed in the 1960s as part of the city\'s modernization efforts, transforming coastal land into a scenic waterfront promenade. The corniche emerged from Abu Dhabi\'s urban planning vision to create public spaces that blend traditional culture with modern amenities. It has evolved into the city\'s premier recreational area.',
                'architecture': 'The corniche features a harmonious blend of modern architecture with traditional Islamic design elements. Luxury hotels, contemporary sculptures, and landscaped gardens line the waterfront. The promenade incorporates sustainable design with shaded walkways, fountains, and recreational facilities that create an inviting public space.',
                'cultural_impact': 'The Corniche has become the heart of Abu Dhabi\'s social and cultural life, serving as a gathering place for locals and visitors. It represents Abu Dhabi\'s identity as a modern Islamic city that values public spaces and community. The corniche has influenced urban planning across the UAE and become a symbol of the emirate\'s development.',
                'conservation': 'The corniche incorporates environmental protection measures including marine ecosystem preservation and sustainable landscaping. Water features and green spaces contribute to urban biodiversity. Conservation efforts focus on maintaining the natural coastal environment while providing recreational amenities.',
                'health_safety': 'The promenade features well-lit pathways, security cameras, and regular patrols ensuring visitor safety. Medical facilities are nearby, and the design includes shaded areas for heat protection. Accessibility features ensure inclusive access for all visitors along the waterfront.',
                'guided_tours': 'Cultural walking tours explore the corniche\'s history and architecture. Photography tours capture the best views of the waterfront and skyline. Evening tours showcase the illuminated landmarks and waterfront entertainment.',
                'nearby_attractions': 'Emirates Palace (adjacent), Heritage Village (nearby), Abu Dhabi Mall (2 km).',
                'photos': [
                    'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '24.4667° N, 54.3667° E',
                'annual_visitors': 'Over 10 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'dubai-aquarium': {
                'id': 'dubai-aquarium',
                'name': 'Dubai Aquarium',
                'location': 'Dubai, UAE',
                'description': 'Massive underwater aquarium featuring a 270-degree viewing tunnel and thousands of marine species.',
                'long_description': 'Dubai Aquarium & Underwater Zoo is one of the world\'s largest suspended aquariums, featuring a massive 270-degree viewing tunnel. The aquarium houses over 33,000 marine animals representing 140 species, including sharks, rays, and colorful tropical fish. It offers an immersive underwater experience with interactive exhibits and educational programs.',
                'facts': [
                    'World\'s largest suspended aquarium',
                    '270-degree viewing tunnel (51 meters long)',
                    'Over 33,000 marine animals',
                    '140 different species including sharks and rays',
                    '10 million liters of water',
                    'Features underwater restaurant and hotel',
                    'Interactive touch pools and exhibits',
                    'Educational programs and conservation focus'
                ],
                'key_sites': [
                    {'name': 'Main Viewing Tunnel', 'slug': 'main-viewing-tunnel', 'description': '51-meter suspended tunnel with marine life', 'significance': 'Immersive underwater experience with sharks swimming overhead'},
                    {'name': 'Shark Aquarium', 'slug': 'shark-aquarium', 'description': 'Dedicated shark exhibit with various species', 'significance': 'Features sand tiger sharks, hammerheads, and reef sharks'},
                    {'name': 'Ray Lagoon', 'slug': 'ray-lagoon', 'description': 'Interactive area with stingrays', 'significance': 'Touch and feed experience with gentle rays'},
                    {'name': 'Penguin Expedition', 'slug': 'penguin-expedition', 'description': 'Antarctic penguin habitat', 'significance': 'Climate-controlled environment for penguin species'}
                ],
                'entrance_fees': 'Dubai Aquarium: 95 AED. Underwater Zoo: 140 AED. Combined: 185 AED.',
                'opening_hours': '10:00 AM to 10:00 PM daily.',
                'best_time': 'Early morning or late afternoon to avoid crowds.',
                'how_to_get_there': 'Located in Dubai Mall. Direct access from mall.',
                'what_to_wear': 'Comfortable clothing and shoes.',
                'visitor_tips': [
                    'Book tickets online to skip queues',
                    'Visit early morning for fewer crowds',
                    'Allow 2-3 hours for complete experience',
                    'Photography allowed throughout',
                    'Wheelchair accessible',
                    'Touch pools available for interactive experience'
                ],
                'discovery': 'Dubai Aquarium opened in 2008 as part of Dubai Mall, emerging from Dubai\'s vision to create world-class entertainment and educational attractions. The aquarium was designed to showcase marine biodiversity and provide immersive underwater experiences. It represents Dubai\'s commitment to combining entertainment with environmental education.',
                'architecture': 'The aquarium features a massive 270-degree viewing tunnel suspended within a 10 million liter tank, creating an immersive underwater experience. The design incorporates modern aquarium technology with educational exhibits and interactive displays. The underwater restaurant and hotel add unique architectural elements to the marine experience.',
                'cultural_impact': 'Dubai Aquarium has become a cultural landmark that promotes marine conservation awareness and environmental education. It has influenced aquarium design worldwide and contributed to Dubai\'s reputation as an innovative entertainment destination. The attraction fosters appreciation for marine ecosystems and biodiversity.',
                'conservation': 'The aquarium supports marine conservation through breeding programs and educational exhibits. Sustainable practices include energy-efficient systems and water recycling. Conservation partnerships work to protect marine species and promote ocean awareness among visitors.',
                'health_safety': 'The facility maintains strict safety protocols with trained staff and emergency response systems. Accessibility features ensure inclusive access for all visitors. Medical facilities are available on-site, and the climate-controlled environment provides comfort throughout the visit.',
                'guided_tours': 'Marine biology tours provide educational insights into aquatic life and conservation. Family tours include interactive elements and touch pool experiences. Photography tours help visitors capture the best underwater views and marine life.',
                'nearby_attractions': 'Dubai Mall (connected), Burj Khalifa (adjacent), Dubai Fountain (nearby).',
                'photos': [
                    'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.1972° N, 55.2791° E',
                'annual_visitors': 'Over 5 million',
                'climate': 'Air-conditioned aquarium.'
            },
            'ski-dubai': {
                'id': 'ski-dubai',
                'name': 'Ski Dubai',
                'location': 'Dubai, UAE',
                'description': 'Indoor ski resort in the desert featuring slopes, penguins, and winter activities year-round.',
                'long_description': 'Ski Dubai is the Middle East\'s first indoor ski resort, located inside Mall of the Emirates. This climate-controlled facility features five different slopes, a penguin habitat, and various winter activities. Despite being in the desert, Ski Dubai offers a complete winter sports experience with real snow and ice.',
                'facts': [
                    'Middle East\'s first indoor ski resort',
                    'Five different ski slopes of varying difficulty',
                    'Temperature maintained at -1°C to -6°C',
                    'Features 22,500 square meters of skiable area',
                    'Home to penguins in climate-controlled habitat',
                    'Snow park with jumps and rails',
                    'Ski and snowboard rental available',
                    'Professional instruction for all levels'
                ],
                'key_sites': [
                    {'name': 'Main Slope', 'slug': 'main-slope', 'description': 'Primary ski run for all skill levels', 'significance': 'Features varying difficulty sections'},
                    {'name': 'Snow Park', 'slug': 'snow-park', 'description': 'Terrain park with jumps and obstacles', 'significance': 'For advanced skiers and snowboarders'},
                    {'name': 'Penguin Habitat', 'slug': 'penguin-habitat', 'description': 'Climate-controlled enclosure with Gentoo penguins', 'significance': 'Unique desert-meets-Arctic experience'},
                    {'name': 'Kids\' Slope', 'description': 'Gentle slope for children and beginners', 'significance': 'Safe learning environment for young skiers'}
                ],
                'entrance_fees': 'Basic entry: 260 AED. Premium packages: 350-450 AED.',
                'opening_hours': '10:00 AM to 11:00 PM Sunday-Wednesday, 10:00 AM to 12:00 AM Thursday-Saturday.',
                'best_time': 'Early morning for fewer crowds and better snow conditions.',
                'how_to_get_there': 'Located in Mall of the Emirates. Direct access from mall.',
                'what_to_wear': 'Warm clothing provided. Gloves and hats recommended.',
                'visitor_tips': [
                    'Book lessons in advance for beginners',
                    'Warm clothing and gloves provided at entrance',
                    'Visit penguin habitat for unique experience',
                    'Allow 2-4 hours depending on activities',
                    'Photography allowed throughout',
                    'Best experienced with family or groups'
                ],
                'discovery': 'Ski Dubai opened in 2005 as the Middle East\'s first indoor ski resort, revolutionizing winter sports in desert climates. The resort emerged from Dubai\'s innovative approach to creating year-round recreational attractions. It represents Dubai\'s ability to engineer winter experiences in tropical environments.',
                'architecture': 'The resort features a climate-controlled dome maintaining sub-zero temperatures with real snow surfaces. The design includes multiple ski slopes, a snow park, and integrated penguin habitat. Advanced refrigeration technology creates authentic winter conditions within a desert environment.',
                'cultural_impact': 'Ski Dubai has become a symbol of Dubai\'s engineering innovation and ability to create impossible attractions. It has influenced indoor ski resort design worldwide and contributed to Dubai\'s image as a city of superlatives. The resort promotes winter sports culture in non-traditional climates.',
                'conservation': 'The resort incorporates energy-efficient refrigeration systems and sustainable practices. Environmental monitoring ensures minimal ecological impact. Conservation education focuses on climate science and the importance of polar ecosystems through the penguin habitat.',
                'health_safety': 'Comprehensive safety measures include ski patrol, medical facilities, and equipment safety checks. Professional instruction ensures appropriate skill levels for slope access. The controlled environment provides protection from external weather while maintaining safe recreational conditions.',
                'guided_tours': 'Ski instruction tours provide lessons for all skill levels. Penguin habitat tours offer insights into Antarctic wildlife. Family tours combine skiing experiences with educational elements about winter sports and climate.',
                'nearby_attractions': 'Mall of the Emirates (connected), Dubai Miracle Garden (nearby), Wild Wadi Water Park (adjacent).',
                'photos': [
                    'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.1183° N, 55.2000° E',
                'annual_visitors': 'Over 1 million',
                'climate': 'Artificially maintained winter conditions.'
            },
            'atlantis-the-palm': {
                'id': 'atlantis-the-palm',
                'name': 'Atlantis The Palm',
                'location': 'Dubai, UAE',
                'description': 'Luxury resort on Palm Jumeirah featuring water park, marine attractions, and underwater experiences.',
                'long_description': 'Atlantis The Palm is a luxury beach resort located at the tip of Palm Jumeirah. This iconic hotel features a massive water park, marine-themed attractions, and underwater experiences. The resort offers a complete entertainment experience with dining, shopping, and recreational facilities.',
                'facts': [
                    'Features world\'s largest open-air marine habitat',
                    'Over 1,500 marine species in aquarium',
                    'Water park with 30+ slides and attractions',
                    'Underwater restaurant with ocean views',
                    'Private beach and lagoon',
                    'Multiple dining options from casual to fine dining',
                    'Spa and wellness facilities',
                    'Capacity for 1,500 guests'
                ],
                'key_sites': [
                    {'name': 'Aquaventure Water Park', 'slug': 'aquaventure-water-park', 'description': 'Massive water park with slides and marine habitats', 'significance': 'Features world\'s largest open-air marine habitat'},
                    {'name': 'The Lost Chambers Aquarium', 'slug': 'the-lost-chambers-aquarium', 'description': 'Underwater aquarium with marine exhibits', 'significance': 'Showcases over 65,000 marine creatures'},
                    {'name': 'Underwater Suite', 'slug': 'underwater-suite', 'description': 'Luxury suite with underwater views', 'significance': 'Unique accommodation with marine life views'},
                    {'name': 'Dolphin Bay', 'slug': 'dolphin-bay', 'description': 'Interactive dolphin and sea lion shows', 'significance': 'Educational and entertaining marine performances'}
                ],
                'entrance_fees': 'Water park day pass: 350 AED. Aquarium: 100 AED.',
                'opening_hours': 'Water park: 10:00 AM to 6:00 PM. Hotel facilities vary.',
                'best_time': 'October to April for outdoor activities.',
                'how_to_get_there': 'Located at Palm Jumeirah tip. Taxi or private car recommended.',
                'what_to_wear': 'Swimwear for water park. Smart casual for dining.',
                'visitor_tips': [
                    'Book water park tickets online in advance',
                    'Visit early morning to avoid peak heat',
                    'Try the underwater restaurant experience',
                    'Allow full day for complete exploration',
                    'Wheelchair accessible throughout',
                    'Photography encouraged in most areas'
                ],
                'discovery': 'Atlantis The Palm opened in 2008 as the centerpiece of Palm Jumeirah, emerging from Dubai\'s ambitious land reclamation and tourism development projects. The resort represents the culmination of engineering innovation and luxury hospitality. It was designed to create a mythical underwater experience in the desert.',
                'architecture': 'The resort features distinctive architectural elements including an underwater suite and marine-themed design. The Aquaventure water park incorporates natural rock formations and marine habitats. The structure blends modern luxury with oceanic themes, creating an immersive underwater fantasy world.',
                'cultural_impact': 'Atlantis has become an iconic symbol of Dubai\'s architectural ambition and hospitality excellence. It has influenced resort design worldwide and contributed to Dubai\'s reputation as a destination for extraordinary experiences. The resort promotes marine conservation and environmental awareness through its exhibits.',
                'conservation': 'The resort supports marine conservation through its extensive aquarium and breeding programs. Sustainable practices include energy-efficient systems and water conservation measures. Environmental education focuses on ocean ecosystems and marine biodiversity protection.',
                'health_safety': 'Comprehensive safety protocols include lifeguard supervision, medical facilities, and emergency response systems. The resort maintains high standards for water park safety and guest security. Accessibility features ensure inclusive access throughout the property.',
                'guided_tours': 'Marine discovery tours explore the aquarium and underwater habitats. Resort tours showcase the architectural features and luxury accommodations. Family tours combine water park experiences with educational marine exhibits.',
                'nearby_attractions': 'Palm Jumeirah (surrounding), Dubai Marina (nearby), Burj Al Arab (adjacent).',
                'photos': [
                    'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.1300° N, 55.1172° E',
                'annual_visitors': 'Over 2 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'wild-wadi-water-park': {
                'id': 'wild-wadi-water-park',
                'name': 'Wild Wadi Water Park',
                'location': 'Dubai, UAE',
                'description': 'Adventure water park featuring thrilling slides, wave pools, and family-friendly attractions.',
                'long_description': 'Wild Wadi Water Park is Dubai\'s premier water adventure park, featuring over 30 thrilling slides and attractions. Inspired by the Arabian Nights tales, the park offers a complete water adventure experience with slides for all ages, wave pools, lazy rivers, and family-friendly areas.',
                'facts': [
                    'Over 30 slides and water attractions',
                    'Features Jumeirah Sceirah, world\'s largest water coaster',
                    'Wave pool with 3-meter waves',
                    'Lazy river and family play areas',
                    'Capacity for 5,000 visitors daily',
                    'Multiple restaurants and food outlets',
                    'Changing facilities and lockers available',
                    'Lifeguards and safety measures throughout'
                ],
                'key_sites': [
                    {'name': 'Jumeirah Sceirah', 'slug': 'jumeirah-sceirah', 'description': 'World\'s largest water coaster with dark ride elements', 'significance': 'Signature attraction combining coaster and water slide'},
                    {'name': 'Burj Suraj', 'slug': 'burj-suraj', 'description': 'Multi-level water playground', 'significance': 'Family-friendly area with various slides'},
                    {'name': 'Riptide Racers', 'slug': 'riptide-racers', 'description': '4-person racing slides', 'significance': 'Thrilling competition between friends'},
                    {'name': 'Wave Pool', 'slug': 'wave-pool', 'description': 'Large pool with generated waves', 'significance': 'Surfing and wave-riding experience'}
                ],
                'entrance_fees': 'Adult day pass: 295 AED. Child day pass: 265 AED.',
                'opening_hours': '10:00 AM to 6:00 PM daily (seasonal).',
                'best_time': 'October to April for comfortable temperatures.',
                'how_to_get_there': 'Located next to Burj Al Arab. Taxi or private car recommended.',
                'what_to_wear': 'Swimwear required. Bring sunscreen and hat.',
                'visitor_tips': [
                    'Book tickets online to skip queues',
                    'Visit early morning for shorter lines',
                    'Use lockers for valuables',
                    'Stay hydrated and use sunscreen',
                    'Allow 4-6 hours for full experience',
                    'Wheelchair accessible areas available'
                ],
                'discovery': 'Wild Wadi Water Park opened in 1999 as Jumeirah Beach\'s companion attraction, emerging from Dubai\'s vision to create world-class water entertainment. The park was inspired by Arabian Nights tales and designed to provide thrilling water adventures. It represents Dubai\'s early commitment to family-oriented tourism attractions.',
                'architecture': 'The park features Jumeirah Sceirah, the world\'s largest water coaster, with innovative water ride technology. The design incorporates natural rock formations, themed areas, and wave pools. Modern engineering creates safe and exciting water experiences with various ride intensities for all ages.',
                'cultural_impact': 'Wild Wadi has become a cultural institution in Dubai, influencing water park design in the region. It promotes family entertainment and water safety education. The park has contributed to Dubai\'s image as a family-friendly destination and fostered community recreational activities.',
                'conservation': 'The park implements water conservation measures and sustainable filtration systems. Environmental education focuses on water safety and marine conservation. The facility supports local biodiversity through landscaping that incorporates native desert plants.',
                'health_safety': 'Comprehensive safety measures include lifeguard supervision, medical facilities, and ride safety protocols. The park maintains strict water quality standards and provides shaded areas for heat protection. Emergency response systems ensure visitor safety throughout the facility.',
                'guided_tours': 'Adventure tours highlight the park\'s signature rides and attractions. Family tours include safety briefings and age-appropriate activity recommendations. Photography tours help visitors capture the best views of the water park features.',
                'nearby_attractions': 'Burj Al Arab (adjacent), Jumeirah Beach (adjacent), Dubai Marina (2 km).',
                'photos': [
                    'https://images.unsplash.com/photo-1530549387789-4c1017266635?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.1390° N, 55.1856° E',
                'annual_visitors': 'Over 1.5 million',
                'climate': 'Desert climate. Best visited October-April.'
            },
            'dubai-zoo': {
                'id': 'dubai-zoo',
                'name': 'Dubai Zoo',
                'location': 'Dubai, UAE',
                'description': 'Modern zoological park featuring diverse animal exhibits, conservation programs, and family attractions.',
                'long_description': 'Dubai Zoo is a modern zoological park that showcases a diverse collection of animals from around the world. The zoo focuses on conservation, education, and providing enriching environments for its residents. With over 300 species, the zoo offers an educational and entertaining experience for visitors of all ages.',
                'facts': [
                    'Features over 300 animal species',
                    'Spans 1.6 million square feet',
                    'Conservation-focused exhibits',
                    'Educational programs and animal encounters',
                    'Multiple themed areas and habitats',
                    'Daily animal feeding demonstrations',
                    'Wheelchair accessible throughout',
                    'Capacity for 4,000 visitors daily'
                ],
                'key_sites': [
                    {'name': 'African Savanna', 'slug': 'african-savanna', 'description': 'Large habitat with giraffes and zebras', 'significance': 'Recreates African grassland environment'},
                    {'name': 'Asian Elephant Habitat', 'slug': 'asian-elephant-habitat', 'description': 'Dedicated area for Asian elephants', 'significance': 'Features conservation and enrichment programs'},
                    {'name': 'Primate Island', 'slug': 'primate-island', 'description': 'Monkey and ape exhibits', 'significance': 'Interactive viewing of primate behavior'},
                    {'name': 'Bird Aviary', 'slug': 'bird-aviary', 'description': 'Large walk-through bird enclosure', 'significance': 'Features tropical and exotic bird species'}
                ],
                'entrance_fees': 'Adult: 25 AED. Child (3-12): 15 AED.',
                'opening_hours': '10:00 AM to 6:00 PM daily.',
                'best_time': 'Early morning or late afternoon to avoid heat.',
                'how_to_get_there': 'Located in Jumeirah. Taxi or private car recommended.',
                'what_to_wear': 'Comfortable clothing and walking shoes.',
                'visitor_tips': [
                    'Visit early morning for animal activity',
                    'Stay on designated paths',
                    'Bring water and sunscreen',
                    'Allow 2-3 hours for complete visit',
                    'Photography allowed in most areas',
                    'Check feeding demonstration schedules'
                ],
                'discovery': 'Dubai Zoo opened in 1967 as one of the UAE\'s first zoological parks, evolving from a small collection to a modern conservation-focused facility. The zoo emerged from Dubai\'s commitment to wildlife preservation and environmental education. It has transformed into a center for animal welfare and biodiversity conservation.',
                'architecture': 'The zoo features modern habitat designs that prioritize animal welfare and naturalistic environments. The layout includes themed areas, educational exhibits, and conservation-focused displays. Contemporary architecture incorporates shaded walkways, interactive exhibits, and accessible viewing areas.',
                'cultural_impact': 'Dubai Zoo has become a cornerstone of environmental education in the UAE, promoting wildlife conservation and biodiversity awareness. It has influenced zoo design in the region and contributed to national conservation efforts. The zoo fosters community engagement with wildlife and environmental stewardship.',
                'conservation': 'The zoo actively participates in breeding programs and species conservation initiatives. Environmental education programs teach visitors about wildlife protection and habitat preservation. Sustainable practices include energy-efficient operations and waste management systems that minimize ecological impact.',
                'health_safety': 'The facility maintains high safety standards with secure enclosures, emergency medical services, and visitor supervision. Accessibility features ensure inclusive access for all visitors. Educational safety programs teach visitors about wildlife behavior and responsible viewing practices.',
                'guided_tours': 'Conservation tours provide insights into animal welfare and breeding programs. Educational tours include interactive learning experiences about wildlife. Family tours combine animal viewing with educational content about conservation.',
                'nearby_attractions': 'Jumeirah Beach (adjacent), Wild Wadi Water Park (nearby), Burj Al Arab (2 km).',
                'photos': [
                    'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
                ],
                'coordinates': '25.2333° N, 55.2667° E',
                'annual_visitors': 'Over 800,000',
                'climate': 'Desert climate. Best visited October-April.'
            }
        }
    }

    # Get the attraction data
    country_data = demo_attractions.get(country.lower())
    if not country_data:
        return redirect('countries')

    attraction = country_data.get(slug)
    if not attraction:
        return redirect('country_detail', country=country)

    # Create photo dictionaries for the template
    photos_urls = attraction.get('photos', [attraction.get('image')])
    hero_photos_json = []
    all_photos_json = []

    for idx, photo_url in enumerate(photos_urls):
        photo_dict = {
            'id': idx,
            'image_url': photo_url,
            'alt_text': f"{attraction['name']} photo {idx+1}",
            'title': f"{attraction['name']} - Image {idx+1}",
            'caption': '',
            'display_order': idx,
            'is_hero': idx < 6,
            'media_type': 'image',
        }
        all_photos_json.append(photo_dict)
        if idx < 6:
            hero_photos_json.append(photo_dict)

    total_photos = len(all_photos_json)

    context = {
        'attraction': attraction,
        'is_demo': True,
        'photos': photos_urls,
        'hero_photos': hero_photos_json,
        'all_photos': all_photos_json,
        'total_photos': total_photos,
        'country': country,
    }

    return render(request, 'core/attraction_detail.html', context)


def uae_attractions(request):
    """UAE Popular Attractions listing page"""
    # Get all UAE attractions from the demo data
    uae_attractions_data = demo_attractions.get('uae', {})

    # Convert to list for template iteration
    attractions_list = []
    for slug, attraction in uae_attractions_data.items():
        attraction_copy = attraction.copy()
        attraction_copy['slug'] = slug
        attractions_list.append(attraction_copy)

    context = {
        'attractions': attractions_list,
        'country': 'uae',
        'country_name': 'United Arab Emirates',
        'is_demo': True,
    }

    return render(request, 'core/uae_attractions.html', context)


# Bulk Actions for Host Dashboard
@login_required
@require_POST
def bulk_activate_listings(request):
    """Activate multiple listings (accommodations or tours)"""
    try:
        listing_ids = request.POST.getlist('listing_ids[]')
        listing_type = request.POST.get('listing_type')  # 'accommodation' or 'tour'

        if not listing_ids:
            return JsonResponse({'success': False, 'error': 'No listings selected'}, status=400)

        if listing_type == 'accommodation':
            updated = Accommodation.objects.filter(
                id__in=listing_ids,
                host=request.user
            ).update(is_active=True)
        elif listing_type == 'tour':
            updated = Tour.objects.filter(
                id__in=listing_ids,
                host=request.user
            ).update(is_active=True)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid listing type'}, status=400)

        return JsonResponse({
            'success': True,
            'message': f'{updated} listing(s) activated successfully',
            'count': updated
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def bulk_deactivate_listings(request):
    """Deactivate multiple listings (accommodations or tours)"""
    try:
        listing_ids = request.POST.getlist('listing_ids[]')
        listing_type = request.POST.get('listing_type')  # 'accommodation' or 'tour'

        if not listing_ids:
            return JsonResponse({'success': False, 'error': 'No listings selected'}, status=400)

        if listing_type == 'accommodation':
            updated = Accommodation.objects.filter(
                id__in=listing_ids,
                host=request.user
            ).update(is_active=False)
        elif listing_type == 'tour':
            updated = Tour.objects.filter(
                id__in=listing_ids,
                host=request.user
            ).update(is_active=False)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid listing type'}, status=400)

        return JsonResponse({
            'success': True,
            'message': f'{updated} listing(s) deactivated successfully',
            'count': updated
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def bulk_delete_listings(request):
    """Delete multiple listings (accommodations or tours)"""
    try:
        listing_ids = request.POST.getlist('listing_ids[]')
        listing_type = request.POST.get('listing_type')  # 'accommodation' or 'tour'

        if not listing_ids:
            return JsonResponse({'success': False, 'error': 'No listings selected'}, status=400)

        if listing_type == 'accommodation':
            listings = Accommodation.objects.filter(
                id__in=listing_ids,
                host=request.user
            )
            count = listings.count()
            listings.delete()
        elif listing_type == 'tour':
            listings = Tour.objects.filter(
                id__in=listing_ids,
                host=request.user
            )
            count = listings.count()
            listings.delete()
        else:
            return JsonResponse({'success': False, 'error': 'Invalid listing type'}, status=400)

        return JsonResponse({
            'success': True,
            'message': f'{count} listing(s) deleted successfully',
            'count': count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def bulk_publish_listings(request):
    """Publish multiple listings (accommodations or tours) - makes them visible on public site"""
    try:
        listing_ids = request.POST.getlist('listing_ids[]')
        listing_type = request.POST.get('listing_type')  # 'accommodation' or 'tour'

        if not listing_ids:
            return JsonResponse({'success': False, 'error': 'No listings selected'}, status=400)

        if listing_type == 'accommodation':
            updated = Accommodation.objects.filter(
                id__in=listing_ids,
                host=request.user
            ).update(is_published=True, is_active=True)
        elif listing_type == 'tour':
            updated = Tour.objects.filter(
                id__in=listing_ids,
                host=request.user
            ).update(is_published=True, is_active=True)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid listing type'}, status=400)

        return JsonResponse({
            'success': True,
            'message': f'{updated} listing(s) published successfully and are now visible on the public site!',
            'count': updated
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def bulk_unpublish_listings(request):
    """Unpublish multiple listings - returns them to draft mode"""
    try:
        listing_ids = request.POST.getlist('listing_ids[]')
        listing_type = request.POST.get('listing_type')  # 'accommodation' or 'tour'

        if not listing_ids:
            return JsonResponse({'success': False, 'error': 'No listings selected'}, status=400)

        if listing_type == 'accommodation':
            updated = Accommodation.objects.filter(
                id__in=listing_ids,
                host=request.user
            ).update(is_published=False)
        elif listing_type == 'tour':
            updated = Tour.objects.filter(
                id__in=listing_ids,
                host=request.user
            ).update(is_published=False)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid listing type'}, status=400)

        return JsonResponse({
            'success': True,
            'message': f'{updated} listing(s) unpublished and returned to draft mode',
            'count': updated
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# Individual listing view functions
@login_required
def view_accommodation(request, listing_id):
    """View detailed information about a specific accommodation listing"""
    try:
        accommodation = get_object_or_404(Accommodation, id=listing_id, host=request.user)

        # Get primary photo
        primary_photo = accommodation.photos.filter(is_hero=True).first()
        if not primary_photo:
            primary_photo = accommodation.photos.first()

        context = {
            'listing': accommodation,
            'listing_type': 'accommodation',
            'primary_photo': primary_photo,
            'photos': accommodation.photos.all(),
            'amenities_list': accommodation.amenities.split(',') if accommodation.amenities else [],
            'features_list': accommodation.property_features.split(',') if accommodation.property_features else [],
            'landmarks_list': accommodation.nearby_landmarks.split(',') if accommodation.nearby_landmarks else [],
        }

        return render(request, 'core/listing_detail.html', context)

    except Exception as e:
        messages.error(request, f'Error viewing accommodation: {str(e)}')
        return redirect('hostdashboard')


@login_required
def view_tour(request, listing_id):
    """View detailed information about a specific tour listing"""
    try:
        tour = get_object_or_404(Tour, id=listing_id, host=request.user)

        # Get primary photo
        primary_photo = tour.photos.filter(is_hero=True).first()
        if not primary_photo:
            primary_photo = tour.photos.first()

        context = {
            'listing': tour,
            'listing_type': 'tour',
            'primary_photo': primary_photo,
            'photos': tour.photos.all(),
            'languages_list': tour.languages.split(',') if tour.languages else [],
            'inclusions_list': tour.inclusions.split(',') if tour.inclusions else [],
            'highlights_list': tour.highlights.split(',') if tour.highlights else [],
        }

        return render(request, 'core/listing_detail.html', context)

    except Exception as e:
        messages.error(request, f'Error viewing tour: {str(e)}')
        return redirect('hostdashboard')


@login_required
def edit_accommodation(request, listing_id):
    """Edit a specific accommodation listing"""
    try:
        accommodation = get_object_or_404(Accommodation, id=listing_id, host=request.user)

        if request.method == 'POST':
            # Update accommodation with form data
            accommodation.property_name = request.POST.get('property_name', accommodation.property_name)
            accommodation.property_type = request.POST.get('property_type', accommodation.property_type)
            accommodation.country = request.POST.get('country', accommodation.country)
            accommodation.city = request.POST.get('city', accommodation.city)
            accommodation.street_address = request.POST.get('street_address', accommodation.street_address)
            accommodation.num_rooms = int(request.POST.get('num_rooms', accommodation.num_rooms))
            accommodation.beds_per_room = int(request.POST.get('beds_per_room', accommodation.beds_per_room))
            accommodation.bed_type = request.POST.get('bed_type', accommodation.bed_type)
            accommodation.num_bathrooms = int(request.POST.get('num_bathrooms', accommodation.num_bathrooms))
            accommodation.max_guests = int(request.POST.get('max_guests', accommodation.max_guests))
            accommodation.tagline = request.POST.get('tagline', accommodation.tagline)
            accommodation.full_description = request.POST.get('full_description', accommodation.full_description)
            accommodation.base_price = float(request.POST.get('base_price', accommodation.base_price))
            accommodation.cleaning_fee = request.POST.get('cleaning_fee')
            if accommodation.cleaning_fee:
                accommodation.cleaning_fee = float(accommodation.cleaning_fee)
            accommodation.cancellation_policy = request.POST.get('cancellation_policy', accommodation.cancellation_policy)
            accommodation.house_rules = request.POST.get('house_rules', accommodation.house_rules)

            # Handle amenities
            amenities = request.POST.getlist('amenities')
            if amenities:
                accommodation.amenities = ','.join(amenities)

            accommodation.save()

            messages.success(request, 'Accommodation updated successfully!')
            return redirect('view_accommodation', listing_id=listing_id)

        # GET request - show edit form
        context = {
            'listing': accommodation,
            'listing_type': 'accommodation',
            'amenities_list': accommodation.amenities.split(',') if accommodation.amenities else [],
            'edit_mode': True,
        }

        return render(request, 'core/listing_detail.html', context)

    except Exception as e:
        messages.error(request, f'Error editing accommodation: {str(e)}')
        return redirect('hostdashboard')


@login_required
def edit_tour(request, listing_id):
    """Edit a specific tour listing"""
    try:
        tour = get_object_or_404(Tour, id=listing_id, host=request.user)

        if request.method == 'POST':
            # Update tour with form data
            tour.tour_name = request.POST.get('tour_name', tour.tour_name)
            tour.tour_category = request.POST.get('tour_category', tour.tour_category)
            tour.duration = request.POST.get('duration', tour.duration)
            tour.country = request.POST.get('country', tour.country)
            tour.city = request.POST.get('city', tour.city)
            tour.min_participants = int(request.POST.get('min_participants', tour.min_participants))
            tour.max_participants = int(request.POST.get('max_participants', tour.max_participants))
            tour.age_restrictions = request.POST.get('age_restrictions', tour.age_restrictions)
            tour.tagline = request.POST.get('tagline', tour.tagline)
            tour.full_description = request.POST.get('full_description', tour.full_description)
            tour.itinerary = request.POST.get('itinerary', tour.itinerary)
            tour.price_per_person = float(request.POST.get('price_per_person', tour.price_per_person))
            tour.fitness_level = request.POST.get('fitness_level', tour.fitness_level)
            tour.cancellation_policy = request.POST.get('cancellation_policy', tour.cancellation_policy)

            # Handle languages
            languages = request.POST.getlist('languages')
            if languages:
                tour.languages = ','.join(languages)

            # Handle inclusions
            inclusions = request.POST.getlist('inclusions')
            if inclusions:
                tour.inclusions = ','.join(inclusions)

            tour.save()

            messages.success(request, 'Tour updated successfully!')
            return redirect('view_tour', listing_id=listing_id)

        # GET request - show edit form
        context = {
            'listing': tour,
            'listing_type': 'tour',
            'languages_list': tour.languages.split(',') if tour.languages else [],
            'inclusions_list': tour.inclusions.split(',') if tour.inclusions else [],
            'edit_mode': True,
        }

        return render(request, 'core/listing_detail.html', context)

    except Exception as e:
        messages.error(request, f'Error editing tour: {str(e)}')
        return redirect('hostdashboard')


@login_required
def update_accommodation(request, listing_id):
    """Update accommodation status and refresh data"""
    try:
        accommodation = get_object_or_404(Accommodation, id=listing_id, host=request.user)

        # This could include updating pricing, availability, or refreshing from external sources
        accommodation.updated_at = timezone.now()
        accommodation.save()

        messages.success(request, f'"{accommodation.property_name}" has been updated and refreshed!')
        return redirect('view_accommodation', listing_id=listing_id)

    except Exception as e:
        messages.error(request, f'Error updating accommodation: {str(e)}')
        return redirect('hostdashboard')


@login_required
def update_tour(request, listing_id):
    """Update tour status and refresh data"""
    try:
        tour = get_object_or_404(Tour, id=listing_id, host=request.user)

        # This could include updating pricing, availability, or refreshing from external sources
        tour.updated_at = timezone.now()
        tour.save()

        messages.success(request, f'"{tour.tour_name}" has been updated and refreshed!')
        return redirect('view_tour', listing_id=listing_id)

    except Exception as e:
        messages.error(request, f'Error updating tour: {str(e)}')
        return redirect('hostdashboard')


@login_required
def create_tour_guide(request):
    """Create tour guide profile page"""
    if request.method == 'POST':
        form = TourGuideForm(request.POST, request.FILES)
        if form.is_valid():
            tour_guide = form.save(commit=False)
            tour_guide.host = request.user
            tour_guide.is_published = True
            tour_guide.save()

            # Handle photo uploads
            photos = request.FILES.getlist('photos')
            for index, photo in enumerate(photos):
                TourGuidePhoto.objects.create(
                    tour_guide=tour_guide,
                    original_file=photo,
                    is_profile_photo=(index == 0),
                    display_order=index
                )

            messages.success(request, f'Tour Guide profile "{tour_guide.guide_name}" created successfully!')
            return redirect('hostdashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TourGuideForm()

    return render(request, 'core/create_tour_guide.html', {'form': form})


@login_required
def create_rental_car(request):
    if request.method == 'POST':
        form = RentalCarForm(request.POST, request.FILES)
        if form.is_valid():
            rental_car = form.save(commit=False)
            rental_car.host = request.user
            rental_car.is_published = True
            rental_car.save()

            # Handle photo uploads
            photos = request.FILES.getlist('photos')
            for index, photo in enumerate(photos):
                RentalCarPhoto.objects.create(
                    rental_car=rental_car,
                    original_file=photo,
                    is_primary=(index == 0),
                    display_order=index
                )

            messages.success(request, f'Rental Car "{rental_car.vehicle_name}" listed successfully!')
            return redirect('hostdashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RentalCarForm()

    return render(request, 'core/create_rental_car.html', {'form': form})

def rental_cars(request):
    """Rental cars listing page"""
    return render(request, 'core/rental_cars.html')

def taxi_service(request):
    """Taxi service page"""
    return render(request, 'core/taxi_service.html')
