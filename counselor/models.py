from django.db import models
from accounts.models import Account
from home.models import Service

# Create your models here.


class CounselorProfile(models.Model):
    counselor = models.ForeignKey(Account, on_delete=models.CASCADE)
    fee = models.BigIntegerField(default=600)
    specialization = models.ForeignKey(
        Service, null=True, blank=True, on_delete=models.SET_NULL)
    state = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.counselor.first_name


class CounselorEducation(models.Model):
    counselor = models.ForeignKey(Account, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    university = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    certificate = models.ImageField(upload_to='certificates/')
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Counselor's Education"

    def __str__(self):
        return self.qualification


class CounselorExperience(models.Model):
    counselor = models.ForeignKey(Account, on_delete=models.CASCADE)
    institute = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    years_of_experience = models.BigIntegerField(null=True, blank=True)
    months_of_experience = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Counselor's Experience"

    def __str__(self):
        return self.institute
