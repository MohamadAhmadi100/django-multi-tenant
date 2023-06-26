from django.contrib import admin

from .models import Organization, MainUser

admin.site.register(Organization)
admin.site.register(MainUser)
