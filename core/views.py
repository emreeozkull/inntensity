from django.shortcuts import render, get_object_or_404
from .models import Event, Performer, Stage, Performance, TicketType, InfoSection, FAQ
from datetime import datetime, timedelta
from django.http import JsonResponse

# Create your views here.

def home(request):
    #featured_event = Event.objects.filter(featured=True).first()
    featured_events = Event.objects.filter().all()
    featured_event = featured_events.filter(featured=True).first()
    featured_performers = Performer.objects.filter(featured=True)[:6]
    return render(request, 'core/home.html', {
        'featured_event': featured_event,
        'featured_performers': featured_performers,
        'featured_events': featured_events,
    })

def lineup(request):
    event = Event.objects.filter(featured=True).first()
    if not event:
        print("No event found for lineup")
        return render(request, 'core/lineup.html', {'error': 'No event found'})
    print("Event found for lineup", event.title)
    performances = Performance.objects.filter(event=event).order_by('date', 'start_time')
    print("Performances found for event", event.title, performances)
    
    # Get unique dates from performances
    unique_dates = Performance.objects.filter(event=event).values_list('date', flat=True).distinct().order_by('date')
    
    # Organize performances by date
    performances_by_date = {}
    # Track stages that have performances for each date
    stages_by_date = {}
    
    for date in unique_dates:
        date_performances = Performance.objects.filter(event=event, date=date)
        performances_by_date[date] = date_performances
        
        # Get only stages that have performances on this date
        active_stage_ids = date_performances.values_list('stage', flat=True).distinct()
        stages_by_date[date] = Stage.objects.filter(id__in=active_stage_ids)
    
    return render(request, 'core/lineup.html', {
        'event': event,
        'unique_dates': unique_dates,
        'performances_by_date': performances_by_date,
        'stages_by_date': stages_by_date,
    })

def tickets(request):
    ticket_types = TicketType.objects.filter(available=True)
    return render(request, 'core/tickets.html', {
        'ticket_types': ticket_types,
    })

def info(request):
    info_sections = InfoSection.objects.all()
    faqs = FAQ.objects.all()
    return render(request, 'core/info.html', {
        'info_sections': info_sections,
        'faqs': faqs,
    })

def performer_detail(request, slug):
    performer = get_object_or_404(Performer, slug=slug)
    events = performer.events.all()
    print("Events found", events)
    
    context = {
        'performer': performer,
        'events': events,
    }
    return render(request, 'core/performer_detail.html', context)

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    performances = Performance.objects.filter(event=event).order_by('date', 'start_time')
    performers = event.performers.all().distinct()
    
    # Get unique dates from performances
    unique_dates = Performance.objects.filter(event=event).values_list('date', flat=True).distinct().order_by('date')
    
    # Organize performances by date
    performances_by_date = {}
    # Track stages that have performances for each date
    stages_by_date = {}
    
    for date in unique_dates:
        date_performances = Performance.objects.filter(event=event, date=date)
        performances_by_date[date] = date_performances
        
        # Get only stages that have performances on this date
        active_stage_ids = date_performances.values_list('stage', flat=True).distinct()
        stages_by_date[date] = Stage.objects.filter(id__in=active_stage_ids)
    
    context = {
        'event': event,
        'performances': performances,
        'unique_dates': unique_dates,
        'performances_by_date': performances_by_date,
        'stages_by_date': stages_by_date,
        'performers': performers,
    }
    return render(request, 'core/event_detail.html', context)

def all_events(request):
    events = Event.objects.all().order_by('date')
    
    context = {
        'events': events,
    }
    return render(request, 'core/all_events.html', context)

def get_event_performers(request):
    """View function to get performers for a specific event, used by admin JavaScript."""
    event_id = request.GET.get('event_id')
    print(f"get_event_performers view called with event_id={event_id}")
    
    # Force no caching for this API endpoint
    response_headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
    
    if not event_id:
        print("No event_id provided in request")
        return JsonResponse([], safe=False, headers=response_headers)
    
    try:
        event = Event.objects.get(pk=event_id)
        print(f"Found event: {event.title}")
        
        performers = event.performers.all().order_by('name')
        performer_count = performers.count()
        print(f"Event has {performer_count} performers")
        
        data = [{'id': p.id, 'name': p.name} for p in performers]
        print(f"Returning {len(data)} performers: {', '.join([p['name'] for p in data])}")
        
        return JsonResponse(data, safe=False, headers=response_headers)
    except Event.DoesNotExist:
        print(f"Event with id={event_id} does not exist")
        return JsonResponse([], safe=False, headers=response_headers)
    except Exception as e:
        print(f"Error in get_event_performers: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500, headers=response_headers)

def all_performers(request):
    performers = Performer.objects.all().order_by('name')
    context = {
        'performers': performers,
    }
    return render(request, 'core/all_performers.html', context)
