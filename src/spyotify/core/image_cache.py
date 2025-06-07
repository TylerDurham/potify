import requests


def local_image(image: dict, path: str = ""):
    requests.get(image["href"])

    if requests.status_codes == 200:
        print("Image Downloaded.")
    else:
        print("Image not downloaded!")
