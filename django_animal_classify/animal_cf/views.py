from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required  # 追加
from django.conf import settings as settings


@login_required
def index(request):
    if request.method == 'GET':
        msg = '動物の画像を洗濯してください'
        params = {
            'msg': msg
        }
        return render(request, 'animal_cf/index.html', params)
