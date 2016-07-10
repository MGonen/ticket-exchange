from django.shortcuts import render, redirect, HttpResponseRedirect

from django.core.urlresolvers import reverse
from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

from ticket_exchange.models import Person, Event, Ticket
from ticket_exchange.forms import NameLocationSearchForm, DateSearchForm, UploadBaseTicket, EventForm
from django.contrib.admin.views.decorators import staff_member_required

from TX.settings import BASE_DIR
# Create your views here.

from django.contrib import messages


import datetime
import calendar
import scriptine


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


def confirmation(request):
    return render(request, 'sell_ticket/confirmation.html', {})
