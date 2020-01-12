import json
import hashlib
from datetime import datetime
from rest_framework import generics
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from chat_room.models import Message

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def messages(request):
    if request.method == 'POST':
        data = request.POST
        message = Message(room_id=data['room_id'],
                          sender=data['sender'],
                          time=datetime.now(),
                          text=data['text'])
        message.save()
        return HttpResponse('success')
    return HttpResponse('failed')

def room(request):
    if request.method == 'POST':
        roomName = request.POST['room_name']
        print(roomName)
        texts = []
        for message in Message.objects.filter(room_id=roomName):
            texts.append(message.text)
        return render(request, 'room.html', {
            'room_name_json': mark_safe(json.dumps(roomName)),
            'texts': mark_safe(json.dumps(texts)),
        })

def find_room(request):
    if request.method == 'POST':
        users = request.POST.getlist('users[]')
        users.sort()
        ori = users[0] + '#' + users[1]
        roomName = hashlib.sha256(ori.encode("utf-8")).hexdigest()
        return HttpResponse(roomName)
    return HttpResponse('failed')
