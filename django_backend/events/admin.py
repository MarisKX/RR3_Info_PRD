from django.contrib import admin
from .models import (
    EventGroup,
    EventSubGroup,
    EventSubGroupRewards,
    Event,
    EventType,
    Track,
    TrackConfiguaration,
    )


class TrackConfiguarationAdmin(admin.TabularInline):
    readonly_fields = ('name', )
    model = TrackConfiguaration
    list_display = (
        'track',
        'display_name',
        'remarks',
    )
    ordering = ('display_name', )


class TrackAdmin(admin.ModelAdmin):
    readonly_fields = ('name', )
    inlines = (TrackConfiguarationAdmin, )
    list_display = (
        'display_name',
        'location',
    )
    ordering = ('display_name', )


class EventTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('name', )
    list_display = (
        'display_name',
        'name',
    )


class EventGroupAdmin(admin.ModelAdmin):
    readonly_fields = ('name', )
    list_display = (
        'display_name',
        'name',
        'section',
        'sequence',
        'available_from_lvl',
    )


class EventSubGroupRewardsAdmin(admin.TabularInline):
    model = EventSubGroupRewards


class EventSubGroupAdmin(admin.ModelAdmin):
    ordering = ['page', '-main_event', ]
    inlines = (EventSubGroupRewardsAdmin, )
    readonly_fields = ('name', )
    list_display = (
        'display_name',
        'name',
        'page',
        'main_event',
        'finished',
    )


class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('name', )
    ordering = ['page', 'page_sequence', ]
    list_display = (
        'event_sub_group',
        'display_name',
        'track_and_config',
        'event_type',
        'laps',
        'page',
        'page_sequence',
        'reward',
        'reward_currency',
        'clean_race_bonus',
        'clean_race_bonus_currency',
        'reward_fame',
        'reward_in_one_minute_spent',
        'fame_in_one_minute_spent',
    )


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(EventGroup, EventGroupAdmin)
admin.site.register(EventSubGroup, EventSubGroupAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Track, TrackAdmin)