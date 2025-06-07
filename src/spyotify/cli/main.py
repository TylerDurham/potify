import base64
from io import BytesIO

import typer
from PIL import Image
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from spyotify.core import image_cache, player

app = typer.Typer()
console = Console()


def display_image_in_terminal(image_path):
    # Open and convert the image to PNG format
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

    # Encode the image in base64
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    # Construct the escape sequence

    print(
        f"\033]1337;File=inline=1;width=auto;height=auto;preserveAspectRatio=1:{img_base64}\a"
    )


@app.command(name="now-playing")
def now_playing():
    """Displays information about the current track playing."""
    ok, track = player.now_playing()

    if ok:
        title = track["name"]
        artists = ", ".join(a["name"] for a in track["artists"])
        album = track["album"]
        album_name = album["name"]

        images = album["images"]

        image_cache.get_local_images(images)
        p = images[0]["local-path"]
        print(p)
        # display_image_in_terminal(p)

        # Show track info
        table = Table.grid(expand=True)
        table.add_column(justify="right")
        table.add_column(justify="left")

        table.add_row("🎵 Track:", f"[bold cyan]{title}[/bold cyan]")
        table.add_row("🎤 Artist:", f"[bold magenta]{artists}[/bold magenta]")
        table.add_row("💿 Album:", f"[green]{album_name}[/green]")
        # table.add_row("⏱ Duration:", f"{track['progress']} / {track_info['duration']}")

        panel = Panel(
            Align.center(table),
            box=box.ROUNDED,
            title="🎧 Now Playing",
            border_style="bright_blue",
        )
        console.print(panel)

    else:
        print("There was an issue getting the current track.")


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
