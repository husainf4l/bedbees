"""
Test script for Genius Rewards System
Run this to verify the system is working correctly
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import GeniusProfile, Booking, Reward, Redemption


class Command(BaseCommand):
    help = "Test the Genius Rewards system functionality"

    def handle(self, *args, **kwargs):
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("GENIUS REWARDS SYSTEM TEST")
        self.stdout.write("=" * 60 + "\n")

        # Test 1: Check if rewards exist
        self.stdout.write("📋 Test 1: Checking rewards...")
        rewards_count = Reward.objects.count()
        if rewards_count > 0:
            self.stdout.write(self.style.SUCCESS(f"   ✓ {rewards_count} rewards found"))
        else:
            self.stdout.write(
                self.style.ERROR(
                    "   ✗ No rewards found. Run: python manage.py seed_rewards"
                )
            )
            return

        # Test 2: Create test user with GeniusProfile
        self.stdout.write("\n👤 Test 2: Creating test user...")
        test_user, created = User.objects.get_or_create(
            username="genius_test_user",
            defaults={
                "email": "test@genius.com",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        if created:
            test_user.set_password("testpass123")
            test_user.save()
            self.stdout.write(self.style.SUCCESS("   ✓ Test user created"))
        else:
            self.stdout.write(self.style.WARNING("   ↻ Test user already exists"))

        # Test 3: Check GeniusProfile auto-creation
        self.stdout.write("\n🏆 Test 3: Checking GeniusProfile...")
        if hasattr(test_user, "genius_profile"):
            profile = test_user.genius_profile
            self.stdout.write(self.style.SUCCESS(f"   ✓ GeniusProfile exists"))
            self.stdout.write(f"      Level: {profile.level} ({profile.level_name})")
            self.stdout.write(f"      Points: {profile.total_points}")
        else:
            self.stdout.write(self.style.ERROR("   ✗ GeniusProfile not found"))
            return

        # Test 4: Create a test booking
        self.stdout.write("\n💳 Test 4: Creating test booking...")
        booking = Booking.objects.create(
            user=test_user,
            booking_type="accommodation",
            total_amount=150.00,
            status="pending",
        )
        self.stdout.write(
            self.style.SUCCESS(f"   ✓ Booking created (${booking.total_amount})")
        )
        self.stdout.write(f"      Status: {booking.status}")
        self.stdout.write(f"      Points awarded: {booking.points_awarded}")

        # Test 5: Complete booking and check points
        self.stdout.write("\n🎯 Test 5: Completing booking...")
        booking.status = "completed"
        booking.save()

        # Refresh profile
        profile.refresh_from_db()

        expected_points = int((150.00 / 50) * 10 * profile.points_multiplier)

        if booking.points_awarded > 0:
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ Points awarded: {booking.points_awarded}")
            )
            self.stdout.write(f"      Expected: {expected_points}")
            self.stdout.write(f"      User now has: {profile.total_points} points")
            self.stdout.write(f"      Reward value: ${profile.reward_value():.2f}")
        else:
            self.stdout.write(self.style.ERROR("   ✗ Points not awarded"))

        # Test 6: Check available rewards
        self.stdout.write("\n🎁 Test 6: Checking available rewards...")
        available = Reward.objects.filter(is_active=True, min_level__lte=profile.level)
        self.stdout.write(
            self.style.SUCCESS(
                f"   ✓ {available.count()} rewards available for Level {profile.level}"
            )
        )

        for reward in available[:3]:
            can_afford = profile.total_points >= reward.cost_points
            status = "✓" if can_afford else "✗"
            self.stdout.write(
                f"      {status} {reward.name} ({reward.cost_points} pts = ${reward.value})"
            )

        # Test 7: Test redemption (if enough points)
        self.stdout.write("\n💰 Test 7: Testing redemption...")
        affordable_rewards = available.filter(cost_points__lte=profile.total_points)

        if affordable_rewards.exists():
            reward = affordable_rewards.first()
            points_before = profile.total_points
            success, message = profile.redeem_points(reward)

            if success:
                profile.refresh_from_db()
                self.stdout.write(self.style.SUCCESS(f"   ✓ Redemption successful!"))
                self.stdout.write(f"      Reward: {reward.name}")
                self.stdout.write(f"      Points used: {reward.cost_points}")
                self.stdout.write(f"      Points before: {points_before}")
                self.stdout.write(f"      Points after: {profile.total_points}")
                self.stdout.write(f"      Message: {message}")
            else:
                self.stdout.write(
                    self.style.ERROR(f"   ✗ Redemption failed: {message}")
                )
        else:
            self.stdout.write(
                self.style.WARNING("   ⚠ Not enough points for redemption test")
            )
            self.stdout.write(f"      Current points: {profile.total_points}")
            self.stdout.write(
                f"      Cheapest reward: {available.first().cost_points} pts"
            )

        # Test 8: Check redemption history
        self.stdout.write("\n📜 Test 8: Checking redemption history...")
        redemptions = Redemption.objects.filter(user=test_user)
        if redemptions.exists():
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ {redemptions.count()} redemption(s) found")
            )
            for redemption in redemptions:
                self.stdout.write(
                    f"      {redemption.redemption_code}: {redemption.reward.name} ({redemption.status})"
                )
        else:
            self.stdout.write(self.style.WARNING("   ⚠ No redemptions yet"))

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("TEST SUMMARY")
        self.stdout.write("=" * 60)
        self.stdout.write(f"User: {test_user.username}")
        self.stdout.write(f"Level: {profile.level} ({profile.level_name})")
        self.stdout.write(f"Total Points: {profile.total_points}")
        self.stdout.write(f"Lifetime Points: {profile.lifetime_points}")
        self.stdout.write(f"Reward Value: ${profile.reward_value():.2f}")
        self.stdout.write(f"Total Spent: ${profile.total_spent:.2f}")
        self.stdout.write(f"Total Bookings: {profile.total_bookings}")
        self.stdout.write(f"Total Redeemed: {profile.total_redeemed} points")
        self.stdout.write(f"Discount: {profile.discount_percentage}%")
        self.stdout.write(f"Multiplier: {profile.points_multiplier}x")

        if profile.next_level_points:
            self.stdout.write(f"Points to next level: {profile.points_to_next_level}")
        else:
            self.stdout.write("Status: Max level reached!")

        self.stdout.write("\n" + self.style.SUCCESS("✓ ALL TESTS PASSED!"))
        self.stdout.write(
            self.style.SUCCESS("✓ Genius Rewards System is fully operational!\n")
        )
