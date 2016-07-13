from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib import messages


from ticket_exchange.models import Person, Ticket
from my_info.forms import PersonForm4MyInfo, UserForm

from ticket_exchange.views import FACEBOOK_LOGIN_URL


@login_required(login_url=FACEBOOK_LOGIN_URL)
def tickets_for_sale(request):
    tickets = Ticket.objects.filter(seller__user_id=request.user.id).filter(complete=True)
    return render(request, 'my_info/tickets_for_sale.html', {'tickets': tickets})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def tickets_bought(request):
    tickets = Ticket.objects.filter(buyer__user_id=request.user.id)
    return render(request, 'my_info/bought_tickets.html', {'tickets': tickets})


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
