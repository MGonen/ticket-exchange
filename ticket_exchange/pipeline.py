from django.contrib.auth.models import User
from .models import Person


def create_profile(strategy, details, response, user, *args, **kwargs):
    username = user
    user_object = User.objects.get(username=username)

    if Person.objects.filter(user=user_object).exists():
        print 'person object found'
        person = Person.objects.get(user=user_object)
    else:
        print 'new person created'
        person = Person(user=user_object)
        user_object.email = response['email']
        user_object.first_name = details['first_name']
        user_object.last_name = details['last_name']
        user_object.save()

    person.fullname = details['fullname']
    person.photo = _get_profile_picture(response)
    person.save()

    return kwargs


def _get_profile_picture(response):
        return 'http://graph.facebook.com/%s/picture' % response['id']
