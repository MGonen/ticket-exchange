from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from ticketexchange.models import Person, Event, Ticket
from ticketexchange.forms import TicketForm


# @staff_member_required
# def ticket_index(request):
#     tickets = Ticket.objects.all()
#     return render(request, 'ticketexchange/Ticket/ticket_index.html', {'tickets': tickets})
#
#
# @staff_member_required
# def ticket_detail(request, ticket_pk):
#     ticket = Ticket.objects.get(id=ticket_pk)
#     return render(request, 'ticketexchange/Ticket/ticket_detail.html', {'ticket': ticket})
#
#
# @staff_member_required
# def ticket_new(request):
#     if request.method == "POST":
#
#         if "cancel" in request.POST:
#             return redirect('ticket_index')
#
#         form = TicketForm(request.POST)
#         if form.is_valid():
#             ticket = form.save()
#             return redirect('ticket_detail', ticket_pk=ticket.pk)
#     else:
#         form = TicketForm()
#
#     return render(request, 'ticketexchange/Ticket/ticket_edit.html', {'form': form})
#
#
# @staff_member_required
# def ticket_edit(request, ticket_pk):
#     ticket = get_object_or_404(Ticket, pk=ticket_pk)
#     if request.method == "POST":
#
#         if "cancel" in request.POST:
#             return redirect('ticket_detail')
#
#         form = TicketForm(request.POST, instance=ticket)
#         if form.is_valid():
#             ticket = form.save()
#             return redirect('ticket_detail', ticket_pk=ticket.pk)
#     else:
#         form = TicketForm(instance=ticket)
#
#     return render(request, 'ticketexchange/Ticket/ticket_edit.html', {'form': form})
