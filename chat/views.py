from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Room, Message


def home(request):
    return render(request, "home.html")


def room(request, room):
    username = request.GET.get("username")

    room_details = Room.objects.get(name=room)

    return render(
        request,
        "room.html",
        {
            "username": username,
            "room": room,
            "room_details": room_details,
        },
    )


def checkview(request):
    room_name = request.POST["room_name"]
    username = request.POST["username"]

    if not Room.objects.filter(name=room_name).exists():
        Room.objects.create(name=room_name)

    return redirect(
        f"/{room_name}/?username={username}"
    )


def send(request):
    if request.method == "POST":
        message = request.POST["message"]
        username = request.POST["username"]
        room_id = request.POST["room_id"]

        Message.objects.create(
            value=message,
            user=username,
            room=room_id,
        )

        return JsonResponse({
            "status": "success"
        })

    return JsonResponse({
        "status": "error"
    }, status=400)


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(
        room=room_details.id
    ).order_by("date")

    return JsonResponse({
        "messages": list(messages.values())
    })


