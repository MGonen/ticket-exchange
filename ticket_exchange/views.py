from django.shortcuts import render, redirect, HttpResponse, Http404

from django.core.urlresolvers import reverse
from jsonview.decorators import json_view
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from ticket_exchange.models import Event, Ticket
from django.contrib.auth.views import logout as auth_logout

import datetime
import calendar


FACEBOOK_LOGIN_URL = '/login/facebook'


def home(request):
    if request.method == "POST":
        if 'sell' in request.POST:
            print 'sell ticket'
            return redirect('sell_ticket:select_event')
        elif 'buy' in request.POST:
            print 'buy ticket'
            return redirect('buy_ticket:select_event')

    return render(request, 'ticket_exchange/home.html')




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
#     # return render(request, 'ticket_exchange/select_event.html', {'name_location_form': name_location_form})
#
#
#
    events = _get_search_results(search_query)
    return render(request, 'ticket_exchange/advanced_search.html', {'events':events})


def facebook_post_login_handler(request):
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

        event_dicts.append(event_dict)

    return event_dicts


def get_date(date):
    return datetime.datetime.strptime(date, '%d-%m-%Y').strftime('%Y%m%d')


def get_ticket_or_404(ticket_id):
    try:
        return Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Http404
