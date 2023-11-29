from django.db import models
from django.contrib.auth.models import User
# import csv
# import qrcode
# import firebase
# import tempfile
# import os
# Create your models here.
# events/models.py



class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField(max_length=255)
    location = models.CharField(max_length=255)

    
    def __str__(self):
        return self.name




class Guest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    qr_data = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='qr_codes/')
    

    def __str__(self):
        return self.name + " " + self.event.name


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return self.guest.name + " " + self.event.name
    
class Feedback(models.Model):

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    feedback = models.CharField(max_length=255)

    def __str__(self):
        return self.event.name + " : " + self.feedback
    
class EventFeedbaackQr(models.Model):
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='feedback_qrcodes/')