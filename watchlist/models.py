from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from investment.models import Investment


class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    investment = models.OneToOneField(Investment, on_delete=models.RESTRICT)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Watchlist'
