from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ticket_exchange.models import Person, Event, Ticket, BaseTicket


class EventForm(forms.ModelForm):
    name = forms.CharField(min_length=2)

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

    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name.replace(' ', '')) < 2:
            raise ValidationError('Ensure this value has at least 2 characters that are not space.')

        return name

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']

        if start_date > end_date:
            raise ValidationError('Ensure that the end date of the event is on the same day, or after the start date.')

        return end_date


class UploadBaseTicketNew(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=True)


class UploadBaseTicketEdit(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)


class BaseTicketPriceForm(forms.ModelForm):
    price = forms.DecimalField(required=True, min_value=0.01)

    class Meta:
        model = BaseTicket
        fields = ('price',)

