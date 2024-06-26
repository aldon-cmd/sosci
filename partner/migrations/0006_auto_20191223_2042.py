# Generated by Django 2.2.9 on 2019-12-24 01:42

from django.db import migrations

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Partner = apps.get_model("partner", "Partner")
    db_alias = schema_editor.connection.alias
    Partner.objects.using(db_alias).bulk_create([
        Partner(code="nesberry",name="Nesberry"),
    ])

def reverse_func(apps, schema_editor):
    # forwards_func() creates two Country instances,
    # so reverse_func() should delete them.
    Partner = apps.get_model("partner", "Partner")
    db_alias = schema_editor.connection.alias
    Partner.objects.using(db_alias).filter(code="nesberry").delete()
class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0005_auto_20181115_1953'),
    ]

    operations = [
    migrations.RunPython(forwards_func, reverse_func),
    ]