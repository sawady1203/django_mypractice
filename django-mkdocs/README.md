# mkdocsを使ったドキュメントをDjangoで配信したい

## 参考

- [Integrating a password-protected MkDocs in Django](https://hacksoft.io/integrating-a-password-protected-mkdocs-in-django/)

## 環境構築

Pythonの仮想環境を構築して必要なパッケージをインストールします。

```sh
# 仮想環境構築
$ python -m venv venv-mkdocs
$ venv-mkdocs/Script/activate
(venv-mkdocks)$

# インストール
(venv-mkdocks)$ python -m pip install --upgrade pip setuptools
(venv-mkdocks)$ python -m pip install django mkdocs

# requirements.txtの作成
(venv-mkdocks)$ python -m pip freeze > requirements.txt
```

Djangoのプロジェクトとアプリケーションを作成していきます。

```sh
# カレントディレクトリにdjangoプロジェクトを作成する
(venv-mkdocks)$ django-admin startproject config .

# docsアプリケーションを作成する
(venv-mkdocks)$ python manage.py startapp docs

# staticディレクトリを作成する
(venv-mkdocks)$ mkdir static
```

`docs`アプリケーションを作成したのでDjangoの`INSTALL_APPS`に追加します。

``` Python
# config/settings.py

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'docs.apps.DocsConfig', # 追加
]
```

mkdocsのプロジェクトを作成していきます。

```sh
# mkdocsでプロジェクトを作成
(venv-mkdocks)$ mkdocs new mkdocks

# mkdocs/docs/index.md を mkdocs/以下に移動
(venv-mkdocks)$ move mkdocs\docs\index.md mkdocs\

# mkdocs.ymlファイルをプロジェクト下に移動
(venv-mkdocks)$ move mkdocs\mkdocs.yml .\

# mkdocs\docsディレクトリを削除
(venv-mkdocks)$ rmdir mkdocs\docs
```

ディレクトリはこうなりました。
![ディレクトリ構造](..\qiita\1_setup_directory.png)

## MkDocs Configuration

mkdocsのドキュメントをDjangoで配信していくにあたって、以下2点を頭に入れておきます。

- mkdocsで作成したドキュメントは`mkdocs`フォルダに設置する。
- mkdocsのドキュメントは`docs/static/mkdocs_build`にビルドされ、Djangoはこのフォルダを配信する。

これらの設定を`mkdocs.yml`に追加します。

```yml
site_name: My Docs

docs_dir: 'mkdocs'
site_dir: 'docs/static/mkdocs_build'

nav:
    - Home: index.md
```

mkdocsの開発サーバーを起動して確認してみましょう。

``` sh
(venv-mkdocks)$ mkdocs serve
```

mkdocsのWelcomeページが確認できました。うまく設定が反映できているようです。
ビルドして指定したフォルダにビルドされるかどうか確認します。

``` sh
(venv-mkdocks)$ mkdocs build
INFO    -  Cleaning site directory
INFO    -  Building documentation to directory: D:\python_projects\django_mypractice\django-mkdocs\docs\static\mkdocs_build
INFO    -  Documentation built in 0.14 seconds
```

## Making Django serve mkdocs

URLconfに配信用のパスを追加します。

``` Python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include('docs.urls')),  # 追加
]
```

`docs/urls.py`を追加します。

```sh
(venv-mkdocks)$ type nul > docs/urls.py
```

``` Python
# docs/urls.py
from django.urls import path
from . import views

app_name = "docs"

urlpatterns = [
    path('', views.serve_docs),
]
```

配信用のViewを追加します。まずはviewが機能することだけ確認したいので簡単なHttpレスポンスを返す機能だけにしてみます。

``` Python
# docs/views.py
from django.http import HttpResponse


def serve_docs(request):
    return HttpResponse('Docs are going to be served here')
```

```sh
(venv-mkdocks)$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
June 08, 2020 - 10:33:59
Django version 3.0.7, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

`http://localhost:8000/docs/`にアクセスすると`Docs are going to be served here`の文字が確認できます。

## URL Configuration

ドキュメントの配信URLを`docs/`以下に設定したい場合、`docs/*`以下の与えられたPathが`mkdocs_build`内を参照するようにしていきます。

`docs/urls.py`を変更しましょう。

``` Python
# docs/urls.py
from django.urls import path, re_path
from . import views

app_name = "docs"

urlpatterns = [
    re_path(r'^(?P<path>.*)$', views.serve_docs, name="serve_docs"),
]

```

`docs/views.py`はpathを受け取って返すようにしてみます。

``` Python
# docs/views.py
from django.http import HttpResponse


def serve_docs(request, path):
    return HttpResponse(path)
```

`http://localhost:8000/`以下を次のように変更すると、下記のようにPATHが表示されるよになりました。

- `/docs/` -> 空文字
- `/docs/index.html` -> index.html
- `/docs/about/` -> about/
- `/docs/about/index.html` -> about/index.html

このPATHを使って`mkdcos_build`を配信していきます。

## Serving the static files

配信用の`mkdocks_build`のフォルダパスなどの情報を`config/settings.py`に追加していきます。

``` Python
# config/settings.py

#######################
# mkdocs configration #
#######################

DOCS_DIR = os.path.join(BASE_DIR, 'docs/static/mkdocs_build')
DOCS_STATIC_NAMESPACE = os.path.basename(DOCS_DIR)
```

`django.contrib.staticfiles.views.serve`を使って静的ファイルを配信します。

`http://localhost:8000/docs/index.html`でMkdocsのWelcomeページが確認できますが、これは`http://localhost:8000/docs/`で配信させた方がよりよいURL設計でしょう。

## Appending index.html to our path

`mkdocks_build`以下には追加した`nav`別にフォルダが追加され、そのフォルダ下に`index.html`が作成されます。

これを考慮してviews.pyを変更しましょう。

``` Python
# docs/views.py
import os

from django.conf import settings
from django.contrib.staticfiles.views import serve


def serve_docs(request, path):
    docs_path = os.path.join(settings.DOCS_DIR, path)

    # /docs/<path>/ に`index.html`を追加する
    if os.path.isdir(docs_path):
        path = os.path.join(path, 'index.html')

    # /docs/<path>/index.html　はそのまま返す
    path = os.path.join(settings.DOCS_STATIC_NAMESPACE, path)

    return serve(request, path)
```

## Extra credit – reading mkdocs.yml in settings.py

`config/settings.py`に追加した`DOCS_DIR`と`DOCS_STATIC_NAMESPACE`は`mkdocs.yml`に記述されています。
わざわざ同じ設定を`settings.py`に追加するよりも、`mkdocs.yml`から参照するように変更しましょう。

pythonからymlファイルを読み込むため、PyYAMLをインストールします。

```sh
(venv-mkdocks)$ pip install PyYAML
```

``` Python
# config/settings.py

#######################
# mkdocs configration #
#######################

import yaml

MKDOCS_CONFIG = os.path.join(BASE_DIR, 'mkdocs.yml')
DOCS_DIR = ''
DOCS_STATIC_NAMESPACE = ''

with open(MKDOCS_CONFIG, 'r') as f:
    DOCS_DIR = yaml.load(f, Loader=yaml.Loader)['site_dir']
    DOCS_STATIC_NAMESPACE = os.path.basename(DOCS_DIR)
```

## Making the documentation password-protected

Djangoの認証システムを使ってユーザー認証を追加します。

``` Python
# views.py

import os

from django.conf import settings

from django.contrib.auth.decorators import login_required  # 追加
from django.contrib.staticfiles.views import serve


@login_required  # 追加
def serve_docs(request, path):
    docs_path = os.path.join(settings.DOCS_DIR, path)

    # /docs/<path>/ に`index.html`を追加する
    if os.path.isdir(docs_path):
        path = os.path.join(path, 'index.html')

    # /docs/<path>/index.html　はそのまま返す
    path = os.path.join(settings.DOCS_STATIC_NAMESPACE, path)

    return serve(request, path, insecure=True)
```

標準のUSERモデルでユーザー認証機能を追加します。

## User authentication

``` Python
# config/settings.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # 追加
    path('docs/', include('docs.urls')),
]

```

`templates/registration`を作成して`login.html`を追加します。

```sh
(venv-mkdocks)$ mkdir templates
(venv-mkdocks)$ cd templates

# base.htmlの作成
(venv-mkdocks)\templates>$ type nul > base.html
(venv-mkdocks)\templates>$ mkdir registration

# login.htmlの作成
(venv-mkdocks)\templates>$ type nul > registration/login.html
```

これで`docs/`にアクセスするとログイン画面が立ち上がり、ログイン後にドキュメントが閲覧できるようになりました。

※ユーザー認証はカスタムユーザーモデルで作成した方がいいです。

マイグレーションします。

```sh
(venv-mkdocks)$ python manage.py migrate
(venv-mkdocks)$ python manage.py runserver
```

## 注意

デプロイ時に静的ファイルを集約するとmkdocs内の静的ファイルも収集されてしまい、ユーザー認証機能を追加した意味が無くなってしまいます。
静的ファイルを集約する際は`mkdocs_build`除くようにする必要がある。

静的ファイルの設定を`config/settings.py`に追加します。

``` Python
# config/settings.py

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")
```

開発時は各アプリケーションの`static`フォルダ内を参照し、デプロイ時は静的ファイルを集約した`static_root`内を参照するようになります。

```sh
# mkdocs_buildを除いて静的ファイルを集約する
(venv-mkdocks)$ python manage.py collectstatic -i mkdocs_build
130 static files copied to 'D:\~~\django-mkdocs\static_root'.
```

仮に`mkdocs_build`を一緒に集約してしまった場合は、`static_root/mkdocs_build`を
削除しておきましょう。
