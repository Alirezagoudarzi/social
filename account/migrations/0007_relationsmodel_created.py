# Generated by Django 5.1 on 2024-09-04 19:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='relationsmodel',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
