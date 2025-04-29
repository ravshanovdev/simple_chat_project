from django.urls import path
from .views import index_view, room, private_index, private_chat


urlpatterns = [
    path('', index_view, name="index"),
    path('chat/<str:room_name>/', room, name="room"),

    path("private_chat/", private_index, name="private_index"),
    path("private_chat/<str:username>/", private_chat, name="private_chat"),


]



