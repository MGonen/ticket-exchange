# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTicket',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('details', models.TextField()),
                ('link', models.CharField(max_length=200)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100, null=True, blank=True)),
                ('country', models.CharField(max_length=100, null=True, blank=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('photo', models.TextField(null=True, blank=True)),
                ('bank_account', models.CharField(null=True, max_length=30, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z]*$', b'Only alphanumeric characters (numbers and letters) are allowed.')], blank=True)),
                ('fullname', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('bought', models.BooleanField(default=False)),
                ('price', models.DecimalField(null=True, max_digits=10, blank=True, decimal_places=2)),
                ('link', models.TextField(null=True, blank=True)),
                ('original_filename', models.CharField(max_length=200, null=True, blank=True)),
                ('complete', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(blank=True, to='ticket_exchange.Person', related_name='buyer', null=True)),
                ('event', models.ForeignKey(related_name='event', to='ticket_exchange.Event')),
                ('holder', models.ForeignKey(related_name='holder', to='ticket_exchange.Person')),
                ('seller', models.ForeignKey(related_name='seller', to='ticket_exchange.Person')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='tickets',
            field=models.ManyToManyField(related_name='tickets', to='ticket_exchange.Event', through='ticket_exchange.Ticket'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='person'),
        ),
        migrations.AddField(
            model_name='baseticket',
            name='event',
            field=models.OneToOneField(to='ticket_exchange.Event'),
        ),
    ]
