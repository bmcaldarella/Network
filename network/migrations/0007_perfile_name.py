# Generated by Django 4.1 on 2023-04-12 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_perfile_biography'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfile',
            name='name',
            field=models.CharField(default=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL), max_length=50),
        ),
    ]
