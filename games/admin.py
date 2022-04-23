from django.contrib import admin
from .models import *

# Register your models here.


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'developer', 'release_date', 'platform')


admin.site.register(Game, GameAdmin)
admin.site.register(Developer)
admin.site.register(Genre)
admin.site.register(Category)
