from django.contrib import admin
from .models import Event, Guest,Attendance,Feedback,EventFeedbaackQr

# Register your models here.
admin.site.register(Event)
admin.site.register(Guest)
admin.site.register(Attendance)
admin.site.register(Feedback)
admin.site.register(EventFeedbaackQr)