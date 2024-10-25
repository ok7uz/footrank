# Generated by Django 5.1.2 on 2024-10-25 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=255, unique=True)),
                ('country_code', models.CharField(max_length=3, primary_key=True, serialize=False, unique=True)),
                ('flag_url', models.URLField(verbose_name='Flag URL')),
                ('confederation', models.CharField(choices=[('UEFA', 'UEFA'), ('AFC', 'AFC'), ('OFC', 'OFC'), ('CONMEBOL', 'CONMEBOL'), ('CAF', 'CAF'), ('CONCACAF', 'CONCACAF')], db_index=True, max_length=10)),
                ('api_id', models.PositiveIntegerField(db_index=True, null=True, unique=True, verbose_name='API ID')),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
                'db_table': 'teams',
                'ordering': ('name',),
            },
        ),
    ]