from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
ALPHANUMERIC = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters (numbers and letters) are allowed.')

class Person(models.Model):
    user = models.OneToOneField(User, related_name='person', on_delete=models.CASCADE)
    photo = models.TextField(null=True, blank=True)
    tickets = models.ManyToManyField('Event', through='Ticket', related_name='tickets', through_fields=('holder', 'event'))
    bank_account = models.CharField(max_length=30, null=True, blank=True, validators=[ALPHANUMERIC])
    fullname = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
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
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    original_filename = models.CharField(max_length=200, null=True, blank=True)
    complete = models.BooleanField(default=False)
    potential_buyer = models.ForeignKey('Person', related_name='potential_buyer', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.bought:
            self.holder = self.seller
        else:
            self.holder = self.buyer

        super(Ticket, self).save(*args, **kwargs)


    def clean(self):
        max_price = float(self.event.baseticket.price) * 1.25
        if self.price and (float(self.price) > max_price):
            validation_error_text = 'The price of the ticket can only be 25%% more than the original ticket price, in this case %s %.2f' % (u"\u20AC", float(self.event.baseticket.price)*1.25)
            raise ValidationError(validation_error_text)


class BaseTicket(models.Model):
    event = models.OneToOneField('Event')
    details = models.TextField()
    link = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)