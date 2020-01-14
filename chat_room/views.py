import os
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
from django.core.files import File

SAVED_FILES_DIR = r'files/'

if not os.path.exists(SAVED_FILES_DIR):
    os.makedirs(SAVED_FILES_DIR)

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('/login/')

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
                          is_file=data['is_file'],
                          sender=data['sender'],
                          time=datetime.now(),
                          text=data['text'])
        message.save()
        return HttpResponse('success')
    return HttpResponse('failed')

def room(request):
    if request.method == 'POST':
        roomName = request.POST['room_name']
        is_files = []
        texts = []
        times = []
        senders = []
        for message in Message.objects.filter(room_id=roomName):
            is_files.append(message.is_file)
            texts.append(message.text)
            times.append(datetime.strftime(message.time, '%Y-%m-%d %H:%M'))
            senders.append(message.sender)
        return render(request, 'room.html', {
            'room_name_json': mark_safe(json.dumps(roomName)),
            'is_files': mark_safe(json.dumps(is_files)),
            'texts': mark_safe(json.dumps(texts)),
            'times': mark_safe(json.dumps(times)),
            'senders': mark_safe(json.dumps(senders)),
        })

def find_room(request):
    if request.method == 'POST':
        users = request.POST.getlist('users[]')
        users = [users[0]] + users[1].split('#')
        users.sort()
        ori = users[0]
        for i in range(1, len(users)):
            ori = ori + '#' + users[i]
        roomName = hashlib.sha256(ori.encode("utf-8")).hexdigest()
        return HttpResponse(roomName)
    return HttpResponse('failed')


def upload(request):
    file = request.FILES.get("filename", None)
    if not file:
        return HttpResponse('failed')
 
    pathname = os.path.join(SAVED_FILES_DIR, file.name)
 
    with open(pathname, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
 
    return HttpResponse('success')

def download(request, filename):
    file_pathname = os.path.join(SAVED_FILES_DIR, filename)

    with open(file_pathname, 'rb') as f:
        file = File(f)
        response = HttpResponse(file.chunks(), content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Length'] = os.path.getsize(file_pathname)
        return response
    return HTTPResponse('failed')
