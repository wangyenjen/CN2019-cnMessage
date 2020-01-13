from django.db import models

class UserState(models.Model):
    username = models.CharField(max_length=20, help_text='Enter username')
    is_online = models.BooleanField()

class Message(models.Model):
    room_id = models.CharField(max_length=64, help_text='Enter room id')
    is_file = models.BooleanField()
    sender = models.CharField(max_length=20, help_text='Enter username')
    time = models.DateTimeField()
    text = models.CharField(max_length=100, help_text='Enter message')
    
