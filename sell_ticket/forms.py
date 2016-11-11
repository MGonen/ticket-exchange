from django import forms

from ticket_exchange.models import Person, Ticket


class NameLocationSearchForm(forms.Form):
    search_query = forms.CharField(widget=forms.TextInput(attrs={'id': 'search_input', 'autocomplete': 'off', 'placeholder': 'Search Events'}), label='')


class DateSearchForm(forms.Form):
    date = forms.CharField(widget=forms.DateInput(attrs={'class': 'date_form_input'}))


class UploadTicket(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))


class TicketPriceForm(forms.ModelForm):
    price = forms.DecimalField(required=True, min_value=0.01)

    def __init__(self, *args, **kwargs):
        super(TicketPriceForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Ticket
        fields = ('price',)


class PersonForm4SellTicket(forms.ModelForm):
    bank_account =  forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(PersonForm4SellTicket, self).__init__(*args, **kwargs)
        self.fields['bank_account'].widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = Person
        fields = ('bank_account',)