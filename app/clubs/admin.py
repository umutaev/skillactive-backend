from django.contrib import admin
from clubs.models import (
    ClubModel,
    PriceObject,
    TutorObject,
    CommunicationObject,
    TimetableObject,
)


class ClubAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'description', 'public']


admin.site.register(ClubModel, ClubAdmin)
admin.site.register(PriceObject)
admin.site.register(TutorObject)
admin.site.register(CommunicationObject)
admin.site.register(TimetableObject)
