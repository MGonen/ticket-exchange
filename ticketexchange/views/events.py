from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from ticketexchange.models import Person, Event, Ticket
from ticketexchange.forms import EventForm

@staff_member_required
def event_index(request):
    events = Event.objects.all()
    return render(request, 'ticketexchange/Event/event_index.html', {'events': events})

# def event_new(request):
#     return render(request, 'ticketexchange/Event/event_edit.html', {})


@staff_member_required
def event_detail(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    return render(request, 'ticketexchange/Event/event_detail.html', {'event': event})




@staff_member_required
def event_new(request):
    if request.method == "POST":

        if "cancel" in request.POST:
            return redirect('event_index')

        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('event_detail', event_pk=event.pk)
    else:
        form = EventForm()

    return render(request, 'ticketexchange/Event/event_edit.html', {'form': form})


@staff_member_required
def event_edit(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    if request.method == "POST":

        if "cancel" in request.POST:
            return redirect('event_detail')

        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            return redirect('event_detail', event_pk=event.pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'ticketexchange/Event/event_edit.html', {'form': form})
