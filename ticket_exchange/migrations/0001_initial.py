# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import time
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('details', models.TextField()),
                ('link', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('photo', models.TextField(null=True, blank=True)),
                ('bank_account', models.CharField(null=True, max_length=30, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z]*$', b'Only alphanumeric characters (numbers and letters) are allowed.')], blank=True)),
                ('fullname', models.CharField(null=True, max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('price', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('link', models.TextField(null=True, blank=True)),
                ('potential_buyer_expiration_moment', models.FloatField(default=time.time)),
                ('buyer', models.ForeignKey(null=True, blank=True, to='ticket_exchange.Person', related_name='buyer')),
                ('event', models.ForeignKey(related_name='event', to='ticket_exchange.Event')),
                ('holder', models.ForeignKey(related_name='holder', to='ticket_exchange.Person')),
                ('potential_buyer', models.ForeignKey(null=True, blank=True, to='ticket_exchange.Person', related_name='potential_buyer')),
                ('seller', models.ForeignKey(related_name='seller', to='ticket_exchange.Person')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='tickets',
            field=models.ManyToManyField(through='ticket_exchange.Ticket', related_name='tickets', to='ticket_exchange.Event'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(related_name='person', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='baseticket',
            name='event',
            field=models.OneToOneField(to='ticket_exchange.Event'),
        ),
    ]
