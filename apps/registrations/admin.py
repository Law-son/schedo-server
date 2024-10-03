from django.contrib import admin
from apps.registrations.models import Ticket, Attendee

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Attendee)
