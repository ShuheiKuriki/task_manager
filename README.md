# task_manager
タスク管理アプリ「Today's Task Schduler」として開発を始めたアプリ。

その後開発を進め、最終的にタスク・ルーティン・買い物・本など生活を総合的に管理するアプリ「Smart Life Planner」になった。
Lifeは"日常生活"と"人生"の掛け言葉になっているが、人生設計の機能はまだつけられていない。

ログイン機能・LINE通知機能あり。日常的に個人使用しており、なくてはならないアプリです。

- 公開url : https://tasks-day-scheduler.herokuapp.com/

## 使用技術
- 主要言語 : Python, javascript
- Webフレームワーク : Django
- JSライブラリ : jQuery, Chart.js
- データベース : PostgreSQL
- デザイン : Bootstrap(デザインテンプレート使用)
- デプロイ先 : heroku
- その他 : LINE API

## ディレクトリ一覧
- accounts : ログインなどユーザーアカウント管理関連
- book : 本関連
- notify : LINE通知関連
- shoppinglist : 買い物リスト関連
- task : タスク・ルーティン関連
- taskManager : 本来設定・全体統括のみを担当すべきディレクトリだが、途中で設計を変更したためタスク・LINE通知関連のモデル定義などが混ざってる

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

