from django.contrib import admin 
from django.urls import path, include


urlpatterns = [
    path('',include('Organizer.urls') ),
    path('admin/', admin.site.urls),
    path('Organizer/', include('Organizer.urls')),  
]
