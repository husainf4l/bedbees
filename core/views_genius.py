"""
Views for Genius Rewards System
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from .models import GeniusProfile, Reward, Redemption, Booking


class GeniusRewardsView(LoginRequiredMixin, TemplateView):
    """
    Main Genius Rewards dashboard
    Shows user's points, level, available rewards, and redemption history
    """

    template_name = "core/genius_rewards.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get or create genius profile
        genius_profile, created = GeniusProfile.objects.get_or_create(user=user)

        # Get available rewards (filtered by user level)
        available_rewards = Reward.objects.filter(
            is_active=True, min_level__lte=genius_profile.level
        )

        # Get user's redemption history
        redemptions = (
            Redemption.objects.filter(user=user)
            .select_related("reward")
            .order_by("-redeemed_at")[:10]
        )

        # Get recent completed bookings
        recent_bookings = Booking.objects.filter(
            user=user, status="completed"
        ).order_by("-updated_at")[:5]

        # Calculate statistics (use separate query to avoid slice+filter issue)
        total_savings = (
            Redemption.objects.filter(
                user=user, status__in=["approved", "fulfilled"]
            ).aggregate(total=Sum("reward__value"))["total"]
            or 0
        )

        # Level benefits
        level_benefits = {
            1: {
                "name": "Explorer",
                "discount": "5%",
                "multiplier": "1.0x",
                "perks": ["5% off next stay", "Member pricing", "Priority support"],
                "next": "Voyager (100 pts)",
            },
            2: {
                "name": "Voyager",
                "discount": "10%",
                "multiplier": "1.1x",
                "perks": [
                    "10% off stays",
                    "1.1x points",
                    "Room upgrades",
                    "Free breakfast",
                ],
                "next": "Elite (300 pts)",
            },
            3: {
                "name": "Elite",
                "discount": "15%",
                "multiplier": "1.2x",
                "perks": [
                    "15% off stays",
                    "1.2x points",
                    "VIP treatment",
                    "Airport transfer",
                    "Late checkout",
                ],
                "next": "Max level reached!",
            },
        }

        context.update(
            {
                "genius_profile": genius_profile,
                "available_rewards": available_rewards,
                "redemptions": redemptions,
                "recent_bookings": recent_bookings,
                "total_savings": total_savings,
                "reward_value": genius_profile.reward_value(),
                "level_benefits": level_benefits,
                "current_level_info": level_benefits.get(genius_profile.level, {}),
                "points_to_next": genius_profile.points_to_next_level,
            }
        )

        return context


@login_required
def redeem_reward(request, reward_id):
    """
    Handle reward redemption
    """
    reward = get_object_or_404(Reward, id=reward_id)
    genius_profile = request.user.genius_profile

    # Check if reward is available
    if not reward.is_available:
        messages.error(request, f"Sorry, {reward.name} is currently unavailable.")
        return redirect("genius_rewards")

    # Check level requirement
    if genius_profile.level < reward.min_level:
        level_names = {1: "Explorer", 2: "Voyager", 3: "Elite"}
        required_level = level_names.get(reward.min_level, "Unknown")
        messages.error(
            request,
            f"You need to be {required_level} level or higher to redeem this reward.",
        )
        return redirect("genius_rewards")

    # Attempt redemption
    if request.method == "POST":
        success, message = genius_profile.redeem_points(reward)

        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)

    return redirect("genius_rewards")


@login_required
def genius_rewards_api(request):
    """
    API endpoint for genius rewards data (for AJAX requests)
    Returns JSON data about user's genius profile
    """
    genius_profile = request.user.genius_profile

    data = {
        "success": True,
        "profile": {
            "total_points": genius_profile.total_points,
            "lifetime_points": genius_profile.lifetime_points,
            "level": genius_profile.level,
            "level_name": genius_profile.level_name,
            "discount_percentage": genius_profile.discount_percentage,
            "points_multiplier": genius_profile.points_multiplier,
            "reward_value": float(genius_profile.reward_value()),
            "total_spent": float(genius_profile.total_spent),
            "total_bookings": genius_profile.total_bookings,
            "points_to_next_level": genius_profile.points_to_next_level,
        },
        "available_rewards": [
            {
                "id": reward.id,
                "name": reward.name,
                "description": reward.description,
                "cost_points": reward.cost_points,
                "value": float(reward.value),
                "type": reward.reward_type,
                "is_available": reward.is_available,
            }
            for reward in Reward.objects.filter(
                is_active=True, min_level__lte=genius_profile.level
            )
        ],
    }

    return JsonResponse(data)


class RewardDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view for a specific reward
    """

    model = Reward
    template_name = "core/reward_detail.html"
    context_object_name = "reward"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genius_profile"] = self.request.user.genius_profile
        context["can_redeem"] = (
            context["genius_profile"].total_points >= self.object.cost_points
            and context["genius_profile"].level >= self.object.min_level
        )
        return context


@login_required
def redemption_history(request):
    """
    Show user's complete redemption history
    """
    redemptions = (
        Redemption.objects.filter(user=request.user)
        .select_related("reward")
        .order_by("-redeemed_at")
    )

    # Calculate total value redeemed
    total_value = (
        redemptions.filter(status__in=["approved", "fulfilled"]).aggregate(
            total=Sum("reward__value")
        )["total"]
        or 0
    )

    context = {
        "redemptions": redemptions,
        "total_value": total_value,
        "genius_profile": request.user.genius_profile,
    }

    return render(request, "core/redemption_history.html", context)


@login_required
def booking_history(request):
    """
    Show user's booking history with points earned
    """
    bookings = Booking.objects.filter(user=request.user).order_by("-created_at")

    # Calculate statistics
    stats = {
        "total_bookings": bookings.count(),
        "completed": bookings.filter(status="completed").count(),
        "total_spent": bookings.filter(status="completed").aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0,
        "total_points_earned": bookings.filter(status="completed").aggregate(
            total=Sum("points_awarded")
        )["total"]
        or 0,
    }

    context = {
        "bookings": bookings,
        "stats": stats,
        "genius_profile": request.user.genius_profile,
    }

    return render(request, "core/booking_history.html", context)
