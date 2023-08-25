from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TimeSlots)
admin.site.register(Appointments)
admin.site.register(MeetLink)