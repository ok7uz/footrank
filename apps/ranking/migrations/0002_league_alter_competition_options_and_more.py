# Generated by Django 5.1.2 on 2024-10-16 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'League',
                'verbose_name_plural': 'Leagues',
                'db_table': 'leagues',
                'ordering': ('name',),
            },
        ),
        migrations.RunSQL('''
            INSERT INTO leagues (name) VALUES ('Champions League');
            INSERT INTO leagues (name) VALUES ('Europa League');
            INSERT INTO leagues (name) VALUES ('Copa del Rey');
        '''),
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ('-coefficient', 'league', 'round'), 'verbose_name': 'Competition', 'verbose_name_plural': 'Competitions'},
        ),
        migrations.RemoveField(
            model_name='competition',
            name='name',
        ),
        migrations.AddField(
            model_name='competition',
            name='round',
            field=models.CharField(default='Round 3 - 4', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='api_id',
            field=models.PositiveIntegerField(db_index=True, null=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='game',
            unique_together={('home_team', 'away_team', 'date')},
        ),
        migrations.AddField(
            model_name='competition',
            name='league',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ranking.league'),
            preserve_default=False,
        ),
    ]