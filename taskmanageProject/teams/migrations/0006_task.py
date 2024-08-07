# Generated by Django 5.0.6 on 2024-07-04 03:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_team_like_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='할일 제목')),
                ('deadline', models.DateTimeField(verbose_name='할일 기한')),
                ('finished', models.BooleanField(default=False)),
                ('manager', models.ManyToManyField(related_name='manager', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
            ],
        ),
    ]
