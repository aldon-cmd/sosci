# Generated by Django 2.2.9 on 2019-12-23 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0007_slugfield_noop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date Created'),
        ),
    ]