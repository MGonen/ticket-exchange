from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import time
from collections import namedtuple

from ticket_exchange.models import Ticket, Event
from my_info.forms import UserForm
from ticket_exchange.views import FACEBOOK_LOGIN_URL
from ticket_exchange.utils import potential_buyer_checks_decorator

from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt

from buy_ticket.forms import NameLocationSearchForm

# Create your views here.
TicketPriceObject = namedtuple("TicketPriceObject", ['commission', 'bank_costs', 'total_price'])
COMMISSION_PERCENTAGE =0.06


def select_event(request):
    if request.method == "POST":
        form = NameLocationSearchForm(request.POST)
        if form.is_valid and "search_button" in request.POST:
            return redirect('advanced_search', search_query=request.POST.get('search_query'))

    else:
        form = NameLocationSearchForm()

    return render(request, 'buy_ticket/select_event.html', {'form':form})

def event_tickets(request, event_id):
    selected_ticket_qs = Ticket.objects.filter(seller__isnull=True).filter(seller__isnull=False) # creating an empty queryset, so 'selected_ticket_qs.exists() is not an exception
    if hasattr(request.user, 'person'):
        selected_ticket_qs = Ticket.objects.filter(event_id=event_id).filter(potential_buyer_id=request.user.person.id)

    if request.method == "POST" and selected_ticket_qs.exists():
        if 'continue' in request.POST:
            ticket = selected_ticket_qs[0]
            return redirect('buy_ticket:ticket_details', ticket.id)
        elif 'new' in request.POST:
            ticket = selected_ticket_qs[0]
            ticket.potential_buyer = None
            ticket.potential_buyer_release_time = None
            ticket.save()
            return redirect('buy_ticket:event_tickets', event_id)


    event = Event.objects.get(pk=event_id)
    tickets_available = len(Ticket.objects.filter(event_id=event.id).filter(bought=False).filter(complete=True))
    tickets_sold = len(Ticket.objects.filter(event_id=event.id).filter(bought=True))

    print 'arrived at render'
    return render(request, 'buy_ticket/event_tickets.html', {'event': event, 'tickets_available': tickets_available, 'tickets_sold': tickets_sold})


@json_view
@csrf_exempt
def get_event_tickets(request, event_id):
    remove_overtime_potential_buyers()
    tickets = Ticket.objects.filter(event_id=event_id).filter(bought=False).filter(complete=True).filter(
    potential_buyer__isnull=True).order_by('price')
    ticket_dicts = create_ticket_dicts(tickets)

    try:
        user_is_already_a_potential_buyer_in_this_event, selected_ticket_info = get_selected_ticket_info(request.user.person.id, event_id)
    except:
        print 'no person linked to user, i.e. anonymous user, i.e. not a buyer'
        user_is_already_a_potential_buyer_in_this_event, selected_ticket_info = False, False


    return {'tickets': ticket_dicts, 'already_a_potential_buyer': user_is_already_a_potential_buyer_in_this_event, 'selected_ticket': selected_ticket_info}


def create_ticket_dicts(tickets):
    ticket_dicts = []

    for ticket_object in tickets:
        ticket_dict = {}
        ticket_dict['id'] = ticket_object.id
        ticket_dict['seller'] = ticket_object.seller.fullname
        ticket_dict['price'] = ticket_object.price

        ticket_dicts.append(ticket_dict)

    return ticket_dicts



@login_required(login_url=FACEBOOK_LOGIN_URL)
def potential_buyer_check(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if ticket.potential_buyer and (ticket.potential_buyer.id != request.user.person.id):
        messages.add_message(request, messages.ERROR,"Sorry, someone else is currently trying to purchase this ticket :-(. Please try a different ticket")
        return redirect('buy_ticket:event_tickets', ticket.event.id)

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
                return redirect('buy_ticket:event_tickets', event_id)

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
                return redirect('buy_ticket:event_tickets', event_id)

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
    return redirect('buy_ticket:event_tickets', event_id)


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



def remove_overtime_potential_buyers():
    current_time = time.time()
    for ticket in Ticket.objects.filter(potential_buyer_release_time__lt=current_time):
        ticket.potential_buyer = None
        ticket.potential_buyer_release_time = None
        ticket.save()


def get_selected_ticket_info(person_id, event_id):
    if Ticket.objects.filter(event_id=event_id).filter(potential_buyer_id=person_id).exists():
        ticket = Ticket.objects.filter(event_id=event_id).filter(potential_buyer_id=person_id)[0]
        selected_ticket_info = {'price': float(ticket.price), 'seller': ticket.seller.fullname}
        return True, selected_ticket_info

    else:
        return False, False

