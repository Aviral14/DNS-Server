"""
Custom Adapter For Validatios before Social Login
"""

from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom Adapter for checking email domain before login."""

    def pre_social_login(self, request, sociallogin):
        user_obj = sociallogin.user
        user_obj.username = user_obj.email.split("@")[0]
        if user_obj.email.split("@")[1] not in settings.ALLOWED_DOMAINS:
            messages.error(
                request, "Please login through bits-mail or contact the administrator."
            )
            raise ImmediateHttpResponse(redirect("account-login"))

    def authentication_error(
        self, request, provider_id, error=None, exception=None, extra_context=None
    ):
        if not request.user.is_anonymous:
            messages.error(
                request,
                (
                    f"You are already logged in as {request.user.username}. "
                    "Please logout first to login as another user"
                ),
            )
            raise ImmediateHttpResponse(redirect("home"))
