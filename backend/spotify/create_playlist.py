import requests
import random

MOOD_KEYWORDS = {
    "happy": ["upbeat", "joy", "party"],
    "sad": ["melancholy", "acoustic", "slow"],
    "relaxed": ["chill", "ambient", "calm"]
}

def create_mood_playlist(access_token: str, mood: str):
    if mood not in MOOD_KEYWORDS:
        raise ValueError("Unsupported mood")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 1. ユーザー情報取得
    user_resp = requests.get("https://api.spotify.com/v1/me", headers=headers)
    user_resp.raise_for_status()
    user_id = user_resp.json()["id"]

    # 2. プレイリスト作成
    playlist_data = {
        "name": f"Emotunes - {mood.capitalize()} 🎶",
        "description": f"{mood} mood auto-generated playlist",
        "public": False
    }

    playlist_resp = requests.post(
        f"https://api.spotify.com/v1/users/{user_id}/playlists",
        headers=headers,
        json=playlist_data
    )
    playlist_resp.raise_for_status()
    playlist_id = playlist_resp.json()["id"]

    # 3. 楽曲検索（ランダムなキーワード）
    keyword = random.choice(MOOD_KEYWORDS[mood])
    search_resp = requests.get(
        "https://api.spotify.com/v1/search",
        headers=headers,
        params={
            "q": keyword,
            "type": "track",
            "limit": 20
        }
    )
    search_resp.raise_for_status()
    tracks = search_resp.json()["tracks"]["items"]
    uris = [track["uri"] for track in random.sample(tracks, k=min(10, len(tracks)))]

    # 4. プレイリストに追加
    requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json={"uris": uris}
    )

    # 5. 完了：URL返す
    return playlist_resp.json()["external_urls"]["spotify"]
