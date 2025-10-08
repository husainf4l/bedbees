from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import HostRegistrationForm, HostProfileForm, AccommodationForm, TourForm, TourGuideForm, RentalCarForm
from .models import UserProfile, Accommodation, Tour, AccommodationPhoto, TourPhoto, TourGuide, TourGuidePhoto, RentalCar, RentalCarPhoto, Country
from .data import countries_data, demo_attractions

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
    share_trip_tours = []


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
    demo_accommodations = []

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
            'tours_count': 800,
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
    demo_country_details = {
        'fes-el-bali-medina': {
            'id': 'fes-el-bali-medina',
            'name': 'Fes el-Bali Medina',
            'location': 'Fez, Morocco',
            'description': 'The oldest walled part of Fez, a UNESCO World Heritage Site, famous for its labyrinthine streets, historic mosques, and vibrant souks.',
            'long_description': 'Fes el-Bali is the ancient medina of Fez, Morocco, dating back to the 9th century. It is one of the world\'s largest car-free urban areas and a UNESCO World Heritage Site. The medina is home to over 9,000 narrow streets, historic mosques, madrasas, and bustling souks. Visitors can explore traditional Moroccan architecture, artisan workshops, and centuries-old monuments.',
            'historical_significance': 'Founded in the 9th century, Fes el-Bali is the spiritual and cultural heart of Morocco and a major center of Islamic learning.',
            'cultural_impact': 'The medina preserves traditional Moroccan culture, crafts, and religious practices, attracting scholars and travelers for centuries.',
            'best_time_to_visit': 'Spring and autumn for mild weather',
            'how_to_get_there': 'Accessible by taxi or walking from central Fez',
            'entrance_fees': 'Free to enter; some monuments charge small fees',
            'opening_hours': 'Open 24/7; shops and monuments have varying hours',
            'what_to_wear': 'Comfortable shoes; modest clothing',
            'guided_tours': 'Recommended for first-time visitors',
            'nearby_attractions': ['Al Quaraouiyine Mosque', 'Bou Inania Madrasa', 'Fes Tanneries', 'Medersa Attarine'],
            'facts': [
                'Over 9,000 streets and alleys',
                'UNESCO World Heritage Site since 1981',
                'Home to the world\'s oldest university',
                'No cars allowed inside the medina',
                'Famous for its blue gates (Bab Bou Jeloud)'
            ],
            'visitor_tips': [
                'Hire a local guide to avoid getting lost',
                'Try traditional Moroccan street food',
                'Visit artisan workshops for handmade crafts',
                'Respect local customs and dress modestly',
                'Beware of pickpockets in crowded areas'
            ],
            'photos': [
                '/static/core/images/fes-el-bali.jpg',
                '/static/core/images/fes-medina.jpg',
                '/static/core/images/fes-gate.jpg',
                '/static/core/images/fes-market.jpg',
                '/static/core/images/fes-mosque.jpg',
                '/static/core/images/fes-souk.jpg',
                '/static/core/images/fes-morocco.jpg',
                '/static/core/images/fes-el-bali-medina.jpg'
            ],
            'coordinates': {'lat': 34.0667, 'lng': -4.9833},
            'annual_visitors': 1000000,
            'climate': 'Mediterranean climate with hot summers and mild winters',
            'discovery': 'Founded in the 9th century by Idris II',
            'architecture': 'Traditional Moroccan and Andalusian styles',
            'conservation': 'Ongoing restoration projects by UNESCO',
            'health_safety': 'Safe for tourists; take care in crowded areas',
            'key_sites': ['Al Quaraouiyine Mosque', 'Bou Inania Madrasa', 'Fes Tanneries', 'Medersa Attarine'],
            'image': '/static/core/images/fes-el-bali-medina.jpg'
        },

        'university-of-al-quaraouiyine-fes': {
            'id': 'university-of-al-quaraouiyine-fes',
            'name': 'University of Al Quaraouiyine',
            'location': 'Fez, Morocco',
            'description': 'The world\'s oldest continuously operating university, founded in 859 AD, featuring stunning Islamic architecture and historic significance.',
            'long_description': 'The University of Al Quaraouiyine is the world\'s oldest continuously operating university, founded in 859 AD by Fatima al-Fihri. Located in Fez, Morocco, it was originally a mosque that evolved into a center of learning. The university has educated countless scholars and produced significant contributions to Islamic scholarship, mathematics, and science. While much of the complex is still used as a mosque, parts are open to visitors.',
            'historical_significance': 'Founded in 859 AD, making it older than the University of Bologna (1088) and Oxford University (1096). It served as a major center of Islamic learning during the Golden Age of Islam.',
            'cultural_impact': 'The university represents the Islamic tradition of knowledge and learning, and has influenced educational systems across the Muslim world.',
            'best_time_to_visit': 'Morning hours when the mosque is less crowded',
            'how_to_get_there': 'Located in Fes el-Bali medina; accessible by taxi or walking',
            'entrance_fees': 'Free (exterior only for non-Muslims)',
            'opening_hours': 'Exterior visible during daylight hours; mosque for Muslims only',
            'what_to_wear': 'Modest, conservative clothing covering shoulders and knees',
            'guided_tours': 'Limited tours available; self-guided exterior viewing',
            'nearby_attractions': ['Fes el-Bali Medina', 'Bou Inania Madrasa', 'Fes Tanneries', 'Al Attarine Madrasa'],
            'facts': [
                'Founded in 859 AD by Fatima al-Fihri, daughter of a wealthy merchant',
                'World\'s oldest continuously operating university',
                'Originally built as a mosque with an adjacent madrasa',
                'Has educated scholars from across the Islamic world',
                'UNESCO World Heritage Site as part of Fes el-Bali'
            ],
            'visitor_tips': [
                'Non-Muslims can only view the exterior architecture',
                'Dress modestly and respectfully when near the mosque',
                'Visit during prayer times to appreciate the call to prayer',
                'The university\'s library contains rare Islamic manuscripts',
                'Combine with other Fes medina sites for a complete experience'
            ],
            'photos': [
                '/static/core/images/al-quaraouiyine-university.jpg',
                '/static/core/images/al-quaraouiyine-mosque.jpg',
                '/static/core/images/al-quaraouiyine-architecture.jpg',
                '/static/core/images/al-quaraouiyine-fes.jpg',
                '/static/core/images/al-quaraouiyine-interior.jpg',
                '/static/core/images/al-quaraouiyine-courtyard.jpg',
                '/static/core/images/al-quaraouiyine-morocco.jpg',
                '/static/core/images/al-quaraouiyine-historic.jpg'
            ],
            'coordinates': {'lat': 34.0644, 'lng': -4.9747},
            'annual_visitors': 300000,
            'climate': 'Mediterranean climate with hot summers and mild winters',
            'discovery': 'Founded as a mosque in 859 AD, evolved into a university over centuries',
            'architecture': 'Classical Islamic architecture with Moroccan-Andalusian elements',
            'conservation': 'Protected as part of UNESCO World Heritage Site',
            'health_safety': 'Respect religious site; maintain appropriate behavior',
            'key_sites': ['Main Mosque', 'Madrasa', 'Library', 'Courtyard'],
            'image': '/static/core/images/al-quaraouiyine-university.jpg'
        },

        'fes-tanneries': {
            'id': 'fes-tanneries',
            'name': 'Fes Tanneries',
            'location': 'Fez, Morocco',
            'description': 'The historic leather tanning district of Fez, where traditional methods have been used for over 1,000 years to produce world-famous Moroccan leather.',
            'long_description': 'The Fes Tanneries are one of the oldest leather tanning districts in the world, with methods unchanged for over 1,000 years. Located in the heart of Fes el-Bali, the tanneries use traditional techniques passed down through generations. Visitors can observe the process from rooftop viewpoints, seeing workers dye and treat leather in large stone vats using natural pigments. The area produces some of the finest leather goods in Morocco.',
            'historical_significance': 'The tanneries have operated continuously since the founding of Fez in the 9th century, representing one of the oldest industrial districts in the world.',
            'cultural_impact': 'The tanneries preserve traditional Moroccan craftsmanship and represent the city\'s economic heritage as a center of leather production.',
            'best_time_to_visit': 'Morning hours (9 AM - 12 PM) when activity is highest',
            'how_to_get_there': 'Located in Fes el-Bali medina; best accessed with a guide',
            'entrance_fees': 'Free to view from rooftops; small tip expected for guide',
            'opening_hours': '8:00 AM - 7:00 PM daily, weather permitting',
            'what_to_wear': 'Old clothes (leather dye can stain); comfortable shoes',
            'guided_tours': 'Essential due to the maze-like access and for safety',
            'nearby_attractions': ['Fes el-Bali Medina', 'Al Quaraouiyine University', 'Bou Inania Madrasa', 'Souks'],
            'facts': [
                'Operating for over 1,000 years using traditional methods',
                'Uses natural dyes from plants, minerals, and spices',
                'Produces leather for bags, jackets, and traditional Moroccan goods',
                'Employs hundreds of workers in a family-based industry',
                'UNESCO World Heritage Site as part of Fes el-Bali'
            ],
            'visitor_tips': [
                'Mint leaves help mask the strong tanning odors',
                'Wear old clothes as leather dye can stain permanently',
                'Visit rooftops for the best views of the tanning process',
                'Tip your guide for showing you around the district',
                'Be respectful of workers and don\'t interfere with their activities'
            ],
            'photos': [
                '/static/core/images/fes-tanneries.jpg',
                '/static/core/images/fes-leather.jpg',
                '/static/core/images/fes-tanning.jpg',
                '/static/core/images/fes-dyeing.jpg',
                '/static/core/images/fes-leather-goods.jpg',
                '/static/core/images/fes-tannery-rooftop.jpg',
                '/static/core/images/fes-morocco.jpg',
                '/static/core/images/fes-traditional.jpg'
            ],
            'coordinates': {'lat': 34.0617, 'lng': -4.9794},
            'annual_visitors': 400000,
            'climate': 'Mediterranean climate; outdoor process affected by weather',
            'discovery': 'Ancient industry dating back to the founding of Fez',
            'architecture': 'Traditional Moroccan industrial buildings with stone vats',
            'conservation': 'Protected traditional craft with modern safety improvements',
            'health_safety': 'Strong chemical odors; slippery surfaces; follow guide instructions',
            'key_sites': ['Tanning vats', 'Dyeing areas', 'Leather drying racks', 'Rooftop viewpoints'],
            'image': '/static/core/images/fes-tanneries.jpg'
        },

        'hassan-ii-mosque-casablanca': {
            'id': 'hassan-ii-mosque-casablanca',
            'name': 'Hassan II Mosque',
            'location': 'Casablanca, Morocco',
            'description': 'The largest mosque in Morocco and one of the largest in the world, featuring stunning Islamic architecture and ocean views.',
            'long_description': 'The Hassan II Mosque is the largest mosque in Morocco and one of the largest in the world, capable of accommodating 25,000 worshippers. Built between 1987 and 1993, it features the world\'s tallest minaret at 210 meters and a retractable roof. The mosque combines traditional Islamic architecture with modern engineering, including laser-guided opening of the roof and heated floors. Non-Muslims can visit during guided tours.',
            'historical_significance': 'Built during the reign of King Hassan II to commemorate 60 years of Moroccan independence, the mosque represents modern Moroccan achievement.',
            'cultural_impact': 'The mosque symbolizes Morocco\'s Islamic heritage and architectural innovation, serving as a major cultural landmark.',
            'best_time_to_visit': 'Morning tours to avoid heat and crowds',
            'how_to_get_there': 'Located on the coast of Casablanca; accessible by taxi',
            'entrance_fees': '120 MAD (about $12 USD) for non-Muslims',
            'opening_hours': '9:00 AM - 6:00 PM daily; tours every 30 minutes',
            'what_to_wear': 'Modest clothing covering shoulders and knees; headscarf provided',
            'guided_tours': 'Mandatory guided tours for non-Muslims',
            'nearby_attractions': ['Casablanca Corniche', 'Habous Quarter', 'Royal Palace', 'Central Market'],
            'facts': [
                'Largest mosque in Morocco, seventh largest in the world',
                'Can accommodate 25,000 worshippers inside, 80,000 in courtyard',
                'Tallest minaret in the world at 210 meters (689 feet)',
                'Features a retractable roof that opens for prayer',
                'Built between 1987 and 1993 at a cost of $800 million'
            ],
            'visitor_tips': [
                'Book tours in advance, especially during peak season',
                'Dress modestly; headscarves provided for women',
                'Remove shoes before entering prayer areas',
                'Photography allowed in designated areas only',
                'The mosque is especially beautiful when illuminated at night'
            ],
            'photos': [
                '/static/core/images/hassan-ii-mosque.jpg',
                '/static/core/images/hassan-ii-minaret.jpg',
                '/static/core/images/hassan-ii-interior.jpg',
                '/static/core/images/hassan-ii-architecture.jpg',
                '/static/core/images/hassan-ii-casablanca.jpg',
                '/static/core/images/hassan-ii-night.jpg',
                '/static/core/images/hassan-ii-details.jpg',
                '/static/core/images/hassan-ii-morocco.jpg'
            ],
            'coordinates': {'lat': 33.6083, 'lng': -7.6319},
            'annual_visitors': 200000,
            'climate': 'Mediterranean climate with mild temperatures year-round',
            'discovery': 'Opened to the public in 1993 after completion',
            'architecture': 'Modern Islamic architecture with traditional Moroccan elements',
            'conservation': 'Well-maintained modern structure with advanced engineering',
            'health_safety': 'Large, well-maintained facility with security measures',
            'key_sites': ['Main Prayer Hall', 'Minaret', 'Courtyard', 'Ablution Areas'],
            'image': '/static/core/images/hassan-ii-mosque.jpg'
        },

        'casablanca-corniche': {
            'id': 'casablanca-corniche',
            'name': 'Casablanca Corniche',
            'location': 'Casablanca, Morocco',
            'description': 'A scenic waterfront promenade along the Atlantic coast, featuring modern architecture, parks, and the iconic Hassan II Mosque.',
            'long_description': 'The Casablanca Corniche is a scenic waterfront promenade along the Atlantic coast, stretching for several kilometers. Built in the 20th century, it features modern architecture, parks, restaurants, and the iconic Hassan II Mosque. The corniche offers stunning ocean views, jogging paths, and is a popular spot for locals and tourists alike. It represents Casablanca\'s modern development and serves as the city\'s recreational and social hub.',
            'historical_significance': 'Developed in the 20th century during the French colonial period and post-independence modernization of Casablanca.',
            'cultural_impact': 'The Corniche represents modern Moroccan urban development and serves as a symbol of Casablanca\'s cosmopolitan character.',
            'best_time_to_visit': 'Evening for sunset views and cooler temperatures',
            'how_to_get_there': 'Located along the coast; accessible by taxi or public transport',
            'entrance_fees': 'Free to walk and enjoy the promenade',
            'opening_hours': '24/7 access; businesses have varying hours',
            'what_to_wear': 'Casual clothing; light jacket for evenings',
            'guided_tours': 'Optional; self-guided exploration recommended',
            'nearby_attractions': ['Hassan II Mosque', 'Mohammed V Square', 'Habous Quarter', 'Twin Center'],
            'facts': [
                'Stretches for several kilometers along the Atlantic coast',
                'Features the world\'s tallest minaret at Hassan II Mosque',
                'Popular spot for jogging, cycling, and recreational activities',
                'Includes modern parks, restaurants, and entertainment venues',
                'Represents Casablanca\'s modern urban development'
            ],
            'visitor_tips': [
                'Visit at sunset for spectacular ocean views',
                'Try fresh seafood at the corniche restaurants',
                'Safe for walking and jogging at any time',
                'Great spot for people-watching and local culture',
                'Combine with Hassan II Mosque for a complete experience'
            ],
            'photos': [
                '/static/core/images/casablanca-corniche.jpg',
                '/static/core/images/casablanca-coast.jpg',
                '/static/core/images/casablanca-hassan-ii.jpg',
                '/static/core/images/casablanca-promenade.jpg',
                '/static/core/images/casablanca-ocean.jpg',
                '/static/core/images/casablanca-sunset.jpg',
                '/static/core/images/casablanca-morocco.jpg',
                '/static/core/images/casablanca-modern.jpg'
            ],
            'coordinates': {'lat': 33.6083, 'lng': -7.6319},
            'annual_visitors': 5000000,
            'climate': 'Mediterranean climate with mild temperatures and ocean breezes',
            'discovery': 'Developed as part of Casablanca\'s modernization in the 20th century',
            'architecture': 'Modern Moroccan architecture with colonial and contemporary influences',
            'conservation': 'Well-maintained urban waterfront with ongoing development',
            'health_safety': 'Generally safe public area with good lighting and security',
            'key_sites': ['Hassan II Mosque', 'Parks and gardens', 'Restaurants', 'Jogging paths'],
            'image': '/static/core/images/casablanca-corniche.jpg'
        },

        'merzouga-sahara-desert': {
            'id': 'merzouga-sahara-desert',
            'name': 'Merzouga Sahara Desert',
            'location': 'Merzouga, Morocco',
            'description': 'Experience the stunning Erg Chebbi dunes in Merzouga, offering camel treks, desert camps, and spectacular Sahara Desert landscapes.',
            'long_description': 'Merzouga is located at the edge of the Erg Chebbi dunes, some of the highest and most spectacular sand dunes in Morocco. The area offers an authentic desert experience with traditional Berber camps, camel treks, and stunning sunsets over the golden sands. Visitors can spend nights in luxury desert camps, ride camels across the dunes, and experience traditional Berber hospitality and cuisine.',
            'historical_significance': 'The region has been home to nomadic Berber tribes for thousands of years and was part of ancient Saharan trade routes.',
            'cultural_impact': 'Merzouga represents the traditional desert culture of Morocco and the Berber way of life in the Sahara.',
            'best_time_to_visit': 'October to April for milder temperatures and desert activities',
            'how_to_get_there': 'Located 55km from Rissani; accessible by bus, taxi, or organized tours',
            'entrance_fees': 'Varies by tour operator; desert camps include meals and activities',
            'opening_hours': '24/7 access; guided tours available throughout the day',
            'what_to_wear': 'Light, breathable clothing; warm layers for evenings; sturdy shoes',
            'guided_tours': 'Essential for safety and cultural understanding; multi-day options available',
            'nearby_attractions': ['Erg Chebbi Dunes', 'Khali Oasis', 'Nomad Heritage Museum', 'Dayet Srji Lake'],
            'facts': [
                'Home to Erg Chebbi dunes reaching heights of 150 meters',
                'Temperatures can drop below freezing at night in winter',
                'Traditional Berber camps offer authentic desert experiences',
                'Contains ancient fossil sites dating back millions of years',
                'Part of the larger Sahara Desert ecosystem'
            ],
            'visitor_tips': [
                'Book desert tours well in advance during peak season',
                'Stay hydrated and use sunscreen even in cooler months',
                'Respect Berber customs and ask permission before photographing',
                'Try traditional Berber food and participate in cultural activities',
                'Consider multi-day stays for the full desert experience'
            ],
            'photos': [
                '/static/core/images/merzouga-desert.jpg',
                '/static/core/images/merzouga-dunes.jpg',
                '/static/core/images/merzouga-camel.jpg',
                '/static/core/images/merzouga-camp.jpg',
                '/static/core/images/merzouga-sunset.jpg',
                '/static/core/images/merzouga-berber.jpg',
                '/static/core/images/merzouga-stars.jpg',
                '/static/core/images/merzouga-morocco.jpg'
            ],
            'coordinates': {'lat': 31.0833, 'lng': -4.0167},
            'annual_visitors': 250000,
            'climate': 'Extreme desert climate with hot days and cold nights',
            'discovery': 'Became a tourist destination in the late 20th century',
            'architecture': 'Traditional Berber tents and modern desert lodges',
            'conservation': 'Protected desert areas with sustainable tourism practices',
            'health_safety': 'Guided tours essential; heat exhaustion risk; scorpion awareness',
            'key_sites': ['Erg Chebbi Dunes', 'Desert camps', 'Khali Oasis', 'Fossil sites'],
            'image': '/static/core/images/merzouga-desert.jpg'
        }
    },
    
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

    # Add country slug to the data
    country_data['slug'] = country.lower()

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


@login_required
def genius_rewards(request):
    """Genius Rewards page - shows user's loyalty rewards and benefits"""
    context = {
        'user': request.user,
        'genius_level': 2,  # Demo level (1=Level 1, 2=Level 2, 3=Level 3)
        'points': 1250,
        'next_level_points': 2000,
        'stays_completed': 12,
        'total_savings': 450,
        'benefits': [
            {'name': '10% discount on stays', 'active': True},
            {'name': 'Free room upgrades', 'active': True},
            {'name': 'Late checkout', 'active': True},
            {'name': 'Priority customer support', 'active': True},
            {'name': 'Free cancellation', 'active': False},
        ],
        'available_rewards': [
            {'title': '$50 Travel Credit', 'points': 500, 'available': True},
            {'title': 'Premium Upgrade Voucher', 'points': 750, 'available': True},
            {'title': '$100 Travel Credit', 'points': 1000, 'available': True},
            {'title': 'Weekend Getaway Package', 'points': 2000, 'available': False},
        ]
    }
    return render(request, 'core/genius_rewards.html', context)


@login_required
def credits_vouchers(request):
    """Credits and Vouchers page - shows user's available credits and vouchers"""
    context = {
        'user': request.user,
        'total_credits': 125.50,
        'credits': [
            {'id': 1, 'amount': 50, 'source': 'Referral Bonus', 'date': '2024-01-15', 'expires': '2025-01-15', 'status': 'active'},
            {'id': 2, 'amount': 75.50, 'source': 'Booking Credit', 'date': '2024-01-10', 'expires': '2025-01-10', 'status': 'active'},
        ],
        'vouchers': [
            {
                'id': 1,
                'code': 'WELCOME20',
                'discount': '20%',
                'description': 'Welcome voucher for new users',
                'min_purchase': 100,
                'expires': '2025-03-31',
                'status': 'active',
                'type': 'percentage'
            },
            {
                'id': 2,
                'code': 'SUMMER50',
                'discount': '$50',
                'description': 'Summer special discount',
                'min_purchase': 200,
                'expires': '2024-08-31',
                'status': 'expired',
                'type': 'fixed'
            },
            {
                'id': 3,
                'code': 'HOTEL15',
                'discount': '15%',
                'description': 'Hotel booking discount',
                'min_purchase': 150,
                'expires': '2025-06-30',
                'status': 'active',
                'type': 'percentage'
            },
        ]
    }
    return render(request, 'core/credits_vouchers.html', context)


@login_required
def my_account(request):
    """My Account page - user's personal information and settings"""
    context = {
        'user': request.user,
        'profile': request.user.profile if hasattr(request.user, 'profile') else None,
        'personal_info': {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': '+971 50 123 4567',  # Demo data
            'date_of_birth': '1990-05-15',  # Demo data
            'nationality': 'United States',  # Demo data
            'gender': 'Male',  # Demo data
        },
        'address': {
            'street': '123 Main Street',
            'city': 'Dubai',
            'state': 'Dubai',
            'country': 'United Arab Emirates',
            'postal_code': '12345',
        },
        'preferences': {
            'currency': 'USD',
            'language': 'English',
            'newsletter': True,
            'notifications': True,
        },
        'security': {
            'two_factor': False,
            'last_password_change': '2024-01-15',
        }
    }
    return render(request, 'core/my_account.html', context)


@login_required
def reviews(request):
    """Reviews page - user's reviews and ratings"""
    context = {
        'user': request.user,
        'my_reviews': [
            {
                'id': 1,
                'type': 'accommodation',
                'name': 'Burj Al Arab Jumeirah',
                'location': 'Dubai, UAE',
                'rating': 5,
                'title': 'Absolutely Amazing Experience',
                'review': 'The service was impeccable and the views were breathtaking. Worth every penny!',
                'date': '2024-01-20',
                'helpful_count': 12,
                'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c',
            },
            {
                'id': 2,
                'type': 'tour',
                'name': 'Petra Full Day Tour',
                'location': 'Petra, Jordan',
                'rating': 5,
                'title': 'Unforgettable Journey',
                'review': 'Our guide was knowledgeable and the ancient city exceeded all expectations.',
                'date': '2024-01-15',
                'helpful_count': 8,
                'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5',
            },
            {
                'id': 3,
                'type': 'accommodation',
                'name': 'Atlantis The Palm',
                'location': 'Dubai, UAE',
                'rating': 4,
                'title': 'Great Family Destination',
                'review': 'Perfect for families with kids. The aquarium and water park were highlights.',
                'date': '2024-01-10',
                'helpful_count': 15,
                'image': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d',
            },
        ],
        'pending_reviews': [
            {
                'id': 4,
                'type': 'tour',
                'name': 'Desert Safari Dubai',
                'location': 'Dubai, UAE',
                'booking_date': '2024-02-01',
                'image': 'https://images.unsplash.com/photo-1451337516015-6b6e9a44a8a3',
            },
        ],
        'review_stats': {
            'total_reviews': 3,
            'average_rating': 4.7,
            'helpful_votes_received': 35,
        }
    }
    return render(request, 'core/reviews.html', context)
