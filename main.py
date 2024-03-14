from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os

client_id = os.environ.get("SPOTIPY_CLIENT_ID")
client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")

spotify_user_id = os.environ.get("SPOTIFY_USER_ID")

scope = "playlist-modify-private"
token = SpotifyOAuth(scope=scope, username=spotify_user_id)
spotify_object = spotipy.Spotify(auth_manager=token)

playlist_name = input("Enter a playlist name: ")
playlist_description = input("Enter a playlist description: ")

playlist = spotify_object.user_playlist_create(user=spotify_user_id, name=playlist_name, public=False,
                                               description=playlist_description)
playlist_id = (playlist["id"])

top_songs = []
list_of_songs = []

user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

url = f"https://www.billboard.com/charts/hot-100/{user_date}"

response = requests.get(url)
website = response.text

soup = BeautifulSoup(website, "html.parser")

song_titles = soup.select(".c-title")

for songs in song_titles:
    top_songs.append(songs.text.strip())

top_songs = top_songs[7:404:4]

for songs in top_songs:
    result = spotify_object.search(q=songs)
    list_of_songs.append(result["tracks"]["items"][0]["uri"])

file = open(f".cache-{spotify_user_id}")
data = json.load(file)

for songs in range(100):
    response = requests.post(url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?position=0&uris="
                                 f"{list_of_songs[songs]}&access_token={data['access_token']}")
