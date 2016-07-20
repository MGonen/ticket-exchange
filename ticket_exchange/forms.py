from django import forms
from .models import Ticket




class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('event', 'seller', 'price')


class NameLocationSearchForm(forms.Form):
    search_query = forms.CharField(widget=forms.TextInput(attrs={'id': 'search_input', 'autocomplete': 'off', 'placeholder': 'Search Events'}), label='')


class DateSearchForm(forms.Form):
    date = forms.CharField(widget=forms.DateInput(attrs={'class': 'date_form_input'}))

