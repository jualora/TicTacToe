# Generated by Django 3.2.9 on 2022-11-24 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tttApp', '0006_alter_user_actual_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='actual_game',
            field=models.CharField(blank=True, default=' ', max_length=50),
        ),
    ]
