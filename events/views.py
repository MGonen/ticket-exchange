from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import Http404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from ticket_exchange.models import Person, Event, Ticket, BaseTicket
from ticket_exchange import messages as message_text
from ticket_exchange.pdfs import ProcessBaseTicket, SavePDF
from events.forms import UploadBaseTicketNew, UploadBaseTicketEdit, EventForm, BaseTicketPriceForm


class CreateEvent(View):
    template_name = 'events/event_details.html'

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateEvent, self).dispatch(*args, **kwargs)

    def create_base_ticket(self, pdf_object, event, price):
        base_ticket = BaseTicket(event=event, price=price)
        base_ticket.save()
        base_ticket.link = SavePDF.save_base_ticket_return_filepath(pdf_object, event.id)
        base_ticket.save()


    def get(self, request):
        event_form = EventForm
        upload_form = UploadBaseTicketNew
        base_ticket_price_form = BaseTicketPriceForm
        return render(request, self.template_name, {'upload_form': upload_form, 'event_form': event_form,
                                                             'base_ticket_price_form': base_ticket_price_form, 'pdf_exists': 'false'})

    def post(self, request):
        event_form = EventForm(request.POST)
        base_ticket_price_form = BaseTicketPriceForm(request.POST)
        upload_form = UploadBaseTicketNew(request.POST, request.FILES)

        if not(event_form.is_valid() and base_ticket_price_form.is_valid() and upload_form.is_valid()):
            return render(request, self.template_name,
                              {'upload_form': upload_form, 'event_form': event_form,
                               'base_ticket_price_form': base_ticket_price_form, 'pdf_exists': 'false'})

        # if the forms were valid
        pdf_file = request.FILES['pdf_file']
        price = request.POST.get('price')

        pdf_object = ProcessBaseTicket(pdf_file)

        if not pdf_object.successful:
            messages.add_message(request, messages.ERROR, pdf_object.message)
            return render(request, self.template_name,
                              {'upload_form': upload_form, 'event_form': event_form,
                               'base_ticket_price_form': base_ticket_price_form, 'pdf_exists': 'false'})

        event = event_form.save()
        self.create_base_ticket(pdf_object, event, price)

        messages.add_message(request, messages.SUCCESS, message_text.event_creation_successful)
        return redirect('buy_ticket:available_tickets', event.id)


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

    def get_pdf_file_or_None(self, files):
        if 'pdf_file' in files:
            return files['pdf_file']
        return None

    def pdf_exists(self, event_id):
        baseticket = self.get_base_ticket(event_id)
        if baseticket.link:
            return 'true'
        return 'false'

    def get(self, request, event_id):
        event = self.get_event(event_id)
        base_ticket = self.get_base_ticket(event_id)

        event_form = EventForm(instance=event)
        upload_form = UploadBaseTicketEdit()
        base_ticket_price_form = BaseTicketPriceForm(instance=base_ticket)
        return render(request, self.template_name,
                      {'upload_form': upload_form, 'event_form': event_form,
                       'base_ticket_price_form': base_ticket_price_form, 'base_ticket': base_ticket, 'event_id': event.id, 'pdf_exists': self.pdf_exists(event_id)})

    def post(self, request, event_id):
        event = self.get_event(event_id)
        base_ticket = self.get_base_ticket(event_id)

        event_form = EventForm(request.POST, instance=event)
        base_ticket_price_form = BaseTicketPriceForm(request.POST, instance=base_ticket)
        upload_form = UploadBaseTicketEdit(request.POST, request.FILES)

        if not(event_form.is_valid() and base_ticket_price_form.is_valid() and upload_form.is_valid()):
            return render(request, self.template_name,
                          {'upload_form': upload_form, 'event_form': event_form,
                           'base_ticket_price_form': base_ticket_price_form, 'base_ticket': base_ticket,
                           'event_id': event.id, 'pdf_exists': self.pdf_exists(event_id)})

        # if forms are valid:
        pdf_file = self.get_pdf_file_or_None(request.FILES)

        if pdf_file:
            pdf_object = ProcessBaseTicket(pdf_file)

            if not pdf_object.successful:
                messages.add_message(request, messages.ERROR, pdf_object.message)
                return render(request, self.template_name,
                          {'upload_form': upload_form, 'event_form': event_form,
                           'base_ticket_price_form': base_ticket_price_form, 'base_ticket': base_ticket,
                           'event_id': event.id, 'pdf_exists': self.pdf_exists(event_id)})

            else:
                base_ticket.link = SavePDF.save_base_ticket_return_filepath(pdf_object, event_id)

        base_ticket.price = request.POST.get('price')
        base_ticket.save()
        event = event_form.save()

        messages.add_message(request, messages.SUCCESS, message_text.event_update_successful)
        return redirect('buy_ticket:available_tickets', event.id)





