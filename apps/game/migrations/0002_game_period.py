# Generated by Django 5.1.2 on 2024-10-25 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
        ('ranking', '0002_alter_ranking_options_alter_ranking_period_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='period',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ranking.period'),
            preserve_default=False,
        ),
    ]