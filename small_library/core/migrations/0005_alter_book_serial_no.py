# Generated by Django 3.2.8 on 2021-10-10 16:17

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_book_serial_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='serial_no',
            field=models.CharField(default=core.models.Book.token_hex_modified, max_length=50, unique=True, verbose_name='serial'),
        ),
    ]