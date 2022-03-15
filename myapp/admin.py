from django.contrib import admin

# Register your models here.
from .models import Uploads, Startups
admin.site.register(Uploads)
admin.site.register(Startups)