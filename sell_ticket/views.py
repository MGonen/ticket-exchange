from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.http import Http404, JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings

import scriptine

from ticket_exchange.models import Person, Event, Ticket
from ticket_exchange import messages as messages_text
from ticket_exchange.views import FACEBOOK_LOGIN_URL
from events.views import pdf_is_safe, save_pdf
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

    def create_ticket(self, event, seller, price, pdf_file):
        ticket = Ticket(event=event, seller=seller, price=price)
        ticket.save()
        file_location = self.save_ticket_pdf(ticket_id=ticket.id, pdf_file=pdf_file)
        ticket.link = file_location
        ticket.save()

    def save_ticket_pdf(self, pdf_file, ticket_id):
        file_location = self.create_ticket_file_location(ticket_id)
        save_pdf(pdf_file, file_location)
        return file_location

    def create_ticket_file_location(self, ticket_id):
        filename = str(ticket_id)
        tickets_directory = scriptine.path(settings.STATIC_ROOT).joinpath('tickets')
        if not tickets_directory.exists():
            tickets_directory.mkdir()

        festival_tickets_directory = tickets_directory.joinpath('festival_tickets')
        if not festival_tickets_directory.exists():
            festival_tickets_directory.mkdir()

        file_location = festival_tickets_directory.joinpath(filename)
        file_location += '.pdf'
        return file_location

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
        render_failed_post_template = render(request, self.template_name, {'event': event, 'price_form': price_form, 'upload_form': upload_form, 'max_ticket_price': max_ticket_price})

        if not (price_form.is_valid() and upload_form.is_valid() and 'pdf_file' in request.FILES):
            return render_failed_post_template

        # if the forms are valid, and 'pdf_file' is in request.FILES
        pdf_file = request.FILES['pdf_file']
        price = request.POST.get('price')

        if not pdf_is_safe(pdf_file):
            messages.add_message(request, messages.ERROR, messages_text.unsafe_pdf)
            return render_failed_post_template

        if not ticket_is_valid(pdf_file, event_id):
            messages.add_message(request, messages.ERROR, messages_text.pdf_invalid)
            return render_failed_post_template

        self.create_ticket(event=event, seller=seller, price=price, pdf_file=pdf_file)

        messages.add_message(request, messages.SUCCESS, 'Ticket successfully put up for sale')
        return redirect('my_info:tickets_for_sale')


def process_pdf(request, pdf_file):
    return


def ticket_is_valid(pdf_file, event_id):
    return True
