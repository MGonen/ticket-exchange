from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ticket_exchange.models import Person, Event, Ticket
from sell_ticket.forms import NameLocationSearchForm, DateSearchForm, UserForm, PersonForm, UploadTicket, PriceForm

from ticket_exchange.views import FACEBOOK_LOGIN_URL, pdf_is_safe, save_pdf
import scriptine

from TX.settings import BASE_DIR


@login_required(login_url=FACEBOOK_LOGIN_URL)
def select_event(request):
    # ticket = Ticket(seller=request.user.person)
    # ticket.save()
    form = NameLocationSearchForm()

    return render(request, 'sell_ticket/select_event.html', {'form': form})


def event_selected(request, event_id):
    event = Event.objects.get(id=event_id)
    post_request = request.method == "POST"

    if post_request and 'continue' in request.POST:
        ticket = Ticket(seller=request.user.person, event=event)
        ticket.save()
        print 'new ticket-object gecreeerd'
        return redirect('sell_ticket:upload_ticket', ticket.id)
    elif post_request and 'return' in request.POST:
        return redirect('sell_ticket:select_event')

    else:
        return render(request, 'sell_ticket/event_selected.html', {'event': event})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def upload_ticket(request, ticket_id):
    """pdf security analysis and content analysis: text and barcode"""

    if request.method == "POST":
        upload_form = UploadTicket(request.POST, request.FILES)

        if 'return' in request.POST:
            redirect('sell_ticket:event_selected', ticket_id)

        if upload_form.is_valid():
            file = request.FILES['file']

            if not pdf_is_safe(file):
                messages.add_message(request, messages.ERROR, 'The PDF was unfortunately deemed unsafe. Please check to make sure it is the correct PDF')
                return render(request, 'sell_ticket/upload_ticket.html', {'upload_form': upload_form})

            if not ticket_is_valid(file, ticket_id):
                messages.add_message(request, messages.ERROR, 'It seems this is not valid. Please make sure you uploaded a valid ticket')
                return render(request, 'sell_ticket/upload_ticket.html', {'upload_form': upload_form})

            file_location = save_ticket_pdf(file, ticket_id)
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.link = file_location
            ticket.save()
            return redirect('sell_ticket:set_price', ticket_id)

    else:
        upload_form = UploadTicket()

    return render(request, 'sell_ticket/upload_ticket.html', {'upload_form': upload_form})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def set_price(request, ticket_id):
    if request.method == "POST":
        form = PriceForm(request.POST)

        if form.is_valid():
            if 'continue' in request.POST:
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.price = request.POST.get('price')
                ticket.save()

                return redirect('sell_ticket:personal_details', ticket_id)
            elif 'return' in request.POST:
                return redirect('sell_ticket:upload_ticket', ticket_id)

    else:
        form = PriceForm()

    return render(request, 'sell_ticket/set_price.html', {'form': form})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def personal_details(request, ticket_id):
    user = get_object_or_404(User, pk=request.user.id)
    person = get_object_or_404(Person, pk=request.user.person.id)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        person_form = PersonForm(request.POST, instance=person)

        if person_form.is_valid() and user_form.is_valid():
            if 'continue' in request.POST:
                person_form.save()
                user_form.save()
                return redirect('sell_ticket:confirmation', ticket_id)
            elif 'return' in request.POST:
                return redirect('sell_ticket:set_price', ticket_id)


    else:
        person_form = PersonForm(instance=person)
        user_form = UserForm(instance=user)

    return render(request, 'sell_ticket/personal_details.html', {'person_form': person_form, 'user_form': user_form})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def confirmation(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":


        if 'continue' in request.POST:
            ticket.complete = True
            ticket.save()
            return redirect('my_info:tickets_for_sale')
        elif 'return' in request.POST:
            return redirect('sell_ticket:personal_details', ticket_id)





    return render(request, 'sell_ticket/confirmation.html', {'ticket': ticket})


def save_ticket_pdf(file, ticket_id):
    file_location = create_ticket_file_location(ticket_id)
    save_pdf(file, file_location)
    return file_location


def create_ticket_file_location(ticket_id):
    filename = str(ticket_id)
    directory = scriptine.path(BASE_DIR).joinpath('tickets')
    file_location = directory.joinpath(filename)
    file_location += '.pdf'

    return file_location


def process_pdf(request, file):
    return


def ticket_is_valid(file, event_id):
    return True