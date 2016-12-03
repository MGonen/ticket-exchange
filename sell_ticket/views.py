from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.http import Http404

from ticket_exchange.models import Person, Event, Ticket
from ticket_exchange.views import FACEBOOK_LOGIN_URL
from ticket_exchange.pdfs import ProcessTicket, ProcessBaseTicket, SavePDF
from sell_ticket.forms import NameLocationSearchForm, UploadTicket, TicketPriceForm


@login_required(login_url=FACEBOOK_LOGIN_URL)
def select_event(request):
    search_form = NameLocationSearchForm()

    return render(request, 'sell_ticket/select_event.html', {'form': search_form})


class Sell(View):
    template_name = 'sell_ticket/sell_ticket.html'

    def get_seller(self, user_id):
        try:
            return User.objects.get(id=user_id).person
        except Person.DoesNotExist:
            return Http404

    def get_event(self, event_id):
        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Http404

    def create_ticket(self, event, seller, price, pdf_object):
        ticket = Ticket(event=event, seller=seller, price=price)
        ticket.save()
        ticket.link = SavePDF.save_festival_ticket_return_filepath(pdf_object, ticket.id)
        ticket.save()

    def get_max_ticket_price(self, event_id):
        event = self.get_event(event_id)
        max_price = float(event.baseticket.price) * 1.2
        return "%.2f" % (max_price,)

    def get(self, request, event_id):
        event = self.get_event(event_id)
        price_form = TicketPriceForm()
        upload_form = UploadTicket()
        max_ticket_price = self.get_max_ticket_price(event_id)
        return render(request, self.template_name, {'event': event, 'price_form': price_form, 'upload_form': upload_form, 'max_ticket_price': max_ticket_price})


    def post(self, request, event_id):
        seller = self.get_seller(request.user.id)
        event = self.get_event(event_id)

        price_form = TicketPriceForm(request.POST)
        upload_form = UploadTicket(request.POST, request.FILES)
        max_ticket_price = self.get_max_ticket_price(event_id)

        if not (price_form.is_valid() and upload_form.is_valid() and 'pdf_file' in request.FILES):
            return render(request, self.template_name, {'event': event, 'price_form': price_form, 'upload_form': upload_form, 'max_ticket_price': max_ticket_price})

        # if the forms are valid, and 'pdf_file' is in request.FILES
        pdf_file = request.FILES['pdf_file']
        price = request.POST.get('price')

        pdf_object = ProcessTicket(pdf_file, event_id=event_id)

        # If ticket is safe and valid, then successful is True, otherwise returns message
        if not pdf_object.successful:
            messages.add_message(request, messages.ERROR, pdf_object.message)
            return render(request, self.template_name, {'event': event, 'price_form': price_form, 'upload_form': upload_form, 'max_ticket_price': max_ticket_price})

        self.create_ticket(event=event, seller=seller, price=price, pdf_object=pdf_object)

        messages.add_message(request, messages.SUCCESS, 'Ticket successfully put up for sale')
        return redirect('my_info:tickets_for_sale')





