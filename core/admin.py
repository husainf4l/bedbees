from django.contrib import admin
from .models import (
    UserProfile, Accommodation, AccommodationPhoto, Tour, TourPhoto,
    AccommodationInventory, TourInventory, SeasonalRate, RecurringRule
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_host', 'email_verified', 'phone_verified', 'created_at']
    list_filter = ['is_host', 'email_verified', 'phone_verified']
    search_fields = ['user__username', 'user__email', 'business_name']


class AccommodationPhotoInline(admin.TabularInline):
    model = AccommodationPhoto
    extra = 1


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['property_name', 'host', 'city', 'country', 'base_price', 'is_published', 'created_at']
    list_filter = ['is_published', 'is_active', 'property_type', 'country']
    search_fields = ['property_name', 'city', 'country', 'host__username']
    inlines = [AccommodationPhotoInline]


class TourPhotoInline(admin.TabularInline):
    model = TourPhoto
    extra = 1


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['tour_name', 'host', 'city', 'country', 'price_per_person', 'is_published', 'created_at']
    list_filter = ['is_published', 'is_active', 'tour_category', 'country']
    search_fields = ['tour_name', 'city', 'country', 'host__username']
    inlines = [TourPhotoInline]


@admin.register(AccommodationInventory)
class AccommodationInventoryAdmin(admin.ModelAdmin):
    list_display = ['accommodation', 'date', 'is_available', 'base_price', 'seasonal_multiplier', 'is_blocked']
    list_filter = ['is_available', 'is_blocked', 'date', 'accommodation__property_type']
    search_fields = ['accommodation__property_name', 'accommodation__host__username']
    date_hierarchy = 'date'
    list_editable = ['is_available', 'base_price', 'is_blocked']


@admin.register(TourInventory) 
class TourInventoryAdmin(admin.ModelAdmin):
    list_display = ['tour', 'date', 'time_slot', 'is_available', 'total_capacity', 'available_spots', 'price_per_person']
    list_filter = ['is_available', 'is_blocked', 'date', 'tour__tour_category']
    search_fields = ['tour__tour_name', 'tour__host__username']
    date_hierarchy = 'date'
    list_editable = ['is_available', 'total_capacity', 'available_spots', 'price_per_person']


@admin.register(SeasonalRate)
class SeasonalRateAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate_type', 'start_date', 'end_date', 'price_multiplier', 'is_active']
    list_filter = ['rate_type', 'is_active', 'is_blackout']
    search_fields = ['name']
    date_hierarchy = 'start_date'
    list_editable = ['price_multiplier', 'is_active']


@admin.register(RecurringRule)
class RecurringRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'rule_type', 'start_date', 'end_date', 'is_available', 'price_multiplier', 'is_active']
    list_filter = ['rule_type', 'is_available', 'is_active']
    search_fields = ['name']
    list_editable = ['is_available', 'price_multiplier', 'is_active']
