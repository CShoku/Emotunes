# Windowsでのポートフォワーディング設定

## 前提条件
- WindowsのIPアドレス: 192.168.11.13
- WSLのIPアドレス: 172.28.139.139

## 注意事項
- 管理者権限のPowerShellで実行する必要があります
- 設定の変更は再起動不要です
- 推奨設定は`0.0.0.0`を使用する方法です

## 設定手順

### 1. 特定のIPアドレスへの転送設定
以下のコマンドで、Windowsの特定IPアドレスからWSLへの転送を設定します：

```powershell
netsh interface portproxy add v4tov4 listenaddress=192.168.11.13 listenport=8000 connectaddress=172.28.139.139 connectport=8000
```

この設定により、`192.168.11.13:8000`へのアクセスが`172.28.139.139:8000`に転送されます。

### 2. 設定の確認
現在の設定を確認するには、以下のコマンドを実行します：

```powershell
netsh interface portproxy show all
```

出力例：
```
Listen on ipv4:             Connect to ipv4:
Address         Port        Address         Port
--------------- ----------  --------------- ----------
192.168.11.13   8000        172.28.139.139  8000
```

### 3. 設定の削除
設定を削除する場合は、以下のコマンドを実行します：

```powershell
netsh interface portproxy delete v4tov4 listenaddress=192.168.11.13 listenport=8000
```

## 推奨設定（任意のIPアドレスへの転送）

### 1. 転送設定
以下のコマンドで、任意のIPアドレスからのアクセスをWSLに転送します：

```powershell
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=8000 connectaddress=172.28.139.139 connectport=8000
```

### 2. Uvicornの起動設定
この設定を使用する場合、Uvicornを以下のように起動する必要があります：

```bash
uvicorn backend.main:app --host 0.0.0.0
```

注意：この設定では`http://127.0.0.1:8000/`でのアクセスができなくなります。

## 技術的な補足

### bindについて
アプリケーションプログラムを特定のIPアドレス/ポート番号で待ち受けることを「bind」と呼びます。

- `uvicorn api.main:app --host 172.28.139.139`
  - IPアドレス`172.28.139.139`、ポート`8000`にbind
- `uvicorn api.main:app --host 0.0.0.0`
  - そのネットワークインターフェースに割り当てられている全てのIPアドレス、ポート`8000`にbind