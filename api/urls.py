from django.urls import path
from .views import get_profiles, search_profiles
urlpatterns = [
    path('profiles', get_profiles),
    path('profiles/search', search_profiles),
]