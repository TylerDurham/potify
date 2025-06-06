import os

import typer
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from notifier import notify

app = typer.Typer()
load_dotenv()

SCOPE = "user-read-playback-state user-modify-playback-state"


SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]


def get_spotify_client():
    return Spotify(
        auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SCOPE,
        )
    )


@app.command("current")
def current():
    """Show the currently playing song."""
    print("Showing current")
    sp = get_spotify_client()
    current_track = sp.current_playback()
    if current_track and current_track.get("item"):
        item = current_track["item"]
        print(
            f"🎵 Now playing: {item['name']} by {', '.join(a['name'] for a in item['artists'])}"
        )
    else:
        print("No song is currently playing.")


def do_notify(sp):
    c = sp.current_playback()
    if c:
        notify(c.get("item"), "")


@app.command()
def next():
    """Plays the next item in the queue."""
    sp = get_spotify_client()
    current_track = sp.current_playback()
    if current_track:
        sp.next_track()
        do_notify(sp)


@app.command()
def previous():
    """Plays the previous item in the queue."""
    sp = get_spotify_client()
    current_track = sp.current_playback()
    if current_track:
        sp.previous_track()
        do_notify(sp)


@app.command()
def pause():
    """Pauses the current track."""
    sp = get_spotify_client()
    current_track = sp.current_playback()
    if current_track:
        sp.pause_playback()


@app.command()
def play():
    sp = get_spotify_client()
    sp.start_playback()
    do_notify(sp)


@app.command(name="debug-info")
def debug_info():
    print(f"CLIENT_ID: {SPOTIFY_CLIENT_ID}")
    print(f"CLIENT_SECRET: {SPOTIFY_CLIENT_SECRET}")
    print(f"REDIRECT_URI: {SPOTIFY_REDIRECT_URI}")


if __name__ == "__main__":
    app()
