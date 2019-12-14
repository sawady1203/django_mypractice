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
        ```
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
    
    python manage.py migrate

    ```

5. views.pyを記述していく
    アプリケーションに必要な機能に合わせてviewを記述する。
    **■Todoアプリに必要な機能**
    - todoの一覧表示(index)
    - todoの登録(add)
    - todoの削除(delete)
    - todoの完了(cross_off)
    - todoの完了取り消し(uncross)
    - todoの編集(edit)
    