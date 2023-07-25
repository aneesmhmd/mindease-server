from django.db import models

# Create your models here.

class Service(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='services')
    is_active = models.BooleanField(default=True)
 
    def __str__(self):
        return self.title

