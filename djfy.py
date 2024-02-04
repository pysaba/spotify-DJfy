import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access variables
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Replace 'your_redirect_uri' with the redirect URI you set in your Spotify app settings
# Replace 'your_client_id' and 'your_client_secret' with your app's details
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri='http://localhost:8888',   # Ensure this matches the URI in your app settings
                                               scope='playlist-modify-public user-library-read'))

camelot_wheel = {
    # (key, mode): Camelot Code
    (0, 1): '8B', # C Major
    (0, 0): '5A', # A minor
    (1, 1): '3B', # C♯ Major / D♭ Major
    (1, 0): '12A', # A♯ minor / B♭ minor
    (2, 1): '10B', # D Major
    (2, 0): '7A', # B minor
    (3, 1): '5B', # D♯ Major / E♭ Major
    (3, 0): '2A', # C minor
    (4, 1): '12B', # E Major
    (4, 0): '9A', # C♯ minor / D♭ minor
    (5, 1): '7B', # F Major
    (5, 0): '4A', # D minor
    (6, 1): '2B', # F♯ Major / G♭ Major
    (6, 0): '11A', # E minor
    (7, 1): '9B', # G Major
    (7, 0): '6A', # E♭ minor / D♯ minor
    (8, 1): '4B', # G♯ Major / A♭ Major
    (8, 0): '1A', # F minor
    (9, 1): '11B', # A Major
    (9, 0): '8A', # F♯ minor / G♭ minor
    (10, 1): '6B', # A♯ Major / B♭ Major
    (10, 0): '3A', # G minor
    (11, 1): '1B', # B Major
    (11, 0): '10A', # G♯ minor / A♭ minor
}


def fetch_playlist_tracks(playlist_id):
    tracks = sp.playlist_tracks(playlist_id)['items']
    track_ids = [track['track']['id'] for track in tracks]
    features = sp.audio_features(track_ids)
    return features


def find_next_track(current_track, available_tracks):
    current_code = camelot_wheel.get((current_track['key'], current_track['mode']))
    closest_track = None
    closest_distance = float('inf')

    for track in available_tracks:
        track_code = camelot_wheel.get((track['key'], track['mode']))

        # Extract the numerical part of the Camelot codes
        current_num = int(current_code[:-1])
        track_num = int(track_code[:-1])

        # Calculate the direct numerical distance
        direct_distance = abs(track_num - current_num)

        # Calculate the wrap-around distance (e.g., from "1" to "12" and vice versa)
        wrap_around_distance = 12 - direct_distance

        # Use the smaller of the two distances as the key distance
        key_distance = min(direct_distance, wrap_around_distance)

        # If tracks are in different modes but have the same Camelot number, prioritize them
        if key_distance == 0 and track_code[-1] != current_code[-1]:
            return track  # Immediate return, as this is the closest match possible

        # If this track is closer than any previous one, update closest_track and closest_distance
        if key_distance < closest_distance:
            closest_distance = key_distance
            closest_track = track

    return closest_track


def sort_tracks_camelot(tracks_features):
    sorted_tracks = []
    available_tracks = tracks_features[:] # Create a copy to modify

    # Start with the first track (could enhance to start with a specific key)
    current_track = available_tracks.pop(0)
    sorted_tracks.append(current_track)

    while available_tracks:
        current_code = camelot_wheel.get((current_track['key'], current_track['mode']))
        next_track = find_next_track(current_track, available_tracks)
        if next_track:
            sorted_tracks.append(next_track)
            available_tracks.remove(next_track)
            current_track = next_track
        else:
            break # No more harmonically matching tracks found

    return sorted_tracks


def create_playlist_and_add_tracks(user_id, sorted_tracks):
    new_playlist = sp.user_playlist_create(user_id, "DJfy Sorted Playlist", public=True)
    track_uris = [track['uri'] for track in sorted_tracks]
    sp.playlist_add_items(new_playlist['id'], track_uris)

playlist_id = input("Enter the Spotify Playlist ID: ")
tracks_features = fetch_playlist_tracks(playlist_id)
sorted_tracks = sort_tracks_camelot(tracks_features)
user_id = sp.current_user()['id']  # Fetch the current user's Spotify ID
create_playlist_and_add_tracks(user_id,sorted_tracks)
for track in sorted_tracks:
    print(camelot_wheel.get((track['key'], track['mode'])))

#TODO: EDGE CASES, MORE CAMELOT MOVEMENT RESEARCH
#TODO: Starting track
#TODO: More sorting according to tempe, mood etc., maybe add different modes (starting fast to ending slow, starting slow to going fast etc.)