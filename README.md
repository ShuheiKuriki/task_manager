## task_manager
タスク管理アプリ
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
- 前回データベースをちゃんと終了しなかった時の対処
```
rm /usr/local/var/postgres/postmaster.pid
launchctl unload -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist
launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist
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

