# Generated by Django 3.2.9 on 2022-11-24 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tttApp', '0005_remove_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='actual_game',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
