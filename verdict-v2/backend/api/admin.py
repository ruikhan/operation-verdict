from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Player, VictimFile, FileReview, GameProgress


@admin.register(Player)
class PlayerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Game Profile', {
            'fields': ('age', 'sex', 'phone_number', 'terms_accepted', 'terms_accepted_at', 'cinematic_viewed'),
        }),
    )
    list_display  = ['username', 'email', 'first_name', 'last_name', 'terms_accepted', 'cinematic_viewed']
    list_filter   = ['terms_accepted', 'cinematic_viewed', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(VictimFile)
class VictimFileAdmin(admin.ModelAdmin):
    list_display  = ['file_id', 'code_name', 'victim_age', 'incident_year', 'location', 'status', 'evidence_strength']
    list_filter   = ['status']
    search_fields = ['file_id', 'code_name', 'location']


@admin.register(FileReview)
class FileReviewAdmin(admin.ModelAdmin):
    list_display  = ['player', 'victim_file', 'reviewed_at']
    list_filter   = ['reviewed_at']
    search_fields = ['player__username', 'victim_file__file_id']


@admin.register(GameProgress)
class GameProgressAdmin(admin.ModelAdmin):
    list_display = ['player', 'files_reviewed', 'conviction_strength', 'verdict_reached', 'last_active']
    list_filter  = ['verdict_reached']
