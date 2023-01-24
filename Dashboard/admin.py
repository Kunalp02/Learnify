from django.contrib import admin
from .models import Playlist, Reminder, Note
# Register your models here.

admin.site.register(Playlist)
admin.site.register(Reminder)
admin.site.register(Note)