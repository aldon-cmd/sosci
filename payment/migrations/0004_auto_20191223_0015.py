# Generated by Django 2.2.9 on 2019-12-23 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20160323_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date Created'),
        ),
    ]
