# Generated by Django 5.1.2 on 2024-10-18 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0004_game_is_calculated_alter_team_api_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
