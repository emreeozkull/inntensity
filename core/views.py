from django.shortcuts import render, get_object_or_404
from .models import Event, Performer, Stage, Performance, TicketType, InfoSection, FAQ
from datetime import datetime, timedelta

# Create your views here.

def home(request):
    featured_event = Event.objects.filter(featured=True).first()
    featured_artists = Performer.objects.filter(featured=True)[:6]
    return render(request, 'core/home.html', {
        'featured_event': featured_event,
        'featured_artists': featured_artists,
    })

def lineup(request):
    event = Event.objects.filter(featured=True).first()
    if not event:
        print("No event found for lineup")
        return render(request, 'core/lineup.html', {'error': 'No event found'})
    print("Event found for lineup", event.title)
    stages = Stage.objects.all()
    print("Stages found", stages)
    performances = Performance.objects.filter(event=event).order_by('date', 'start_time')
    print("Performances found for event", event.title, performances)
    
    # Get unique dates from performances
    unique_dates = Performance.objects.filter(event=event).values_list('date', flat=True).distinct().order_by('date')
    
    # Organize performances by date
    performances_by_date = {}
    for date in unique_dates:
        performances_by_date[date] = Performance.objects.filter(event=event, date=date)
    
    return render(request, 'core/lineup.html', {
        'event': event,
        'stages': stages,
        'unique_dates': unique_dates,
        'performances_by_date': performances_by_date,
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
    
    context = {
        'performer': performer,
        'events': events,
    }
    return render(request, 'core/performer_detail.html', context)

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    stages = Stage.objects.all()
    performances = Performance.objects.filter(event=event).order_by('date', 'start_time')
    
    # Get unique dates from performances
    unique_dates = Performance.objects.filter(event=event).values_list('date', flat=True).distinct().order_by('date')
    
    # Organize performances by date
    performances_by_date = {}
    for date in unique_dates:
        performances_by_date[date] = Performance.objects.filter(event=event, date=date)
    
    context = {
        'event': event,
        'stages': stages,
        'performances': performances,
        'unique_dates': unique_dates,
        'performances_by_date': performances_by_date,
    }
    return render(request, 'core/event_detail.html', context)

def all_events(request):
    events = Event.objects.all().order_by('date')
    
    context = {
        'events': events,
    }
    return render(request, 'core/all_events.html', context)
