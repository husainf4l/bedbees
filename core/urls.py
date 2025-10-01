from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tours/', views.tours, name='tours'),
    path('tours/<str:category>/', views.tours, name='tours_category'),
    path('tours/share-trip/', views.share_trip_tours, name='share_trip_tours'),
    path('accommodations/', views.accommodations, name='accommodations'),
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
]
