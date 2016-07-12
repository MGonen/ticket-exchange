from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User


from ticket_exchange.models import Person, Event, Ticket
from sell_ticket.forms import NameLocationSearchForm, DateSearchForm, UserForm, PersonForm


def select_event(request):
    form = NameLocationSearchForm()

    return render(request, 'sell_ticket/select_event.html', {'form': form})


def selected_event(request, event_id):
    print 'arrived at select-event view'
    event = Event.objects.get(id=event_id)
    return render(request, 'sell_ticket/selected_event.html', {'event': event})


def upload_ticket(request):
    """pdf security analysis and content analysis: text and barcode"""
    return render(request, 'sell_ticket/upload_ticket.html', {})


def set_price(request):
    return render(request, 'sell_ticket/set_price.html', {})


def personal_details(request):
    return render(request, 'sell_ticket/personal_details.html', {})

def confirm_details(request):
    # user = get_object_or_404(User, pk=request.user.id)
    # person = get_object_or_404(Person, pk=request.user.person.id)
    #
    # if request.method == "POST":
    #     user_form = UserForm(request.POST, instance=user)
    #     person_form = PersonForm(request.POST, instance=person)
    #
    #     if person_form.is_valid() and user_form.is_valid():
    #         person_form.save()
    #         user_form.save()
    #         return redirect('home')
    #
    # else:
    #     person_form = PersonForm(instance=person)
    #     user_form = UserForm(instance=user)
    #
    # return render(request, 'sell_ticket/user_details.html', {'person_form': person_form, 'user_form': user_form})

    return render(request, 'sell_ticket/user_details.html', {})



def confirmation(request):
    return render(request, 'sell_ticket/confirmation.html', {})
