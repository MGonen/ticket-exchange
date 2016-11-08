from django.shortcuts import render, redirect

from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt

from ticket_exchange.models import Person, Event, Ticket, BaseTicket
from events.forms import UploadBaseTicketNew, UploadBaseTicketEdit, EventForm, BaseTicketPriceForm
from django.contrib.admin.views.decorators import staff_member_required

from TX.settings import BASE_DIR, STATIC_ROOT

from django.contrib import messages

import scriptine
import time



@staff_member_required
def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        base_ticket_price_form = BaseTicketPriceForm(request.POST)
        upload_form = UploadBaseTicketNew(request.POST, request.FILES)

        if event_form.is_valid() and base_ticket_price_form.is_valid() and upload_form.is_valid():
            file = request.FILES['file']
            price = request.POST.get('price')

            if not pdf_is_safe(file):
                messages.add_message(request, messages.ERROR, 'The PDF was unfortunately deemed unsafe. Please check to make sure it is the correct PDF')
                return render(request, 'events/event_details.html', {'upload_form': upload_form, 'event_form': event_form, 'base_ticket_price_form': base_ticket_price_form})

            event = event_form.save()
            create_base_ticket_object(file, event, price)

            messages.add_message(request, messages.SUCCESS, 'The event has been succesfully created')
            return redirect('buy_ticket:event_tickets', event.id)

        else:
            return render(request, 'events/event_details.html', {'upload_form': upload_form, 'event_form': event_form, 'base_ticket_price_form': base_ticket_price_form})

    else:
        event_form = EventForm()
        upload_form = UploadBaseTicketNew()
        base_ticket_price_form = BaseTicketPriceForm()
        return render(request, 'events/event_details.html', {'upload_form': upload_form, 'event_form': event_form, 'base_ticket_price_form': base_ticket_price_form})


@staff_member_required
def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    base_ticket = BaseTicket.objects.get(event_id=event_id)

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        base_ticket_price_form = BaseTicketPriceForm(request.POST, instance=base_ticket)
        upload_form = UploadBaseTicketEdit(request.POST, request.FILES)

        if not base_ticket.link and not 'file' in request.FILES:
            messages.add_message(request, messages.ERROR, 'You need to upload a PDF ticket')
            return redirect('events:edit_event', event_id)

        if event_form.is_valid() and base_ticket_price_form.is_valid() and upload_form.is_valid():
            base_ticket.price = request.POST.get('price')

            if 'file' in request.FILES and not pdf_is_safe(file):
                messages.add_message(request, messages.ERROR, 'The PDF was unfortunately deemed unsafe. Please check to make sure it is the correct PDF')
                return redirect('events:edit_event', event_id)

            elif 'file' in request.FILES and pdf_is_safe(file):
                base_ticket.file = file

            base_ticket.save()
            event = event_form.save()

            messages.add_message(request, messages.SUCCESS, 'The event has been succesfully saved')
            return redirect('events:event_tickets', event.id)

        else:
            return render(request, 'events/event_details.html',
                          {'upload_form': upload_form, 'event_form': event_form,
                           'base_ticket_price_form': base_ticket_price_form, 'base_ticket': base_ticket})

    else:
        event_form = EventForm(instance=event)
        upload_form = UploadBaseTicketEdit()
        base_ticket_price_form = BaseTicketPriceForm(instance=base_ticket)
        return render(request, 'events/event_details.html',
                      {'upload_form': upload_form, 'event_form': event_form,
                       'base_ticket_price_form': base_ticket_price_form, 'base_ticket': base_ticket})


def pdf_is_safe(file):
    return True


def create_base_ticket_object(file, event, price):
    file_location = create_base_ticket_file_location(event.id)
    save_pdf(file, file_location)
    base_ticket = BaseTicket(event=event, details='Will come later', link=file_location, price=price)
    base_ticket.save()


def save_pdf(file, file_location):
    with open(file_location, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def create_base_ticket_file_location(event_id):
    filename = str(event_id)
    tickets_directory = scriptine.path(STATIC_ROOT).joinpath('tickets')
    if not tickets_directory.exists():
        tickets_directory.mkdir()

    base_tickets_directory = tickets_directory.joinpath('base_tickets')
    if not base_tickets_directory.exists():
        base_tickets_directory.mkdir()

    file_location = base_tickets_directory.joinpath(filename)
    file_location += '.pdf'
    return file_location



