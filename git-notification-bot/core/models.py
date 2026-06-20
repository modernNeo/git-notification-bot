from django.db import models


class ClientConfig(models.Model):
    messaging_service = models.CharField(
        null=True,
        blank=True
    )
    git_hosting_service = models.CharField(
        null=True,
        blank=True
    )
