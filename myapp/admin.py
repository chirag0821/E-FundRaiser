from django.contrib import admin
from .models import Uploads, Startups, Investments, Founders, UseUsers

admin.site.register(Uploads)
admin.site.register(Startups)
admin.site.register(Investments)
admin.site.register(Founders)
admin.site.register(UseUsers)
