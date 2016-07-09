from django.shortcuts import render, redirect, HttpResponseRedirect

from django.core.urlresolvers import reverse
from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

from ticketexchange.models import Person, Event, Ticket
from ticketexchange.forms import NameLocationSearchForm, DateSearchForm, UploadBaseTicket, EventForm
from django.contrib.admin.views.decorators import staff_member_required

from TX.settings import BASE_DIR
# Create your views here.

from django.contrib import messages


import datetime
import calendar
import scriptine


def home(request):
    if request.method == "POST":
        form = NameLocationSearchForm(request.POST)
        if form.is_valid and "search_button" in request.POST:
            return redirect('advanced_search', search_query=request.POST.get('search_query'))

    else:
        form = NameLocationSearchForm()

    return render(request, 'ticketexchange/home.html', {'form':form})


# def admin_home(request):
#     persons = Person.objects.filter(user__is_superuser=False)
#     events = Event.objects.all()
#     tickets = Ticket.objects.all()
#     return render(request, 'ticketexchange/Admin/admin_home.html', {'persons': persons, 'events': events, 'tickets': tickets})



@json_view
@csrf_exempt
def get_ajax_search_results(request, search_query):
    event_objects = _get_search_results(search_query)
    event_dicts = create_event_dicts(event_objects)

    return {'events': event_dicts}


def _get_search_results(search_query):
    """
    If the name of an event starts with the typed search input, it is at the top of the list.
    In other cases the words typed all have to match something in the name of the event to be shown
    """

    split_search_query = search_query.split(' ')
    search_words = filter(lambda item: not item in ['', ' '], split_search_query)

    event_objects = list(Event.objects.filter(Q(name__startswith=search_query) | Q(location__startswith=search_query))[:7])

    event_objects_contains = list(Event.objects.filter(name__contains=search_words[0]))
    for word in search_words[1:]:
        event_objects_contains = filter(lambda item: item in event_objects_contains, Event.objects.filter(Q(name__contains=word) | Q(location__contains=word)))

    event_objects += filter(lambda item: not item in event_objects, event_objects_contains)

    return event_objects[:7]





def create_event_dicts(event_objects):
    event_dicts = []

    for event_object in event_objects:

        event_dict = {}
        event_dict['id'] = event_object.id
        event_dict['name'] = event_object.name
        event_dict['location'] = event_object.location
        date = event_object.start_date
        event_dict['start_date'] = '%s %i %s %i' % (calendar.day_name[date.weekday()], date.day, date.strftime('%B'), date.year)
        # event_dict['end_date'] = event_object.end_date

        event_dicts.append(event_dict)

    return event_dicts


def advanced_search(request, search_query):
#     # name_location_form = NameLocationSearchForm(request.POST)
#     # if request.method == "POST":
#     #     name_location_form = NameLocationSearchForm(request.POST)
#     #     date_form = DateSearchForm(request.POST)
#     #     if name_location_form.is_valid and "search_button" in request.POST:
#     #         return redirect('advanced_search', search_query=request.POST.get('search_query'))
#     #
#     # else:
#     #     name_location_form = NameLocationSearchForm()
#     #
#     # return render(request, 'ticketexchange/home.html', {'name_location_form': name_location_form})
#
#
#
    events = _get_search_results(search_query)
    return render(request, 'ticketexchange/advanced_search.html', {'events':events})


@staff_member_required
def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        upload_form = UploadBaseTicket(request.POST, request.FILES)

        if upload_form.is_valid() and event_form.is_valid():
            file = request.FILES['file']
            event = request.POST.get('name')
            date = get_date(request.POST.get('start_date'))

            if not pdf_is_safe(file):
                messages.add_message(request, messages.ERROR, 'The PDF was unfortunately deemed unsafe. Please check to make sure it is the correct PDF')
                return render(request, 'ticketexchange/create_event.html', {'upload_form': upload_form, 'event_form': event_form})

            save_pdf(file, event, date)

            event = event_form.save()
            messages.add_message(request, messages.SUCCESS, 'The event has been succesfully created')
            return redirect('event_tickets', event.id)

        else:
            messages.add_message(request, messages.ERROR, 'The creation of the event failed. Please try again.')
            return render(request, 'ticketexchange/create_event.html', {'upload_form': upload_form, 'event_form': event_form})

    else:
        event_form = EventForm()
        upload_form = UploadBaseTicket()
        return render(request, 'ticketexchange/create_event.html', {'upload_form': upload_form, 'event_form': event_form})




def handle_uploaded_file(file, event, date):
    if not pdf_is_safe(file):
        return True

    save_pdf(file, event, date)
    return True

def pdf_is_safe(file):
    return True


def save_pdf(file, event, date):
    file_location = create_ticket_file_location(event, date)

    with open(file_location, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def create_ticket_file_location(event, date):
    filename = date + event
    directory = scriptine.path(BASE_DIR).joinpath('tickets')
    file_location = directory.joinpath(filename)
    file_location += '.pdf'

    return file_location

def get_date(date):
    return datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y%m%d')



def event_tickets(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    tickets = Ticket.objects.filter(event_id=event.id)
    return render(request, 'ticketexchange/event_tickets.html', {'event': event, 'tickets':tickets})
