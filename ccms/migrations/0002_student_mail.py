# Generated by Django 2.0.3 on 2019-05-19 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='mail',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
    ]
