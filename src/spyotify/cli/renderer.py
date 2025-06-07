import os

import requests
import typer
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
# If you're using rich.image.Image, it needs pillow installed
from rich_pixels import Pixels

app = typer.Typer()
console = Console()


# Sample data (simulate what's playing)
def get_current_track():
    return {
        "track": "Waking Light",
        "artist": "Beck",
        "album": "Morning Phase",
        "art_url": "https://img.apmcdn.org/506a2ffb06d8e2f5d76cd04de698128cee3e7f3f/uncropped/58e385-20140222-beck-morning-phase.jpg",
        "duration": "5:01",
        "progress": "2:35",
    }


def now_playing():
    track_info = get_current_track()

    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Define the directory path relative to the home directory
    directory_path = os.path.join(home_dir, "temp")
    art_file_name = (
        f"{track_info['artist']}-{track_info['album']}-{track_info['track']}.jpg"
    )
    art_file_path = os.path.join(directory_path, art_file_name)

    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)

    # Download album art temporarily
    response = requests.get(track_info["art_url"])

    if response.status_code == 200:
        print("Downloaded arg file")
    else:
        print(f"Can't download {track_info['art_url']}")

    print(f"Writing to {art_file_path}")
    with open(art_file_path, "wb") as f:
        f.write(response.content)
        f.close()

    # Show album art (only works in some terminals)
    try:
        p = Pixels()
        p.from_image_path(art_file_path)
        console.print(p)
    except Exception as e:
        console.print("[bold red]Image rendering failed[/bold red]", e)

    # Clean up later
    os.unlink(art_file_path)

    # Show track info
    table = Table.grid(expand=True)
    table.add_column(justify="right")
    table.add_column(justify="left")

    table.add_row("🎵 Track:", f"[bold cyan]{track_info['track']}[/bold cyan]")
    table.add_row("🎤 Artist:", f"[bold magenta]{track_info['artist']}[/bold magenta]")
    table.add_row("💿 Album:", f"[green]{track_info['album']}[/green]")
    table.add_row("⏱ Duration:", f"{track_info['progress']} / {track_info['duration']}")

    panel = Panel(
        Align.center(table),
        box=box.ROUNDED,
        title="🎧 Now Playing",
        border_style="bright_blue",
    )
    console.print(panel)
