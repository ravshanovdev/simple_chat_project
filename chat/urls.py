from django.urls import path
from .views import index_view, room


urlpatterns = [
    path('', index_view, name="index"),
    path('chat/<str:room_name>/', room, name="room"),


]



