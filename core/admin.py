from django.contrib import admin
from django import forms
from django.urls import path
from .models import Event, Performer, Stage, Performance, TicketType, InfoSection, FAQ
from django.http import JsonResponse

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'featured', 'created_at')
    list_filter = ('featured', 'date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
    filter_horizontal = ('performers',)

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

class PerformanceAdminForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        print(f"PerformanceAdminForm.__init__ called, is_bound={self.is_bound}")
        
        # If we're editing an existing performance, filter by its event
        if self.instance.pk and self.instance.event:
            print(f"Editing existing performance with event {self.instance.event.title}")
            self.fields['performer'].queryset = self.instance.event.performers.all()
        else:
            # Handle form validation errors - if the form was submitted and has errors,
            # we want to keep the performer selection intact
            if self.is_bound and self.errors and 'event' in self.data and 'performer' in self.data:
                print("Form has errors, trying to preserve performer dropdown")
                try:
                    event_id = int(self.data.get('event'))
                    performer_id = int(self.data.get('performer'))
                    event = Event.objects.get(pk=event_id)
                    performer = Performer.objects.get(pk=performer_id)
                    self.fields['performer'].queryset = event.performers.all()
                    print(f"Preserved performer dropdown with {self.fields['performer'].queryset.count()} performers")
                except (ValueError, Event.DoesNotExist, Performer.DoesNotExist) as e:
                    print(f"Error preserving performer dropdown: {str(e)}")
                    self.fields['performer'].queryset = Performer.objects.none()
            else:
                # Handle the case of initial form render (no event selected yet)
                print("New performance, no event selected yet")
                self.fields['performer'].queryset = Performer.objects.none()
                
                # If the form is bound (submitted) and has event data
                if self.is_bound and 'event' in self.data:
                    try:
                        event_id = int(self.data.get('event'))
                        event = Event.objects.get(pk=event_id)
                        self.fields['performer'].queryset = event.performers.all()
                        print(f"Selected event {event.title} has {self.fields['performer'].queryset.count()} performers")
                    except (ValueError, Event.DoesNotExist) as e:
                        print(f"Error setting performers for event: {str(e)}")
    
    def clean(self):
        cleaned_data = super().clean()
        event = cleaned_data.get('event')
        performer = cleaned_data.get('performer')
        
        if event and performer:
            if performer not in event.performers.all():
                print(f"Validation error: Performer {performer} not in event {event}")
                raise forms.ValidationError({
                    'performer': 'This performer is not associated with the selected event. '
                                'Please choose a performer that belongs to this event.'
                })
            else:
                print(f"Validation passed: Performer {performer} is in event {event}")
            
        return cleaned_data

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    form = PerformanceAdminForm
    list_display = ('performer', 'stage', 'event', 'date', 'start_time', 'end_time')
    list_filter = ('date', 'event', 'stage')
    search_fields = ('performer__name', 'stage__name')
    autocomplete_fields = ['stage', 'event']
    date_hierarchy = 'date'
    
    class Media:
        js = ('js/admin/direct_select.js',)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get_event_performers/', self.admin_site.admin_view(self.get_event_performers), name='get_event_performers'),
        ]
        return custom_urls + urls
    
    def get_event_performers(self, request):
        event_id = request.GET.get('event_id')
        print(f"get_event_performers called with event_id={event_id}")
        
        if not event_id:
            print("No event_id provided in request")
            return JsonResponse([], safe=False)
        
        try:
            event = Event.objects.get(pk=event_id)
            print(f"Found event: {event.title}")
            
            performers = event.performers.all()
            print(f"Event has {performers.count()} performers")
            
            data = [{'id': p.id, 'name': p.name} for p in performers]
            print(f"Returning data: {data}")
            
            return JsonResponse(data, safe=False)
        except Event.DoesNotExist:
            print(f"Event with id={event_id} does not exist")
            return JsonResponse([], safe=False)
        except Exception as e:
            print(f"Error in get_event_performers: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    def add_view(self, request, form_url='', extra_context=None):
        """Add an inline script to handle event changes on the add form"""
        extra_context = extra_context or {}
        extra_context['inline_performer_script'] = True
        return super().add_view(request, form_url, extra_context)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add an inline script to handle event changes on the change form"""
        extra_context = extra_context or {}
        extra_context['inline_performer_script'] = True
        return super().change_view(request, object_id, form_url, extra_context)

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
