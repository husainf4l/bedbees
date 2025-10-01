from rest_framework import serializers
from .models import (
    Listing, RoomType, AvailabilityDay, DayRoomInventory
)


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'base_price', 'total_units']


class DayRoomInventorySerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room_type.name', read_only=True)
    base_price = serializers.DecimalField(source='room_type.base_price', max_digits=10, decimal_places=2, read_only=True)
    total_units = serializers.IntegerField(source='room_type.total_units', read_only=True)
    available = serializers.SerializerMethodField()
    
    class Meta:
        model = DayRoomInventory
        fields = [
            'room_type_id', 'room_name', 'base_price', 'total_units',
            'units_open', 'units_booked', 'available', 'stop_sell',
            'cta', 'ctd', 'override_price', 'note'
        ]
        read_only_fields = ['units_booked']
    
    def get_available(self, obj):
        return obj.available


class AvailabilityDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityDay
        fields = ['date', 'status', 'price', 'min_stay', 'notes']


class CalendarDaySerializer(serializers.Serializer):
    """Serializer for calendar day data"""
    date = serializers.DateField()
    status = serializers.CharField()
    effective_status = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    min_stay = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    summary = serializers.DictField()
    rooms = DayRoomInventorySerializer(many=True)


class BulkCalendarUpdateSerializer(serializers.Serializer):
    """Serializer for bulk calendar updates"""
    listing = serializers.IntegerField()
    date_range = serializers.DictField()
    weekday_filter = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=6),
        required=False,
        allow_empty=True
    )
    updates = serializers.DictField()
    
    def validate_date_range(self, value):
        if 'from' not in value or 'to' not in value:
            raise serializers.ValidationError("date_range must contain 'from' and 'to' dates")
        return value


class DayUpdateSerializer(serializers.Serializer):
    """Serializer for single day updates"""
    listing = serializers.IntegerField()
    date = serializers.DateField()
    status = serializers.ChoiceField(
        choices=['OPEN', 'CLOSED', 'BLOCKED'],
        required=False
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2,
        required=False, allow_null=True
    )
    min_stay = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class DayRoomUpdateSerializer(serializers.Serializer):
    """Serializer for day room inventory updates"""
    listing = serializers.IntegerField()
    date = serializers.DateField()
    rooms = serializers.ListField(child=serializers.DictField())
