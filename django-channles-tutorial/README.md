# Django-channles-Tutorial を進める

Official Document : https://channels.readthedocs.io/en/latest/

## 環境構築

```sh
$ python -m venv venv-channles
$ venv-channels\Scripts\activate
$ python -m pip install --upgrade pip setuptools
$ python -m pip install django channels
```

## Django プロジェクトを始める

```sh
$ django-admin startproject config .
```

### channels の installation

settings.py へ`channels`の追加

```python

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
]

```

`config/routing.py`の追加

```sh
$ type nul > config\routing.py
```

```python
# config/routing.py

from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})
```

`config/settings.py`に`ASGI_APPLICATION`を追加

```python
ASGI_APPLICATION = "config.routing.application"
```

## Chat アプリケーションを作成

```sh
$ pyton manage.py startapp chat
```

`config/settings.py`に`chat`を追加

```python
# config/settings.py
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'chat.apps.ChatConfig',
]
```

template ディレクトリを作成する。
chat ディレクトリに index.html も作成する。

```sh
$ mkdir templates
$ mkdir templates\chat
$ type nul templates\chat\index.html
```

`chat/index.html`を編集する

```html
<!-- templates/chat/index.html -->
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Chat Room</title>
  </head>
  <body>
      What chat room would you like to enter?</br>
      <input id="room-name-input" type="text" size="100"></br>
      <input id="room-name-submit" type="button" value="Enter">
  </body>
  <script>
      document.querySelector("#room-name-input").focus();
      document.querySelector("#room-name-input").onkeyup = function(e){
          if (e.keyCode === 13) {  // enter, return
              document.querySelector('#room-name-submit').click();
          }
      };
      document.querySelector('#room-name-submit').onclick = function (e) {
            var roomName = document.querySelector('#room-name-input').value;
            window.location.pathname = '/chat/' + roomName + '/';
        };
  </script>
</html>
```

`#room-name-input`が入力されると`window.location.pathname = '/chat/' + roomName + '/';`によって
ページ URL が変更されることがわかる。すなわち get リクエストが投げられる。

### URL

`config/urls.py`に`chat`への分岐を追加する。

```python
# confing/settings.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
]
```

`chat/urls.py`を追加する。

```sh
$ type nul > chat\urls.py
```

```python
# chat/urls.py

from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

### views

`chat/views.py`に`views.index`を追加する

```python
# chat/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html', {})
```

この状態で`python manage.py runserver`をするとどうなるか

```sh
$ python manage.py runserver

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
March 17, 2020 - 14:49:31
Django version 3.0.4, using settings 'config.settings'
Starting ASGI/Channels version 2.4.0 development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
