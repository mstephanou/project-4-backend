from django.contrib import admin
from .models import Review
# Register your models here.
# Allows admin to access Reviews
admin.site.register(Review)