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

    def __init__(self, *args, **kwargs):
        self.baseticket_price = kwargs.pop('baseticket_price')
        super(TicketPriceForm, self).__init__(*args, **kwargs)

    def clean_price(self):
        price = float(self.cleaned_data['price'])
        max_price = float(self.baseticket_price) * 1.2

        if price > max_price:
            validation_error_text = 'The price of the ticket can only be 20%% more than the original ticket price, in this case %s %.2f' % (u"\u20AC", max_price)
            raise ValidationError(validation_error_text)

        return price


class PersonForm4SellTicket(forms.ModelForm):
    bank_account =  forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(PersonForm4SellTicket, self).__init__(*args, **kwargs)
        self.fields['bank_account'].widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = Person
        fields = ('bank_account',)