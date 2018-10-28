# Generated by Django 2.1.2 on 2018-10-28 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0005_lesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('card_a', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='card_a', to='lessons.Card')),
                ('card_b', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='card_b', to='lessons.Card')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.Lesson')),
            ],
        ),
    ]
