## task_manager
タスク管理アプリ「Task Manager」として開発を始めたが、
タスク・ルーティン・買い物・本など生活を総合的に管理するアプリ「Life Planner」になった。

# 使用技術
- 主要言語 : Python, javascript
- Webフレームワーク : Django
- JSライブラリ : Jquery, Chart.js
- データベース : PostgreSQL
- デプロイ先 : heroku
- その他 : LINE API

# ディレクトリ一覧
- accounts
- book
- notify
- shoppinglist
- task
- taskManager

## 開発用メモ
- データベースサーバー起動
```
postgres -D /usr/local/var/postgres
```
- ローカルサーバー起動
```
python manage.py runserver
```
- データベースmigrate
```
python manage.py makemigrations
python manage.py migrate
```
- push
```
git push heroku master
git push origin master
heroku run python manage.py migrate
```

