# Generated by Django 5.0.6 on 2024-06-30 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_doctor_profile_pic_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='booked',
            field=models.BooleanField(default=False),
        ),
    ]
