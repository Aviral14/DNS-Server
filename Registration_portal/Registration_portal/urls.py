"""Registration_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from importlib import import_module
from django.contrib import admin
from django.urls import path, include
from allauth.account.views import LoginView, LogoutView
from allauth.socialaccount import providers


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="account-login"),
    path("", LoginView.as_view(), name="home"),
    path("logout/", LogoutView.as_view(), name="account-logout"),
    path("social/", include("allauth.socialaccount.urls")),
    path("registration/", include("registration.urls"), name="registration"),
]


# for django-allauth
# Provider urlpatterns, as separate attribute (for reusability).
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns
