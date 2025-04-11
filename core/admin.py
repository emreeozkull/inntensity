from django.contrib import admin
from .models import Event, Performer, Stage, Performance, TicketType, InfoSection, FAQ

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'featured', 'created_at')
    list_filter = ('featured', 'date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'

@admin.register(Performer)
class PerformerAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured', 'created_at')
    list_filter = ('featured',)
    search_fields = ('name', 'bio')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('performer', 'stage', 'event', 'date', 'start_time', 'end_time')
    list_filter = ('date', 'event', 'stage')
    search_fields = ('performer__name', 'stage__name')
    autocomplete_fields = ['performer', 'stage', 'event']
    date_hierarchy = 'date'

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'featured')
    list_filter = ('available', 'featured')
    search_fields = ('name', 'description')

@admin.register(InfoSection)
class InfoSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_filter = ('order',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'created_at')
    list_filter = ('order',)
    search_fields = ('question', 'answer')
