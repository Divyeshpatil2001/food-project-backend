# Generated by Django 5.0.2 on 2024-04-12 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('razorpay_backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='payment',
            new_name='payment_id',
        ),
    ]
