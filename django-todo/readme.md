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
    python manage.py makemigration
    pytho
    ```

7. 管理ユーザーを作成する。
   管理ユーザーを登録して管理画面にログインする。 
    ```sh
    python manage.py createsuperuser   
    ```
    マイグレーションをせずに行うとエラーが発生する。
    まずは