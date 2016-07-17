from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import time
from collections import namedtuple

from ticket_exchange.models import Ticket
from my_info.forms import UserForm
from ticket_exchange.views import FACEBOOK_LOGIN_URL
from ticket_exchange.utils import potential_buyer_checks_decorator

# Create your views here.
TicketPriceObject = namedtuple("TicketPriceObject", ['commission', 'bank_costs', 'total_price'])
COMMISSION_PERCENTAGE =0.06

@login_required(login_url=FACEBOOK_LOGIN_URL)
def potential_buyer_check(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if ticket.potential_buyer and (ticket.potential_buyer.id != request.user.person.id):
        messages.add_message(request, messages.ERROR,"Sorry, someone else is currently trying to purchase this ticket :-(. Please try a different ticket")
        return redirect('event_tickets', ticket.event.id)

    elif ticket.potential_buyer and (ticket.potential_buyer.id == request.user.person.id):
        return redirect('buy_ticket:ticket_details', ticket_id)

    else:
        messages.add_message(request, messages.INFO, "You have 10 minutes to purchase this ticket, otherwise other people will be able to buy it")
        ticket.potential_buyer = request.user.person
        ticket.potential_buyer_release_time = time.time() +  30
        ticket.save()
        return redirect('buy_ticket:ticket_details', ticket_id)


@login_required(login_url=FACEBOOK_LOGIN_URL)
@potential_buyer_checks_decorator
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket_price_object = _get_ticket_price_object(ticket.price)
    return render(request, 'buy_ticket/ticket_details.html', {'ticket': ticket, 'ticket_price_object': ticket_price_object})


@login_required(login_url=FACEBOOK_LOGIN_URL)
@potential_buyer_checks_decorator
def confirm_personal_details(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    user = get_object_or_404(User, pk=request.user.id)
    event_id = ticket.event.id

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)

        if user_form.is_valid():
            if 'continue' in request.POST:
                user_form.save()
                return redirect('buy_ticket:select_payment_method', ticket_id)
            elif 'return' in request.POST:
                return redirect('buy_ticket:ticket_details', ticket_id)
            elif 'cancel' in request.POST:
                cancel_ticket(ticket.id)
                return redirect('event_tickets', event_id)

    else:
        user_form = UserForm(instance=user)

    return render(request, 'buy_ticket/confirm_personal_details.html', {'user_form': user_form, 'ticket':ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
@potential_buyer_checks_decorator
def select_payment_method(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    event_id = ticket.event.id

    if request.method == "POST":
        # user_form = UserForm(request.POST, instance=user)

        # if user_form.is_valid():
        if True:
            if 'continue' in request.POST:
                return redirect('buy_ticket:confirm_purchase', ticket_id)
            elif 'return' in request.POST:
                return redirect('buy_ticket:confirm_personal_details', ticket_id)
            elif 'cancel' in request.POST:
                cancel_ticket(ticket.id)
                return redirect('event_tickets', event_id)

    else:
        # user_form = UserForm(instance=user)
        pass

    return render(request, 'buy_ticket/select_payment_method.html', {'ticket': ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
@potential_buyer_checks_decorator
def confirm_purchase(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.potential_buyer_release_time = time.time() + 60
    ticket.save()

    ticket_price_object = _get_ticket_price_object(ticket.price)

    if request.method == "POST":
        if 'confirm' in request.POST:
            ticket.buyer = ticket.potential_buyer
            ticket.potential_buyer = None
            ticket.potential_buyer_release_time = None
            ticket.bought = True
            ticket.save()
            return redirect('buy_ticket:payment_confirmation', ticket_id)

    return render(request, 'buy_ticket/confirm_purchase.html', {'ticket': ticket, 'ticket_price_object': ticket_price_object})



@login_required(login_url=FACEBOOK_LOGIN_URL)
def payment_confirmation(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'buy_ticket/payment_confirmation.html', {'ticket': ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def payment_failed(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'buy_ticket/payment_failed.html', {'ticket': ticket})



@login_required(login_url=FACEBOOK_LOGIN_URL)
def cancel_ticket_view(request, ticket_id):
    cancel_ticket(ticket_id)
    ticket = Ticket.objects.get(id=ticket_id)
    event_id = ticket.event.id
    return redirect('event_tickets', event_id)


def _get_ticket_price_object(ticket_price):
    commission = COMMISSION_PERCENTAGE * float(ticket_price)
    bank_costs = (0.019 * float(ticket_price)) + 0.6
    total_price = float(ticket_price) + commission + bank_costs

    commission_string = '%.2f' % (commission,)
    bank_costs_string = '%.2f' % (bank_costs,)
    total_price_string = '%.2f' % (total_price,)

    return TicketPriceObject(commission=commission_string, bank_costs=bank_costs_string, total_price=total_price_string)


def cancel_ticket(ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.potential_buyer = None
    ticket.potential_buyer_release_time = None
    ticket.save()