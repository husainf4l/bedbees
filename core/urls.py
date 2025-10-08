from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

# API Router
router = DefaultRouter()
router.register(r'calendar', api_views.CalendarViewSet, basename='calendar')

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    path('tours/', views.tours, name='tours'),
    path('tours/<int:id>/', views.tour_detail, name='tour_detail'),
    # path('tours/<int:id>/book/', views.book_tour, name='book_tour'),  # Temporarily disabled
    path('tours/<str:category>/', views.tours, name='tours_category'),
    path('tours/share-trip/', views.share_trip_tours, name='share_trip_tours'),
    path('experiences/', views.experiences, name='experiences'),
    path('rental-cars/', views.rental_cars, name='rental_cars'),
    path('taxi-service/', views.taxi_service, name='taxi_service'),
    path('taxis/', views.taxi_service, name='taxis'),
    # path('tour-guides/', views.tour_guides, name='tour_guides'),  # Temporarily disabled
    path('accommodations/', views.accommodations, name='accommodations'),
    path('accommodations/<int:id>/', views.accommodation_detail, name='accommodation_detail'),
    path('accommodations/<int:id>/book/', views.book_accommodation, name='book_accommodation'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('hostregister/', views.hostregister, name='hostregister'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('hostdashboard/', views.hostdashboard, name='hostdashboard'),
    path('host-profile/', views.host_profile, name='host_profile'),
    path('profile/', views.profile, name='profile'),
    path('bookings/', views.bookings, name='bookings'),
    path('logout/', views.logout_view, name='logout'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('create-accommodation/', views.create_accommodation, name='create_accommodation'),
    path('create-tour/', views.create_tour, name='create_tour'),
    path('create-tour-guide/', views.create_tour_guide, name='create_tour_guide'),
    path('create-rental-car/', views.create_rental_car, name='create_rental_car'),
    path('countries/', views.countries, name='countries'),
    path('countries/<str:country>/', views.country_detail, name='country_detail'),
    path('countries/<str:country>/accommodation/<str:slug>/', views.demo_accommodation_detail, name='demo_accommodation_detail'),
    path('countries/<str:country>/tour/<str:slug>/', views.demo_tour_detail, name='demo_tour_detail'),
    path('countries/<str:country>/attraction/<str:slug>/', views.attraction_detail, name='attraction_detail'),
    path('countries/uae/attractions/', views.uae_attractions, name='uae_attractions'),
    path('destinations/', views.destinations, name='destinations'),
    path('search/', views.search_results, name='search_results'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    
    # New User Account Pages
    path('genius-rewards/', views.genius_rewards, name='genius_rewards'),
    path('credits-vouchers/', views.credits_vouchers, name='credits_vouchers'),
    path('my-account/', views.my_account, name='my_account'),
    path('reviews/', views.reviews, name='reviews'),

    # Bulk actions for host dashboard
    path('bulk-activate-listings/', views.bulk_activate_listings, name='bulk_activate_listings'),
    path('bulk-deactivate-listings/', views.bulk_deactivate_listings, name='bulk_deactivate_listings'),
    path('bulk-delete-listings/', views.bulk_delete_listings, name='bulk_delete_listings'),
    path('bulk-publish-listings/', views.bulk_publish_listings, name='bulk_publish_listings'),
    path('bulk-unpublish-listings/', views.bulk_unpublish_listings, name='bulk_unpublish_listings'),

    # Individual listing actions
    path('accommodation/<int:listing_id>/view/', views.view_accommodation, name='view_accommodation'),
    path('accommodation/<int:listing_id>/edit/', views.edit_accommodation, name='edit_accommodation'),
    path('accommodation/<int:listing_id>/update/', views.update_accommodation, name='update_accommodation'),
    path('tour/<int:listing_id>/view/', views.view_tour, name='view_tour'),
    path('tour/<int:listing_id>/edit/', views.edit_tour, name='edit_tour'),
    path('tour/<int:listing_id>/update/', views.update_tour, name='update_tour'),
]
