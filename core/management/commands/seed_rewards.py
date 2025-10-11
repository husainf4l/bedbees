"""
Management command to seed initial Genius Rewards data
"""

from django.core.management.base import BaseCommand
from core.models import Reward


class Command(BaseCommand):
    help = "Seed initial rewards for Genius Rewards system"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Genius Rewards...\n")

        rewards_data = [
            # Credit rewards
            {
                "name": "$10 Travel Credit",
                "description": "Get $10 credit towards your next booking. Valid for 12 months.",
                "reward_type": "credit",
                "cost_points": 100,
                "value": 10.00,
                "min_level": 1,
                "featured": True,
                "display_order": 1,
            },
            {
                "name": "$25 Travel Credit",
                "description": "Get $25 credit towards your next booking. Valid for 12 months.",
                "reward_type": "credit",
                "cost_points": 250,
                "value": 25.00,
                "min_level": 1,
                "featured": True,
                "display_order": 2,
            },
            {
                "name": "$50 Travel Credit",
                "description": "Get $50 credit towards your next booking. Valid for 12 months.",
                "reward_type": "credit",
                "cost_points": 500,
                "value": 50.00,
                "min_level": 2,
                "featured": True,
                "display_order": 3,
            },
            # Upgrade rewards
            {
                "name": "Free Room Upgrade",
                "description": "Upgrade to the next room category at no extra cost. Subject to availability.",
                "reward_type": "upgrade",
                "cost_points": 150,
                "value": 50.00,
                "min_level": 1,
                "display_order": 4,
            },
            {
                "name": "Premium Suite Upgrade",
                "description": "Upgrade to a premium suite. Includes late checkout and breakfast.",
                "reward_type": "upgrade",
                "cost_points": 350,
                "value": 150.00,
                "min_level": 2,
                "display_order": 5,
            },
            # Getaway rewards
            {
                "name": "Weekend Getaway",
                "description": "2-night stay at selected properties. Includes breakfast and late checkout.",
                "reward_type": "getaway",
                "cost_points": 600,
                "value": 200.00,
                "min_level": 2,
                "featured": True,
                "display_order": 6,
            },
            {
                "name": "Luxury Escape",
                "description": "3-night stay at 5-star properties. Includes all meals and spa treatment.",
                "reward_type": "getaway",
                "cost_points": 1200,
                "value": 500.00,
                "min_level": 3,
                "featured": True,
                "display_order": 7,
            },
            # Special offers
            {
                "name": "Early Check-in",
                "description": "Check in early at any property, subject to availability.",
                "reward_type": "special",
                "cost_points": 50,
                "value": 20.00,
                "min_level": 1,
                "display_order": 8,
            },
            {
                "name": "Late Checkout",
                "description": "Enjoy late checkout until 2 PM at any property.",
                "reward_type": "special",
                "cost_points": 50,
                "value": 20.00,
                "min_level": 1,
                "display_order": 9,
            },
            {
                "name": "Airport Transfer",
                "description": "Complimentary airport transfer to your accommodation.",
                "reward_type": "special",
                "cost_points": 200,
                "value": 75.00,
                "min_level": 2,
                "display_order": 10,
            },
            {
                "name": "Spa Day Package",
                "description": "Full day spa package including massage, facial, and sauna.",
                "reward_type": "special",
                "cost_points": 400,
                "value": 150.00,
                "min_level": 2,
                "display_order": 11,
            },
            {
                "name": "VIP Concierge Service",
                "description": "Personal concierge service for your entire stay.",
                "reward_type": "special",
                "cost_points": 300,
                "value": 100.00,
                "min_level": 3,
                "display_order": 12,
            },
        ]

        created_count = 0
        updated_count = 0

        for reward_data in rewards_data:
            reward, created = Reward.objects.update_or_create(
                name=reward_data["name"], defaults=reward_data
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Created: {reward.name}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"↻ Updated: {reward.name}"))

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS(f"\n✓ Seeding complete!"))
        self.stdout.write(f"  Created: {created_count} rewards")
        self.stdout.write(f"  Updated: {updated_count} rewards")
        self.stdout.write(f"  Total: {Reward.objects.count()} rewards in database\n")
