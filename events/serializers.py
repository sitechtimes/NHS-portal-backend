from os import read
from rest_framework import serializers
from .models import ServiceEvent
from profiles.models import EventActivity, ServiceProfile
from users.models import CustomUser
import json
import os
from rest_framework.response import Response
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
            "creator",
        ]
        read_only_fields = ["creator"]

    def create(self, validated_data):
        request = self.context.get("request")
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
                creator=request.user,
                nfc_id=created_event["id"],
            )
        return service_event


class EventActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventActivity
        fields = [
            "id",
            "event",
            "service_profile",
        ]
        read_only_fields = ["user"]
