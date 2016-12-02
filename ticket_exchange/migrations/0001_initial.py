# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.utils.timezone
from django.conf import settings
import time


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTicket',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('link', models.TextField(null=True, blank=True)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='BaseTicketBarcodeLocation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('x_min', models.IntegerField()),
                ('x_max', models.IntegerField()),
                ('y_min', models.IntegerField()),
                ('y_max', models.IntegerField()),
                ('baseticket', models.ForeignKey(to='ticket_exchange.BaseTicket')),
            ],
        ),
        migrations.CreateModel(
            name='BaseTicketBarcodeType',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('type', models.CharField(max_length=100)),
                ('baseticket', models.ForeignKey(to='ticket_exchange.BaseTicket')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('photo', models.TextField(null=True, blank=True)),
                ('iban', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z]*$', b'Only alphanumeric characters (numbers and letters) are allowed.')], blank=True, null=True)),
                ('fullname', models.CharField(null=True, blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('link', models.TextField(null=True, blank=True)),
                ('potential_buyer_expiration_moment', models.FloatField(default=time.time)),
                ('buyer', models.ForeignKey(null=True, blank=True, related_name='buyer', to='ticket_exchange.Person')),
                ('event', models.ForeignKey(to='ticket_exchange.Event', related_name='event')),
                ('holder', models.ForeignKey(to='ticket_exchange.Person', related_name='holder')),
                ('potential_buyer', models.ForeignKey(null=True, blank=True, related_name='potential_buyer', to='ticket_exchange.Person')),
                ('seller', models.ForeignKey(to='ticket_exchange.Person', related_name='seller')),
            ],
        ),
        migrations.CreateModel(
            name='TicketBarcodeNumber',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('number', models.CharField(max_length=200)),
                ('ticket', models.ForeignKey(to='ticket_exchange.Ticket')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='tickets',
            field=models.ManyToManyField(to='ticket_exchange.Event', through='ticket_exchange.Ticket', related_name='tickets'),
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
