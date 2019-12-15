# sample/views.py

from django.shortcuts import render


def index(request):
    if request.method == 'GET':
        msg = 'Hello django!'
        params = {
            'msg': msg
        }
        return render(request, 'sample/index.html', params)
