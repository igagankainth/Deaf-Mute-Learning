# api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('translate/', views.translate_text, name='translate_text'),
    path('voice_to_text/', views.voice_to_text, name='voice_to_text'),
]


