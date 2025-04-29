from django.shortcuts import render

# Create your views here.


def index_view(request):
    return render(request, "index.html")


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})


def private_index(request):
    return render(request, 'private_index.html')


def private_chat(request, username):
    return render(request, 'private_chat.html', {'username': username})
