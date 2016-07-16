from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from ticket_exchange.models import Person, Ticket


@receiver(post_save, sender=User)
def create_person_object_for_user(sender, **kwargs):
    user = kwargs['instance']

    # create Person when none match user:
    if len(Person.objects.filter(user_id=user.id)) == 0:
        person = Person(user=user)
        person.save()

    # create Person fullname
    person = Person.objects.get(user_id=user.id)
    person.fullname = '%s %s' % (user.first_name, user.last_name)
    person.save()


@receiver(post_save, sender=Ticket)
def remove_same_potential_buyer_two_tickets_same_event(sender, **kwargs):
    """user can only be potential buyer for one ticket per event"""
    this_ticket = kwargs['instance']
    if this_ticket.potential_buyer:
        event = this_ticket.event
        potential_buyer = this_ticket.potential_buyer
        for ticket in Ticket.objects.filter(event=event).filter(potential_buyer=potential_buyer):
            if ticket.id != this_ticket.id:
                ticket.potential_buyer = None
                ticket.potential_buyer_release_time = None
                ticket.save()