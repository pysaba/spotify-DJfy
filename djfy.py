import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access variables
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')


# Replace 'your_redirect_uri' with the redirect URI you set in your Spotify app settings
# Replace 'your_client_id' and 'your_client_secret' with your app's details
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='your_client_id',
                                               client_secret='your_client_secret',
                                               redirect_uri='your_redirect_uri',
                                               scope='playlist-modify-public'))

def fetch_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def analyze_tracks(tracks):
    track_ids = [track['track']['id'] for track in tracks]
    features = sp.audio_features(track_ids)
    return features

def create_playlist_and_add_tracks(user_id, sorted_tracks):
    new_playlist = sp.user_playlist_create(user_id, "DJfy Sorted Playlist", public=True)
    track_uris = [track['uri'] for track, _ in sorted_tracks]
    sp.playlist_add_items(new_playlist['id'], track_uris)
