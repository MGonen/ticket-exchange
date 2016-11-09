from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import Http404
from django.contrib import messages

from ticket_exchange.models import Person, Event, Ticket, BaseTicket
from ticket_exchange import messages as message_text
from events.forms import UploadBaseTicketNew, UploadBaseTicketEdit, EventForm, BaseTicketPriceForm
from django.contrib.admin.views.decorators import staff_member_required

from django.conf import settings

import scriptine
import time


class CreateEvent(View):
    template_name = 'events/event_details.html'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateEvent, self).dispatch(*args, **kwargs)

    def get(self, request):
        event_form = EventForm()
        upload_form = UploadBaseTicketNew()
        base_ticket_price_form = BaseTicketPriceForm()
        return render(request, self.template_name, {'upload_form': upload_form, 'event_form': event_form,
                                                             'base_ticket_price_form': base_ticket_price_form})

    def post(self, request):
        event_form = EventForm(request.POST)
        base_ticket_price_form = BaseTicketPriceForm(request.POST)
        upload_form = UploadBaseTicketNew(request.POST, request.FILES)

        if event_form.is_valid() and base_ticket_price_form.is_valid() and upload_form.is_valid():
            file = request.FILES['file']
            price = request.POST.get('price')

            if not pdf_is_safe(file):
                messages.add_message(request, messages.ERROR, message_text.unsafe_pdf)
                return render(request, self.template_name,
                              {'upload_form': upload_form, 'event_form': event_form,
                               'base_ticket_price_form': base_ticket_price_form})

            event = event_form.save()
            create_base_ticket_object(file, event, price)

            messages.add_message(request, messages.SUCCESS, message_text.event_creation_successful)
            return redirect('buy_ticket:available_tickets', event.id)

        else:
            messages.add_message(request, messages.ERROR, message_text.event_creation_failed)
            return render(request, self.template_name, {'upload_form': upload_form, 'event_form': event_form,
                                                                 'base_ticket_price_form': base_ticket_price_form})


class EditEvent(View):
    template_name = 'events/event_details.html'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(EditEvent, self).dispatch(*args, **kwargs)

    def get_event(self, event_id):
        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise Http404

    def get_base_ticket(self, event_id):
        try:
            return BaseTicket.objects.get(id=event_id)
        except BaseTicket.DoesNotExist:
            raise Http404


    def get(self, request, event_id):
        event = self.get_event(event_id)
        base_ticket = self.get_base_ticket(event_id)

        event_form = EventForm(instance=event)
        upload_form = UploadBaseTicketEdit()
        base_ticket_price_form = BaseTicketPriceForm(instance=base_ticket)
        return render(request, self.template_name,
                      {'upload_form': upload_form, 'event_form': event_form,
                       'base_ticket_price_form': base_ticket_price_form, 'base_ticket': base_ticket, 'event_id': event.id})


    def post(self, request, event_id):
        event = self.get_event(event_id)
        base_ticket = self.get_base_ticket(event_id)

        event_form = EventForm(request.POST, instance=event)
        base_ticket_price_form = BaseTicketPriceForm(request.POST, instance=base_ticket)
        upload_form = UploadBaseTicketEdit(request.POST, request.FILES)

        if not base_ticket.link and not 'file' in request.FILES:
            messages.add_message(request, messages.ERROR, message_text.pdf_needed)
            return redirect('events:edit_event', event_id)

        print 'arrived to just before form checks'
        if event_form.is_valid() and base_ticket_price_form.is_valid() and upload_form.is_valid():
            base_ticket.price = request.POST.get('price')

            if 'file' in request.FILES and not pdf_is_safe(file):
                messages.add_message(request, messages.ERROR, message_text.unsafe_pdf)
                return redirect('events:edit_event', event_id)

            elif 'file' in request.FILES and pdf_is_safe(file):
                base_ticket.file = file

            base_ticket.save()
            event = event_form.save()

            messages.add_message(request, messages.SUCCESS, message_text.event_update_successful)
            return redirect('buy_ticket:available_tickets', event.id)

        else:
            return render(request, self.template_name,
                          {'upload_form': upload_form, 'event_form': event_form,
                           'base_ticket_price_form': base_ticket_price_form, 'base_ticket': base_ticket, 'event_id': event.id})


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
    tickets_directory = scriptine.path(settings.STATIC_ROOT).joinpath('tickets')
    if not tickets_directory.exists():
        tickets_directory.mkdir()

    base_tickets_directory = tickets_directory.joinpath('base_tickets')
    if not base_tickets_directory.exists():
        base_tickets_directory.mkdir()

    file_location = base_tickets_directory.joinpath(filename)
    file_location += '.pdf'
    return file_location



