from django.db import models
from django.utils.translation import gettext as _


class PostAccessToken(models.Model):
    token = models.CharField(max_length=4000)
    expires = models.DateTimeField()

    class Meta:
        verbose_name = _('Post access token')
        verbose_name_plural = _('Post access tokens')
