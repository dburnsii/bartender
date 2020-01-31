from django.contrib import admin
from django.db import models


class Settings(models.Model):
    oz_interval = models.IntegerField(default=1000)
    name = models.CharField(max_length=32, default="Bartender")
    color = models.CharField(max_length=32, default="#b87333")


class SettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not Settings.objects.exists()
