from django.shortcuts import redirect
from django.contrib import messages

from ticket_exchange.models import Ticket



def ticket_complete_check(func):
    def inner(*args, **kwargs):
        request = args[0]
        ticket_id = kwargs['ticket_id']

        ticket = Ticket.objects.get(id=ticket_id)

        if ticket.complete:
            messages.add_message(request, messages.ERROR, "For safety reasons, it is not possible to edit completed tickets. If you want to change something, you will have to delete it, and put it up for sale again.")
            return redirect('my_info:tickets_for_sale')


        return func(*args, **kwargs)
    return inner
