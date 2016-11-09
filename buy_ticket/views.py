from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import Http404

import time
from collections import namedtuple

from ticket_exchange.models import Ticket, Event
from my_info.forms import UserForm
from ticket_exchange.views import FACEBOOK_LOGIN_URL
from ticket_exchange.utils import potential_buyer_checks_decorator
from ticket_exchange import messages as message_text

from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt

from buy_ticket.forms import NameLocationSearchForm

import braintree
from django.conf import settings

braintree.Configuration.configure(braintree.Environment.Sandbox,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC_KEY,
    private_key=settings.BRAINTREE_PRIVATE_KEY)

# Create your views here.
TicketPriceObject = namedtuple("TicketPriceObject", ['commission', 'bank_costs', 'total_price'])
COMMISSION_PERCENTAGE = 0.06


class SelectEvent(View):
    form_class = NameLocationSearchForm
    template_name = 'buy_ticket/select_event.html'

    def get(self, request):
        print 'arrived at get'
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid and "search_button" in request.POST:
            return redirect('advanced_search', search_query=request.POST.get('search_query'))


class AvailableTickets(View):
    template_name = 'buy_ticket/available_tickets.html'

    def get(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        tickets_available = len(
            Ticket.objects.filter(event_id=event.id).filter(buyer__isnull=True).filter(complete=True).filter(
                potential_buyer_expiration_moment__lte=time.time()))
        tickets_sold = len(Ticket.objects.filter(event_id=event.id).filter(buyer__isnull=False))

        return render(request, self.template_name, {'event': event, 'tickets_available': tickets_available, 'tickets_sold': tickets_sold})


    def post(self, request, event_id):
        # Only applies if the user is already in the process of buying another ticket for the same event
        selected_ticket = get_selected_ticket(request, event_id)
        if not selected_ticket:
            return render(request, self.template_name)

        else:
            if 'continue' in request.POST:
                return redirect('buy_ticket:purchase', selected_ticket.id)
            elif 'new' in request.POST:
                selected_ticket.potential_buyer_expiration_moment = 0
                selected_ticket.save()
                return redirect('buy_ticket:available_tickets', event_id)


@json_view
@csrf_exempt
def get_available_tickets_ajax(request, event_id):
    tickets = get_available_tickets(event_id)
    ticket_dicts = create_ticket_dicts(tickets)

    selected_ticket = get_selected_ticket(request, event_id)

    if selected_ticket:
        user_is_already_a_potential_buyer_in_this_event = True
        selected_ticket_info = { 'price': float(selected_ticket.price), 'seller': selected_ticket.seller.fullname }

    else:
        user_is_already_a_potential_buyer_in_this_event = False
        selected_ticket_info = None

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

    if ticket.potential_buyer_expiration_moment > time.time() and (ticket.potential_buyer.id != request.user.person.id): # User is not the potential buyer
        messages.add_message(request, messages.ERROR, message_text.other_potential_buyer)
        return redirect('buy_ticket:available_tickets', ticket.event.id)

    elif ticket.potential_buyer_expiration_moment > time.time() and (ticket.potential_buyer.id == request.user.person.id): # User is already the potential buyer
        return redirect('buy_ticket:purchase', ticket_id)

    elif Ticket.objects.filter(potential_buyer=request.user.person).filter(potential_buyer_expiration_moment__gte=time.time()): # User is already buying another ticket for this event
        ticket.potential_buyer_expiration_moment = 0
        ticket.save()
        messages.add_message(request, messages.ERROR, message_text.user_already_potential_buyer_other_ticket)
        return redirect('buy_ticket:available_tickets', ticket.event.id)

    else: # User becomes the potential buyer
        ticket.potential_buyer = request.user.person
        ticket.potential_buyer_expiration_moment = time.time() +  100
        ticket.save()
        return redirect('buy_ticket:purchase', ticket_id)


class Purchase(View):
    template_name = 'buy_ticket/purchase.html'

    def get_ticket(self, ticket_id):
        try:
            return Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            raise Http404

    def get_ticket_price_object(self, ticket_price):
        commission = COMMISSION_PERCENTAGE * float(ticket_price)
        bank_costs = (0.019 * float(ticket_price)) + 0.6
        total_price = float(ticket_price) + commission + bank_costs

        commission_string = '%.2f' % (commission,)
        bank_costs_string = '%.2f' % (bank_costs,)
        total_price_string = '%.2f' % (total_price,)

        return TicketPriceObject(commission=commission_string, bank_costs=bank_costs_string,
                                 total_price=total_price_string)

    @method_decorator(login_required(login_url=FACEBOOK_LOGIN_URL))
    @method_decorator(potential_buyer_checks_decorator)
    def get(self, request, ticket_id):
        ticket = self.get_ticket(ticket_id)
        ticket_price_object = self.get_ticket_price_object(ticket.price)
        token = braintree.ClientToken.generate()
        return render(request, self.template_name,
                      {'token': token, 'ticket': ticket, 'ticket_price_object': ticket_price_object,
                       'time_left': get_time_left(ticket.potential_buyer_expiration_moment)})

    @method_decorator(login_required(login_url=FACEBOOK_LOGIN_URL))
    @method_decorator(potential_buyer_checks_decorator)
    def post(self, request, ticket_id):
        ticket = self.get_ticket(ticket_id)
        ticket_price_object = self.get_ticket_price_object(ticket.price)
        nonce_from_the_client = request.POST["payment_method_nonce"]

        result = braintree.Transaction.sale({
            "amount": ticket_price_object.total_price,
            "payment_method_nonce": nonce_from_the_client,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            return redirect('buy_ticket:purchase_successful', ticket_id)
        else:
            return redirect('buy_ticket:purchase_failed', ticket_id)


@login_required(login_url=FACEBOOK_LOGIN_URL)
def purchase_successful(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.buyer = request.user.person
    ticket.potential_buyer = None
    ticket.save()
    return render(request, 'buy_ticket/purchase_successful.html', {'ticket': ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def purchase_failed(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'buy_ticket/purchase_failed.html', {'ticket': ticket})



@login_required(login_url=FACEBOOK_LOGIN_URL)
def cancel_ticket_view(request, ticket_id):
    cancel_ticket(ticket_id)
    ticket = Ticket.objects.get(id=ticket_id)
    event_id = ticket.event.id
    return redirect('buy_ticket:available_tickets', event_id)

def cancel_ticket(ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    ticket.potential_buyer_expiration_moment = 0
    ticket.save()


def remove_overtime_potential_buyers():
    current_time = time.time()
    for ticket in Ticket.objects.filter(potential_buyer_expiration_moment__lt=current_time):
        ticket.potential_buyer = None
        ticket.potential_buyer_expiration_moment = 0
        ticket.save()


def get_time_left(potential_buyer_expiration_moment):
    time_left = float(potential_buyer_expiration_moment) - float(time.time())
    return round(time_left)


def get_available_tickets(event_id):
    return Ticket.objects.filter(event_id=event_id).filter(buyer__isnull=True).filter(complete=True).filter(potential_buyer_expiration_moment__lte=time.time()).order_by('price')


def get_selected_ticket(request, event_id):
    if hasattr(request.user, 'person'): # user not anonymous
        selected_ticket = Ticket.objects.filter(event_id=event_id).filter(potential_buyer_expiration_moment__gte=time.time()).filter(potential_buyer=request.user.person)
        if len(selected_ticket) == 1:
            return selected_ticket[0]
