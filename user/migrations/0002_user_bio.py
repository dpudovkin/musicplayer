# Generated by Django 3.2.9 on 2021-11-14 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, default='no info', max_length=300, null=True),
        ),
    ]