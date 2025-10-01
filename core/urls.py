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
    path('tours/<str:category>/', views.tours, name='tours_category'),
    path('tours/share-trip/', views.share_trip_tours, name='share_trip_tours'),
    path('accommodations/', views.accommodations, name='accommodations'),
    path('accommodations/<int:id>/', views.accommodation_detail, name='accommodation_detail'),
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
    path('countries/', views.countries, name='countries'),
    path('countries/<str:country>/', views.country_detail, name='country_detail'),
    path('destinations/', views.destinations, name='destinations'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),

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
