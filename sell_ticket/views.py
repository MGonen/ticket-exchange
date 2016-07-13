from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ticket_exchange.models import Person, Event, Ticket
from sell_ticket.forms import NameLocationSearchForm, DateSearchForm, UserForm, PersonForm, UploadTicket, PriceForm
from ticket_exchange.utils import ticket_complete_check

from ticket_exchange.views import FACEBOOK_LOGIN_URL, pdf_is_safe, save_pdf
import scriptine

from TX.settings import BASE_DIR


@login_required(login_url=FACEBOOK_LOGIN_URL)
def select_event(request):
    form = NameLocationSearchForm()

    return render(request, 'sell_ticket/select_event.html', {'form': form})


@login_required(login_url=FACEBOOK_LOGIN_URL)
def incomplete_ticket_check(request, event_id):
    if request.method == "POST":
        if 'continue' in request.POST:
            return redirect('sell_ticket:ticket_creation', event_id, 0)
        elif 'new' in request.POST:
            return redirect('sell_ticket:ticket_creation', event_id, 1)

    else:
        if Ticket.objects.filter(seller=request.user.person).filter(event_id=event_id).filter(complete=False).exists():
            return render(request, 'sell_ticket/incomplete_ticket.html', {})

        else:
            return redirect('sell_ticket:ticket_creation', event_id, 1)


@login_required(login_url=FACEBOOK_LOGIN_URL)
def ticket_creation(request, event_id, create_new_ticket):
    create_new_ticket = int(create_new_ticket)
    event = Event.objects.get(id=event_id)
    incomplete_ticket = Ticket.objects.filter(seller=request.user.person).filter(event_id=event_id).filter(complete=False)

    if create_new_ticket and incomplete_ticket.exists():
        incomplete_ticket[0].delete()

    if request.method == "POST":
        if 'continue' in request.POST:
            if create_new_ticket:
                ticket = Ticket(seller=request.user.person, event=event)
                ticket.save()
            else:
                ticket = incomplete_ticket[0]

            return redirect('sell_ticket:upload_ticket', ticket.id)

        elif 'return' in request.POST:
            return redirect('sell_ticket:select_event')

    else:
        return render(request, 'sell_ticket/event_selected.html', {'event': event})



@login_required(login_url=FACEBOOK_LOGIN_URL)
@ticket_complete_check
def upload_ticket(request, ticket_id):
    """pdf security analysis and content analysis: text and barcode"""
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        upload_form = UploadTicket(request.POST, request.FILES)

        if 'return' in request.POST:
            redirect('sell_ticket:ticket_creation', ticket_id, 0)

        if upload_form.is_valid():

            if not ticket.link and not 'file' in request.FILES:
                messages.add_message(request, messages.ERROR, 'You need to upload a PDF ticket')
                # return redirect('sell_ticket:upload_ticket', ticket_id)
                return render(request, 'sell_ticket/upload_ticket.html', {'upload_form': upload_form, 'ticket_original_filename':ticket.original_filename})

            if 'file' in request.FILES:
                file = request.FILES['file']


                if not pdf_is_safe(file):
                    messages.add_message(request, messages.ERROR, 'The PDF was unfortunately deemed unsafe. Please check to make sure it is the correct PDF')
                    return render(request, 'sell_ticket/upload_ticket.html', {'upload_form': upload_form, 'ticket_original_filename':ticket.original_filename})

                if not ticket_is_valid(file, ticket_id):
                    messages.add_message(request, messages.ERROR, 'It seems this is not valid. Please make sure you uploaded a valid ticket')
                    return render(request, 'sell_ticket/upload_ticket.html', {'upload_form': upload_form, 'ticket_original_filename':ticket.original_filename})

                file_location = save_ticket_pdf(file, ticket_id)
                ticket = Ticket.objects.get(id=ticket_id)
                ticket.link = file_location
                ticket.original_filename = file
                ticket.save()
            return redirect('sell_ticket:set_price', ticket_id)

    else:
        upload_form = UploadTicket()

    return render(request, 'sell_ticket/upload_ticket.html', {'upload_form': upload_form, 'ticket_original_filename':ticket.original_filename})


@login_required(login_url=FACEBOOK_LOGIN_URL)
@ticket_complete_check
def set_price(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        form = PriceForm(request.POST)

        if form.is_valid():
            if 'continue' in request.POST:
                ticket.price = request.POST.get('price')
                if not ticket.price:
                    messages.add_message(request, messages.ERROR, 'You need to set a price for the ticket to continue')
                    return redirect('sell_ticket:set_price', ticket_id)

                ticket.save()

                return redirect('sell_ticket:personal_details', ticket_id)
            elif 'return' in request.POST:
                return redirect('sell_ticket:upload_ticket', ticket_id)

    else:
        print 'ticket price', ticket.price
        if ticket.price:
            form = PriceForm(initial={'price':ticket.price})
        else:
            form = PriceForm()

    return render(request, 'sell_ticket/set_price.html', {'form': form})


@login_required(login_url=FACEBOOK_LOGIN_URL)
@ticket_complete_check
def personal_details(request, ticket_id):
    user = get_object_or_404(User, pk=request.user.id)
    person = get_object_or_404(Person, pk=request.user.person.id)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        person_form = PersonForm(request.POST, instance=person)

        if person_form.is_valid() and user_form.is_valid():
            if 'continue' in request.POST:
                person_form.save()
                user_form.save()
                return redirect('sell_ticket:completion', ticket_id)
            elif 'return' in request.POST:
                return redirect('sell_ticket:set_price', ticket_id)


    else:
        person_form = PersonForm(instance=person)
        user_form = UserForm(instance=user)

    return render(request, 'sell_ticket/personal_details.html', {'person_form': person_form, 'user_form': user_form})


@login_required(login_url=FACEBOOK_LOGIN_URL)
@ticket_complete_check
def completion(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":


        if 'continue' in request.POST:
            missing_ticket_info = ticket_complete(request, ticket_id)
            if missing_ticket_info:
                messages.add_message(request, messages.ERROR, "Unfortunately you're missing some info to put this ticket up for sale. You are still missing: %s" % (missing_ticket_info,))
                return render(request, 'sell_ticket/completion.html', {'ticket': ticket})
            ticket.complete = True
            ticket.save()
            return redirect('my_info:tickets_for_sale')
        elif 'return' in request.POST:
            return redirect('sell_ticket:personal_details', ticket_id)

    return render(request, 'sell_ticket/completion.html', {'ticket': ticket})


def save_ticket_pdf(file, ticket_id):
    file_location = create_ticket_file_location(ticket_id)
    save_pdf(file, file_location)
    return file_location


def create_ticket_file_location(ticket_id):
    filename = str(ticket_id)
    directory = scriptine.path(BASE_DIR).joinpath('tickets')
    file_location = directory.joinpath(filename)
    file_location += '.pdf'

    return file_location


def process_pdf(request, file):
    return


def ticket_is_valid(file, event_id):
    return True

def ticket_complete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    missing_ticket_info = ""

    if not ticket.event:
        missing_ticket_info +="-Event "
    if not ticket.original_filename:
        missing_ticket_info += "-PDF "
    if not ticket.price:
        missing_ticket_info += "-Ticket Price "

    return missing_ticket_info

