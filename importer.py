import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from mutagen import File
import json

# Get directory to import songs from
directory = input("Please enter the directory you want to search: ")
if not os.path.isdir(directory):
    print("Invalid directory - please enter a valid directory to import songs from.")
    exit(1)

# Configuration file
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except Exception as e:
    print(f"Error reading configuration file: {e}")
    exit(1)

client_id = config['client_id']
client_secret = config['client_secret']
username = config['username']
playlist_id = config['playlist_id']

if not all([client_id, client_secret, username, playlist_id]):
    print("Invalid configuration detected, refer to 'config.json.example' for the correct format.")
    exit(1)

# Spotify authentication
try:
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                        client_secret=client_secret,
                                                        redirect_uri='http://localhost:8888/callback',
                                                        scope='playlist-modify-public playlist-modify-private'))
except spotipy.exceptions.SpotifyException as e:
    print(f"Spotify authentication failed: {e}")
    exit(1)

not_found_songs = []
not_added_songs = []

# Process files in the directory
for root, dirs, files in os.walk(directory):
    for filename in files:
        file_path = os.path.join(root, filename)
        
        try:
            # Extract metadata from audio file found
            audio_file = File(file_path, easy=True)
        except Exception as e:
            print(f"Error processing file '{filename}': {e}")
            continue
        
        if audio_file:
            artist = audio_file.get('artist', [None])[0]
            title = audio_file.get('title', [None])[0]
            
            if artist and title:
                # Search for the track in Spotify and import if found
                results = spotify.search(q=f"artist:{artist} track:{title}", type='track')
                tracks = results['tracks']['items']
                
                if tracks:
                    track_id = tracks[0]['id']
                    try:
                        spotify.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=[track_id])
                        print(f"Added '{title}' by '{artist}' to the playlist.")
                    except spotipy.exceptions.SpotifyException as e:
                        print(f"Failed to add track '{title}' by '{artist}' to the playlist: {e}")
                        not_added_songs.append(f"'{title}' by '{artist}'")
                else:
                    print(f"Unable to find '{title}' by '{artist}' on Spotify.")
                    not_found_songs.append(f"'{title}' by '{artist}'")
            else:
                print(f"Metadata missing for file: {filename}")
                not_added_songs.append(filename)
        else:
            print(f"Unsupported file format: {filename}")
            not_added_songs.append(filename)

# Print summary
print("\nSummary of songs not found/added:")
if not_found_songs:
    print("\nSongs not found on Spotify:")
    for song in not_found_songs:
        print(song)
else:
    print("\nAll songs were found on Spotify.")

if not_added_songs:
    print("\nSongs not added (missing metadata or unsupported file format):")
    for song in not_added_songs:
        print(song)
else:
    print("\nAll songs were added successfully.")
