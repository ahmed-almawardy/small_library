# Generated by Django 3.2.8 on 2021-10-09 11:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import secrets


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('phone', models.CharField(max_length=20, unique=True, verbose_name='phone')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('phone', models.CharField(max_length=20, unique=True, verbose_name='phone')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='book title')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime, verbose_name='created at')),
                ('serial_no', models.CharField(default=secrets.randbelow, max_length=50, verbose_name='serial')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='core.author', verbose_name='author')),
                ('readers', models.ManyToManyField(related_name='books', to='core.Reader', verbose_name='reader')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
