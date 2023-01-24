from django.shortcuts import render
from .models import Playlist, Note
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from urllib.parse import urlparse
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
import re
import requests
from pprint import pprint
from googleapiclient.discovery import build
from django.core.paginator import Paginator
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from Accounts.models import Account
from trycourier import Courier
from Dashboard.models import Reminder, Playlist
from django.views.decorators.csrf import csrf_exempt

api_key = 'AIzaSyA-0BV5qEM-RKv4GtTQ-D_drmgr3k-RNV4'

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='login')
def add_playlist(request):
    if request.method == 'POST':
        submitted_item = request.POST.get('url')
        pattern = re.compile(r'^(https?\:\/\/)?(www\.)?(youtube\.com\/playlist\?list=)([a-zA-Z0-9_-]+)')
        match = pattern.match(submitted_item)
        if match:
            playlist_id = match.group(4)
            url = f'https://www.googleapis.com/youtube/v3/playlists?part=snippet&id={playlist_id}&key={api_key}'
            response = requests.get(url)
            data = response.json()
            title = data['items'][0]['snippet']['title']
            description = data["items"][0]["snippet"]["description"]
            thumbnail_url = data["items"][0]["snippet"]["thumbnails"]["high"]["url"]

            playlist = Playlist.objects.filter(user=request.user, playlist_id=playlist_id)
            if playlist.exists():
                messages.warning(request, 'Playlist already exists')
                return redirect('add_playlist')
            else:
                pl = Playlist.objects.create(user=request.user, name=title, url=submitted_item, playlist_id=playlist_id, description=description, thumbnail_url=thumbnail_url)
                pl.save()
                return redirect('playlists')
        else:
            messages.warning(request, 'Invalid URL')
            return redirect('add_playlist')
    else:
        return render(request, 'add_playlist.html')
            

@login_required(login_url='login')
def delete_playlist(request, playlist_id=None):
    if playlist_id is not None:
        pl = Playlist.objects.get(user=request.user, playlist_id=playlist_id)
        pl.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('playlists')
    else:
        messages.warning(request, 'Playlist does not exist')
        return redirect('playlists')


@login_required(login_url='login')
def playlists(request):
    all_playlists = Playlist.objects.filter(user=request.user)
    print(all_playlists)
    context = {
        'playlists': all_playlists,
    }

    return render(request, 'all_playlists.html', context)

@login_required(login_url='login')
def watch_now(request, playlist_id=None):
    if playlist_id:
        url = 'https://www.googleapis.com/youtube/v3/playlistItems'
        params = {
            'part': 'snippet',
            'playlistId': playlist_id,
            'key': api_key,
            'maxResults': 50
        }
        videos = []
        while True:
            res = requests.get(url, params=params)
            data = res.json()
            videos += data['items']
            if 'nextPageToken' not in data:
                break
            params['pageToken'] = data['nextPageToken']
        
        paginator = Paginator(videos, 5) # Show 10 videos per page
        page = request.GET.get('page')
        videos = paginator.get_page(page)
        first_video_id = videos[0]['snippet']['resourceId']['videoId']   

        notes = Note.objects.filter(user=request.user, playlist_id=playlist_id)

        context = {
            'videos': videos,
            'first_video': first_video_id,
            'playlist_id': playlist_id,
            'notes': notes,
        }
        return render(request, 'new_watch.html', context)

    return render(request, 'all_playlists.html')

def set_reminder(request):
    return render(request, 'set_reminders.html')


def add_note(request, playlist_id):
    if request.method == 'POST':
        note = request.POST.get('note')
        print(note, id)
        nt = Note(user=request.user, playlist_id=playlist_id, note=note)
        nt.note = note
        nt.save()
        messages.success(request, 'Note added successfully')
        return redirect('watch_now', playlist_id=playlist_id)
    else:
        return render(request, 'new_watch.html')

def delete_note(request, playlist_id, note_id):
    nt = Note.objects.get(user=request.user, playlist_id=playlist_id, id=note_id)
    nt.delete()
    messages.success(request, 'Note deleted successfully')
    return redirect('watch_now', playlist_id=playlist_id)

def notes(request):
    playlists = Playlist.objects.filter(user=request.user)
    notes = Note.objects.filter(user=request.user)
    context = {
        'playlists': playlists, 'notes': notes
    }
    return render(request, 'notes.html', context)
