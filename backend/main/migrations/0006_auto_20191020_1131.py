# Generated by Django 2.2a1 on 2019-10-20 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20191018_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='completed_tasks',
            field=models.ManyToManyField(blank=True, related_name='_profile_completed_tasks_+', to='main.Task'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='todo_tasks',
            field=models.ManyToManyField(blank=True, related_name='_profile_todo_tasks_+', to='main.Task'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='wa_tasks',
            field=models.ManyToManyField(blank=True, related_name='_profile_wa_tasks_+', to='main.Task'),
        ),
    ]
