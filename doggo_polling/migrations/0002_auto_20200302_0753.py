# Generated by Django 3.0.2 on 2020-03-02 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doggo_polling', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='doggo',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.DeleteModel(
            name='Doggo',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
