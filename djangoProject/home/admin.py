from django.contrib import admin

# Register your models here.
from home.models import Person, Car

admin.site.register(Person)
admin.site.register(Car)