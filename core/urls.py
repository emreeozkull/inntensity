from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('lineup/', views.lineup, name='lineup'),
    path('tickets/', views.tickets, name='tickets'),
    path('info/', views.info, name='info'),
    path('performer/<slug:slug>/', views.performer_detail, name='performer_detail'),
    path('events/', views.all_events, name='all_events'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
] 