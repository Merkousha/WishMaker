# Generated by Django 3.2.20 on 2023-10-15 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoalDuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=90)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GoalType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=90)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=90)),
                ('description', models.TextField()),
                ('duration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Organizer.goalduration')),
                ('goal_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Organizer.goaltype')),
            ],
        ),
        migrations.CreateModel(
            name='DailyTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=90)),
                ('description', models.TextField()),
                ('goal', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Organizer.goal')),
            ],
        ),
    ]
