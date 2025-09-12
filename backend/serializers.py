from os import read
from rest_framework import serializers
from .models import ServiceEvent
from profiles.models import EventParticipation, ServiceProfile
from users.models import CustomUser
import json
from rest_framework.response import Response
from utils.create_event_nfc import create_event_nfc


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEvent
        fields = [
            "name",
            "description",
            "timeStart",
            "timeEnd",
            "creator",
        ]
        read_only_fields = ["creator"]

    def create(self, validated_data):
        request = self.context.get("request")
        # created_event = create_event_nfc(
        #     name=validated_data["name"],
        #     time_start=validated_data["timeStart"].isoformat(),
        #     time_end=validated_data["timeEnd"].isoformat(),
        # )
        # if "error" in created_event:
        #     raise serializers.ValidationError(created_event["error"])
        # else:
        ServiceEvent.objects.create(
            name=validated_data["name"],
            description=validated_data["description"],
            timeStart=validated_data["timeStart"],
            timeEnd=validated_data["timeEnd"],
            creator=request.user,
            nfc_id=1,
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
