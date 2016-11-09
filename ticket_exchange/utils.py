from django.shortcuts import redirect
from django.contrib import messages

from ticket_exchange.models import Ticket
from ticket_exchange import messages as message_text

import time


def ticket_complete_check(func):
    def inner(*args, **kwargs):
        request = args[0]
        ticket_id = kwargs['ticket_id']

        ticket = Ticket.objects.get(id=ticket_id)

        if ticket.complete:
            messages.add_message(request, messages.ERROR, message_text.no_editing_completed_tickets)
            return redirect('my_info:tickets_for_sale')


        return func(*args, **kwargs)
    return inner


def potential_buyer_checks_decorator(func):
    def inner(*args, **kwargs):
        request = args[0]
        ticket_id = kwargs['ticket_id']
        ticket = Ticket.objects.get(id=ticket_id)

        if ticket_already_bought(request, ticket) or ticket_already_other_potential_buyer(request, ticket) or overtime_check(request, ticket) or user_already_potential_buyer_same_event(request, ticket):
            return redirect('buy_ticket:available_tickets', ticket.event.id)

        return func(*args, **kwargs)
    return inner


def ticket_already_other_potential_buyer(request, ticket):
    if ticket.potential_buyer_expiration_moment >= time.time() and (ticket.potential_buyer.id != request.user.person.id):
        messages.add_message(request, messages.ERROR, message_text.other_potential_buyer)

        return True


def overtime_check(request, ticket):
    if ticket.potential_buyer_expiration_moment < time.time():
        messages.add_message(request, messages.ERROR, message_text.user_no_longer_potential_buyer)
        ticket.save()
        return True

def ticket_already_bought(request, ticket):
    if ticket.buyer:
        messages.add_message(request, messages.ERROR, message_text.ticket_already_sold)
        return True

def user_already_potential_buyer_same_event(request, ticket):
    for ticket in Ticket.objects.filter(event_id=ticket.event_id).filter(potential_buyer=request.user.person).exclude(id=ticket.id):
        if ticket.potential_buyer_expiration_moment > time.time():
            print 'User already potential buyer other ticket same event'
            messages.add_message(request, messages.ERROR, message_text.user_already_potential_buyer_other_ticket)
            return True
