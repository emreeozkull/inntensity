from django.shortcuts import render, get_object_or_404
from .models import Event, Artist, Stage, Performance, TicketType, InfoSection, FAQ

# Create your views here.

def home(request):
    featured_event = Event.objects.filter(featured=True).first()
    featured_artists = Artist.objects.filter(featured=True)[:3]
    return render(request, 'core/home.html', {
        'featured_event': featured_event,
        'featured_artists': featured_artists,
    })

def lineup(request):
    event = Event.objects.filter(featured=True).first()
    if not event:
        return render(request, 'core/lineup.html', {'error': 'No event found'})
    
    stages = Stage.objects.all()
    performances = Performance.objects.filter(event=event).select_related('artist', 'stage')
    
    # Organize performances by day
    days = {1: [], 2: [], 3: []}  # Friday, Saturday, Sunday
    for performance in performances:
        days[performance.day].append(performance)
    
    return render(request, 'core/lineup.html', {
        'event': event,
        'stages': stages,
        'friday_performances': days[1],
        'saturday_performances': days[2],
        'sunday_performances': days[3],
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
