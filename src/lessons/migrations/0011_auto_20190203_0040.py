# Generated by Django 2.1.2 on 2019-02-03 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0010_trainingscore_trainingscoreconcept'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trainingscoreconcept',
            old_name='score',
            new_name='mistakes',
        ),
    ]
