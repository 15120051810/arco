# Generated by Django 5.0.7 on 2025-01-07 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_orgs'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorg',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='users.userorg'),
        ),
    ]
