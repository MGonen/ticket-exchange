from django import forms
from django.contrib.auth.models import User

from .models import Person, Event, Ticket



class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['location'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['city'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['country'].widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = Event
        fields = ('name', 'location', 'city', 'country', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'date_form_input'}),
            'end_date': forms.DateInput(attrs={'class': 'date_form_input'}),
        }


class UploadBaseTicket(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('event', 'seller', 'price')


class NameLocationSearchForm(forms.Form):
    search_query = forms.CharField(widget=forms.TextInput(attrs={'id': 'search_input', 'autocomplete': 'off', 'placeholder': 'Search Events'}), label='')


class DateSearchForm(forms.Form):
    date = forms.CharField(widget=forms.DateInput(attrs={'class': 'date_form_input'}))