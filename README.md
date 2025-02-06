This short Python program will take your Deezer playlists file (I used https://www.tunemymusic.com/ for this, any app with the same format should work) and uploads them to your Spotify account.
Will output any songs not found into the console, and also into a file.

Steps to use:
1. Download your playlists into a .csv file using https://www.tunemymusic.com/.
2. Connect your Spotify account to developers.spotify.com/create and create a project.
3. Give your projects the Redirect URI of http://localhost:8888/, name and decription don't matter. You will be using the Web API, so mark that.
4. Make sure you have Python 3.13 (The version I tested this on), and the libraries spotipy and csv.
5. Run the script, with it being in the same directory as the deezer csv file.
6. After it's done, go to your Spotify Desktop app, to the Favorite Tracks playlist and Ctrl A -> Right Click -> Like all songs.
   
Now all your favorite songs from Deezer should be available on Spotify.
