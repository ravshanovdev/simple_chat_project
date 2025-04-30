from django.shortcuts import render
from django.http import HttpResponse


def index_view(request):
    return render(request, "index.html")


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})


def private_index(request):
    if not request.user.is_authenticated:
        return HttpResponse("royxatdan otish kerak.!")
    return render(request, 'private_index.html')


def private_chat(request, username):
    if not request.user.is_authenticated:
        return HttpResponse("royxatdan otish kerak.!")
    return render(request, 'private_chat.html', {'username': username})
