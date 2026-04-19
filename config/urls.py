from django.contrib import admin
from django.urls import path
from api.views import (
    create_profile,
    get_all_profiles,
    get_profile,
    delete_profile,
    classify_name
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/classify', classify_name),

    # ✅ POST
    path('api/profiles', create_profile),

    # ✅ GET ALL (IMPORTANT: trailing slash)
    path('api/profiles/', get_all_profiles),

    # ✅ GET SINGLE + DELETE (SAME ENDPOINT)
    path('api/profiles/<uuid:id>', get_profile),
    path('api/profiles/<uuid:id>', delete_profile),
]