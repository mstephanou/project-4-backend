from django.urls import path # Import path function from django
from .views import * # Import all views

urlpatterns = [

    # Class-based views for registration and login
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('credentials/', CredentialsView.as_view()),
]