from django.db import models
from accounts.models import Account
from counselor.models import CounselorAccount
import datetime

# Create your models here.


class TimeSlots(models.Model):
    counselor = models.ForeignKey(CounselorAccount, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField(null=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.start)

    def save(self, *args, **kwargs):
        if self.start and not self.end:
            duration = datetime.timedelta(hours=1)
            self.end = (datetime.datetime.combine(
                datetime.date.min, self.start) + duration).time()

        super(TimeSlots, self).save(*args, **kwargs)


class AppointmentPayments(models.Model):
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    transaction_id = models.CharField(max_length=255)
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
    amount_paid = models.PositiveBigIntegerField(null=True)
    is_paid = models.BooleanField(default=False)
    is_rescheduled = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, default='Pending', choices=STATUS_CHOICES)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class MeetLink(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointments, on_delete=models.CASCADE)
    link = models.CharField(max_length=100)

    def __str__(self):
        return str(self.link)