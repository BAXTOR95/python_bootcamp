import os
import spotipy
from dotenv import load_dotenv
from pathlib import Path
from spotipy.oauth2 import SpotifyOAuth


ENV_PATH = Path("..", "..", ".env")

load_dotenv(dotenv_path=ENV_PATH)

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")


class Spotify:
    def __init__(self):
        self.sp = spotipy.Spotify(
            client_credentials_manager=SpotifyOAuth(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET,
                redirect_uri="http://example.com",
                scope="playlist-modify-public playlist-modify-private",
                show_dialog=True,
                cache_path="token.txt",
            )
        )

    def search_song(self, song_name):
        result = self.sp.search(q=song_name, type="track")
        if result["tracks"]["items"]:
            return result["tracks"]["items"][0]
        else:
            return None

    def search_song_by_artist(self, song_name, artist):
        result = self.sp.search(q=f"track:{song_name} artist:{artist}", type="track")
        if result["tracks"]["items"]:
            return result["tracks"]["items"][0]
        else:
            return None

    def get_song_preview_url(self, song_name):
        song = self.search_song(song_name)
        if song:
            return song["preview_url"]
        else:
            return None

    def get_song_preview_url_by_artist(self, song_name, artist):
        song = self.search_song_by_artist(song_name, artist)
        if song:
            return song["preview_url"]
        else:
            return None

    def get_current_user(self):
        return self.sp.current_user()

    def create_playlist(self, user_id, name, description, public=False):
        return self.sp.user_playlist_create(
            user=user_id, name=name, description=description, public=public
        )

    def add_to_playlist(self, playlist_id, songs_uri):
        return self.sp.playlist_add_items(playlist_id, songs_uri)