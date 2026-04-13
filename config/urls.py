from django.contrib import admin
from django.urls import path
from api.views import classify_name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/classify', classify_name),
]