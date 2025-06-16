from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json

app = FastAPI()

# JSONファイルからプレイリストを読み込み
with open("data/playlist.json", "r", encoding="utf-8") as f:
    playlists = json.load(f)

# リクエスト用スキーマ
class MoodRequest(BaseModel):
    mood: str

# 【ここがAPI本体】POST: プレイリストを返す
@app.post("/api/playlists")
def get_playlist(req: MoodRequest):
    mood = req.mood.lower()
    if mood not in playlists:
        raise HTTPException(status_code=400, detail="無効な気分です")
    return {
        "mood": mood,
        "playlist": playlists[mood]
    }

#  GET: 利用可能な気分の一覧
@app.get("/api/moods")
def get_available_moods():
    return {"moods": list(playlists.keys())}

#  ここから下が【静的ファイルの配信処理】
# staticフォルダのマウント（/static以下のファイルを配信可能にする）
app.mount("/static", StaticFiles(directory="static"), name="static")

# ルート（/）にアクセスしたときに index.html を返す
@app.get("/")
def root():
    return FileResponse("static/index.html")