from os import read
from rest_framework import serializers
from .models import ServiceEvent
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
        created = create_event_nfc(
            name=validated_data["name"],
            time_start=validated_data["timeStart"].isoformat(),
            time_end=validated_data["timeEnd"].isoformat(),
            description=validated_data["description"],
        )
        if "error" in created:
            raise serializers.ValidationError(created["error"])
        else:
            event = ServiceEvent.objects.create(
                name=validated_data["name"],
                description=validated_data["description"],
                timeStart=validated_data["timeStart"],
                timeEnd=validated_data["timeEnd"],
                creator=request.user,
            )
        return event
