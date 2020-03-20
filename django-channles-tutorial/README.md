# Django-channles-Tutorial を進める

Official Document : https://channels.readthedocs.io/en/latest/

## 環境構築

```sh
$ python -m venv venv-channles
$ venv-channels\Scripts\activate
$ python -m pip install --upgrade pip setuptools
$ python -m pip install django channels
```

## Tutorial 1

### Django プロジェクトを始める

```sh
$ django-admin startproject config .
```

### channels の installation

settings.py へ `channels` の追加

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

`config/routing.py` の追加

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

`config/settings.py` に `ASGI_APPLICATION` を追加

```python
ASGI_APPLICATION = "config.routing.application"
```

### Chat アプリケーションを作成

```sh
$ pyton manage.py startapp chat
```

`config/settings.py` に `chat` を追加

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

`chat/index.html` を編集する

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
    document.querySelector("#room-name-input").onkeyup = function(e) {
        if (e.keyCode === 13) { // enter, return
            document.querySelector('#room-name-submit').click();
        }
    };
    document.querySelector('#room-name-submit').onclick = function(e) {
        var roomName = document.querySelector('#room-name-input').value;
        window.location.pathname = '/chat/' + roomName + '/';
    };
</script>

</html>
```

`#room-name-input` が入力されると `window.location.pathname = '/chat/' + roomName + '/';` によって
ページ URL が変更されることがわかる。すなわち get リクエストが投げられる。

#### URL

`config/urls.py` に `chat` への分岐を追加する。

```python
# confing/settings.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
]
```

`chat/urls.py` を追加する。

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

#### views

`chat/views.py` に `views.index` を追加する

```python
# chat/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html', {})
```

この状態で `python manage.py runserver` をするとどうなるか

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

channels を APP に追加したことで開発用サーバーが ASGI/Channels になった。

## Tutorial 2

### add the room view

`index.html` で `#room-name-submit` を POST したときに room 内に入れるようにしていきたい。

`templates/chat/room.html` を追加する。

```sh
$ type nul > templates\chat\room.html
```

```HTML
<!-- templates\chat\room.html -->
<!DOCTYPE html>
<html lang="ja">

  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>

  <body>
    <textarea id="chat-log" cols="100" rows="20"></textarea><br />
    <input id="chat-message-input" type="text" size="100" /><br />
    <input id="chat-message-submit" type="button" value="Send" /> {{ room_name|json_script:"room-name" }}
  </body>

  <script>
    // Django templateのjson_scriptフィルターについては下記参照
    // https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#json-script
    const roomName = JSON.parse(
      document.getElementById("room-name").textContent
    );

    // WebSocketインスタンスの作成
    const chatSocket = new WebSocket(
      "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
    );

    chatSocket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      document.querySelector("#chat-log").value += data.message + "\n";
    };

    chatSocket.onclose = function(e) {
      console.log("chat socket closed unexpectedly");
    };

    document.querySelector("#chat-message-input").focus();
    document.querySelector("#chat-message-input").onkeyup = function(e) {
      if (e.keyCode === 13) {
        // enter, return
        docuemt.querySelector("#chat-messge-submit").click();
      }
    };

    document.querySelector("#chat-message-submit").onclick = function(e) {
      const messageInputDom = document.querySelector("#chat-message-input");
      const message = messageInputDom.value;
      chatSocket.send(
        JSON.stringify({
          message: message
        })
      );
      messageInputDom.value = "";
    };
  </script>

</html>
```

`room.html`を見ると`room-name`や`chat-message-input`を JSON で受け取っているのがわかる。

`views.room`を追加する。

```Python
# chat/views.py

from django.shortcuts import render

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

```

`room.html`への URL を追加する。

```Python
# chat/urls.py

from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room-name>', views.room, name="room"),
]

```

開発用サーバーを立ち上げて`http://127.0.0.1:8000/chat/`にアクセスする。

room_name に room 名`lobby`を入力してみると、`http://127.0.0.1:8000/chat/lobby`に GET リクエストが投げられ、
`room.html`が表示される。

開発者ツールでネットワークを確認すると、`Request URL`が`http`と`ws`の 2 種類あることがわかる。

- Request URL: http://127.0.0.1:8000/chat/test/
  - Request URL: ws://127.0.0.1:8000/ws/chat/test/

コンソールを確認すると WebSocket の接続ができなかったことがわかる。

```sh
(index):22 WebSocket connection to 'ws://127.0.0.1:8000/ws/chat/test/' failed: Error during WebSocket handshake: net::ERR_CONNECTION_RESET

(index):32 chat socket closed unexpectedly
```

Django 側で WebSocket のハンドシェイクを行うための準備が必要だとわかる。

### Write your first consumer

Channels が WebSocket 接続を受けたとき、Channels の root Configration が*consumer*を探し、
*consumer*が WebSocket 接続時のイベント内容をあれこれする。

`chat/consumer.py`を作成する。

```sh
$ type nul > chat\consumers.py
```

```Python
# chat\consumers.py

import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        print(close_code)
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # 受け取ったmessageをオウム返しする
        self.send(text_data=json.dumps({
            'message': message
        }))

```

`chat/routing.py`を作成する。

```sh
$ type nul > chat\routing.py
```

```Python
# chat\routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer)
]

# ここでre_pathを使う理由がよくわからない
# (Note we use re_path() due to limitations in URLRouter.)
# https://channels.readthedocs.io/en/latest/topics/routing.html#urlrouter

```

`config/routing.py`から`chat/routing.py`に分岐させる処理を追加する。

```Python
# config/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

```

Channels の開発用サーバーに接続が行われると`ProtocolTypeRouter`がどのプロトコルなのかを判定し、
`ws://`や`wss://`から WebSocket だとわかると connection は`AuthMiddlewareStack`が投げられ、
`AuthMiddlewareStack`は接続元の`scope`を認証済みユーザーから参照する。
`scope`を参照した後、connection は`URLRouter`を与えられる。なんのこっちゃ。

ここで migrate しておく。これは Django の session フレームワークがテーブルを必要とするため。
migrateするとsessionテーブルが作成される。

```sh
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying sessions.0001_initial... OK

$ python manage.py runserver

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
March 19, 2020 - 16:59:41
Django version 3.0.4, using settings 'config.settings'
Starting ASGI/Channels version 2.4.0 development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
HTTP GET /chat/ 200 [0.02, 127.0.0.1:62358]
HTTP GET /chat/lobby/ 200 [0.00, 127.0.0.1:62358]
WebSocket HANDSHAKING /ws/chat/lobby/ [127.0.0.1:62363]
WebSocket CONNECT /ws/chat/lobby/ [127.0.0.1:62363]

```

`http://127.0.0.1:8000/chat/`にアクセスしてroom名を`lobby`としてEnterを押すと、
`http://127.0.0.1:8000/chat/lobby/`に遷移され、このタイミングでWebSocketのHANDSHAKING⇒CONNECTが行われたことがわかる。

ただこれは1ユーザー内でのレスポンスとなっているが、これを複数ユーザー間で行うにはどのようにしたらよいのか、
すなわち複数の`ChatConsumer`インスタンスがお互いにやりとりするには、どのようにしたらよいのか。

これを実現するのが*`channel layer`*であり、`channel layer`が複数のcunsumerとのやりとりを可能にする。

### Enable a channel layer

channel layerは複数のconsumerインスタンスがお互いにやりとりをするための仕組みである。

