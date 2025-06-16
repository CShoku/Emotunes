# FastAPIのインストールと起動手順

## 1. 必要なパッケージのインストール
仮想環境を有効化した状態で、以下のコマンドを実行します：

```bash
# FastAPIのインストール
pip install fastapi

# Webサーバー（Uvicorn）のインストール
pip install uvicorn
```

## 2. Webサーバーの起動
以下のコマンドでWebサーバーを起動します：

```bash
uvicorn backend.main:app
```

### コマンドの説明
- `backend.main`: `backend/main.py`ファイルを指します
- `app`: `main.py`内で`FastAPI()`を使用して作成したインスタンス変数名です

## 3. 動作確認

### 基本的なエンドポイントの確認
ブラウザで以下のURLにアクセスしてください：
- http://127.0.0.1:8000/

以下のようなJSONレスポンスが表示されることを確認します：
```json
{
    "message": "Hello World",
    "status": 200
}
```

### APIドキュメントの確認
ブラウザで以下のURLにアクセスしてください：
- http://127.0.0.1:8000/docs

このページでは以下のことが可能です：
- APIの仕様を確認
- 各エンドポイントのテスト実行
- リクエスト/レスポンスの詳細な確認