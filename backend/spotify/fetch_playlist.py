from .auth import get_access_token
import requests

MOOD_KEYWORDS = {
    "happy": "happy upbeat",
    "sad": "sad acoustic",
    "relaxed": "chill relax"
}

def fetch_playlist_by_mood(mood: str):
    access_token = get_access_token()
    keyword = MOOD_KEYWORDS.get(mood, "chill")

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"q": keyword, "type": "playlist", "limit": 3}
    )
    response.raise_for_status()

    items = response.json()["playlists"]["items"]

    result = []
    for item in items:
        result.append({
            "title": item["name"],
            "artist": item["owner"]["display_name"],
            "url": item["external_urls"]["spotify"],
            "image": item["images"][0]["url"] if item["images"] else None
        })

    return result
