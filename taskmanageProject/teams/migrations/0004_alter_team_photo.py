# Generated by Django 5.0.6 on 2024-07-02 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_team_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='photo',
            field=models.ImageField(blank=True, default='team_photo/default_photo.jpg', null=True, upload_to='team_photo', verbose_name='팀이미지'),
        ),
    ]
