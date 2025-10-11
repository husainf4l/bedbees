"""
Signals for Genius Rewards System
Handles automatic profile creation and points awarding
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import GeniusProfile, Booking


@receiver(post_save, sender=User)
def create_genius_profile(sender, instance, created, **kwargs):
    """
    Automatically create a GeniusProfile when a new user registers
    """
    if created:
        GeniusProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_genius_profile(sender, instance, **kwargs):
    """
    Ensure GeniusProfile exists and is saved
    """
    if not hasattr(instance, "genius_profile"):
        GeniusProfile.objects.create(user=instance)
    else:
        instance.genius_profile.save()


@receiver(pre_save, sender=Booking)
def track_booking_status_change(sender, instance, **kwargs):
    """
    Track when booking status changes to 'completed'
    and award points automatically
    """
    if instance.pk:  # Only for existing bookings (updates)
        try:
            old_booking = Booking.objects.get(pk=instance.pk)

            # Check if status changed to 'completed'
            if old_booking.status != "completed" and instance.status == "completed":
                # Award points only if not already awarded
                if instance.points_awarded == 0:
                    genius_profile = instance.user.genius_profile
                    points_earned = genius_profile.add_points(instance)

                    # Update the instance with points (will be saved automatically)
                    instance.points_awarded = points_earned

                    print(
                        f"✅ Awarded {points_earned} points to {instance.user.username} for booking #{instance.pk}"
                    )

        except Booking.DoesNotExist:
            pass
