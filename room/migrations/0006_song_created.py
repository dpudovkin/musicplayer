# Generated by Django 3.2.9 on 2021-11-16 17:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0005_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='created',
            field=models.TimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]