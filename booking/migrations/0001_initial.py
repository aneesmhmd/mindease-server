# Generated by Django 4.2.3 on 2023-08-09 07:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('counselor', '0013_counseloraccount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField()),
                ('amount_paid', models.PositiveBigIntegerField()),
                ('paid_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(max_length=20)),
                ('counselor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='counselor.counseloraccount')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='booking.appointmentpayments')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='booking.slots')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]