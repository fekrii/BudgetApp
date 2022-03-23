from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("grappelli/", include('grappelli.urls')),
    path("", include('budget.urls')),
    path('admin/', admin.site.urls),
]
