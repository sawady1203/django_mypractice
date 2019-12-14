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
