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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('details', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.TextField(blank=True, null=True)),
                ('bank_account', models.CharField(blank=True, max_length=30, null=True)),
                ('fullname', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bought', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buyer', models.ForeignKey(blank=True, related_name='buyer', to='ticketexchange.Person', null=True)),
                ('event', models.ForeignKey(to='ticketexchange.Event', related_name='event')),
                ('holder', models.ForeignKey(to='ticketexchange.Person', related_name='holder')),
                ('seller', models.ForeignKey(to='ticketexchange.Person', related_name='seller')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='tickets',
            field=models.ManyToManyField(through='ticketexchange.Ticket', to='ticketexchange.Event', related_name='tickets'),
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(related_name='person', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='baseticket',
            name='event',
            field=models.ForeignKey(to='ticketexchange.Event'),
        ),
    ]
