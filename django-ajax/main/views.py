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
