from django.contrib import admin
from clubs.models import ClubModel, PriceObject, TutorObject, CommunicationObject

admin.site.register(ClubModel)
admin.site.register(PriceObject)
admin.site.register(TutorObject)
admin.site.register(CommunicationObject)
