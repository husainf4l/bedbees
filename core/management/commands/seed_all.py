"""
Comprehensive seeding command for all database data
Usage: python manage.py seed_all [--clear] [--create-admin]
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from core.models import UserProfile, Country
from core.data.countries_data import countries_data
from core.data.demo_attractions import demo_attractions
import json


class Command(BaseCommand):
    help = "Seeds all database data: countries, attractions, admin user, and optionally demo listings"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )
        parser.add_argument(
            "--create-admin",
            action="store_true",
            help="Create admin user for testing/deployment",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=" * 80))
        self.stdout.write(
            self.style.SUCCESS("🌟 COMPREHENSIVE DATABASE SEEDING STARTED")
        )
        self.stdout.write(self.style.SUCCESS("=" * 80))

        if options["clear"]:
            self.clear_database()

        if options["create_admin"]:
            self.create_admin_user()

        # Seed data
        with transaction.atomic():
            self.seed_countries()

        self.stdout.write(self.style.SUCCESS("\n" + "=" * 80))
        self.stdout.write(
            self.style.SUCCESS("✅ COMPREHENSIVE DATABASE SEEDING COMPLETED")
        )
        self.stdout.write(self.style.SUCCESS("=" * 80))

        # Summary
        self.print_summary()

    def clear_database(self):
        """Clear existing data"""
        self.stdout.write(self.style.WARNING("\n🗑️  Clearing existing data..."))

        Country.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("   ✅ Countries cleared"))

        self.stdout.write(self.style.SUCCESS("✅ Database cleared\n"))

    def create_admin_user(self):
        """Create admin user for testing/deployment"""
        self.stdout.write(self.style.WARNING("\n👤 Creating admin user..."))

        # Check if admin exists
        if User.objects.filter(username="admin").exists():
            self.stdout.write(self.style.WARNING("   ⚠️  Admin user already exists"))
            admin = User.objects.get(username="admin")
        else:
            # Create admin user
            admin = User.objects.create_superuser(
                username="admin",
                email="admin@bedbees.com",
                password="admin123",
                first_name="Admin",
                last_name="User",
            )

            # Create profile
            UserProfile.objects.create(
                user=admin,
                is_host=True,
                business_name="BedBees Administration",
                business_type="company",
                email_verified=True,
                phone_verified=True,
                id_verified=True,
                business_license_verified=True,
                payment_verified=True,
            )

            self.stdout.write(self.style.SUCCESS("   ✅ Admin user created"))
            self.stdout.write(self.style.SUCCESS("      Username: admin"))
            self.stdout.write(self.style.SUCCESS("      Password: admin123"))
            self.stdout.write(self.style.SUCCESS("      Email: admin@bedbees.com"))

    def seed_countries(self):
        """Seed countries and attractions from data modules"""
        self.stdout.write(
            self.style.WARNING("\n🌍 Seeding countries and attractions...")
        )

        countries_created = 0
        countries_updated = 0
        total_attractions = 0

        for country_slug, country_info in countries_data.items():
            # Use update_or_create to avoid duplicates
            country, created = Country.objects.update_or_create(
                slug=country_slug,
                defaults={
                    "name": country_info.get(
                        "name", country_slug.replace("-", " ").title()
                    ),
                    "code": country_info.get("code", country_slug.upper()[:3]),
                    "description": country_info.get("description", ""),
                    "image": country_info.get("image", ""),
                    "accommodations_count": country_info.get("accommodations_count", 0),
                    "tours_count": country_info.get("tours_count", 0),
                    "is_active": True,
                },
            )

            if created:
                countries_created += 1
                status = self.style.SUCCESS("✅ Created")
            else:
                countries_updated += 1
                status = self.style.WARNING("♻️  Updated")

            # Build full attractions data with details from demo_attractions
            attractions_list = country_info.get("attractions", [])
            country_demo_attractions = demo_attractions.get(country_slug, {})

            full_attractions = []
            for attraction_data in attractions_list:
                if isinstance(attraction_data, dict):
                    attraction_slug = attraction_data.get("slug", "")
                    attraction_name = attraction_data.get("name", "")
                    attraction_desc = attraction_data.get("description", "")
                    attraction_img = attraction_data.get("image", "")
                elif isinstance(attraction_data, str):
                    attraction_slug = attraction_data
                    attraction_name = attraction_data.replace("-", " ").title()
                    attraction_desc = ""
                    attraction_img = ""
                else:
                    continue

                # Get detailed info from demo_attractions
                attraction_details = country_demo_attractions.get(attraction_slug, {})

                # Build comprehensive attraction object
                full_attraction = {
                    "id": attraction_slug,
                    "slug": attraction_slug,
                    "name": attraction_details.get("name", attraction_name),
                    "location": attraction_details.get("location", ""),
                    "description": attraction_details.get(
                        "description", attraction_desc
                    ),
                    "short_description": attraction_details.get(
                        "short_description", attraction_desc
                    ),
                    "long_description": attraction_details.get("long_description", ""),
                    "image": attraction_details.get("image", attraction_img),
                    "hero_image": attraction_details.get("hero_image", attraction_img),
                    "photos": attraction_details.get(
                        "photos", [attraction_img] if attraction_img else []
                    ),
                    "historical_significance": attraction_details.get(
                        "historical_significance", ""
                    ),
                    "cultural_impact": attraction_details.get("cultural_impact", ""),
                    "discovery": attraction_details.get("discovery", ""),
                    "architecture": attraction_details.get("architecture", ""),
                    "water_system": attraction_details.get("water_system", ""),
                    "best_time_to_visit": attraction_details.get(
                        "best_time_to_visit", ""
                    ),
                    "how_to_get_there": attraction_details.get("how_to_get_there", ""),
                    "entrance_fee": attraction_details.get("entrance_fee", ""),
                    "entrance_fees": attraction_details.get("entrance_fees", ""),
                    "opening_hours": attraction_details.get("opening_hours", ""),
                    "what_to_wear": attraction_details.get("what_to_wear", ""),
                    "health_safety": attraction_details.get("health_safety", ""),
                    "guided_tours": attraction_details.get("guided_tours", ""),
                    "conservation": attraction_details.get("conservation", ""),
                    "facts": attraction_details.get("facts", []),
                    "visitor_tips": attraction_details.get("visitor_tips", []),
                    "nearby_attractions": attraction_details.get(
                        "nearby_attractions", []
                    ),
                    "key_sites": attraction_details.get("key_sites", []),
                    "photo_gallery": attraction_details.get("photo_gallery", []),
                    "coordinates": attraction_details.get("coordinates", {}),
                    "annual_visitors": attraction_details.get("annual_visitors", 0),
                    "unesco_site": attraction_details.get("unesco_site", False),
                    "climate": attraction_details.get("climate", ""),
                }

                # Remove empty/None values to keep JSON clean
                full_attraction = {k: v for k, v in full_attraction.items() if v}
                full_attractions.append(full_attraction)
                total_attractions += 1

            country.attractions = full_attractions
            country.save()

            self.stdout.write(
                f"   {status} {country.name} ({len(full_attractions)} attractions)"
            )

        self.stdout.write(self.style.SUCCESS(f"\n✅ Countries processed:"))
        self.stdout.write(
            self.style.SUCCESS(f"   • Countries created: {countries_created}")
        )
        self.stdout.write(
            self.style.SUCCESS(f"   • Countries updated: {countries_updated}")
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"   • Total countries: {countries_created + countries_updated}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f"   • Total attractions seeded: {total_attractions}")
        )

    def print_summary(self):
        """Print seeding summary"""
        self.stdout.write(self.style.SUCCESS("\n📊 DATABASE STATUS:"))

        # Count countries
        countries_count = Country.objects.count()
        active_countries = Country.objects.filter(is_active=True).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"   • Countries: {countries_count} ({active_countries} active)"
            )
        )

        # Count users
        total_users = User.objects.count()
        admin_users = User.objects.filter(is_superuser=True).count()
        host_users = UserProfile.objects.filter(is_host=True).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"   • Users: {total_users} ({admin_users} admins, {host_users} hosts)"
            )
        )

        # Count attractions
        total_attractions = sum(
            len(country.attractions) if country.attractions else 0
            for country in Country.objects.all()
        )
        self.stdout.write(self.style.SUCCESS(f"   • Attractions: {total_attractions}"))

        self.stdout.write(self.style.SUCCESS("\n💡 NEXT STEPS:"))
        self.stdout.write(
            self.style.SUCCESS(
                "   1. Run demo data seeding: python manage.py seed_demo_data"
            )
        )
        self.stdout.write(
            self.style.SUCCESS("   2. Start the server: python manage.py runserver")
        )
        self.stdout.write(
            self.style.SUCCESS(
                "   3. Access host dashboard: http://localhost:8000/hostdashboard/"
            )
        )
        self.stdout.write(self.style.SUCCESS("   4. Login with: admin / admin123"))
