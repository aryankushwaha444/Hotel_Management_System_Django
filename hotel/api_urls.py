from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.room_list_api, name='room_list_api'),
]
