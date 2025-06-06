import subprocess


def notify(item, album_art_url):

    subprocess.run(
        [
            "terminal-notifier",
            "-title",
            item["name"],
            "-subtitle",
            ", ".join(a["name"] for a in item["artists"]),
            "-message",
            f"Album: {item['album']['name']}",
            "-open",
            item["album"]["images"][0]["url"],
        ]
    )
