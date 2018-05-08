from django.contrib import admin
from .models import *

class CommentAdmin(admin.ModelAdmin):
    list_display = ['text','create_time']


admin.site.register(Comment, CommentAdmin)


