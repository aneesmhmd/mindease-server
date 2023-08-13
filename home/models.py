from django.db import models

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
