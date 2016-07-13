from django import forms
from django.contrib.auth.models import User

from ticket_exchange.models import Person


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('bank_account',)

class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['last_name'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['email'].widget.attrs.update({'autocomplete': 'off'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
