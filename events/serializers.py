from rest_framework import serializers
from .models import ServiceEvent
from profiles.models import EventActivity
from utils.create_event_nfc import create_event_nfc


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEvent
        fields = [
            "id",
            "name",
            "description",
            "time_start",
            "time_end",
            "is_active",
        ]

    def create(self, validated_data):
        if validated_data["time_start"] >= validated_data["time_end"]:
            raise serializers.ValidationError(
                "Event end time must be after event start time."
            )
        created_event = create_event_nfc(
            name=validated_data["name"],
            time_start=validated_data["time_start"].isoformat(),
            time_end=validated_data["time_end"].isoformat(),
        )
        if "error" in created_event:
            raise serializers.ValidationError(created_event["error"])
        else:
            service_event = ServiceEvent.objects.create(
                name=validated_data["name"],
                description=validated_data["description"],
                time_start=validated_data["time_start"],
                time_end=validated_data["time_end"],
                nfc_id=created_event["id"],
            )
        return service_event
