from django.db import models
from django.contrib.auth import get_user_model


class Domain(models.Model):
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registerer")
    domain = models.TextField(null=False, blank=False)
    ip = models.IPAddressField(null=False, blank=False)
    registered_at = models.DateTimeField(auto_now_add=True)

