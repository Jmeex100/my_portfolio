from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    path('api/cooldown-status/', views.cooldown_status, name='cooldown_status'),

    path('document/view/<int:doc_id>/', views.view_document, name='view_document'),
    path('document/download/<int:doc_id>/', views.download_document, name='download_document'),
]
