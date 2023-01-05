from django.contrib import admin

from service.models import Service, Plan, Subscription

# Register your models here.
admin.site.register((Service, Plan, Subscription))
