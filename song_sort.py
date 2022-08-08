import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

os.environ["SPOTIPY_CLIENT_ID"]='2a5689d36ad648fc90db4f2354679d5a'
os.environ["SPOTIPY_CLIENT_SECRET"]='e4510eb5bbed49d2bae960b04f78d52e'
os.environ["SPOTIPY_REDIRECT_URI"]='http://localhost:8081'

library_scope = 'user-library-read'
playlist_scope = 'playlist-modify-public'


# sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='2a5689d36ad648fc90db4f2354679d5a', client_secret='e4510eb5bbed49d2bae960b04f78d52e'))
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=library_scope))


songs = sp.current_user_saved_tracks()
playlists = sp.current_user_playlists()
playlists = list(filter(lambda x: (x['name'].startswith('_')),playlists['items']))

def shift_scope_playlist():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=playlist_scope))

def shift_scope_library():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=library_scope))



def create_playlist(name):
    print(f'creating playist with name: {name}')
    shift_scope_playlist()
    created_playlist = sp.user_playlist_create(user='12139404693', name=f'_{name}', public=True)
    shift_scope_library()
    return created_playlist

def add_song_to_playlist(song, playlist):
        print(f"Adding {song['name']} to {playlist['name']}")
        shift_scope_playlist()
        sp.playlist_add_items(playlist_id=playlist['id'], items=[song['uri']])
        shift_scope_library()

def process_song(song, playlists):
    print('Processing song: ', song['artists'][0]['name'], " – ", song['name'])
    print('current sorting playlists:')
    [print(i, p['name']) for i, p in enumerate(playlists)]
    val = input('Enter index of playlist to add to or enter a new playlist name. s to skip -> ')

    if val == 's':
        return
    try:
        val = int(val)
    except ValueError:
        playlists.append(create_playlist(val))
        val = len(playlists)-1
        # print(playlists)

    while val < 0 or val >= len(playlists):
        val = input('invalid input for value, try again -> ')

    add_song_to_playlist(song, playlists[val])

while songs:
    for idx, item in enumerate(songs['items']):
        process_song(song = item['track'], playlists=playlists)

    if songs['next']:
        songs = sp.next(songs)
    else:
        songs = None

