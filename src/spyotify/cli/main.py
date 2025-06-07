import typer

from spyotify.core import player

app = typer.Typer()


@app.command(name="now-playing")
def now_playing():
    """Displays information about the current track playing."""
    status, track = player.now_playing()

    if status:
        album = track["album"]

        images = album["images"]

        for image in images:
            print(image)
    else:
        print("There was an issue getting the current track.")
    # print(track)


@app.command(name="next")
def next():
    """Advances to the next track."""
    print("next()")


if __name__ == "__main__":
    app()


# import spyotify.cli.renderer as r
# from spyotify.cli.notifier import notify
# from spyotify.core.oauth import get_spotify_client
#
# app = typer.Typer()  # Sample data (simulate what's playing)
#
#
# def get_current_track():
#     return {
#         "track": "Waking Light",
#         "artist": "Beck",
#         "album": "Morning Phase",
#         "art_url": "https://upload.wikimedia.org/wikipedia/en/2/26/Beck_Morning_Phase.jpg",
#         "duration": "5:01",
#         "progress": "2:35",
#     }
#
#
# @app.command()
# def now_playing():
#     r.now_playing()
#
#
# @app.command("current")
# def current():
#     """Show the currently playing song."""
#     print("Showing current")
#     sp = get_spotify_client()
#     current_track = sp.current_playback()
#     if current_track and current_track.get("item"):
#         item = current_track["item"]
#         print(
#             f"🎵 Now playing: {item['name']} by {', '.join(a['name'] for a in item['artists'])}"
#         )
#     else:
#         print("No song is currently playing.")
#
#
# def do_notify(sp):
#     c = sp.current_playback()
#     if c:
#         notify(c.get("item"), "")
#
#
# @app.command()
# def next():
#     """Plays the next item in the queue."""
#     sp = get_spotify_client()
#     current_track = sp.current_playback()
#     if current_track:
#         sp.next_track()
#         do_notify(sp)
#
#
# @app.command()
# def previous():
#     """Plays the previous item in the queue."""
#     sp = get_spotify_client()
#     current_track = sp.current_playback()
#     if current_track:
#         sp.previous_track()
#         do_notify(sp)
#
#
# @app.command()
# def pause():
#     """Pauses the current track."""
#     sp = get_spotify_client()
#     current_track = sp.current_playback()
#     if current_track:
#         sp.pause_playback()
#
#
# @app.command()
# def play():
#     sp = get_spotify_client()
#     sp.start_playback()
#     do_notify(sp)
#
#
# # @app.command(name="debug-info")
# # def debug_info():
# #     print(f"CLIENT_ID: {SPOTIFY_CLIENT_ID}")
# #     print(f"CLIENT_SECRET: {SPOTIFY_CLIENT_SECRET}")
# #     print(f"REDIRECT_URI: {SPOTIFY_REDIRECT_URI}")
# #
#
# if __name__ == "__main__":
#     app()
