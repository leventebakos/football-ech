from django.contrib import admin

from .models import League, LeagueParticipants

admin.site.register(League)
admin.site.register(LeagueParticipants)