# DjangoでAjaxをやってみる

仮想環境をつくる

```sh
# 仮想環境の作成
python -m venv venv-ajax
# 仮想環境の有効化
venv-ajax\Script\activate
# 基本モジュールのupgrade
python -m pip install --upgrade pip setuptools
# djangoのインストール
pip install django
```

djagnoプロジェクトを作成する

```sh
django-admin startproject config .
```

settings.pyを変更する
ajaxを実行したいだけなので、本当に基本的な部分だけ。

```python
# config/settings.py

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = os.path.basename(BASE_DIR)  # 追加

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kw%_pswukizbf45#)0yb1knzlgj4u9!2ik3+@0a$s1*n6@4jup'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # 変更


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 変更
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # 追加
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')  # 追加

```

templatesとstaticフォルダを作成する。

```sh
mkdir templates
mkdir static
cd static
mkdir js
cd ../
```

ここでmigrateしておく。

```sh
python manage.py migrate
```

migrateができたのでcommitする。

```sh
git add .
git commit -m "first commit"
```

mainアプリケーションを作成する

```sh
python manage.py startapp main
type nul > main/urls.py
type nul > main/forms.py
```

URLconfを編集してmain/urls.pyへの分岐を作成する。

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
```

mainアプリのurls.pyを作成する。

```python
# main/urls.py
from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax_get/', views.ajax_get, name="ajax_get"),
    path('ajax_post/', views.ajax_post, name="ajax_post"),
]
```

mainアプリのviewsを記述していく。

```python
# main/views.py

from django.shortcuts import render, HttpResponse
import json
# Create your views here.


def index(request):
    # if request.method == 'GET':
    return render(request, 'main/index.html', {})


def ajax_get(request):
    if request.method == 'GET':
        print('request to ajax_get')
        return HttpResponse('ajax_get is done')


def ajax_post(request):
    if request.method == 'POST':
        print('request to ajax_post')
        data = request.body
        data = json.loads(data)
        print(data)
        return HttpResponse('ajax is done in POST!')

```

templatesを作成していく。

```sh
type nul > templates/base.html
mkdir templates/main
type nul > templates/main/index.html
```

```html
<!-- templates/base.html -->

{% load static %}

<!DOCTYPE html>
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>{% block title %}{% endblock title %}</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    </head>
    <body>
        <nav class="navbar navbar-expand-md navbar-dark bg-dark">
            <a class="navbar-brand" href="{% url 'main:index' %}">Ajax Test Page</a>
        </nav>
        <br>
        <div class="container">
            {% block content %}
            {% endblock content %}
        </div>
        <script src="{% static 'js/common.js' %}"></script>
            {% block javascripts %}
            {% endblock javascripts %}
    </body>
</html>
```

base.htmlをextendsした表示画面をindex.htmlとして作成する。

```html
<!-- templates/main/index.html -->

{% extends 'base.html' %}

{% load static %}

{% block title %}
Index
{% endblock title %}

{% block content %}

<form method='GET'>
<h1>This is index page.</h1>

<p id="result"></p>

<button type="submit" id="submit_in_get">Submit In Get</button>
</form>

<form method='POST'>
{% csrf_token %}
<button type="submit" id="submit_in_post">Submit In Post</button>
</form>

{% endblock content %}

{% block javascripts %}
<script src="{% static 'js/django_ajax.js' %}"></script>
{% endblock javascripts %}

```

ここで開発用サーバで確認する。

```sh
python manage.py runserver
```

ajax用のjavascriptを作成する。

ajaxでPOSTをする場合はcookieからcsrftokenを取得する必要がある。
この関数をcommon.jsとして作成する。

```javascript
// common.js
// -- using pure javascript -- //
function parse_cookies() {
    var cookies = {};
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(function (c) {
            var m = c.trim().match(/(\w+)=(.*)/);
            if(m !== undefined) {
                cookies[m[1]] = decodeURIComponent(m[2]);
            }
        });
    }
    return cookies;
}
```

index.htmlに適用するjavascriptをdjango_ajax.jsとして作成する。
今回は素のjavascriptでajaxを実装した。
参考URL：https://qiita.com/soup01/items/f356d6ee09534007f76d

```javascript
// django_ajax.js

console.log('django_ajax.js is start')
var cookies = parse_cookies();
console.log(cookies);
var result = document.getElementById('result');


function submit_in_post() {
    var xhr = new XMLHttpRequest();
    var data = {'user':'index'};
    var json = JSON.stringify(data);
    console.log(json);
    xhr.open('POST', 'ajax_post/');
    xhr.setRequestHeader('X-CSRFToken', cookies['csrftoken']);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4){
            if (xhr.status === 200){
                console.log(post_result);
            }else{
                console.log(xhr.status);
                console.log('submit_in_get is failed...');
            }
        }else{
            console.log('通信中...');
        };
    };
    xhr.send(json);
};

document.getElementById('submit_in_get').addEventListener('click', function(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'ajax_get/');
    xhr.onload = function () {
        if (xhr.readyState === 4){
            if (xhr.status === 200){
                console.log(xhr.responseText);
            }else{
                console.log(xhr.status);
                console.log('submit_in_get is failed...');
            }
        };
    }
    xhr.send(null);
    result.textContent = "get!";
}, false);

document.getElementById('submit_in_post').addEventListener('click',function () {
    result_txt = submit_in_post();
    result.textContent = "clicked...";
});

console.log(result);

```

開発用サーバで確認すると、確かにpostとgetをajaxで送信できているのがわかる。
