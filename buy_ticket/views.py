from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from ticket_exchange.models import Ticket
from my_info.forms import UserForm
from ticket_exchange.views import FACEBOOK_LOGIN_URL

# Create your views here.

@login_required(login_url=FACEBOOK_LOGIN_URL)
def ticket_details(request, ticket_id):
    # Add filters to template to show the commission fee and total price
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'buy_ticket/ticket_details.html', {'ticket': ticket})



@login_required(login_url=FACEBOOK_LOGIN_URL)
def confirm_personal_details(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    user = get_object_or_404(User, pk=request.user.id)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)

        if user_form.is_valid():
            if 'continue' in request.POST:
                user_form.save()
                return redirect('buy_ticket:select_payment_method', ticket_id)
            elif 'return' in request.POST:
                return redirect('buy_ticket:ticket_details', ticket_id)

    else:
        user_form = UserForm(instance=user)

    return render(request, 'buy_ticket/confirm_personal_details.html', {'user_form': user_form, 'ticket':ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def select_payment_method(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'buy_ticket/select_payment_method.html', {'ticket': ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def payment_confirmation(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'buy_ticket/payment_confirmation.html', {'ticket': ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def payment_failed(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'buy_ticket/payment_failed.html', {'ticket': ticket})

