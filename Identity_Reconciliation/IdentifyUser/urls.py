from django.urls import path
from . import views

urlpatterns = [
    path('identify/', views.identify_user, name='identify_user'),
]