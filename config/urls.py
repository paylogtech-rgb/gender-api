from django.contrib import admin
from django.urls import path
from api.views import classify_name, create_profile, get_profile, get_all_profiles

urlpatterns = [
    path('admin/', admin.site.urls),

    # Stage 0
    path('api/classify', classify_name),

    # Stage 1
    path('api/profiles', create_profile),        # POST
    path('api/profiles/', get_all_profiles),     # GET ALL
    path('api/profiles/<uuid:id>', get_profile), # GET + DELETE
]