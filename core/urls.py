from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('lineup/', views.lineup, name='lineup'),
    path('tickets/', views.tickets, name='tickets'),
    path('info/', views.info, name='info'),
] 