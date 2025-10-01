from rest_framework import permissions
from .models import Listing


class IsListingOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a listing to access it.
    """
    
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        # obj should be a Listing instance
        if isinstance(obj, Listing):
            return obj.owner == request.user
        return False


class IsListingOwnerFromParams(permissions.BasePermission):
    """
    Custom permission for views that get listing_id from URL params or request data.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Get listing_id from URL kwargs or request data
        listing_id = view.kwargs.get('listing_id') or request.data.get('listing')
        
        if not listing_id:
            return False
            
        try:
            listing = Listing.objects.get(id=listing_id)
            return listing.owner == request.user
        except Listing.DoesNotExist:
            return False
