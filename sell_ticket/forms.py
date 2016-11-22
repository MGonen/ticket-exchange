from django import forms
from django.core.exceptions import ValidationError

from ticket_exchange.models import Person, Ticket


class NameLocationSearchForm(forms.Form):
    search_query = forms.CharField(widget=forms.TextInput(attrs={'id': 'search_input', 'autocomplete': 'off', 'placeholder': 'Search Events'}), label='')


class DateSearchForm(forms.Form):
    date = forms.CharField(widget=forms.DateInput(attrs={'class': 'date_form_input'}))


class UploadTicket(forms.Form):
    pdf_file = forms.FileField(widget=forms.FileInput(attrs={'multiple': False}))


class TicketPriceForm(forms.Form):
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


class PersonForm4SellTicket(forms.ModelForm):
    iban =  forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(PersonForm4SellTicket, self).__init__(*args, **kwargs)
        self.fields['iban'].widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = Person
        fields = ('iban',)