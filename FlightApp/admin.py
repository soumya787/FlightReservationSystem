from django.contrib import admin

from FlightApp.models import Flight, DestinationCity, ArrivalCity

# Register your models here.
admin.site.register(Flight)
admin.site.register(DestinationCity)
admin.site.register(ArrivalCity)