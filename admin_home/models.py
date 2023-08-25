from django.db import models
from accounts.models import Account

# Create your models here.


class RandomTokenGenerator(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token


class PsychologicalTasks(models.Model):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='psy_tasks/')
    description = models.TextField()
    amount = models.PositiveBigIntegerField(default=699)
    validity = models.PositiveBigIntegerField(default=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class TaskItems(models.Model):
    task = models.ForeignKey(PsychologicalTasks, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,unique=True)
    instructions = models.TextField()
    demo_link = models.URLField(null=True)

    def __str__(self) -> str:
        return self.title




