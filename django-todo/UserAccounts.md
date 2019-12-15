# Djangoでユーザー管理機能を作る

DJANGO FOR BIGINNERSを参照
https://www.amazon.co.jp/dp/B079ZZLRRL/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1

## User Authntication

Djangoではプロジェクトを作成した時点で`auth`アプリができている。
`auth`アプリは`User`オブジェクトを使って作成されている。
Djangoの`User`オブジェクトをつかってユーザー管理機能を作ることができる。

- log in
- log out
- sign up

### Login機能

Djangoはデフォルトのviewを用意してくれている(`LoginView`)。
必要なのはURLの追加とtemplateの追加とsettings.pyの編集。

#### 1. setting.pyの編集

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('todo_app.urls'), name='todo'),  # 変更
]
```

#### 2．templatesの追加

Djagnoはデフォルトで`templates/registration/login.html`を探しに行くので、ディレクトリをつくる必要がある。

```sh
mkdir templates/registration
type nul > templates/registration/login.html
```

```html
<!-- templates/registration/login.html -->
{% extends "base.html" %}

{% load static %}

{% block content %}
    <h2>Log In</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Log in</button>
    </form>
{% endblock content %}
```

ユーザーがログインしたらどこにredirectされるのかを`settings.py`に記述する。

```python
LOGIN_REDIRECT_URL = '/'  # 追加
```

この状態でhttp:127.0.0.1:8000/accounts/login/にアクセスするとログイン画面が表示される
`superuser`アカウントでログインすると、indexページに飛ばされるのが確認できる。

views.pyもモデルも追加せずとも、Djangoの機能だけをつかってログイン機能を実装できる。

#### 3. base.htmlの編集

ログインユーザー名を表示させるため、templates/base.htmlを編集する。
html上でログインしているかどうかの判断は`user.is_authenticate`を使う。

```html
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
        <!-- 追加 -->
        {% if user.is_authenticated %}
            <p class="navbar-brand">Hi, {{ user.username }}</p>
        {% else %}
            <p>you are not logged in.</p>
            <a href="{% url 'login' %}">Log In</a>
        {% endif %}
        <!-- 追加終わり -->
    </nav>
    <br>
    <div class="container">
        {% block content %}
        {% endblock content %}
    </div>
    <script src="{% static 'js/jquery-3.4.1.min.js' %}"></script>
    <script src="{% static 'js/bootstrap.js' %}"></script>
</body>
```

### LogOut機能

base.htmlにログアウトのリンクを追加してログアウト機能を実装する。

```html
{% if user.is_authenticated %}
    <p class="navbar-brand">Hi, {{ user.username }}</p>
    <p><a href="{% url 'logout' %}">Log Out</a></p>
{% else %}
    <p>you are not logged in.</p>
    <a href="{% url 'login' %}">Log In</a>
{% endif %}
```

あとはloginとlogoutの機能はdjangoが用意してくれているので、リダイレクト先を指定する。
ログイン時と同じようにログアウトのリダイレクト先もsettigs.pyで指定する。

```python
# config/settings.py

LOGIN_REDIRECT_URL = '/'  # 追加
LOGOUT_REDIRECT_URL = '/accounts/login'  # 追加
```

ログインしたらIndexページ、ログアウトしたらログインページへ飛ばされるようになった。

### Sign Up機能

sign up機能については自分でviewを書く必要があるが、DjangoのUserCreationFromを使うとより簡単にできる。

UserCreationFormのデフォルトはusername, password1, password2。

ユーザー管理機能を最適化するため、`accounts`アプリを作成する。

```sh
python manage.py startapp accounts
```

pathを追加する。

```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # 追加
    path('accounts/', include('accounts.urls')),  # 追加
    path('', include('todo_app.urls')),
]
```

login, logout機能は`django.contrib.auth.urls`を参照しにいくため、pathの順番に気を付けること。

accounts/urls.pyを作成する。

```python
# accounts/urls.py
from django.urls import path

from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
```

続いてaccounts/views.pyにサインアップ機能を実装する。

```python
# accounts/views.py

from django.contrib.auth.form import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # redirectさせる
    template_name = 'accounts/signup.html'
```

ここでreverse_lazyをつかってredirectさせている理由は。generic クラスベースのviewはファイルがimportされた時点ではURLsがimportされておらず、reverse先にurlを指定してもうまくいかない？

templates/accounts/signup.htmlを作成する。

```html
<!-- templates/accounts/signup.html -->
{% extends "base.html" %}

{% load static %}

{% block content %}
    <h2>Sign Up</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Sign Up</button>
    </form>
{% endblock content %}
```

これでhttp://127.0.0.1:8000/accounts/signup/にアクセスするとsignup画面が確認できるようになった。

ここでcommitしておく。

## Custom User Modelを使う

DjangoのBuild-inのUserモデルを利用しても良いが、ユーザー情報を追加した場合はUserモデルを更新するのはマジで大変らしい。

公式で紹介されている`AbstractBaseUser`はあんまりおススメされていないため、ここではよりカスタマイズしやすい`AbstractUser`を作成してみる。

**カスタムユーザーモデルの作成手順**

1. settings.pyの更新
2. CustomUser modelの作成3
3. UserCreationFormとUserChangeFormの作成
4. users/admin.pyの更新

### 1. settings.pyの更新

認証用のユーザーモデルはカスタムモデルを使用することを宣言する。
accountsアプリにカスタムユーザーモデルを作成して、利用する形を取る。

```python
# config/settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'  # 追加
```
models.pyにAbstractUserを継承したカスタムユーザーモデルを作成する。

```python 
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIngerField(null=True, blank=True)
```

accounts/forms.pyを作成して入力用のフォームやvalidationに使用する。
このformはユーザーがサインアップのためにも使用し、管理者が既存のユーザーを操作したいときに使用する。

```python
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('age',)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields

```

UserCreationFormを継承して、使用するfieldsにはカスタムモデルの'age'を追加した。

続いてaccounts/admin.pyを更新する。CustomUserモデルを使うためにAccountsAdminモデルを作成する。

```python
# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
```

カスタムユーザーモデルをテーブルに反映させるため、makemigraionsを行う

```sh
python manage.py makemigrations acconts
python manage.py migrate
```