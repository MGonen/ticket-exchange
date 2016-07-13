from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import scriptine

from ticket_exchange.models import Person, Event, Ticket
from ticket_exchange.utils import ticket_complete_check
from ticket_exchange.views import FACEBOOK_LOGIN_URL, pdf_is_safe, save_pdf
from my_info.forms import UserForm
from sell_ticket.forms import NameLocationSearchForm, DateSearchForm, PersonForm4SellTicket, UploadTicket, TicketPriceForm
from TX.settings import BASE_DIR


@login_required(login_url=FACEBOOK_LOGIN_URL)
def select_event(request):
    search_form = NameLocationSearchForm()

    return render(request, 'sell_ticket/select_event.html', {'form': search_form})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def incomplete_ticket_check(request, event_id):
    if request.method == "POST":
        ticket = Ticket.objects.filter(seller=request.user.person).filter(event_id=event_id).filter(complete=False)[0]
        if 'continue' in request.POST:
            return redirect('sell_ticket:event_selected', ticket.id)

        elif 'new' in request.POST:
            Ticket.objects.filter(seller=request.user.person).filter(event_id=event_id).filter(complete=False).delete()
            ticket = Ticket(seller=request.user.person, event_id=event_id)
            ticket.save()
            return redirect('sell_ticket:event_selected', ticket.id)

    else:
        if not incomplete_ticket_exists(request.user.person, event_id):
            Ticket.objects.filter(seller=request.user.person).filter(event_id=event_id).filter(complete=False).delete()
            ticket = Ticket(seller=request.user.person, event_id=event_id)
            ticket.save()
            return redirect('sell_ticket:event_selected', ticket.id)

        else:
            return render(request, 'sell_ticket/incomplete_ticket.html', {})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def event_selected(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        if 'continue' in request.POST:
            return redirect('sell_ticket:upload_pdf', ticket.id)

        elif 'return' in request.POST:
            return redirect('sell_ticket:select_event')

    else:
        return render(request, 'sell_ticket/event_selected.html', {'ticket': ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
@ticket_complete_check
def upload_pdf(request, ticket_id):
    """pdf security analysis and content analysis: text and barcode"""
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        upload_form = UploadTicket(request.POST, request.FILES)

        if upload_form.is_valid():

            if not ticket.link and not 'file' in request.FILES:
                messages.add_message(request, messages.ERROR, 'You need to upload a PDF ticket')
                return render(request, 'sell_ticket/upload_pdf.html', {'upload_form': upload_form, 'ticket': ticket})

            if 'file' in request.FILES:
                file = request.FILES['file']

                if not pdf_is_safe(file):
                    messages.add_message(request, messages.ERROR, 'The PDF was unfortunately deemed unsafe. Please check to make sure it is the correct PDF')
                    return render(request, 'sell_ticket/upload_pdf.html', {'upload_form': upload_form, 'ticket': ticket})

                if not ticket_is_valid(file, ticket_id):
                    messages.add_message(request, messages.ERROR, 'It seems this is not valid. Please make sure you uploaded a valid ticket')
                    return render(request, 'sell_ticket/upload_pdf.html', {'upload_form': upload_form, 'ticket': ticket})

                file_location = save_ticket_pdf(file, ticket_id)
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.link = file_location
                ticket.original_filename = file
                ticket.save()

            if 'continue' in request.POST:
                return redirect('sell_ticket:set_price', ticket_id)
            elif 'return' in request.POST:
                return redirect('sell_ticket:event_selected', ticket_id)

    else:
        upload_form = UploadTicket()

    return render(request, 'sell_ticket/upload_pdf.html', {'upload_form': upload_form, 'ticket':ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
@ticket_complete_check
def set_price(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        form = TicketPriceForm(request.POST, instance=ticket)

        if form.is_valid():
            ticket.price = request.POST.get('price')
            ticket.save()

            if 'continue' in request.POST:
                return redirect('sell_ticket:personal_details', ticket_id)
            elif 'return' in request.POST:
                return redirect('sell_ticket:upload_pdf', ticket_id)

    else:
        form = TicketPriceForm(instance=ticket)

    return render(request, 'sell_ticket/set_price.html', {'form': form, 'ticket': ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
@ticket_complete_check
def personal_details(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    user = get_object_or_404(User, pk=request.user.id)
    person = get_object_or_404(Person, pk=request.user.person.id)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        person_form = PersonForm4SellTicket(request.POST, instance=person)

        if person_form.is_valid() and user_form.is_valid():
            if 'continue' in request.POST:
                person_form.save()
                user_form.save()
                return redirect('sell_ticket:completion', ticket_id)
            elif 'return' in request.POST:
                return redirect('sell_ticket:set_price', ticket_id)


    else:
        person_form = PersonForm4SellTicket(instance=person)
        user_form = UserForm(instance=user)

    return render(request, 'sell_ticket/personal_details.html', {'person_form': person_form, 'user_form': user_form, 'ticket':ticket})


@login_required(login_url=FACEBOOK_LOGIN_URL)
@ticket_complete_check
def completion(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":


        if 'continue' in request.POST:
            missing_ticket_info = ticket_complete(request, ticket_id)
            if missing_ticket_info:
                messages.add_message(request, messages.ERROR, "Unfortunately you're missing some info to put this ticket up for sale. You are still missing: %s" % (missing_ticket_info,))
                return render(request, 'sell_ticket/completion.html', {'ticket': ticket})
            ticket.complete = True
            ticket.save()
            return redirect('my_info:tickets_for_sale')
        elif 'return' in request.POST:
            return redirect('sell_ticket:personal_details', ticket_id)

    return render(request, 'sell_ticket/completion.html', {'ticket': ticket})


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


def ticket_complete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    missing_ticket_info = ""

    if not ticket.event:
        missing_ticket_info +="Event, "
    if not ticket.original_filename:
        missing_ticket_info += "PDF, "
    if not ticket.price:
        missing_ticket_info += "Ticket Price, "
    if not ticket.seller.bank_account:
        missing_ticket_info += "Bank Account (Personal Details)"

    return missing_ticket_info


def incomplete_ticket_exists(person, event_id):
    incomplete_ticket_queryset = Ticket.objects.filter(seller=person).filter(event_id=event_id).filter(complete=False)

    if not incomplete_ticket_queryset.exists():
        return False

    else:
        incomplete_ticket = incomplete_ticket_queryset[0]

        if (not incomplete_ticket.link) and (not incomplete_ticket.price):
            return False

    return True