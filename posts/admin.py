from . import models
from django.contrib import admin

admin.site.register(models.Post)
admin.site.register(models.Like)
admin.site.register(models.Comment)
admin.site.register(models.Category)
admin.site.register(models.PostView)
admin.site.register(models.Category_Of_Post)
