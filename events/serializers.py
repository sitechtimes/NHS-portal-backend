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
            "name",
            "description",
            "time_start",
            "time_end",
            "creator",
        ]
        read_only_fields = ["creator"]

    def create(self, validated_data):
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


class EventActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventActivity
        fields = [
            "event",
            "service_profile",
        ]
        read_only_fields = ["user"]

    def create(self, validated_data):
        service_profile = ServiceProfile.objects.get(user=validated_data["user"])
        event_activity = EventActivity.objects.create(
            event=validated_data["event"],
            service_profile=service_profile,
        )
        return event_activity
