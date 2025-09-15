from os import read
from rest_framework import serializers
from .models import ServiceEvent
from profiles.models import EventParticipation, ServiceProfile
from users.models import CustomUser
import json
import os
from rest_framework.response import Response
from utils.create_event_nfc import create_event_nfc


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEvent
        fields = [
            "name",
            "description",
            "time_start",
            "time_end",
            "creator",
        ]
        read_only_fields = ["creator"]

    def create(self, validated_data):
        if validated_data["api_key"] != os.getenv("NFC_BACKEND_API_KEY"):
            raise serializers.ValidationError("Invalid API key")
        request = self.context.get("request")
        created_event = create_event_nfc(
            name=validated_data["name"],
            time_start=validated_data["time_start"].isoformat(),
            time_end=validated_data["time_end"].isoformat(),
        )
        if "error" in created_event:
            raise serializers.ValidationError(created_event["error"])
        else:
            ServiceEvent.objects.create(
                name=validated_data["name"],
                description=validated_data["description"],
                time_start=validated_data["time_start"],
                time_end=validated_data["time_end"],
                creator=request.user,
                nfc_id=created_event["id"],
            )
        return validated_data
        # return event


class EventParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipation
        fields = [
            "event",
            "service_profile",
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):
        service_profile = ServiceProfile.objects.get(user=validated_data["user"])
        participation = EventParticipation.objects.create(
            event=validated_data["event"],
            service_profile=service_profile,
        )
        return participation
