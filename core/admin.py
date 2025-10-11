from django.contrib import admin
from .models import (
    UserProfile,
    Accommodation,
    AccommodationPhoto,
    Tour,
    TourPhoto,
    AccommodationInventory,
    TourInventory,
    SeasonalRate,
    RecurringRule,
    Booking,
    GeniusProfile,
    Reward,
    Redemption,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "is_host", "email_verified", "phone_verified", "created_at"]
    list_filter = ["is_host", "email_verified", "phone_verified"]
    search_fields = ["user__username", "user__email", "business_name"]


class AccommodationPhotoInline(admin.TabularInline):
    model = AccommodationPhoto
    extra = 1


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = [
        "property_name",
        "host",
        "city",
        "country",
        "base_price",
        "is_published",
        "created_at",
    ]
    list_filter = ["is_published", "is_active", "property_type", "country"]
    search_fields = ["property_name", "city", "country", "host__username"]
    inlines = [AccommodationPhotoInline]


class TourPhotoInline(admin.TabularInline):
    model = TourPhoto
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = [
        "tour_name",
        "host",
        "city",
        "country",
        "price_per_person",
        "is_published",
        "created_at",
    ]
    list_filter = ["is_published", "is_active", "tour_category", "country"]
    search_fields = ["tour_name", "city", "country", "host__username"]
    inlines = [TourPhotoInline]


@admin.register(AccommodationInventory)
class AccommodationInventoryAdmin(admin.ModelAdmin):
    list_display = [
        "accommodation",
        "date",
        "is_available",
        "base_price",
        "seasonal_multiplier",
        "is_blocked",
    ]
    list_filter = ["is_available", "is_blocked", "date", "accommodation__property_type"]
    search_fields = ["accommodation__property_name", "accommodation__host__username"]
    date_hierarchy = "date"
    list_editable = ["is_available", "base_price", "is_blocked"]


@admin.register(TourInventory)
class TourInventoryAdmin(admin.ModelAdmin):
    list_display = [
        "tour",
        "date",
        "time_slot",
        "is_available",
        "total_capacity",
        "available_spots",
        "price_per_person",
    ]
    list_filter = ["is_available", "is_blocked", "date", "tour__tour_category"]
    search_fields = ["tour__tour_name", "tour__host__username"]
    date_hierarchy = "date"
    list_editable = [
        "is_available",
        "total_capacity",
        "available_spots",
        "price_per_person",
    ]


@admin.register(SeasonalRate)
class SeasonalRateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "rate_type",
        "start_date",
        "end_date",
        "price_multiplier",
        "is_active",
    ]
    list_filter = ["rate_type", "is_active", "is_blackout"]
    search_fields = ["name"]
    date_hierarchy = "start_date"
    list_editable = ["price_multiplier", "is_active"]


@admin.register(RecurringRule)
class RecurringRuleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "rule_type",
        "start_date",
        "end_date",
        "is_available",
        "price_multiplier",
        "is_active",
    ]
    list_filter = ["rule_type", "is_available", "is_active"]
    search_fields = ["name"]
    list_editable = ["is_available", "price_multiplier", "is_active"]


# ============================================================================
# GENIUS REWARDS ADMIN
# ============================================================================

from .models import Booking, GeniusProfile, Reward, Redemption


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "booking_type",
        "item_name",
        "total_amount",
        "status",
        "points_awarded",
        "created_at",
    ]
    list_filter = ["status", "booking_type", "created_at"]
    search_fields = ["user__username", "user__email"]
    date_hierarchy = "created_at"
    readonly_fields = [
        "points_awarded",
        "points_awarded_at",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Booking Information",
            {"fields": ("user", "booking_type", "accommodation", "tour")},
        ),
        ("Dates", {"fields": ("check_in", "check_out", "booking_date")}),
        ("Financial", {"fields": ("total_amount", "status")}),
        (
            "Points",
            {
                "fields": ("points_awarded", "points_awarded_at"),
                "classes": ("collapse",),
            },
        ),
        (
            "Additional Info",
            {"fields": ("notes", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def item_name(self, obj):
        return obj.item_name

    item_name.short_description = "Booked Item"


@admin.register(GeniusProfile)
class GeniusProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "level",
        "level_name",
        "total_points",
        "lifetime_points",
        "reward_value_display",
        "discount_percentage",
        "total_bookings",
        "created_at",
    ]
    list_filter = ["level", "created_at"]
    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    ]
    readonly_fields = [
        "total_points",
        "lifetime_points",
        "total_spent",
        "total_bookings",
        "total_redeemed",
        "created_at",
        "updated_at",
        "level_updated_at",
        "reward_value_display",
        "discount_percentage",
        "points_multiplier",
        "points_to_next_level",
    ]

    fieldsets = (
        ("User", {"fields": ("user",)}),
        (
            "Level & Points",
            {
                "fields": (
                    "level",
                    "total_points",
                    "lifetime_points",
                    "reward_value_display",
                    "discount_percentage",
                    "points_multiplier",
                    "points_to_next_level",
                )
            },
        ),
        (
            "Statistics",
            {
                "fields": (
                    "total_spent",
                    "total_bookings",
                    "total_redeemed",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at", "level_updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def reward_value_display(self, obj):
        return f"${obj.reward_value():.2f}"

    reward_value_display.short_description = "Reward Value"

    def level_name(self, obj):
        return obj.level_name

    level_name.short_description = "Level Name"


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "reward_type",
        "cost_points",
        "value",
        "min_level",
        "is_active",
        "stock_remaining",
        "redeemed_count",
        "featured",
    ]
    list_filter = ["reward_type", "is_active", "featured", "min_level"]
    search_fields = ["name", "description"]
    list_editable = ["is_active", "featured", "cost_points"]
    readonly_fields = ["redeemed_count", "created_at", "updated_at"]

    fieldsets = (
        (
            "Reward Information",
            {"fields": ("name", "description", "reward_type", "image")},
        ),
        ("Points & Value", {"fields": ("cost_points", "value")}),
        (
            "Availability",
            {"fields": ("is_active", "stock_quantity", "redeemed_count", "min_level")},
        ),
        ("Display", {"fields": ("featured", "display_order")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    list_display = [
        "redemption_code",
        "user",
        "reward",
        "points_used",
        "status",
        "redeemed_at",
        "fulfilled_at",
    ]
    list_filter = ["status", "redeemed_at"]
    search_fields = ["user__username", "user__email", "redemption_code", "reward__name"]
    date_hierarchy = "redeemed_at"
    readonly_fields = ["redemption_code", "redeemed_at", "fulfilled_at"]

    fieldsets = (
        (
            "Redemption Information",
            {"fields": ("redemption_code", "user", "genius_profile", "reward")},
        ),
        ("Details", {"fields": ("points_used", "status")}),
        ("Tracking", {"fields": ("redeemed_at", "fulfilled_at", "notes")}),
    )

    actions = ["mark_as_fulfilled", "mark_as_approved"]

    def mark_as_fulfilled(self, request, queryset):
        for redemption in queryset:
            redemption.fulfill()
        self.message_user(
            request, f"{queryset.count()} redemptions marked as fulfilled."
        )

    mark_as_fulfilled.short_description = "Mark selected as fulfilled"

    def mark_as_approved(self, request, queryset):
        queryset.update(status="approved")
        self.message_user(
            request, f"{queryset.count()} redemptions marked as approved."
        )

    mark_as_approved.short_description = "Mark selected as approved"
