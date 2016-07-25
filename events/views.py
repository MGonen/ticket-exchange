from django.shortcuts import render, redirect

from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt

from ticket_exchange.models import Person, Event, Ticket, BaseTicket
from events.forms import UploadBaseTicketNew, UploadBaseTicketEdit, EventForm, BaseTicketPriceForm
from django.contrib.admin.views.decorators import staff_member_required

from TX.settings import BASE_DIR

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
            return redirect('events:event_tickets', event.id)

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
            return redirect('events:event_tickets', event_id)


    event = Event.objects.get(pk=event_id)
    tickets_available = len(Ticket.objects.filter(event_id=event.id).filter(bought=False).filter(complete=True))
    tickets_sold = len(Ticket.objects.filter(event_id=event.id).filter(bought=True))

    return render(request, 'events/event_tickets.html', {'event': event, 'tickets_available': tickets_available, 'tickets_sold': tickets_sold})


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


def pdf_is_safe(file):
    return True


def create_base_ticket_object(file, event, price):
    file_location = create_ticket_file_location(event.id)
    save_pdf(file, file_location)
    base_ticket = BaseTicket(event=event, details='Will come later', link=file_location, price=price)
    base_ticket.save()


def save_pdf(file, file_location):
    with open(file_location, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def create_ticket_file_location(event_id):
    filename = str(event_id)
    directory = scriptine.path(BASE_DIR).joinpath('tickets')
    file_location = directory.joinpath(filename)
    file_location += '.pdf'

    return file_location


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

