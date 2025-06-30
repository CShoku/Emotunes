# from fastapi import FastAPI, HTTPException
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from backend.spotify.fetch_playlist import fetch_playlist_by_mood
# from dotenv import load_dotenv

# load_dotenv()

# from fastapi import FastAPI, HTTPException, Request
# from pydantic import BaseModel
# from backend.spotify.create_playlist import create_mood_playlist

# app = FastAPI()

# # 仮：ここでは固定のアクセストークンを使う
# # ※ 実際はログイン後に取得したトークンをセッション等で保持するべきです
# HARDCODED_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE"

# class MoodRequest(BaseModel):
#     mood: str

# @app.post("/api/playlists")
# def generate_playlist(req: MoodRequest):
#     try:
#         url = create_mood_playlist(HARDCODED_ACCESS_TOKEN, req.mood.lower())
#         return {"url": url}
#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"作成中にエラー: {str(e)}")

# # @app.post("/api/playlists")
# # def get_playlist(req: MoodRequest):
# #     mood = req.mood.lower()
# #     try:
# #         playlist = fetch_playlist_by_mood(mood)
# #         return {"mood": mood, "playlist": playlist}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))

# # 静的ファイル
# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/")
# def root():
#     return FileResponse("static/index.html")

import os
import random
import requests
from urllib.parse import urlencode

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

print("redirect_uri:", REDIRECT_URI)  # 確認用（あとで削除OK）

app = FastAPI()

# 静的ファイルをマウント
app.mount("/static", StaticFiles(directory="static"), name="static")

# トップページで index.html を返す
@app.get("/")
def root():
    return FileResponse("static/index.html")

# セッション代わりの仮変数（本番ではセッション管理すべき）
access_token_global = ""
user_id_global = ""

# 1. 認可URLにリダイレクト
@app.get("/login")
def login():
    scope = "playlist-modify-public playlist-modify-private"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope
    }
    url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    return RedirectResponse(url)

# 2. コールバックでアクセストークンとユーザーIDを取得
@app.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="codeがありません")

    # アクセストークン取得
    token_resp = requests.post("https://accounts.spotify.com/api/token", data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })
    token_json = token_resp.json()
    access_token = token_json.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="トークンが取得できませんでした")

    # ユーザーID取得
    me_resp = requests.get("https://api.spotify.com/v1/me", headers={
        "Authorization": f"Bearer {access_token}"
    })
    me_json = me_resp.json()
    user_id = me_json.get("id")

    global access_token_global, user_id_global
    access_token_global = access_token
    user_id_global = user_id

    return JSONResponse({"message": "ログイン完了", "user_id": user_id})

# 3. プレイリストを作成
@app.post("/create_playlist")
def create_playlist(mood: str = "happy"):
    global access_token_global, user_id_global

    if not access_token_global or not user_id_global:
        raise HTTPException(status_code=401, detail="未認証です")

    keywords = {
        "happy": ["joy", "upbeat", "party"],
        "sad": ["melancholy", "acoustic"],
        "relaxed": ["chill", "ambient"]
    }

    query = random.choice(keywords.get(mood, ["mood"]))

    # 楽曲を検索
    search = requests.get("https://api.spotify.com/v1/search", headers={
        "Authorization": f"Bearer {access_token_global}"
    }, params={"q": query, "type": "track", "limit": 10}).json()

    tracks = search.get("tracks", {}).get("items", [])
    uris = [t["uri"] for t in tracks]

    # プレイリスト作成
    pl_resp = requests.post(
        f"https://api.spotify.com/v1/users/{user_id_global}/playlists",
        headers={
            "Authorization": f"Bearer {access_token_global}",
            "Content-Type": "application/json"
        },
        json={
            "name": f"{mood.capitalize()} Mood by Emotunes",
            "public": False
        }
    )
    playlist_id = pl_resp.json()["id"]

    # トラック追加
    requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers={"Authorization": f"Bearer {access_token_global}"},
        json={"uris": uris}
    )

    return {"message": "プレイリスト作成完了", "url": pl_resp.json()["external_urls"]["spotify"]}
