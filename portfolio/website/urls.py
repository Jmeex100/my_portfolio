# website/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('api/cooldown-status/', views.cooldown_status, name='cooldown_status'),
       # View CV inline (no auto-download)
    path('view-cv/', views.view_cv, name='view_cv'),

    # Download CV when user clicks
    path('download-cv/', views.download_cv, name='download_cv'),
]