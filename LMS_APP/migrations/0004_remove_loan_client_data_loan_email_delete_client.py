# Generated by Django 5.1.3 on 2024-11-15 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS_APP', '0003_loan_address_loan_contact_loan_fullname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='client_data',
        ),
        migrations.AddField(
            model_name='loan',
            name='Email',
            field=models.EmailField(default='example@domin.com', max_length=254),
        ),
        migrations.DeleteModel(
            name='Client',
        ),
    ]
