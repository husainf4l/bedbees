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
