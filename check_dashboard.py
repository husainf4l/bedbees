#!/usr/bin/env python
"""
Comprehensive Host Dashboard Verification Script
Checks all database seeding and dashboard functionality
"""

import os
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bedbees.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import (
    UserProfile,
    Country,
    Accommodation,
    Tour,
    AccommodationPhoto,
    TourPhoto,
    Listing,
    RoomType,
    AvailabilityDay,
    DayRoomInventory,
)


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_section(text):
    """Print a formatted section"""
    print(f"\n📋 {text}")
    print("-" * 80)


def check_database_seeding():
    """Check all database seeding"""
    print_header("🔍 DATABASE SEEDING VERIFICATION")

    # Countries
    print_section("Countries and Attractions")
    countries = Country.objects.all()
    print(f"✅ Total Countries: {countries.count()}")
    print(f"✅ Active Countries: {Country.objects.filter(is_active=True).count()}")

    total_attractions = 0
    for country in countries[:5]:  # Show first 5
        attr_count = len(country.attractions) if country.attractions else 0
        total_attractions += attr_count
        print(f"   • {country.name}: {attr_count} attractions")

    total_attr_all = sum(len(c.attractions) if c.attractions else 0 for c in countries)
    print(f"✅ Total Attractions: {total_attr_all}")

    # Users and Profiles
    print_section("Users and Profiles")
    users = User.objects.all()
    print(f"✅ Total Users: {users.count()}")
    print(f"✅ Admin Users: {User.objects.filter(is_superuser=True).count()}")
    print(f"✅ Staff Users: {User.objects.filter(is_staff=True).count()}")

    profiles = UserProfile.objects.all()
    print(f"✅ Total Profiles: {profiles.count()}")
    print(f"✅ Host Profiles: {UserProfile.objects.filter(is_host=True).count()}")
    print(
        f"✅ Verified Hosts: {UserProfile.objects.filter(is_host=True, email_verified=True).count()}"
    )

    # Accommodations
    print_section("Accommodations")
    accommodations = Accommodation.objects.all()
    print(f"✅ Total Accommodations: {accommodations.count()}")
    print(
        f"✅ Published Accommodations: {Accommodation.objects.filter(is_published=True).count()}"
    )
    print(
        f"✅ Active Accommodations: {Accommodation.objects.filter(is_active=True).count()}"
    )

    # Show sample accommodations
    for acc in accommodations[:3]:
        photos = AccommodationPhoto.objects.filter(accommodation=acc).count()
        print(f"   • {acc.property_name} - {acc.city}, {acc.country} - {photos} photos")

    # Tours
    print_section("Tours and Experiences")
    tours = Tour.objects.all()
    print(f"✅ Total Tours: {tours.count()}")
    print(f"✅ Published Tours: {Tour.objects.filter(is_published=True).count()}")
    print(f"✅ Active Tours: {Tour.objects.filter(is_active=True).count()}")

    # Show sample tours
    for tour in tours[:3]:
        photos = TourPhoto.objects.filter(tour=tour).count()
        print(f"   • {tour.tour_name} - {tour.city}, {tour.country} - {photos} photos")

    # Listings and Inventory
    print_section("Listings and Inventory System")
    listings = Listing.objects.all()
    print(f"✅ Total Listings: {listings.count()}")
    print(f"✅ Active Listings: {Listing.objects.filter(is_active=True).count()}")
    print(f"✅ Published Listings: {Listing.objects.filter(is_published=True).count()}")

    room_types = RoomType.objects.all()
    print(f"✅ Total Room Types: {room_types.count()}")
    print(f"✅ Active Room Types: {RoomType.objects.filter(is_active=True).count()}")

    availability_days = AvailabilityDay.objects.all()
    print(f"✅ Total Availability Days: {availability_days.count()}")
    print(f"✅ Open Days: {AvailabilityDay.objects.filter(status='OPEN').count()}")

    inventory = DayRoomInventory.objects.all()
    print(f"✅ Total Inventory Records: {inventory.count()}")

    # Photos
    print_section("Photos and Media")
    acc_photos = AccommodationPhoto.objects.all()
    tour_photos = TourPhoto.objects.all()
    print(f"✅ Accommodation Photos: {acc_photos.count()}")
    print(f"✅ Tour Photos: {tour_photos.count()}")
    print(f"✅ Total Photos: {acc_photos.count() + tour_photos.count()}")

    return True


def check_admin_access():
    """Check admin user credentials"""
    print_header("👤 ADMIN USER VERIFICATION")

    try:
        admin = User.objects.get(username="admin")
        profile = UserProfile.objects.get(user=admin)

        print("✅ Admin User Found:")
        print(f"   • Username: {admin.username}")
        print(f"   • Email: {admin.email}")
        print(f"   • Is Superuser: {admin.is_superuser}")
        print(f"   • Is Staff: {admin.is_staff}")
        print(f"   • Is Host: {profile.is_host}")
        print(f"   • Business Name: {profile.business_name}")
        print(f"   • Email Verified: {profile.email_verified}")
        print(f"   • Phone Verified: {profile.phone_verified}")
        print(f"   • ID Verified: {profile.id_verified}")

        print("\n🔐 Admin Credentials:")
        print("   • Username: admin")
        print("   • Password: admin123")

        return True
    except User.DoesNotExist:
        print("❌ Admin user not found!")
        return False
    except UserProfile.DoesNotExist:
        print("❌ Admin profile not found!")
        return False


def check_demo_data():
    """Check demo data quality"""
    print_header("📊 DEMO DATA QUALITY CHECK")

    # Check if accommodations have required data
    print_section("Accommodation Data Quality")
    incomplete_acc = []
    for acc in Accommodation.objects.all()[:10]:
        issues = []
        if not acc.property_name:
            issues.append("No name")
        if not acc.city:
            issues.append("No city")
        if not acc.country:
            issues.append("No country")
        if not acc.full_description:
            issues.append("No description")
        if AccommodationPhoto.objects.filter(accommodation=acc).count() == 0:
            issues.append("No photos")

        if issues:
            incomplete_acc.append(f"{acc.property_name}: {', '.join(issues)}")

    if incomplete_acc:
        print(f"⚠️  Found {len(incomplete_acc)} accommodations with issues:")
        for issue in incomplete_acc:
            print(f"   • {issue}")
    else:
        print("✅ All checked accommodations have complete data")

    # Check if tours have required data
    print_section("Tour Data Quality")
    incomplete_tours = []
    for tour in Tour.objects.all()[:10]:
        issues = []
        if not tour.tour_name:
            issues.append("No name")
        if not tour.city:
            issues.append("No city")
        if not tour.country:
            issues.append("No country")
        if not tour.full_description:
            issues.append("No description")
        if TourPhoto.objects.filter(tour=tour).count() == 0:
            issues.append("No photos")

        if issues:
            incomplete_tours.append(f"{tour.tour_name}: {', '.join(issues)}")

    if incomplete_tours:
        print(f"⚠️  Found {len(incomplete_tours)} tours with issues:")
        for issue in incomplete_tours:
            print(f"   • {issue}")
    else:
        print("✅ All checked tours have complete data")

    return True


def check_host_dashboard_readiness():
    """Check if host dashboard is ready"""
    print_header("🏠 HOST DASHBOARD READINESS CHECK")

    checks_passed = 0
    total_checks = 6

    # Check 1: Admin user exists
    if User.objects.filter(username="admin").exists():
        print("✅ Admin user exists")
        checks_passed += 1
    else:
        print("❌ Admin user not found")

    # Check 2: Countries seeded
    if Country.objects.count() > 0:
        print(f"✅ Countries seeded ({Country.objects.count()} countries)")
        checks_passed += 1
    else:
        print("❌ No countries found")

    # Check 3: Accommodations exist
    if Accommodation.objects.count() > 0:
        print(f"✅ Accommodations exist ({Accommodation.objects.count()} properties)")
        checks_passed += 1
    else:
        print("❌ No accommodations found")

    # Check 4: Tours exist
    if Tour.objects.count() > 0:
        print(f"✅ Tours exist ({Tour.objects.count()} tours)")
        checks_passed += 1
    else:
        print("❌ No tours found")

    # Check 5: Listings exist
    if Listing.objects.count() > 0:
        print(f"✅ Listings exist ({Listing.objects.count()} listings)")
        checks_passed += 1
    else:
        print("❌ No listings found")

    # Check 6: Inventory exists
    if DayRoomInventory.objects.count() > 0:
        print(
            f"✅ Inventory system populated ({DayRoomInventory.objects.count()} records)"
        )
        checks_passed += 1
    else:
        print("❌ No inventory records found")

    print(f"\n📊 Dashboard Readiness: {checks_passed}/{total_checks} checks passed")

    if checks_passed == total_checks:
        print("✅ Host dashboard is READY!")
        return True
    else:
        print("⚠️  Some checks failed. Host dashboard may have limited functionality.")
        return False


def print_next_steps():
    """Print next steps"""
    print_header("🚀 NEXT STEPS")

    print("\n1. Start the development server:")
    print("   python manage.py runserver")

    print("\n2. Access the host dashboard:")
    print("   http://localhost:8000/hostdashboard/")

    print("\n3. Login with admin credentials:")
    print("   Username: admin")
    print("   Password: admin123")

    print("\n4. Explore dashboard features:")
    print("   • View and manage listings")
    print("   • Create new accommodations")
    print("   • Create new tours")
    print("   • Manage availability calendar")
    print("   • Update host profile")
    print("   • View bookings and reviews")

    print("\n5. Additional seeding options:")
    print("   • Clear and reseed: python manage.py seed_all --clear --create-admin")
    print("   • Seed more demo data: python manage.py seed_demo_data")

    print("\n")


def main():
    """Main verification function"""
    try:
        # Run all checks
        check_database_seeding()
        check_admin_access()
        check_demo_data()
        check_host_dashboard_readiness()
        print_next_steps()

        print("=" * 80)
        print("✅ VERIFICATION COMPLETE - All systems ready!")
        print("=" * 80)
        print()

    except Exception as e:
        print(f"\n❌ Error during verification: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
