# Generated by Django 3.2.8 on 2022-01-14 21:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0005_auto_20220110_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255, verbose_name='First Name')),
                ('lastname', models.CharField(max_length=255, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
            ],
            options={
                'verbose_name': 'Contact Form',
                'db_table': 'contact_form',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='GuessTheTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255, verbose_name='First Name')),
                ('lastname', models.CharField(max_length=255, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('theme', models.TextField(blank=True, null=True, verbose_name='Theme')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation Date')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='EventTheme', to='main_site.event')),
            ],
            options={
                'verbose_name': 'Guess the Theme',
                'db_table': 'guess_the_theme',
                'ordering': ['event', 'created_at'],
            },
        ),
    ]
