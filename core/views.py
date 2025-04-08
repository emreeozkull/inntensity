from django.shortcuts import render, get_object_or_404
from .models import Event, Artist, Stage, Performance, TicketType, InfoSection, FAQ
from django.db.models import Q
from datetime import datetime
from collections import defaultdict

# Create your views here.

def home(request):
    featured_event = Event.objects.filter(featured=True).first()
    featured_artists = Artist.objects.filter(featured=True)[:6]
    return render(request, 'core/home.html', {
        'featured_event': featured_event,
        'featured_artists': featured_artists,
    })

def lineup(request):
    # Get all events ordered by date
    events = Event.objects.all().order_by('date')
    
    # Get all stages
    stages = Stage.objects.all()
    
    # Get all performances
    performances = Performance.objects.all().order_by('start_time')
    
    context = {
        'events': events,
        'stages': stages,
        'performances': performances,
    }
    return render(request, 'core/lineup.html', context)

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

def artist_detail(request, slug):
    artist = get_object_or_404(Artist, slug=slug)
    events = artist.events.all()
    
    context = {
        'artist': artist,
        'events': events,
    }
    return render(request, 'core/artist_detail.html', context)

def all_events(request):
    events = Event.objects.all().order_by('date')
    
    context = {
        'events': events,
    }
    return render(request, 'core/all_events.html', context)
