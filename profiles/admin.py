from django.contrib import admin
from .models import (
    ServiceProfile,
    LeadershipProfile,
    PersonalProfile,
    ServiceActivity,
    LeadershipActivity,
    EventActivity,
    GPARecord,
)

admin.site.register(ServiceProfile)
admin.site.register(LeadershipProfile)
admin.site.register(PersonalProfile)
admin.site.register(ServiceActivity)
admin.site.register(LeadershipActivity)
admin.site.register(EventActivity)
admin.site.register(GPARecord)
