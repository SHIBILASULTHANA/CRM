# Generated by Django 5.0.1 on 2024-02-28 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office_time', models.TimeField(default='09:30')),
                ('late_time', models.TimeField(default='09:40')),
                ('end_time', models.TimeField(default='18:00')),
            ],
        ),
    ]
