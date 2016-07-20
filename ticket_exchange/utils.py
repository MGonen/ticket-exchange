from django.shortcuts import redirect
from django.contrib import messages

from ticket_exchange.models import Ticket

import time


def ticket_complete_check(func):
    def inner(*args, **kwargs):
        request = args[0]
        ticket_id = kwargs['ticket_id']

        ticket = Ticket.objects.get(id=ticket_id)

        if ticket.complete:
            messages.add_message(request, messages.ERROR, "For safety reasons, it is not possible to edit completed tickets. If you want to change something, you will have to delete the ticket, and put it up for sale again.")
            return redirect('my_info:tickets_for_sale')


        return func(*args, **kwargs)
    return inner


def potential_buyer_checks_decorator(func):
    def inner(*args, **kwargs):
        request = args[0]
        ticket_id = kwargs['ticket_id']
        ticket = Ticket.objects.get(id=ticket_id)

        if ticket_already_bought(request, ticket) or ticket_already_other_potential_buyer(request, ticket) or overtime_check(request, ticket):
            return redirect('event_tickets', ticket.event.id)

        return func(*args, **kwargs)
    return inner


def ticket_already_other_potential_buyer(request, ticket):
    if ticket.potential_buyer and (ticket.potential_buyer.id != request.user.person.id):
        messages.add_message(request, messages.ERROR, "Sorry, someone else is currently trying to purchase this ticket :-(. Please try a different ticket")

        return True


def overtime_check(request, ticket):
    if ticket.potential_buyer_release_time < time.time():
        messages.add_message(request, messages.ERROR, "Sorry, you are no longer the potential buyer of this ticket. You might have gone over the time given for purchasing a ticket, or perhaps selected a different ticket for the same event. ")
        ticket.potential_buyer = None
        ticket.potential_buyer_release_time = None
        ticket.save()
        return True

def ticket_already_bought(request, ticket):
    if ticket.bought or ticket.buyer:
        messages.add_message(request, messages.ERROR,
                             "Sorry, this ticket has already been bought. Please try another ticket.")
        return True
