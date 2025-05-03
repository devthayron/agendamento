from django.urls import path
from .views import painel_dashboard


urlpatterns = [
    path('', painel_dashboard, name='painel_dashboard'),    
]