from django.db import models
from Accounts.models import Account

# Create your models here.
class Playlist(models.Model):
    name=models.CharField(max_length=225)
    url = models.URLField()
    playlist_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    
class Reminder(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    message = models.TextField()

    def __str__(self):
        return f'Reminder for {self.email} at {self.reminder_time}'

class Note(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, default=False)
    playlist_id = models.CharField(max_length=50, default=False)
    note = models.TextField()

    def __str__(self):
        return f'Note for {self.playlist_id}'