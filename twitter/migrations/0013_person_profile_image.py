# Generated by Django 5.0.6 on 2024-08-28 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0012_person_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='profile_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]