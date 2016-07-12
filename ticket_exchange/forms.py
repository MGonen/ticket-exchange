from django import forms
from django.contrib.auth.models import User

from .models import Person, Event, Ticket



class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'location', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'date'}),
        }

class UploadBaseTicket(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        # events = forms.ModelMultipleChoiceField(queryset=Event.objects.all().order_by('-start_date'))
        fields = ('event', 'seller', 'price')


class NameLocationSearchForm(forms.Form):
    search_query = forms.CharField(widget=forms.TextInput(attrs={'id': 'search_input', 'autocomplete': 'off', 'placeholder': 'Search Events'}), label='')

class DateSearchForm(forms.Form):
    date = forms.CharField(widget=forms.DateInput(attrs={'class': 'date'}))