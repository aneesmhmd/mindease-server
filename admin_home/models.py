from django.db import models
from accounts.models import Account

# Create your models here.

class RandomTokenGenerator(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token