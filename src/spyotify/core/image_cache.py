# ##################################################
# _ _  _ ____ ____ ____    ____ ____ ____ _  _ ____
# | |\/| |__| | __ |___    |    |__| |    |__| |___
# | |  | |  | |__] |___    |___ |  | |___ |  | |___
#
# ##################################################

import os
from urllib.parse import urlparse

import requests

# Get the user's home directory
HOME_DIR = os.path.expanduser("~")

# Location of the cache directory
CACHE_DIR = os.path.join(HOME_DIR, ".local/cache/spyotify/images/")


def ensure_cache_dir():
    """Creates the cache directory if it does not exists."""
    os.makedirs(CACHE_DIR, exist_ok=True)


def get_local_file_name(url: str, ext: str = ".jpg"):
    """Gets the base name of the image and appends the specified extension. The default extension is '.jpg'."""
    p = urlparse(url)
    return f"{os.path.basename(p.path)}.{ext}"


def get_local_file_path(url: str, ext: str = ".jpg") -> str:
    """Gets the full path of the image from the cache directory and appends the specified extension. The default extension is '.jpg'."""
    return f"{os.path.join(CACHE_DIR, get_local_file_name(url, ext))}"


def get_local_images(images: list[dict], ext: str = ".jpg"):
    ensure_cache_dir()

    for image in images:
        lfp = get_local_image(image, ext)
        image["local-path"] = lfp


def get_local_image(image: dict, ext: str = ".jpg"):
    """Fetches an image from the cache. If it doesn't exist, it will downloaded to the cache."""
    ensure_cache_dir()

    url = image["url"]

    lfp = get_local_file_path(url, ext)

    print(f"Checking file {lfp} exists...")

    if os.path.exists(lfp):
        print(f"File {lfp} exists!")
        return lfp
    else:

        # Download the image
        response = requests.get(url)

        if response.status_code == 200:

            content_type = response.headers.get("Content-Type", "")
            ext = content_type.split("/")[-1].split(";")[0].strip().lower()

            print(
                f"Image {url} Downloaded. content-type: {content_type} size: {len(response.content)}"
            )
            lfp = get_local_file_path(url, ext)
            print(f"Writing file {lfp} size: {len(response.content)}")
            with open(lfp, "wb") as f:
                f.write(response.content)

            return lfp
        else:
            print(f"Image {url} not downloaded! {response.status_code}")
            return None
