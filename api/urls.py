from django.urls import path
from .views import (
    classify_name,
    create_profile,
    get_profile,
    delete_profile,
    get_profiles,
    search_profiles
)

urlpatterns = [
    path('classify', classify_name),

    # CRUD
    path('profiles', get_profiles),        # GET (with filter, sort, pagination)
    path('profiles/create', create_profile),  # POST
    path('profiles/<uuid:id>', get_profile),  # GET single
    path('profiles/<uuid:id>/delete', delete_profile),  # DELETE

    # Search
    path('profiles/search', search_profiles),
]