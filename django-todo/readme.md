# Django ToDo App

## Djangoのプロジェクト開始時に最初にやること

0. Githubにレポジトリを作成する。
    - .gitignoreはPythonを選択する。

1. ローカルにプロジェクトディレクトリを作成してgit pull

    ```sh
    mkdir django-todo
    git remote add origin [URL]
    git pull origin master
    ```

    ローカルに.gitignoreやREADME.mdがpullされたことを確認する。

2. 仮想環境の構築

    ```sh
    # 仮想環境の作成
    # python -m venv [仮想環境名]
    python -m venv venv
    # 仮想環境に入る
    venv\Script\activate
    ```

3. djangoのインストール
    LTSバージョンを指定してインストール

    ```sh
    pip insatll django==2.2
    ```

4. プロジェクトを開始する

    ```sh
    django-admin startproject config .
    ```

    こうすることで現状のフォルダ直下にプロジェクトのフォルダが作成される。

5. settings.pyの編集
    githubに上げたくないSECRET_KEYなどを.envファイルにまとめて管理する。そのためにはpython-dotenvを利用する。

    ```sh
    # python-dotenvをインスール
    pip install python-dotenv
    # .envの作成
    type nul > .env
    # templatesフォルダの作成
    mkdir templates
    ```

    プロジェクトの直下に.envファイルが作成される。
    プロジェクトの直下にtemplatesフォルダが作成される。  

    setting.pyを編集する。

    ```python
    import os
    from dotenv import load_dotenv  # 追加


    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_NAME = os.path.basename(BASE_DIR)

    # .envの読み込み
    load_dotenv(os.path.join(BASE_DIR, '.env'))  # 追加

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '!izlmnzr&3tmywtcu9)1tb++x1-)1cjr^cmnpq=z+&&fn(2mt=' # 削除して.envファイルへ
    SECRET_KEY = os.getenv('SECRET_KEY') # 変更

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = ['*'] # 変更

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
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
    # https://docs.djangoproject.com/en/2.2/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/2.2/topics/i18n/

    LANGUAGE_CODE = 'ja'

    TIME_ZONE = 'Asia/Tokyo'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.2/howto/static-files/

    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # 追加
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')  # 追加

    MEDIA_URL = '/media/'  # 追加
    ```

    .envファイルにSECRET_KEYを記述する。

    ```sh
    SECRET_KEY = '!izlmnzr&3tmywtcu9)1tb++x1-)1cjr^cmnpq=z+&&fn(2mt='
    ```

    djangoの開発用サーバーが起動するか確認する。

    ```sh
    python manage.py runserver
    ```

    ロケットが確認されればOK.
    .envにsecret_keyが登録され、.gitignoreで.envはプッシュされない設定になっている。
    この状態でコミットしておく。

    ```sh
    git add .
    git commit -m "first commit"
    git push origin master
    ```

6. マイグレーションを行う。

    ```sh
    python manage.py makemigrations # No changes
    python manage.py migrate
    ```

    migrateしたことで管理用ユーザー用のテーブルがsettings.pyのdefaultで登録したデータベースに作成された。
    python manage.py makemigrationsをしたタイミングで必ずコミットしておく。

    ```sh
    git add .
    git commit -m "first migrate"
    ```

7. 管理ユーザーを作成する。
   管理ユーザーを登録して管理画面にログインする。

    ```sh
    # 管理者ユーザーIDとパスワードを入力する。
    # パスワードは表示されない。
    # マイグレーションをせずに行うとエラーが発生する。
    python manage.py createsuperuser
    ```

    開発用サーバーを起動してhttp://127.0.0.1:8000/adminにアクセスする。

    ```sh
    python manage.py runserver
    ```

    createsuperuserで作成したIDとパスワードで管理用画面にログインできればOK。

## Todoアプリを作っていく

1. アプリケーションフォルダをつくる

    ```sh
    python manage.py startapp todo_app
    git add .
    git commit -m "startapp todo_app"
    ```

2. 作成したアプリケーションをsettigs.pyに登録する。

    ```python
    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'todo_app'  # 追加
    ]
    ```

3. todo_appにurl.pyを作成する。

    ```sh
    type nul > todo_app/urls.py
    ```

    config内のurls.pyにtodo_app/urls.pyへの分岐を追加する。

    ```python
    # config/urls.py

    from django.contrib import admin
    from django.urls import path, include # includeを追加

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('todo_app.urls')),  # 追加
    ]

    ```

    作成したtodo_app/urls.pyにviewへの分岐を記述する。

    ```python
    # todo_app/urls.py

    from django.urls import path
    from . import views  # 追加

    app_name = "todo_app"  # 追加

    urlpatterns = [
        path('', views.index, name='index'),  # 追加
    ]
    ```

    ここで開発用サーバーを起動してみるが、下記エラーがでる。

    ```sh
    AttributeError: module 'todo_app.views' has no attribute 'index'
    ```

    まだtodo_app/views.indexを記述していないため。後で書く。
    ここでコミット。

    ```sh
    git add .
    git commit -m "todo_app/urls.py作成"
    ```

4. Todoアプリに必要なテーブルを作成する。
    todo_app/models.pyにテーブル構成を記述。
    マイグレーションファイルを作成し、マイグレイトする。

    ```python
    # todo_app/models.py
    from django.db import models

    # Create your models here.


    class List(models.Model):

        # item名
        item = models.CharField(
            max_length=200
            )

        # 完了かどうか
        completed = models.BooleanField(
            default=False
            )

        def __str__(self):
            return self.item + '|' + str(self.completed)
    ```

    models.pyに記述した内容をテーブルとして作成する

    ```sh
    python manage.py makemigrations todo_app
    > Migrations for 'todo_app':
       todo_app\migrations\0001_initial.py
         - Create model List
    # テーブルの変更内容を記述したファイルが作成される。
    # これを元にテーブルが更新される

    # マイグレーションに失敗するとつらいので、migrationファイルを作成したら必ずコミットする。
    git add .
    git commit -m "makemigrations todo_app/List"

    # マイグレーションしてテーブルを作成する
    python manage.py migrate
        Operations to perform:
            Apply all migrations: admin, auth, contenttypes, sessions, todo_app
        Running migrations:
            Applying todo_app.0001_initial... OK

    git add .
    git commit -m "migrate done todo_app/List"
    ```

    これでデータの追加ができるようになった。

5. views.pyを記述していく
    アプリケーションに必要な機能に合わせてviewを記述する。
    **■Todoアプリに必要な機能**
    - todoの一覧表示(index)
    - todoの登録(add)
    - todoの削除(delete)
    - todoの完了(cross_off)
    - todoの完了取り消し(uncross)
    - todoの編集(edit)
    これらを作っていく。
    まずはindexをつくる。

    ```python
    # todo_app/views.py
    
    from django.shortcuts import render, redirect  # 追加
    from .models import List

    # Create your views here.


    def index(request):
        if request.method == 'GET':
            all_items = List.objects.all()  # テーブルのアイテムを抜き出す.
            params = {
                'items': all_items
            }
            return render(request, 'todo_app/index.html', params)
    ```

    これで開発用サーバーを起動すると

    ```
    django.template.exceptions.TemplateDoesNotExist: todo_app/index.html
    ```

    となる。
    表示するhtmlを作成する。
6. 一覧画面を作成する
    フロント側をつくっていく。

    ```sh
    mkdir static
    cd static
    mkdir css
    mkdir js
    mkdir ../ # 元のプロジェクト下に戻る
    ```

    bootstrapのファイルをダウンロードしてstatic/css, static/js下に入れる。
    templates/base.htmlを作成してcss, jsを読み込ませる。
    templates/todo_app/index.htmlを作成してbase.htmlをextendsして記述内容を分割する。
    views.py/index はアイテムを全て集めてindex.htmlに投げる。

    ```python
    # todo_app/views.py
    from django.shortcuts import render, redirect  # 追加
    from .models import List

    # Create your views here.


    def index(request):
        if request.method == 'GET':
            all_items = List.objects.all()  # テーブルのアイテムを抜き出す.
            params = {
                'all_items': all_items
            }
            return render(request, 'todo_app/index.html', params)
    ```

    templates/base.htmlはこんな感じ。

    ```html
    {% load static %}

    <!DOCTYPE html>
        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>ToDo</title>
            <meta name="description" content="">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link rel="stylesheet" type="text/css" href="{% static 'css/bootstrap.css' %}">
            <link rel="stylesheet" type="text/css" href="{% static 'css/main.css' %}">
        </head>
        <body>
            <nav class="navbar navbar-expand-md navbar-dark bg-dark">
                <a class="navbar-brand" href="{% url 'todo_app:index' %}">Todo APP</a>
                <button type="button" class="navbar-toggler" data-toggle="collapse" data-target="#Navber" aria-controls="Navber" aria-expanded="false" aria-label="ナビゲーションの切替">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarsExampleDefault">
                    <form class="form-inline my-2 my-lg-0" action="{% url 'todo_app:add' %}" method="POST">
                        {% csrf_token %}
                        <input class="form-control mr-sm-2" type="text" placeholder="New Item" aria-label="ADD" name='item'>
                        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Add</button>
                    </form>
                </div>
            </nav>
            <br>
            <div class="container">
                {% block content %}
                {% endblock content %}
            </div>
            <script src="{% static 'js/jquery-3.4.1.min.js' %}"></script>
            <script src="{% static 'js/bootstrap.js' %}"></script>
        </body>
    </html>
    ```

    templates/todo_app/index.htmlはこんな感じ。

    ```html
    {% extends "base.html" %}

    {% load static %}

    {% block content %}
        {% if all_items %}
        <table class="table table-bordered">
            {% for things in all_items %}
                {% if things.completed %}
                    <tr class="table-secondary">
                        <td class="striker"><a href="{% url 'todo_app:edit' things.id %}">{{ things.item }}</a></td>
                        <td class="text-center"><a href="{% url 'todo_app:uncross' things.id %}">元に戻す</a></td>
                        <td class="text-center"><a href="{% url 'todo_app:delete' things.id %}">削除</a></td>
                    </tr>
                {% else %}
                    <tr>
                        <td><a href="{% url 'todo_app:edit' things.id %}">{{things.item}}</a></td>
                        <td class="text-center"><a href="{% url 'todo_app:cross_off' things.id %}">完了</a></td>
                        <td class="text-center"><a href="{% url 'todo_app:delete' things.id %}">削除</a></td>
                    </tr>
                {% endif %}
            {% endfor %}
        </table>
        {% else %}
        <h2>No item!</h2>
        {% endif %}
    {% endblock content %}
    ```

    main.cssを作成して文字に取り消し線をつける

    ```css
    .striker {
        text-decoration: line-through;
    }
    ```

    フロントはこれだけで済まし、view.pyに処理を追加していく。

7. formの作成
    入力のvalidationを行うため、formを使ったvalidationを行う。
    todo_app/forms.pyを作成する。

    ```python
    # todo_app/forms.py

    from django import forms
    from .models import List


    class ListForm(forms.ModelForm):

        class Meta:
            model = List
            fields = ['item', 'completed']
    ```

8. addの作成
    forms.pyを使って入力値のvalidationを行い、OKなら追加、NGなら警告を出す。

    ```python
    # todo_app/views.py

    def add(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)

        if form.is_valid():  # validation
            form.save()  # 保存
            print('Validation Clear!')
            all_items = List.objects.all()
            params = {
                'all_items': all_items
            }
            messages.success(request, ('Item has been added to list!'))
            return render(requests, 'todo/index.html', params)
        else:
            messages.warning(requests, ('Validation faults!'))
            print('Validation faults!')
            print(form.errors)
            all_items = List.objects.all()
            params = {
                'all_items': all_items
            }
            return render(request, 'todo/index.html', params)
    ```
9. delete, cross_off, uncross, editの作成
    対象となるitemのidをキーにしてデータを引っ張り、消去、編集をする

    ```python
    # todo_app/views.py


    def delete(request, list_id):
        item = List.objects.get(id=list_id)
        item.delete()  # 消去
        messages.success(request, ('Item Has Been Deleted!'))
        return redirect('todo_app:index')


    def cross_off(request, list_id):
        item = List.objects.get(id=list_id)
        item.completed = True
        item.save()
        return redirect('todo_app:index')


    def uncross(request, list_id):
        item = List.objects.get(id=list_id)
        item.completed = False
        item.save()
        return redirect('todo_app:index')


    def edit(request, list_id):
        if request.method == 'GET':
            item = List.objects.get(id=list_id)
            params = {
                'item': item,
            }
            return render(request, 'todo_app/edit.html', params)
        else:
            item = List.objects.get(id=list_id)
            form = ListForm(request.POST or None, instance=item)

            if form.is_valid():
                form.save()
                messages.success(request, ('Item has Been Edited!'))
                return redirect('todo_app:index')
            else:
                messages.warning(request, ('validation faults!'))
                print('edit validation faults!')
                print(form.errors)
                return redirect('todo_app:index')
    ```

    これでTODOアプリができた。
    お疲れ様でした。
