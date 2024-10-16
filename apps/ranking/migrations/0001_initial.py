# Generated by Django 5.1.2 on 2024-10-16 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('coefficient', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Competition',
                'verbose_name_plural': 'Competitions',
                'db_table': 'competitions',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'verbose_name': 'Period',
                'verbose_name_plural': 'Periods',
                'db_table': 'periods',
                'ordering': ('start_date',),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=255, unique=True)),
                ('country_code', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
                ('flag_url', models.URLField()),
                ('current_rank', models.PositiveIntegerField(db_index=True, null=True)),
                ('previous_rank', models.PositiveIntegerField(db_index=True, null=True)),
                ('current_points', models.DecimalField(decimal_places=5, max_digits=10)),
                ('previous_points', models.DecimalField(decimal_places=5, max_digits=10)),
                ('confederation', models.CharField(choices=[('UEFA', 'UEFA'), ('AFC', 'AFC'), ('OFC', 'OFC'), ('CONMEBOL', 'CONMEBOL'), ('CAF', 'CAF'), ('CONCACAF', 'CONCACAF'), ('N/A', 'Not Applicable')], db_index=True, default='N/A', max_length=10)),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
                'db_table': 'teams',
                'ordering': ('current_rank',),
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_knockout', models.BooleanField(default=False)),
                ('home_goals', models.PositiveIntegerField()),
                ('away_goals', models.PositiveIntegerField()),
                ('home_points_change', models.DecimalField(decimal_places=5, default=0, max_digits=10)),
                ('away_points_change', models.DecimalField(decimal_places=5, default=0, max_digits=10)),
                ('date', models.DateField()),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranking.competition')),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_games', to='ranking.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_games', to='ranking.team')),
            ],
            options={
                'verbose_name': 'Game',
                'verbose_name_plural': 'Games',
                'db_table': 'games',
                'ordering': ('-date',),
            },
        ),
    ]