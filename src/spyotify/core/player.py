from typing import Any

from spyotify.core.oauth import get_spotify_client


def next():
    raise NotImplementedError("This method is not implemented.")


def previous():
    raise NotImplementedError("This method is not implemented.")


def now_playing() -> tuple[bool, Any]:
    sp = get_spotify_client()

    player = sp.current_playback()
    if player and player.get("item"):
        return True, player["item"]
    else:
        return False, "Nothing is playing."


def pause():
    raise NotImplementedError("This method is not implemented.")
