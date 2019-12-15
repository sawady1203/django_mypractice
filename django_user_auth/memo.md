# Djangoのユーザー管理機能を実装する

## やりたいこと

django-allauthを使って認証機能を実装する。

1. 新規プロジェクトを立ち上げる
2. Hello Worldレベルのアプリをつくる
3. ユーザー管理機能を作っていく

### 1. 新規プロジェクトを立ち上げる

```sh
mkdir django_user_auth
cd django_user_auth
python -m venv venv_user_auth
venv_user_auth\Script\activate
(venv_user_auth)python -m pip install --upgrade pip setuptools
# 以下すべては仮想環境下で行う。

# 必要なもののインストール
pip install django==3.0 python-dotenv django-allauth

# 新規プロジェクトを作成
django-admin startproject config .

```

### 2. Hello Worldレベルのアプリをつくる
### 3. ユーザー管理機能を作っていく