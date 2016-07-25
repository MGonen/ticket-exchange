from django import forms
from .models import Ticket




class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('event', 'seller', 'price')


class DateSearchForm(forms.Form):
    date = forms.CharField(widget=forms.DateInput(attrs={'class': 'date_form_input'}))

