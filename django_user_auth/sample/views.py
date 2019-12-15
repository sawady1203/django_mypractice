# sample/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # 追加

@login_required  # 追加
def index(request):
    if request.method == 'GET':
        msg = 'Hello django!'
        params = {
            'msg': msg
        }
        return render(request, 'sample/index.html', params)
