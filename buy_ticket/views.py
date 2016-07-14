from django.shortcuts import render

# Create your views here.


def ticket_details(request, ticket_id):
    return render(request, 'buy_ticket/ticket_details.html', {})