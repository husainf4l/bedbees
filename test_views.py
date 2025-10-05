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
