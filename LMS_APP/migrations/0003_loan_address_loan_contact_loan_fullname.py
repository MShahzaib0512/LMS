# Generated by Django 5.1.3 on 2024-11-15 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS_APP', '0002_remove_loan_intrest_rate_loan_cnic_loan_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='address',
            field=models.CharField(default='undefined', max_length=250),
        ),
        migrations.AddField(
            model_name='loan',
            name='contact',
            field=models.IntegerField(default='0000'),
        ),
        migrations.AddField(
            model_name='loan',
            name='fullname',
            field=models.CharField(default='undefined', max_length=50),
        ),
    ]
