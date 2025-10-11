"""
Publishing System Views for BedBees
Handles listing publishing, approvals, and status management.

🎯 Features:
- Automatic location-based placement (country/city detection)
- Category organization (hotels, villas, tours, etc.)
- Optional admin approval workflow
- Email notifications for hosts and admins
- Instant visibility on homepage and destination pages
- Draft/Published status management
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import Accommodation, Tour, RentalCar
from .email_utils import (
    send_listing_published_email,
    send_listing_approved_email,
    send_listing_rejected_email,
    send_listing_edit_notification,
)


# Settings - Enable/Disable moderation
MODERATION_ENABLED = False  # Set to True to require admin approval for all listings

# 🌍 Location Mapping: Maps city names and country names to standardized country names
COUNTRY_MAPPING = {
    # Jordan
    "jordan": "Jordan",
    "amman": "Jordan",
    "petra": "Jordan",
    "aqaba": "Jordan",
    "dead sea": "Jordan",
    # UAE
    "uae": "UAE",
    "united arab emirates": "UAE",
    "dubai": "UAE",
    "abu dhabi": "UAE",
    "sharjah": "UAE",
    "ajman": "UAE",
    # Egypt
    "egypt": "Egypt",
    "cairo": "Egypt",
    "alexandria": "Egypt",
    "luxor": "Egypt",
    "aswan": "Egypt",
    "sharm el sheikh": "Egypt",
    # Saudi Arabia
    "saudi arabia": "Saudi Arabia",
    "riyadh": "Saudi Arabia",
    "jeddah": "Saudi Arabia",
    "mecca": "Saudi Arabia",
    "medina": "Saudi Arabia",
    # Qatar
    "qatar": "Qatar",
    "doha": "Qatar",
    # Lebanon
    "lebanon": "Lebanon",
    "beirut": "Lebanon",
    # Oman
    "oman": "Oman",
    "muscat": "Oman",
    # Kuwait
    "kuwait": "Kuwait",
    "kuwait city": "Kuwait",
    # Bahrain
    "bahrain": "Bahrain",
    "manama": "Bahrain",
    # Morocco
    "morocco": "Morocco",
    "marrakech": "Morocco",
    "casablanca": "Morocco",
    "fes": "Morocco",
    # Tunisia
    "tunisia": "Tunisia",
    "tunis": "Tunisia",
    # Algeria
    "algeria": "Algeria",
    "algiers": "Algeria",
}


def normalize_location(location_string):
    """
    Normalize location names to standard country names.

    Examples:
        "dubai" → "UAE"
        "Dubai, UAE" → "UAE"
        "amman" → "Jordan"
        "Jordan" → "Jordan"
    """
    if not location_string:
        return location_string

    # Convert to lowercase and strip whitespace
    location_lower = location_string.lower().strip()

    # Split by comma and check each part (handles "City, Country" format)
    parts = [part.strip() for part in location_lower.split(",")]
    for part in parts:
        if part in COUNTRY_MAPPING:
            return COUNTRY_MAPPING[part]

    # Check if the full string matches
    if location_lower in COUNTRY_MAPPING:
        return COUNTRY_MAPPING[location_lower]

    # Return original if no match
    return location_string.title()


@login_required
@require_POST
def publish_accommodation(request, accommodation_id):
    """
    Publish an accommodation listing with automatic location detection and categorization.

    🎯 What happens when publish is clicked:
    1. Mark listing as published and active
    2. Detect and normalize location (country/city)
    3. Categorize by property type (hotel, villa, apartment, etc.)
    4. Make visible on homepage, country pages, and category pages
    5. Send confirmation email to host
    6. (Optional) Queue for admin approval if MODERATION_ENABLED
    """
    accommodation = get_object_or_404(
        Accommodation, id=accommodation_id, host=request.user
    )

    # Check if listing is already published
    if accommodation.is_published and accommodation.status == "published":
        messages.info(request, f'"{accommodation.property_name}" is already published.')
        return redirect("core:hostdashboard")

    # 📍 STEP 1: Normalize and detect location
    original_country = accommodation.country
    normalized_country = normalize_location(accommodation.country)
    if normalized_country and normalized_country != original_country:
        accommodation.country = normalized_country

    # 📍 STEP 2: Ensure city is set
    if not accommodation.city:
        accommodation.city = "Unknown"

    # 🏷️ STEP 3: Categorize by property type (already in property_type field)
    # Property types: hotel, apartment, villa, resort, hostel, etc.

    # ✅ STEP 4: Publish the listing
    accommodation.is_published = True
    accommodation.is_active = True
    accommodation.published_at = timezone.now()

    if MODERATION_ENABLED and accommodation.requires_approval:
        # Set to pending if moderation is enabled
        accommodation.status = "pending"
        accommodation.save()

        messages.success(
            request,
            f'🎉 "{accommodation.property_name}" has been submitted for approval! '
            f"We'll review it and notify you once it's live. "
            f"📧 Check your email for confirmation.",
        )

        # Send notification email (pending approval)
        send_listing_edit_notification(accommodation, "accommodation")
    else:
        # ✅ Publish immediately (no moderation)
        accommodation.status = "published"
        accommodation.save()

        messages.success(
            request,
            f'🎉 Congratulations! "{accommodation.property_name}" is now LIVE! '
            f"✨ Your listing is visible in {accommodation.city}, {accommodation.country}. "
            f"📍 It appears on the homepage, {accommodation.country} page, and {accommodation.property_type} category. "
            f"📧 Confirmation email sent!",
        )

        # 📧 Send confirmation email to host
        send_listing_published_email(accommodation, "accommodation")

        # 📧 Notify admin about new listing
        send_admin_notification(accommodation, "accommodation")

    return redirect("core:hostdashboard")


@login_required
@require_POST
def publish_tour(request, tour_id):
    """
    Publish a tour listing with automatic location detection and categorization.

    🎯 What happens when publish is clicked:
    1. Mark tour as published and active
    2. Detect and normalize location (country/city)
    3. Categorize by tour type (adventure, cultural, food, etc.)
    4. Make visible on homepage, country pages, and tour category pages
    5. Send confirmation email to host
    6. (Optional) Queue for admin approval if MODERATION_ENABLED
    """
    tour = get_object_or_404(Tour, id=tour_id, host=request.user)

    # Check if listing is already published
    if tour.is_published and tour.status == "published":
        messages.info(request, f'"{tour.tour_name}" is already published.')
        return redirect("core:hostdashboard")

    # 📍 STEP 1: Normalize and detect location
    original_country = tour.country
    normalized_country = normalize_location(tour.country)
    if normalized_country and normalized_country != original_country:
        tour.country = normalized_country

    # 📍 STEP 2: Ensure city is set
    if not tour.city:
        tour.city = "Unknown"

    # 🏷️ STEP 3: Categorize by tour type (already in tour_category field)
    # Tour categories: Cultural, Adventure, Food & Drink, Nature, etc.

    # ✅ STEP 4: Publish the tour
    tour.is_published = True
    tour.is_active = True
    tour.published_at = timezone.now()

    if MODERATION_ENABLED and tour.requires_approval:
        # Set to pending if moderation is enabled
        tour.status = "pending"
        tour.save()

        messages.success(
            request,
            f'🎉 "{tour.tour_name}" has been submitted for approval! '
            f"We'll review it and notify you once it's live. "
            f"📧 Check your email for confirmation.",
        )

        # Send notification email (pending approval)
        send_listing_edit_notification(tour, "tour")
    else:
        # ✅ Publish immediately (no moderation)
        tour.status = "published"
        tour.save()

        messages.success(
            request,
            f'🎉 Congratulations! "{tour.tour_name}" is now LIVE! '
            f"✨ Your tour is visible in {tour.city}, {tour.country}. "
            f"📍 It appears on the homepage, {tour.country} page, and {tour.tour_category} tours. "
            f"📧 Confirmation email sent!",
        )

        # 📧 Send confirmation email to host
        send_listing_published_email(tour, "tour")

        # 📧 Notify admin about new tour
        send_admin_notification(tour, "tour")

    return redirect("core:hostdashboard")


@login_required
@require_POST
def publish_rental_car(request, car_id):
    """
    Publish a rental car listing.
    """
    rental_car = get_object_or_404(RentalCar, id=car_id, host=request.user)

    # Check if listing is already published
    if rental_car.is_published and rental_car.status == "published":
        messages.info(request, f'"{rental_car.vehicle_name}" is already published.')
        return redirect("core:hostdashboard")

    # Publish the listing
    rental_car.is_published = True
    rental_car.is_active = True
    rental_car.published_at = timezone.now()

    if MODERATION_ENABLED and rental_car.requires_approval:
        rental_car.status = "pending"
        rental_car.save()

        messages.success(
            request, f'🎉 "{rental_car.vehicle_name}" has been submitted for approval!'
        )

        send_listing_edit_notification(rental_car, "rental_car")
    else:
        rental_car.status = "published"
        rental_car.save()

        messages.success(
            request,
            f'🎉 Congratulations! "{rental_car.vehicle_name}" is now live in '
            f"{rental_car.city}, {rental_car.country}!",
        )

        send_listing_published_email(rental_car, "rental_car")

    return redirect("core:hostdashboard")


@login_required
@require_POST
def unpublish_accommodation(request, accommodation_id):
    """Unpublish an accommodation listing."""
    accommodation = get_object_or_404(
        Accommodation, id=accommodation_id, host=request.user
    )

    accommodation.is_published = False
    accommodation.is_active = False
    accommodation.status = "draft"
    accommodation.save()

    messages.success(request, f'"{accommodation.property_name}" has been unpublished.')
    return redirect("core:hostdashboard")


@login_required
@require_POST
def unpublish_tour(request, tour_id):
    """Unpublish a tour listing."""
    tour = get_object_or_404(Tour, id=tour_id, host=request.user)

    tour.is_published = False
    tour.is_active = False
    tour.status = "draft"
    tour.save()

    messages.success(request, f'"{tour.tour_name}" has been unpublished.')
    return redirect("core:hostdashboard")


@login_required
@require_POST
def unpublish_rental_car(request, car_id):
    """Unpublish a rental car listing."""
    rental_car = get_object_or_404(RentalCar, id=car_id, host=request.user)

    rental_car.is_published = False
    rental_car.is_active = False
    rental_car.status = "draft"
    rental_car.save()

    messages.success(request, f'"{rental_car.vehicle_name}" has been unpublished.')
    return redirect("core:hostdashboard")


# Admin approval functions
def is_admin(user):
    """Check if user is admin or staff."""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_approve_accommodation(request, accommodation_id):
    """Admin approves an accommodation listing."""
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)

    accommodation.status = "published"
    accommodation.is_published = True
    accommodation.is_active = True
    accommodation.approved_at = timezone.now()
    accommodation.approved_by = request.user
    accommodation.requires_approval = False

    if not accommodation.published_at:
        accommodation.published_at = timezone.now()

    accommodation.save()

    # Send approval email
    send_listing_approved_email(accommodation, "accommodation")

    messages.success(
        request,
        f'Accommodation "{accommodation.property_name}" has been approved and published.',
    )
    return redirect("admin:core_accommodation_changelist")


@login_required
@user_passes_test(is_admin)
def admin_reject_accommodation(request, accommodation_id):
    """Admin rejects an accommodation listing."""
    accommodation = get_object_or_404(Accommodation, id=accommodation_id)

    if request.method == "POST":
        reason = request.POST.get("reason", "")

        accommodation.status = "rejected"
        accommodation.is_published = False
        accommodation.is_active = False
        accommodation.rejection_reason = reason
        accommodation.save()

        # Send rejection email
        send_listing_rejected_email(accommodation, "accommodation", reason)

        messages.success(
            request, f'Accommodation "{accommodation.property_name}" has been rejected.'
        )
        return redirect("admin:core_accommodation_changelist")

    return render(
        request,
        "core/admin_reject_listing.html",
        {"listing": accommodation, "listing_type": "accommodation"},
    )


@login_required
@user_passes_test(is_admin)
def admin_approve_tour(request, tour_id):
    """Admin approves a tour listing."""
    tour = get_object_or_404(Tour, id=tour_id)

    tour.status = "published"
    tour.is_published = True
    tour.is_active = True
    tour.approved_at = timezone.now()
    tour.approved_by = request.user
    tour.requires_approval = False

    if not tour.published_at:
        tour.published_at = timezone.now()

    tour.save()

    # Send approval email
    send_listing_approved_email(tour, "tour")

    messages.success(
        request, f'Tour "{tour.tour_name}" has been approved and published.'
    )
    return redirect("admin:core_tour_changelist")


@login_required
@user_passes_test(is_admin)
def admin_reject_tour(request, tour_id):
    """Admin rejects a tour listing."""
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == "POST":
        reason = request.POST.get("reason", "")

        tour.status = "rejected"
        tour.is_published = False
        tour.is_active = False
        tour.rejection_reason = reason
        tour.save()

        # Send rejection email
        send_listing_rejected_email(tour, "tour", reason)

        messages.success(request, f'Tour "{tour.tour_name}" has been rejected.')
        return redirect("admin:core_tour_changelist")

    return render(
        request,
        "core/admin_reject_listing.html",
        {"listing": tour, "listing_type": "tour"},
    )


@login_required
def get_published_listings_by_location(request, country=None, city=None):
    """
    API endpoint to get published listings by location.
    Used for displaying listings on country/city pages.
    """
    # Get published accommodations
    accommodations = Accommodation.objects.filter(
        is_published=True, is_active=True, status="published"
    )

    # Get published tours
    tours = Tour.objects.filter(is_published=True, is_active=True, status="published")

    # Get published rental cars
    rental_cars = RentalCar.objects.filter(
        is_published=True, is_active=True, status="published"
    )

    # Filter by location
    if country:
        accommodations = accommodations.filter(country__iexact=country)
        tours = tours.filter(country__iexact=country)
        rental_cars = rental_cars.filter(country__iexact=country)

    if city:
        accommodations = accommodations.filter(city__iexact=city)
        tours = tours.filter(city__iexact=city)
        rental_cars = rental_cars.filter(city__iexact=city)

    return JsonResponse(
        {
            "accommodations": list(
                accommodations.values(
                    "id", "property_name", "city", "country", "base_price"
                )
            ),
            "tours": list(
                tours.values("id", "tour_name", "city", "country", "price_per_person")
            ),
            "rental_cars": list(
                rental_cars.values(
                    "id", "vehicle_name", "city", "country", "daily_rate"
                )
            ),
        }
    )


def send_admin_notification(listing, listing_type):
    """
    Send email notification to admin when new listing is published.

    📧 Notifies site admin about new content for monitoring.
    """
    try:
        # Get admin email from settings or use default
        admin_email = getattr(settings, "ADMIN_EMAIL", "admin@bedbees.com")

        if listing_type == "accommodation":
            subject = f"New Accommodation Published: {listing.property_name}"
            message = f"""
New accommodation listing published:

Property: {listing.property_name}
Type: {listing.property_type}
Location: {listing.city}, {listing.country}
Host: {listing.host.get_full_name() if hasattr(listing.host, 'get_full_name') else listing.host.username}
Price: ${listing.base_price}/night

Published at: {listing.published_at}

View in admin panel to monitor quality.
            """
        else:  # tour
            subject = f"New Tour Published: {listing.tour_name}"
            message = f"""
New tour listing published:

Tour: {listing.tour_name}
Category: {listing.tour_category}
Location: {listing.city}, {listing.country}
Host: {listing.host.get_full_name() if hasattr(listing.host, 'get_full_name') else listing.host.username}
Price: ${listing.price_per_person}/person

Published at: {listing.published_at}

View in admin panel to monitor quality.
            """

        # Send email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=True,  # Don't break if email fails
        )
    except Exception as e:
        # Log error but don't break the publishing flow
        print(f"Admin notification email failed: {str(e)}")
        pass
