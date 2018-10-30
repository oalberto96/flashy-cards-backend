# Generated by Django 2.1.2 on 2018-10-28 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_mediatype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=150)),
                ('audio', models.CharField(max_length=2000)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('media_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lessons.MediaType')),
            ],
        ),
    ]