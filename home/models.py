from django.db import models
from accounts.models import Account
from admin_home.models import PsychologicalTasks
# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='services/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class CallBackReqs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.PositiveBigIntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    

class TaskSubscription(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(PsychologicalTasks, on_delete=models.SET_NULL, null=True)
    amount_paid = models.PositiveBigIntegerField()
    validity = models.PositiveBigIntegerField()
    subscribed_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True)   
    is_paid = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.task.title