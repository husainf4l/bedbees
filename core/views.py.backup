from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import HostRegistrationForm, HostProfileForm, AccommodationForm, TourForm, TourGuideForm, RentalCarForm
from .models import UserProfile, Accommodation, Tour, AccommodationPhoto, TourPhoto, TourGuide, TourGuidePhoto, RentalCar, RentalCarPhoto

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
    
    return render(request, 'core/home.html')

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
    """Individual accommodation detail page view"""
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

    # Get booking parameters from request or set defaults
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

    context = {
        'accommodation': accommodation,
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
                {'name': 'Petra', 'description': 'Ancient rock-cut city and UNESCO World Heritage Site', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Dead Sea', 'description': 'Lowest point on Earth with mineral-rich waters', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Wadi Rum', 'description': 'Desert landscape known as Valley of the Moon', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Jerash', 'description': 'Ancient Roman city with well-preserved ruins', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Amman Citadel', 'description': 'Ancient fortress overlooking the capital city', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Nicosia', 'description': 'Last divided capital in Europe with rich history', 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Limassol', 'description': 'Vibrant coastal city with medieval castle', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Paphos', 'description': 'UNESCO site with ancient mosaics and beaches', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Troodos Mountains', 'description': 'Mountainous region with Byzantine churches', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Famagusta', 'description': 'Historic city with Venetian walls and Gothic cathedral', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Athens', 'description': 'Ancient capital with Acropolis and Parthenon', 'image': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80'},
                {'name': 'Santorini', 'description': 'Stunning volcanic island with white-washed buildings', 'image': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Mykonos', 'description': 'Cosmopolitan island known for nightlife and beaches', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Crete', 'description': 'Largest Greek island with palaces and gorges', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Olympia', 'description': 'Birthplace of the Olympic Games', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Istanbul', 'description': 'City of two continents with Hagia Sophia and Blue Mosque', 'image': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Cappadocia', 'description': 'Surreal landscape with cave dwellings and hot air balloons', 'image': 'https://images.unsplash.com/photo-1578271887552-5ac9e7c7b5d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Pamukkale', 'description': 'Natural thermal pools and ancient Hierapolis', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Ephesus', 'description': 'Ancient Greek city with well-preserved ruins', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Antalya', 'description': 'Mediterranean coastal city with ancient harbor', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Pyramids of Giza', 'description': 'Ancient wonders and last remaining Seven Wonders', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Luxor', 'description': 'City of temples with Karnak and Valley of the Kings', 'image': 'https://images.unsplash.com/photo-1464822759844-d150f38d609c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Aswan', 'description': 'Southern city with temples and Nile River beauty', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Cairo', 'description': 'Vibrant capital with Egyptian Museum and Khan el-Khalili', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Red Sea', 'description': 'Crystal clear waters perfect for diving and snorkeling', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Marrakech', 'description': 'Imperial city with Bahia Palace and Saadian Tombs', 'image': 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Sahara Desert', 'description': 'Vast desert with sand dunes and Berber camps', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Chefchaouen', 'description': 'Blue-washed mountain town with stunning views', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Atlas Mountains', 'description': 'Majestic mountain range with Berber villages', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Fes', 'description': 'Ancient medina and spiritual capital of Morocco', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Burj Khalifa', 'description': 'World\'s tallest building with stunning city views', 'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Palm Jumeirah', 'description': 'Artificial island paradise with luxury resorts', 'image': 'https://images.unsplash.com/photo-1518684079-3c830dcef090?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Mall', 'description': 'World\'s largest shopping and entertainment complex', 'image': 'https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Sheikh Zayed Grand Mosque', 'description': 'Magnificent mosque with intricate Islamic architecture', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Dubai Desert Safari', 'description': 'Thrilling desert adventure with dune bashing', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Beirut', 'description': 'Vibrant capital city with historic and modern attractions', 'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Baalbek', 'description': 'Ancient Roman temple complex and UNESCO World Heritage Site', 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Byblos', 'description': 'Oldest continuously inhabited city in the world', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Jeita Grotto', 'description': 'Spectacular limestone cave with underground river', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Cedars of God', 'description': 'Ancient cedar forest in the mountains', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Doha', 'description': 'Modern capital with stunning Islamic architecture', 'image': 'https://images.unsplash.com/photo-1539037116277-4db20889f2d4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Museum of Islamic Art', 'description': 'World-class museum showcasing Islamic art and culture', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Souq Waqif', 'description': 'Traditional market with authentic Arabian atmosphere', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Katara Cultural Village', 'description': 'Cultural complex showcasing Qatari heritage', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Al Zubarah Fort', 'description': '18th-century fort and UNESCO World Heritage Site', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Mecca', 'description': 'Holiest city in Islam with the Kaaba and Grand Mosque', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Medina', 'description': 'Second holiest city with Prophet\'s Mosque', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Riyadh', 'description': 'Modern capital with museums and cultural sites', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'AlUla', 'description': 'Ancient oasis city with Nabatean tombs', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Red Sea Coast', 'description': 'Stunning coastline with coral reefs and beaches', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Kuwait City', 'description': 'Modern capital with traditional souks and contemporary architecture', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Kuwait Towers', 'description': 'Iconic water towers symbolizing Kuwait\'s modernity', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Liberation Tower', 'description': 'Tallest structure in Kuwait with panoramic views', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Tareq Rajab Museum', 'description': 'Cultural museum showcasing Kuwaiti heritage', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Al Shaheed Park', 'description': 'Beautiful coastal park with beaches and recreational facilities', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Manama', 'description': 'Vibrant capital with modern skyscrapers and traditional souks', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bahrain Fort', 'description': 'Ancient fort dating back to 2800 BC', 'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'},
                {'name': 'Al Fateh Grand Mosque', 'description': 'Largest mosque in Bahrain with stunning architecture', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bahrain World Trade Center', 'description': 'Iconic twin towers with integrated wind turbines', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Tree of Life', 'description': 'Ancient tree in the desert, a natural wonder', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Muscat', 'description': 'Beautiful capital with white-washed buildings and harbor', 'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Nizwa Fort', 'description': 'Impressive 17th-century fort with circular towers', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Wahiba Sands', 'description': 'Spectacular desert with red dunes and Bedouin camps', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Jebel Shams', 'description': 'Highest mountain in Oman with breathtaking views', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Sur', 'description': 'Coastal town famous for traditional dhow building', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Damascus', 'description': 'Ancient capital city with Umayyad Mosque and souks', 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Aleppo', 'description': 'Historic city with Citadel and ancient medina', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Palmyra', 'description': 'Ancient oasis city with Roman ruins', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Krak des Chevaliers', 'description': 'Magnificent Crusader castle and UNESCO site', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Bosra', 'description': 'Ancient Roman theater and archaeological site', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Baghdad', 'description': 'Historic capital with Abbasid heritage and modern developments', 'image': 'https://images.unsplash.com/photo-1555992336-fb0d29498b13?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Babylon', 'description': 'Ancient city with Hanging Gardens and Ishtar Gate', 'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Uruk', 'description': 'Ancient Sumerian city and birthplace of writing', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Karbala', 'description': 'Sacred city with Imam Hussein Shrine', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Erbil Citadel', 'description': 'Ancient fortified settlement and UNESCO World Heritage Site', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
                {'name': 'Socotra Island', 'description': 'Unique island with dragon\'s blood trees and biodiversity', 'image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Zabid', 'description': 'Historic city and UNESCO World Heritage Site', 'image': 'https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Shibam', 'description': 'Manhattan of the desert with mud skyscrapers', 'image': 'https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'},
                {'name': 'Aden', 'description': 'Port city with volcanic crater and British colonial history', 'image': 'https://images.unsplash.com/photo-1539650116574-75c0c6d0b7ef?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'}
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
        primary_photo = acc.photos.filter(is_primary=True).first()
        if not primary_photo:
            primary_photo = acc.photos.first()

        real_accommodation_list.append({
            'id': acc.id,
            'name': acc.property_name,
            'location': acc.city,
            'price': float(acc.base_price),
            'image': primary_photo.image.url if primary_photo else 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
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
        primary_photo = tour.photos.filter(is_primary=True).first()
        if not primary_photo:
            primary_photo = tour.photos.first()

        real_tour_list.append({
            'id': tour.id,
            'name': tour.tour_name,
            'duration': tour.duration,
            'price': float(tour.price_per_person),
            'image': primary_photo.image.url if primary_photo else 'https://images.unsplash.com/photo-1539020140153-e365f8dc0c7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80',
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
        primary_photo = accommodation.photos.filter(is_primary=True).first()
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
        primary_photo = tour.photos.filter(is_primary=True).first()
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
