from django import forms

from ticket_exchange.models import Person


class NameLocationSearchForm(forms.Form):
    search_query = forms.CharField(widget=forms.TextInput(attrs={'id': 'search_input', 'autocomplete': 'off', 'placeholder': 'Search Events'}), label='')


class DateSearchForm(forms.Form):
    date = forms.CharField(widget=forms.DateInput(attrs={'class': 'date_form_input'}))


class UploadTicket(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=False)


class PriceForm(forms.Form):
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)


class PersonForm4SellTicket(forms.ModelForm):
    bank_account =  forms.CharField(required=True,)

    def __init__(self, *args, **kwargs):
        super(PersonForm4SellTicket, self).__init__(*args, **kwargs)
        self.fields['bank_account'].widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = Person
        fields = ('bank_account',)
