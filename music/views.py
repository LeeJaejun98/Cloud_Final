from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
from django.conf import settings

cid = 'e3219977dde745f38af54c01a5082501'
secret = settings.SPOTIFY_KEY
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_list(request):
    result = sp.search(q='Top 50 - SOUTH KOREA', limit=1, type='playlist')
    playlist_id = result['playlists']['items'][0]['id']
    result = sp.playlist_items(playlist_id, limit=20, fields='items(track(external_urls, name, artists(name)))')

    return render(request, 'music/list.html', {
        'result': result['items']
    })


def get_search_list(request, search_text):
    result = sp.search(q=search_text, limit=1)
    song_info = {}
    song_info['artist_name'] = result['tracks']['items'][0]['artists'][0]['name']
    song_info['song_name'] = result['tracks']['items'][0]['name']
    song_info['url'] = result['tracks']['items'][0]['external_urls']['spotify']

    return render(request, 'music/search.html', {
        'song_info': song_info,
    })
