from django.contrib import admin
from django.urls import path
from api.views import (
    classify_name,
    create_profile,
    get_all_profiles,
    get_profile,
    delete_profile
)

# ✅ handle both GET and POST in one route
def profiles_entry(request):
    if request.method == "POST":
        return create_profile(request)
    elif request.method == "GET":
        return get_all_profiles(request)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Stage 0
    path('api/classify', classify_name),

    # ✅ FIXED (NO TRAILING SLASH PROBLEM)
    path('api/profiles', profiles_entry),

    # Single profile
    path('api/profiles/<uuid:id>', get_profile),

    # Delete
    path('api/profiles/<uuid:id>', delete_profile),
]