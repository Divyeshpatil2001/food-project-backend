# Generated by Django 5.0.2 on 2024-04-16 17:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='id',
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]