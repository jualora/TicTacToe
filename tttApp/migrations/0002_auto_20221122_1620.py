# Generated by Django 3.2.9 on 2022-11-22 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tttApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='finished',
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
