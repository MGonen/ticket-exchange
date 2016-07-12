# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTicket',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('details', models.TextField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('photo', models.TextField(blank=True, null=True)),
                ('bank_account', models.CharField(blank=True, max_length=30, null=True)),
                ('fullname', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('bought', models.BooleanField(default=False)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('link', models.TextField(blank=True, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(blank=True, to='ticket_exchange.Person', null=True, related_name='buyer')),
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
            field=models.ForeignKey(to='ticket_exchange.Event'),
        ),
    ]
