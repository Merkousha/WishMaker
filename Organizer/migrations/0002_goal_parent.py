# Generated by Django 3.2.20 on 2023-10-15 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Organizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='Organizer.goal'),
        ),
    ]
