from django.db import models
from accounts.models import Account
from counselor.models import CounselorAccount

# Create your models here.


class TimeSlots(models.Model):
    counselor = models.ForeignKey(CounselorAccount, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.start)


class AppointmentPayments(models.Model):
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    transaction_id = models.CharField()
    amount_paid = models.PositiveBigIntegerField()
    paid_date = models.DateField()

    def __str__(self):
        return self.transaction_id


class Appointments(models.Model):
    STATUS_CHOICES = (
        ('Attended', 'Attended'),
        ('Not attended', 'Not attended'),
        ('Pending', 'Pending')
    )
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    counselor = models.ForeignKey(
        CounselorAccount, on_delete=models.DO_NOTHING)
    slot = models.ForeignKey(TimeSlots, on_delete=models.DO_NOTHING)
    session_date = models.DateField()
    amount_paid = models.PositiveBigIntegerField(default=200)
    is_paid = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, default='Pending', choices=STATUS_CHOICES)
