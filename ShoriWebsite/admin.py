from django.contrib import admin
from .models import Team, Match


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo_name', 'color')
    search_fields = ('name',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'datetime', 'location')
    list_filter = ('datetime',)
    autocomplete_fields = ('home_team', 'away_team')
