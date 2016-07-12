from django import forms
from django.contrib.auth.models import User

from ticket_exchange.models import Person


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('bank_account',)

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


