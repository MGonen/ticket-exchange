from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages


from ticketexchange.models import Person, Event, Ticket
from ticketexchange.forms import PersonForm, SellTicketForm, UserForm

facebook_login_url = '/login/facebook'

@login_required(login_url=facebook_login_url)
def my_tickets_for_sale(request):
    tickets = Ticket.objects.filter(seller__user_id=request.user.id)
    return render(request, 'ticketexchange/My/tickets_for_sale.html', {'tickets': tickets})


@login_required(login_url=facebook_login_url)
def my_tickets_bought(request):
    tickets = Ticket.objects.filter(buyer__user_id=request.user.id)
    return render(request, 'ticketexchange/My/bought_tickets.html', {'tickets': tickets})


@login_required(login_url=facebook_login_url)
def my_payouts(request):
    return render(request, 'ticketexchange/My/payouts.html', {})


@login_required(login_url=facebook_login_url)
def my_profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    person = get_object_or_404(Person, pk=request.user.person.id)

    if request.method == "POST":

        if "cancel" in request.POST:
            return redirect('person_index')

        user_form = UserForm(request.POST, instance=user)
        person_form = PersonForm(request.POST, instance=person)

        if person_form.is_valid() and user_form.is_valid():
            person_form.save()
            user_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your Profile has been successfully updated')
            return render(request, 'ticketexchange/My/profile.html', {'person_form': person_form, 'user_form': user_form})

    else:
        person_form = PersonForm(instance=person)
        user_form = UserForm(instance=user)

    return render(request, 'ticketexchange/My/profile.html', {'person_form': person_form, 'user_form': user_form})


@login_required(login_url=facebook_login_url)
def sell_ticket(request):
    if request.method == "POST":

        if "cancel" in request.POST:
            return redirect('person_index')

        form = SellTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.seller = request.user.person
            ticket.save()

            return redirect('home')
    else:
        form = SellTicketForm()

    return render(request, 'ticketexchange/SellTicket/sell_ticket.html', {'form': form})
