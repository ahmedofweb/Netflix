from django.contrib import admin
from .models import *

@admin.register(Aktyor)
class AktyorAdmin(admin.ModelAdmin):
    list_display = ['ism', 'davlat', 'jins']

@admin.register(Kino)
class KinoAdmin(admin.ModelAdmin):
    list_display = ['nom']

@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    list_display = ['nom']