from django.db import models
from accounts.models import Account
from counselor.models import CounselorAccount

# Create your models here.
class Slots(models.Model):
    slot = models.CharField(max_length=20)
    def __str__(self):
        self.slot

class AppointmentPayments(models.Model):
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    transaction_id = models.CharField()
    amount_paid = models.PositiveBigIntegerField()
    paid_date = models.DateField()

    def __str__(self):
        return self.transaction_id


class Appointments(models.Model):
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    counselor = models.ForeignKey(CounselorAccount, on_delete=models.DO_NOTHING)
    slot = models.ForeignKey(Slots, on_delete=models.DO_NOTHING)
    date = models.DateField()
    payment = models.ForeignKey(AppointmentPayments, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20)
