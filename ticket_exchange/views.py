from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse
from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from ticket_exchange.models import Person, Event, Ticket, BaseTicket
from ticket_exchange.forms import NameLocationSearchForm, DateSearchForm, UploadBaseTicket, EventForm, BaseTicketPriceForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import logout as auth_logout

from TX.settings import BASE_DIR
# Create your views here.

from django.contrib import messages


import datetime
import calendar
import scriptine


FACEBOOK_LOGIN_URL = '/login/facebook'

def home(request):
    if request.method == "POST":
        form = NameLocationSearchForm(request.POST)
        if form.is_valid and "search_button" in request.POST:
            return redirect('advanced_search', search_query=request.POST.get('search_query'))

    else:
        form = NameLocationSearchForm()

    return render(request, 'ticket_exchange/home.html', {'form':form})


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
#     # return render(request, 'ticket_exchange/home.html', {'name_location_form': name_location_form})
#
#
#
    events = _get_search_results(search_query)
    return render(request, 'ticket_exchange/advanced_search.html', {'events':events})



@staff_member_required
def create_event(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        base_ticket_price_form = BaseTicketPriceForm(request.POST)
        upload_form = UploadBaseTicket(request.POST, request.FILES)

        if event_form.is_valid() and base_ticket_price_form.is_valid() and upload_form.is_valid():
            file = request.FILES['file']
            price = request.POST.get('price')

            if not pdf_is_safe(file):
                messages.add_message(request, messages.ERROR, 'The PDF was unfortunately deemed unsafe. Please check to make sure it is the correct PDF')
                return render(request, 'ticket_exchange/create_event.html', {'upload_form': upload_form, 'event_form': event_form, 'base_ticket_price_form': base_ticket_price_form})

            event = event_form.save()
            create_base_ticket_object(file, event, price)

            messages.add_message(request, messages.SUCCESS, 'The event has been succesfully created')
            return redirect('event_tickets', event.id)

        else:
            return render(request, 'ticket_exchange/create_event.html', {'upload_form': upload_form, 'event_form': event_form, 'base_ticket_price_form': base_ticket_price_form})

    else:
        event_form = EventForm()
        upload_form = UploadBaseTicket()
        base_ticket_price_form = BaseTicketPriceForm()
        return render(request, 'ticket_exchange/create_event.html', {'upload_form': upload_form, 'event_form': event_form, 'base_ticket_price_form': base_ticket_price_form})



def event_tickets(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    tickets = Ticket.objects.filter(event_id=event.id).filter(bought=False).filter(complete=True).filter(potential_buyer__isnull=True).order_by('price')
    tickets_available = len(Ticket.objects.filter(event_id=event.id).filter(bought=False))
    tickets_sold = len(Ticket.objects.filter(event_id=event.id).filter(bought=True))

    return render(request, 'ticket_exchange/event_tickets.html', {'event': event, 'tickets':tickets, 'tickets_available': tickets_available, 'tickets_sold': tickets_sold})


def facebook_login_handler(request):
    return HttpResponse('<script type="text/javascript">window.opener.location.href = window.opener.location.href;window.close();</script>')


def fb_logout(request):
    redirect_url = request.build_absolute_uri(reverse('home'))
    access_token = _get_access_token(request.user)

    if access_token:
        fb_logout_url = "https://www.facebook.com/logout.php?next=%s&access_token=%s" % (redirect_url, access_token)
        auth_logout(request)
        return redirect(fb_logout_url)
    else:
        auth_logout(request)
        return redirect('home')


def _get_access_token(user):
    try:
        return user.social_auth.get(provider='facebook').extra_data['access_token']
    except (AttributeError, ObjectDoesNotExist) as e:
        return None


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
        event_dict['city'] = event_object.city
        event_dict['country'] = event_object.country
        date = event_object.start_date
        event_dict['start_date'] = '%s %i %s %i' % (calendar.day_name[date.weekday()], date.day, date.strftime('%B'), date.year)
        # event_dict['end_date'] = event_object.end_date

        event_dicts.append(event_dict)

    return event_dicts


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

def get_date(date):
    return datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y%m%d')

