from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages

from ticket_exchange.models import Person, Ticket
from ticket_exchange.utils import is_own_ticket
from ticket_exchange.views import FACEBOOK_LOGIN_URL
from ticket_exchange import messages as message_text

from my_info.forms import PersonForm4MyInfo, UserForm

import time

@login_required(login_url=FACEBOOK_LOGIN_URL)
def tickets_for_sale(request):
    print 'tickets for sale reached'
    tickets_for_sale = Ticket.objects.filter(seller__user_id=request.user.id).filter(buyer__isnull=True)
    tickets_being_sold = Ticket.objects.filter(seller__user_id=request.user.id).filter(potential_buyer_expiration_moment__gte=time.time())
    tickets_sold = Ticket.objects.filter(seller__user_id=request.user.id).filter(buyer__isnull=False)
    return render(request, 'my_info/tickets_for_sale.html', {'tickets_for_sale': tickets_for_sale, 'tickets_being_sold': tickets_being_sold, 'tickets_sold': tickets_sold})

@is_own_ticket
def ticket_for_sale_details(request, ticket_id):
    ticket = get_ticket_or_404(ticket_id)
    return render(request, 'my_info/ticket_for_sale_details.html', {'ticket': ticket})

@is_own_ticket
def remove_for_sale_ticket(request, ticket_id):
    ticket = get_ticket_or_404(ticket_id)
    print ticket.potential_buyer_expiration_moment >= time.time()
    print ticket.potential_buyer_expiration_moment - time.time()


    if request.user.person != ticket.potential_buyer and ticket.potential_buyer_expiration_moment >= time.time():
        messages.add_message(request, messages.INFO, message_text.cant_remove_potential_buyer)
        redirect('my_info:tickets_for_sale')

    if request.method == "GET":
        ticket.potential_buyer = request.user.person
        ticket.potential_buyer_expiration_moment = time.time() + 15
        ticket.save()
        return render(request, 'my_info/remove_for_sale_ticket.html', {'ticket_id': ticket.id})
    # show countdown timer on 'Remove' Button

    if request.method == "POST":
        ticket.delete()
        return redirect('my_info:tickets_for_sale')


@is_own_ticket
def cancel_remove_ticket(request, ticket_id):
    print 'cancel ticket reached'
    ticket = get_ticket_or_404(ticket_id)
    ticket.potential_buyer_expiration_moment = time.time()
    ticket.save()

    messages.add_message(request, messages.INFO, message_text.ticket_removal_cancelled)
    return redirect('my_info:tickets_for_sale')



@login_required(login_url=FACEBOOK_LOGIN_URL)
def tickets_bought(request):
    tickets = Ticket.objects.filter(buyer__user_id=request.user.id)
    return render(request, 'my_info/bought_tickets.html', {'tickets': tickets})


@is_own_ticket
def ticket_bought_details(request, ticket_id):
    ticket = get_ticket_or_404(ticket_id)

    return render(request, 'my_info/bought_ticket_details.html', {'ticket': ticket})

@login_required(login_url=FACEBOOK_LOGIN_URL)
def payouts(request):
    return render(request, 'my_info/payouts.html', {})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    person = get_object_or_404(Person, pk=request.user.person.id)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        person_form = PersonForm4MyInfo(request.POST, instance=person)

        if person_form.is_valid() and user_form.is_valid():
            person_form.save()
            user_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your Profile has been successfully updated')
            return render(request, 'my_info/profile.html', {'person_form': person_form, 'user_form': user_form})

    else:
        person_form = PersonForm4MyInfo(instance=person)
        user_form = UserForm(instance=user)

    return render(request, 'my_info/profile.html', {'person_form': person_form, 'user_form': user_form})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def cancel_profile_update(request):
    messages.add_message(request, messages.WARNING, message_text.profile_changes_discarded)
    return redirect('home')


def get_ticket_or_404(ticket_id):
    try:
        return Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Http404
