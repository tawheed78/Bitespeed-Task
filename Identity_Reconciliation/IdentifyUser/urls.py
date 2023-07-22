from django.urls import path
from . import views

#Url Pattern for IdentifyUser
urlpatterns = [
    path('identify/', views.identify_user, name='identify_user'),
]