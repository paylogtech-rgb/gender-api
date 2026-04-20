from django.contrib import admin
from django.urls import path
from api.views import (
    classify_name,
    create_profile,
    get_all_profiles,
    get_profile,
    delete_profile
)

def profiles_entry(request):
    if request.method == "POST":
        return create_profile(request)
    elif request.method == "GET":
        return get_all_profiles(request)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/classify', classify_name),

    # ✅ NO SLASH VERSION
    path('api/profiles', profiles_entry),

    path('api/profiles/<uuid:id>', get_profile),
    path('api/profiles/<uuid:id>', delete_profile),
]