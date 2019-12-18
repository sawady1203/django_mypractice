from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # 追加
# Create your views here.


@login_required
def index(request):
    if request.method == 'GET':
        msg = 'This is animal classification page.'
        params = {
            'msg': msg
        }
        return render(request, 'animal_cf/index.html', params)
