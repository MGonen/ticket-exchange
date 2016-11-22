from django import forms
from django.contrib.auth.models import User

from ticket_exchange.models import Person


class PersonForm4MyInfo(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PersonForm4MyInfo, self).__init__(*args, **kwargs)
        self.fields['fullname'].widget.attrs.update({'autocomplete': 'off', 'class': 'form-control'})
        self.fields['iban'].widget.attrs.update({'autocomplete': 'off', 'class': 'form-control'})

    class Meta:
        model = Person
        fields = ('fullname', 'iban',)


class UserForm(forms.ModelForm):
    email = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autocomplete': 'off', 'class': 'form-control'})

    class Meta:
        model = User
        fields = ('email',)
