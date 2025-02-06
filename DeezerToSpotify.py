import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# -------------------------------
# Configuration - Replace with your Spotify Developer details
# -------------------------------
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:8888/'
SCOPE = 'playlist-modify-public'  # Use 'playlist-modify-private' if you prefer private playlists
FILE_PREFIX = '' # Deezer file name will be {FILE_PREFIX}Deezer.csv, output file will be NotFoundDeezer{FILE_PREFIX}.csv

# -------------------------------
# Helper Function to Find a Track's Spotify URI
# -------------------------------
def get_spotify_track_uri(sp, isrc, track_name, artist):
    """
    Attempts to retrieve the Spotify URI for a track.
    First, it uses the ISRC code if available.
    If not found, it falls back to searching by track name and artist.
    """
    # Try to search by ISRC first (which is usually more accurate)
    if isrc:
        query = f"isrc:{isrc}"
        results = sp.search(q=query, type="track")
        items = results.get("tracks", {}).get("items", [])
        if items:
            return items[0]["uri"]

    # Fallback: search by track name and artist
    query = f"track:{track_name} artist:{artist}"
    results = sp.search(q=query, type="track")
    items = results.get("tracks", {}).get("items", [])
    if items:
        return items[0]["uri"]
    
    # If not found, return None
    return None

# -------------------------------
# Main Function
# -------------------------------
def main():
    # Authenticate with Spotify using Spotipy's OAuth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        cache_path=None
    ))
    
    # Retrieve current user's Spotify ID
    user_id = sp.current_user()["id"]

    # Dictionary to group tracks by playlist name
    playlists = {}

    # Read the CSV file (adjust the filename/path as needed)
    csv_file = f"{FILE_PREFIX}Deezer.csv"
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            playlist_name = row["Playlist name"]
            if playlist_name not in playlists:
                playlists[playlist_name] = []
            playlists[playlist_name].append(row)
    
    # Don't add artists / albums as songs
    playlists.pop('Favorite Artists', None)
    playlists.pop('Favorite Albums', None)

    # Process each playlist from the CSV
    for playlist_name, tracks in playlists.items():
        print(f"\nCreating Spotify playlist: '{playlist_name}' with {len(tracks)} tracks...")
        
        # Create a new playlist in Spotify for this group of tracks
        new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        playlist_id = new_playlist["id"]
        
        track_uris = []  # List to store Spotify URIs for tracks
        for track in tracks:
            track_name = track["Track name"]
            artist = track["Artist name"]
            isrc = track["ISRC"].strip()  # Remove any extra spaces
            
            uri = get_spotify_track_uri(sp, isrc, track_name, artist)
            if uri:
                track_uris.append(uri)
            else:
                print(f"Warning: Could not find '{track_name}' by {artist} on Spotify.")
                with open(f'NotFoundDeezer{FILE_PREFIX}.csv', mode='a', encoding='utf-8') as file:
                    file.write(f"{playlist_name}: {track_name} by {artist}, {isrc}\n")
        
        # Spotify's API allows adding up to 100 tracks per request, so we batch them.
        for i in range(0, len(track_uris), 100):
            sp.playlist_add_items(playlist_id, track_uris[i:i+100])
        
        print(f"Playlist '{playlist_name}' created with {len(track_uris)} tracks added.")
    
if __name__ == "__main__":
    main()
