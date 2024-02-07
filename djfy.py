import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring

# Load environment variables from .env file
load_dotenv()

# Access variables
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Replace 'your_redirect_uri' with the redirect URI you set in your Spotify app settings
# Replace 'your_client_id' and 'your_client_secret' with your app's details
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri='http://localhost:8888',
                                               # Ensure this matches the URI in your app settings
                                               scope='playlist-modify-public user-library-read'))

camelot_wheel = {
    # (key, mode): Camelot Code
    (0, 1): '8B',  # C Major
    (0, 0): '5A',  # A minor
    (1, 1): '3B',  # C♯ Major / D♭ Major
    (1, 0): '12A',  # A♯ minor / B♭ minor
    (2, 1): '10B',  # D Major
    (2, 0): '7A',  # B minor
    (3, 1): '5B',  # D♯ Major / E♭ Major
    (3, 0): '2A',  # C minor
    (4, 1): '12B',  # E Major
    (4, 0): '9A',  # C♯ minor / D♭ minor
    (5, 1): '7B',  # F Major
    (5, 0): '4A',  # D minor
    (6, 1): '2B',  # F♯ Major / G♭ Major
    (6, 0): '11A',  # E minor
    (7, 1): '9B',  # G Major
    (7, 0): '6A',  # E♭ minor / D♯ minor
    (8, 1): '4B',  # G♯ Major / A♭ Major
    (8, 0): '1A',  # F minor
    (9, 1): '11B',  # A Major
    (9, 0): '8A',  # F♯ minor / G♭ minor
    (10, 1): '6B',  # A♯ Major / B♭ Major
    (10, 0): '3A',  # G minor
    (11, 1): '1B',  # B Major
    (11, 0): '10A',  # G♯ minor / A♭ minor
}


def fetch_playlist_tracks(playlist_id):
    tracks = sp.playlist_tracks(playlist_id)['items']
    track_ids = [track['track']['id'] for track in tracks]
    features = sp.audio_features(track_ids)
    return features

def fetch_tracks_metadata(playlist_id):
    tracks_metadata = []
    tracks = sp.playlist_tracks(playlist_id)['items']
    track_ids = [track['track']['id'] for track in tracks]
    # Spotify allows fetching metadata for up to 50 tracks at once
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        tracks_data = sp.tracks(batch)
        tracks_metadata.extend(tracks_data['tracks'])
    return tracks_metadata

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


def sort_tracks_camelot(tracks_features, starting_track_index):
    sorted_tracks = [tracks_features[starting_track_index]]  # Start with the selected track
    available_tracks = [t for t in tracks_features if
                        t != tracks_features[starting_track_index]]  # Remove the starting track from available tracks
    current_track = tracks_features[starting_track_index]
    while available_tracks:
        current_code = camelot_wheel.get((current_track['key'], current_track['mode']))
        next_track = find_next_track(current_track, available_tracks)
        if next_track:
            sorted_tracks.append(next_track)
            available_tracks.remove(next_track)
            current_track = next_track
        else:
            break  # No more harmonically matching tracks found

    return sorted_tracks


def create_playlist_and_add_tracks(user_id, sorted_tracks):
    new_playlist = sp.user_playlist_create(user_id, "DJfy Sorted Playlist", public=True)
    track_uris = [track['uri'] for track in sorted_tracks]
    sp.playlist_add_items(new_playlist['id'], track_uris)


def get_user_input_for_starting_track_index(tracks_metadata):
    starting_track_title = input("Enter the starting track title: ")
    # Corrected to use list comprehension for immediate evaluation
    matching_tracks = [track for track in tracks_metadata if starting_track_title.lower() in track['name'].lower()]

    if not matching_tracks:
        print("Track title not found in the playlist. Defaulting to first track in playlist.")
        return 0  # Handle this case appropriately in your code

    if len(matching_tracks) > 1:
        print("Multiple tracks found with that title:")
        for i, track in enumerate(matching_tracks):
            artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown Artist"
            print(f"{i+1}: {track['name']} by {artist_name}")
        chosen_index = int(input("Enter the number of the correct track: ")) - 1
        chosen_track = matching_tracks[chosen_index]
    else:
        chosen_track = matching_tracks[0]

    # Find the index of the chosen track in the original tracks_metadata list
    chosen_track_index = tracks_metadata.index(chosen_track)
    return chosen_track_index


def get_starting_track_index(tracks_metadata,starting_track_title):
    # Corrected to use list comprehension for immediate evaluation
    matching_tracks = [track for track in tracks_metadata if starting_track_title.lower() in track['name'].lower()]

    if not matching_tracks:
        print("Track title not found in the playlist. Defaulting to first track in playlist.")
        return 0  # Handle this case appropriately in your code

    if len(matching_tracks) > 1:
        print("Multiple tracks found with that title:")
        for i, track in enumerate(matching_tracks):
            artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown Artist"
            print(f"{i+1}: {track['name']} by {artist_name}")
        chosen_index = int(input("Enter the number of the correct track: ")) - 1
        chosen_track = matching_tracks[chosen_index]
    else:
        chosen_track = matching_tracks[0]

    # Find the index of the chosen track in the original tracks_metadata list
    chosen_track_index = tracks_metadata.index(chosen_track)
    return chosen_track_index

def sort_and_create_playlist():
    playlist_id = playlist_id_entry.get()
    starting_track_title = starting_track_entry.get()
    if not playlist_id:
        messagebox.showerror("Error", "Please enter a Spotify playlist ID.")
        return
    try:
        track_metadata = fetch_tracks_metadata(playlist_id)
        tracks_features = fetch_playlist_tracks(playlist_id)
        starting_track_index = get_starting_track_index(track_metadata,starting_track_title)
        sorted_tracks = sort_tracks_camelot(tracks_features, starting_track_index)
        user_id = sp.current_user()['id']  # Fetch the current user's Spotify ID
        create_playlist_and_add_tracks(user_id, sorted_tracks)
        for track in sorted_tracks:
           print(camelot_wheel.get((track['key'], track['mode'])))
        print(f"Sorting playlist {playlist_id} starting from track '{starting_track_title}'...")
        messagebox.showinfo("Success", "Playlist sorted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("DJfy: Harmonic Playlist Sorting")

# Create and pack the widgets
tk.Label(root, text="Spotify Playlist ID:").pack()
playlist_id_entry = tk.Entry(root)
playlist_id_entry.pack()

tk.Label(root, text="Starting Track (optional):").pack()
starting_track_entry = tk.Entry(root)
starting_track_entry.pack()

sort_button = tk.Button(root, text="Sort Playlist", command=sort_and_create_playlist)
sort_button.pack()

# Start the GUI event loop
root.mainloop()


#playlist_id = input("Enter the Spotify Playlist ID: ")
#track_metadata = fetch_tracks_metadata(playlist_id)
#tracks_features = fetch_playlist_tracks(playlist_id)
#starting_track_index = get_user_input_for_starting_track_index(track_metadata)
#sorted_tracks = sort_tracks_camelot(tracks_features, starting_track_index)
#user_id = sp.current_user()['id']  # Fetch the current user's Spotify ID
#create_playlist_and_add_tracks(user_id, sorted_tracks)
#for track in sorted_tracks:
#    print(camelot_wheel.get((track['key'], track['mode'])))

# TODO: MORE CAMELOT MOVEMENT RESEARCH
# TODO: More sorting according to tempe, mood etc., maybe add different modes (starting fast to ending slow, starting slow to going fast etc.)
# TODO: Website
