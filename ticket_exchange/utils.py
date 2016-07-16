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


def potential_buyer_overtime_check(func):
    def inner(*args, **kwargs):
        request = args[0]
        ticket_id = kwargs['ticket_id']

        ticket = Ticket.objects.get(id=ticket_id)

        if ticket.potential_buyer_release_time < time.time():
            messages.add_message(request, messages.ERROR, "Sorry, you went over the time given for purchasing a ticket :-(")
            ticket.potential_buyer = None
            ticket.potential_buyer_release_time = None
            ticket.save()
            return redirect('event_tickets', ticket.event.id)

        return func(*args, **kwargs)
    return inner


def user_is_potential_buyer_check(func):
    def inner(*args, **kwargs):
        request = args[0]
        ticket_id = kwargs['ticket_id']

        ticket = Ticket.objects.get(id=ticket_id)
        user_id = request.user.person.id

        if ticket.potential_buyer and (ticket.potential_buyer.id != user_id):
            messages.add_message(request, messages.ERROR,
                                 "Sorry, someone else is currently trying to purchase this ticket :-(. Please try to select a different ticket")
            return redirect('event_tickets', ticket.event.id)

        return func(*args, **kwargs)
    return inner