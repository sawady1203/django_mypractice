from django.shortcuts import render, redirect
from .models import List
from .forms import ListForm  # 追加
from django.contrib import messages

# Create your views here.


def index(request):
    if request.method == 'GET':
        all_items = List.objects.all()  # テーブルのアイテムを抜き出す.
        params = {
            'all_items': all_items
        }
        return render(request, 'todo_app/index.html', params)


def add(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)

        if form.is_valid():  # validation
            form.save()  # 保存
            print('Validation Clear!')
            all_items = List.objects.all()
            params = {
                'all_items': all_items
            }
            messages.success(request, ('Item has been added to list!'))
            return render(request, 'todo_app/index.html', params)
        else:
            messages.warning(requests, ('Validation faults!'))
            print('Validation faults!')
            print(form.errors)
            all_items = List.objects.all()
            params = {
                'all_items': all_items
            }
            return render(request, 'todo_app/index.html', params)

def delete(request, list_id):
    pass

def cross_off(request, list_id):
    pass

def uncross(request, list_id):
    pass

def edit(request, list_id):
    pass