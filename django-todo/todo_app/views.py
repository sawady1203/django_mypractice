from django.shortcuts import render, redirect
from .models import List
from .forms import ListForm  # 追加
from django.contrib import messages

# Create your views here.


def index(request):
    if request.method == 'GET':
        all_items = List.objects.all()  # テーブルのアイテムを抜き出す.
        params = {
            'all_items': all_items,
        }
        return render(request, 'todo_app/index.html', params)


def add(request):
    print(request.method)
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
            messages.warning(request, ('Validation faults!'))
            print('Validation faults!')
            print(form.errors)
            return redirect('todo_app:index')
    else:
        return redirect('todo_app:index')


def delete(request, list_id):
    item = List.objects.get(id=list_id)
    item.delete()  # 消去
    messages.success(request, ('Item Has Been Deleted!'))
    return redirect('todo_app:index')


def cross_off(request, list_id):
    item = List.objects.get(id=list_id)
    item.completed = True
    item.save()
    return redirect('todo_app:index')


def uncross(request, list_id):
    item = List.objects.get(id=list_id)
    item.completed = False
    item.save()
    return redirect('todo_app:index')


def edit(request, list_id):
    if request.method == 'GET':
        item = List.objects.get(id=list_id)
        params = {
            'item': item,
        }
        return render(request, 'todo_app/edit.html', params)
    else:
        item = List.objects.get(id=list_id)
        form = ListForm(request.POST or None, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, ('Item has Been Edited!'))
            return redirect('todo_app:index')
        else:
            messages.warning(request, ('validation faults!'))
            print('edit validation faults!')
            print(form.errors)
            return redirect('todo_app:index')
