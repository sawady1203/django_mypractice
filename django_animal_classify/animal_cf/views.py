from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required  # 追加
from django.conf import settings as settings
from .models import AnimalImage
from .forms import AnimalImageForm


@login_required
def index(request):
    if request.method == 'GET':
        msg = '動物の画像を選択してください'
        form = AnimalImageForm
        params = {
            'msg': msg,
            'form': form,
        }
        return render(request, 'animal_cf/index.html', params)
