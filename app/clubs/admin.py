from django.contrib import admin
from clubs.models import (
    ClubModel,
    PriceObject,
    TutorObject,
    CommunicationObject,
    TimetableObject,
)

admin.site.register(ClubModel)
admin.site.register(PriceObject)
admin.site.register(TutorObject)
admin.site.register(CommunicationObject)
admin.site.register(TimetableObject)
