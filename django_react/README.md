# Django Rest with Rect: Django and React Together tutorial
https://www.valentinog.com/blog/drf/

DjangoとReactの組合せパターン

1. Djangoのアプリケーション`frontend`内でReactを組込む(難しさ: medium)
2. スタンドアロンAPIとしてのDjango RESTとスタンドアロンSPAとしてのReact(難しさ: hard, 特にJWT周り)
3. Djangoテンプレートの内に小さくReactを利用する(難しさ: simple, 長期的にはメンテナンスが大変)

ユーザー認証まわりを簡単に進めるならReactとDjangoは近い位置に設置した方が良い。

今回は[1.]で進める。

