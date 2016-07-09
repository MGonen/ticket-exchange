from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User, related_name='person', on_delete=models.CASCADE)
    photo = models.TextField(null=True, blank=True)
    tickets = models.ManyToManyField('Event', through='Ticket', related_name='tickets', through_fields=('holder', 'event'))
    bank_account = models.CharField(max_length=30, null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.user.username


class Event(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    event = models.ForeignKey('Event', related_name='event')
    seller = models.ForeignKey('Person', related_name='seller')
    buyer = models.ForeignKey('Person', null=True, blank=True, related_name='buyer')
    holder = models.ForeignKey('Person', related_name='holder')
    bought = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.festival.name


    def save(self, *args, **kwargs):
        if not self.bought:
            self.holder = self.seller

        else:
            self.holder = self.buyer

        super(Ticket, self).save(*args, **kwargs)


class BaseTicket(models.Model):
    event = models.ForeignKey('Event')
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)