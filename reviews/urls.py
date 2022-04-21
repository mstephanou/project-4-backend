from django.urls import path # Import path function from django
from .views import * 

urlpatterns = [
    path('create/', ReviewCreate.as_view()),
]