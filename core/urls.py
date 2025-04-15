from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('lineup/', views.lineup, name='lineup'),
    path('tickets/', views.tickets, name='tickets'),
    path('info/', views.info, name='info'),
    path('performers/<slug:slug>/', views.performer_detail, name='performer_detail'),
    path('performers/', views.all_performers, name='all_performers'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('events/', views.all_events, name='all_events'),
    path('api/get_event_performers/', views.get_event_performers, name='get_event_performers'),
] 