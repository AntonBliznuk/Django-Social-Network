from django.contrib import admin
from . import models

admin.site.register(models.CustomUser)
admin.site.register(models.Subscribe)
