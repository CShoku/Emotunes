# ディレクトリ構造の設計目標を記述したファイルです
mood_api/
├── app/
│   ├── __init__.py
│   ├── main.py                    # メインアプリケーション
│   ├── models/
│   │   ├── __init__.py
│   │   ├── mood.py               # 気分データモデル
│   │   ├── playlist.py           # プレイリストモデル
│   │   └── user.py               # ユーザーモデル
│   ├── api/
│   │   ├── __init__.py
│   │   ├── mood_routes.py        # 気分関連API (GET/POST)
│   │   ├── playlist_routes.py    # プレイリスト関連API
│   │   └── spotify_routes.py     # Spotify連携API
│   ├── services/
│   │   ├── __init__.py
│   │   ├── mood_service.py       # 気分分析・管理ロジック
│   │   ├── spotify_service.py    # Spotify API連携サービス
│   │   └── playlist_generator.py # プレイリスト生成ロジック
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth.py               # 認証関連ユーティリティ
│   │   ├── validators.py         # データバリデーション
│   │   └── helpers.py            # その他ヘルパー関数
│   └── database/
│       ├── __init__.py
│       ├── connection.py         # DB接続設定
│       └── migrations/           # DBマイグレーション
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── components.css
│   ├── js/
│   │   ├── app.js               # メインJS
│   │   ├── mood-selector.js     # 気分選択UI
│   │   ├── playlist-manager.js  # プレイリスト管理
│   │   └── spotify-auth.js      # Spotify認証処理
│   ├── images/
│   │   ├── mood-icons/          # 気分アイコン
│   │   └── ui-assets/
│   └── favicon.ico
├── templates/
│   ├── base.html               # ベーステンプレート
│   ├── index.html              # メインページ
│   ├── mood/
│   │   ├── selector.html       # 気分選択画面
│   │   └── history.html        # 気分履歴
│   ├── playlist/
│   │   ├── generator.html      # プレイリスト生成画面
│   │   └── library.html        # プレイリストライブラリ
│   └── auth/
│       ├── login.html          # ログイン画面
│       └── callback.html       # Spotify認証コールバック
├── data/
│   ├── moods.json              # 気分カテゴリ定義
│   ├── playlists.json          # プレイリストデータ
│   ├── mood_mappings.json      # 気分→音楽ジャンルマッピング
│   └── sample_data/            # サンプルデータ
├── config/
│   ├── __init__.py
│   ├── settings.py             # アプリケーション設定
│   ├── spotify_config.py       # Spotify API設定
│   └── database_config.py      # データベース設定
├── tests/
│   ├── __init__.py
│   ├── test_mood_api.py        # 気分API テスト
│   ├── test_spotify_service.py # Spotify連携テスト
│   ├── test_playlist_generator.py # プレイリスト生成テスト
│   └── fixtures/               # テスト用データ
├── logs/
│   ├── app.log
│   ├── error.log
│   └── spotify_api.log
├── docs/
│   ├── API.md                  # API仕様書
│   ├── SETUP.md                # セットアップガイド
│   └── DEPLOYMENT.md           # デプロイメント手順
├── scripts/
│   ├── setup_db.py             # DB初期化スクリプト
│   ├── seed_data.py            # サンプルデータ投入
│   └── backup.py               # バックアップスクリプト
├── requirements.txt            # Python依存関係
├── requirements-dev.txt        # 開発用依存関係
├── .env.example               # 環境変数テンプレート
├── .env                       # 環境変数（秘匿情報）
├── .gitignore
├── README.md
├── docker-compose.yml         # Docker設定
├── Dockerfile
└── run.py                     # アプリケーション起動スクリプト