from django.urls import path
from . import views

urlpatterns = [
    path("", views.register_domain, name="register-page"),
    path("signup/", views.signup, name="account_signup"),
]

