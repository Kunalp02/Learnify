from django.contrib import admin
from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('add_playlist/', views.add_playlist, name="add_playlist"),
    path('delete_playlist/<playlist_id>/', views.delete_playlist, name="delete_playlist"),
    path('playlists/', views.playlists, name="playlists"),
    path('watch_now/<playlist_id>/', views.watch_now, name="watch_now"),
    path('set_reminder/', views.set_reminder, name="set_reminder"),
    path('notes/', views.notes, name="notes"),
    path('add_note/<playlist_id>/', views.add_note, name="add_note"),
    path('delete_note/<playlist_id>/<note_id>/', views.delete_note, name="delete_note"),
    
]
