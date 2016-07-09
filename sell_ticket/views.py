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


def select_event(request, event_id=None):
    print 'arrived at select-event view'
    if not event_id:
        return render(request, 'sell_ticket/select_event.html', {})


# Create your views here.
