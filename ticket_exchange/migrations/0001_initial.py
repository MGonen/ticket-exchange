# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import time
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('details', models.TextField()),
                ('link', models.CharField(max_length=200)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=100)),
                ('city', models.CharField(null=True, blank=True, max_length=100)),
                ('country', models.CharField(null=True, blank=True, max_length=100)),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('photo', models.TextField(null=True, blank=True)),
                ('bank_account', models.CharField(validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z]*$', b'Only alphanumeric characters (numbers and letters) are allowed.')], blank=True, null=True, max_length=30)),
                ('fullname', models.CharField(null=True, blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('price', models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)),
                ('link', models.TextField(null=True, blank=True)),
                ('original_filename', models.CharField(null=True, blank=True, max_length=200)),
                ('complete', models.BooleanField(default=False)),
                ('potential_buyer_expiration_moment', models.FloatField(default=time.time)),
                ('buyer', models.ForeignKey(related_name='buyer', to='ticket_exchange.Person', null=True, blank=True)),
                ('event', models.ForeignKey(to='ticket_exchange.Event', related_name='event')),
                ('holder', models.ForeignKey(to='ticket_exchange.Person', related_name='holder')),
                ('potential_buyer', models.ForeignKey(related_name='potential_buyer', to='ticket_exchange.Person', null=True, blank=True)),
                ('seller', models.ForeignKey(to='ticket_exchange.Person', related_name='seller')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='tickets',
            field=models.ManyToManyField(related_name='tickets', through='ticket_exchange.Ticket', to='ticket_exchange.Event'),
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
