from django.contrib import admin
from .models import List


class ListAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'item',
        'completed',
    ]
    list_editable = [
        'item',
        'completed',
    ]


admin.site.register(List,ListAdmin)