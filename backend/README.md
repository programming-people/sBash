## 開発環境でDBに接続

### 環境変数を設定

`.env` ファイルを作成

```.env
DB_HOST=localhost
DB_USER=postgres
DB_NAME=postgres
DB_PASS=password
```

### DBを起動

`docker compose up -d`

### サーバーを起動

`fastapi dev main.py`

or

`uv run fastapi dev main.py`

## データベース接続
### postgresユーザーで接続
sudo -u postgres psql
### mydatabaseに接続
sudo -u postgres psql -d mydatabase

## データベースマイグレーションのやり方
1. models.pyに仕様を記載する
2. マイグレーションファイル作成
alembic revision --autogenerate -m "Initial migration"
3. マイグレーション実行
alembic upgrade head

## CRUD APIの使用法
APIエンドポイントの仕様に従い、下記curlコマンドを打つ
### ユーザー作成
curl -X POST "http://127.0.0.1:8000/users/?name=YourName&email=your.email@example.com"
### ユーザー表示
http://127.0.0.1:8000/users/を直接叩く
### ユーザー更新
curl -X PUT 127.0.0.1:8000/users/1?name=updateduser
### ユーザー削除
curl -X DELETE "http://127.0.0.1:8000/users/1"
