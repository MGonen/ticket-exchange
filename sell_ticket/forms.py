from django import forms
from django.contrib.auth.models import User

from ticket_exchange.models import Person, Event, Ticket


class NameLocationSearchForm(forms.Form):
    search_query = forms.CharField(widget=forms.TextInput(attrs={'id': 'search_input', 'autocomplete': 'off', 'placeholder': 'Search Events'}), label='')


class DateSearchForm(forms.Form):
    date = forms.CharField(widget=forms.DateInput(attrs={'class': 'date'}))


class UploadTicket(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('bank_account',)

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class PriceForm(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2)
