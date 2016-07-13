# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('details', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
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
                ('photo', models.TextField(null=True, blank=True)),
                ('bank_account', models.CharField(max_length=30, null=True, blank=True, validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z]*$', b'Only alphanumeric characters (numbers and letters) are allowed.')])),
                ('fullname', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('bought', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)),
                ('link', models.TextField(null=True, blank=True)),
                ('original_filename', models.CharField(max_length=200, null=True, blank=True)),
                ('complete', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(null=True, related_name='buyer', blank=True, to='ticket_exchange.Person')),
                ('event', models.ForeignKey(related_name='event', to='ticket_exchange.Event')),
                ('holder', models.ForeignKey(related_name='holder', to='ticket_exchange.Person')),
                ('seller', models.ForeignKey(related_name='seller', to='ticket_exchange.Person')),
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
            field=models.ForeignKey(to='ticket_exchange.Event'),
        ),
    ]
