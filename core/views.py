from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import HostRegistrationForm, HostProfileForm, AccommodationForm, TourForm
from .models import UserProfile, Accommodation, Tour, AccommodationPhoto, TourPhoto

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

def tours(request, category=None):
    """Tours page view"""
    # Demo tours data
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

    # Filter tours by category
    if category and category.lower() in category_mapping:
        filter_cat = category_mapping[category.lower()]
        if filter_cat:
            filtered_tours = [tour for tour in demo_tours if tour['category'] == filter_cat]
        else:
            filtered_tours = demo_tours
    else:
        filtered_tours = demo_tours

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

    context = {
        'tours': filtered_tours,
        'category': category,
        'display_category': display_category,
        'total_tours': len(filtered_tours),
        'all_categories': category_names
    }

    return render(request, 'core/tours.html', context)

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
                    UserProfile.objects.create(user=user, is_host=False)
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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile for traveler
            UserProfile.objects.create(user=user, is_host=False)
            login(request, user)
            messages.success(request, f"Traveler account created successfully! Welcome, {user.username}! Start exploring amazing experiences.")
            return redirect('dashboard')  # Redirect travelers to dashboard
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def accommodations(request):
    """Accommodations page view"""
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
            'image': 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
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
            'image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
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
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
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
            'image': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
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
            'image': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
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
            'image': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
        }
    ]

    # Filter by type if provided
    accommodation_type = request.GET.get('type')
    if accommodation_type:
        filtered_accommodations = [acc for acc in demo_accommodations if acc['type'] == accommodation_type]
    else:
        filtered_accommodations = demo_accommodations

    context = {
        'accommodations': filtered_accommodations,
        'current_type': accommodation_type,
        'total_accommodations': len(filtered_accommodations),
        'types': ['resort', 'hotel', 'chalet', 'riad', 'bungalow', 'apartment']
    }

    return render(request, 'core/accommodations.html', context)

def hostregister(request):
    """Host registration page view"""
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

def dashboard(request):
    """Traveler dashboard page view"""
    if not request.user.is_authenticated:
        messages.warning(request, "Please sign in to access your dashboard.")
        return redirect('signin')

    # Check if user is a host trying to access traveler dashboard
    try:
        profile = request.user.profile
        if profile.is_host:
            messages.info(request, "Welcome back! Redirecting to your host dashboard.")
            return redirect('hostdashboard')
    except UserProfile.DoesNotExist:
        # Create profile for traveler if it doesn't exist
        UserProfile.objects.create(user=request.user, is_host=False)

    # Mock dashboard data (in a real app, this would come from the database)
    dashboard_data = {
        'stats': {
            'total_trips': 0,
            'upcoming_trips': 0,
            'total_spent': 0,
            'favorite_destinations': 0,
        },
        'upcoming_bookings': [],
        'recent_activity': [],
        'favorite_destinations': [],
        'profile': {
            'name': request.user.first_name or request.user.username,
            'email': request.user.email,
            'joined_date': request.user.date_joined,
            'total_trips': 0,
            'reviews_given': 0,
            'average_rating': 0,
        },
    }

    context = {
        'dashboard_data': dashboard_data,
    }
    return render(request, 'core/dashboard.html', context)

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
    
    context = {
        'user': request.user,
        'profile': profile,
        'form': form,
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
            accommodation.save()

            # Handle photo uploads
            photos = request.FILES.getlist('photos')
            for index, photo in enumerate(photos):
                AccommodationPhoto.objects.create(
                    accommodation=accommodation,
                    image=photo,
                    is_primary=(index == 0),
                    order=index
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
