from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ticket_exchange.models import Person, Event, Ticket, BaseTicket


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'autocomplete': 'off', 'class': 'form-control'})
        self.fields['location'].widget.attrs.update({'autocomplete': 'off', 'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'autocomplete': 'off', 'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'autocomplete': 'off', 'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'autocomplete': 'off', 'class': 'date_form_input form-control'})
        self.fields['end_date'].widget.attrs.update({'autocomplete': 'off', 'class': 'date_form_input form-control'})

    class Meta:
        model = Event
        fields = ('name', 'location', 'city', 'country', 'start_date', 'end_date')


class UploadBaseTicketNew(forms.Form):
    pdf_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=True)


class UploadBaseTicketEdit(forms.Form):
    pdf_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)


class BaseTicketPriceForm(forms.ModelForm):
    price = forms.DecimalField(required=True, min_value=0.01)

    def __init__(self, *args, **kwargs):
        super(BaseTicketPriceForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs.update({'autocomplete': 'off', 'class': 'form-control'})

    class Meta:
        model = BaseTicket
        fields = ('price',)

