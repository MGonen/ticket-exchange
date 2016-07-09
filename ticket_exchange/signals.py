from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from ticket_exchange.models import Person


@receiver(post_save, sender=User)
def create_person_object_for_user(sender, **kwargs):
    user = kwargs['instance']

    # create Person when none match user:
    if len(Person.objects.filter(user_id=user.id)) == 0:
        person = Person(user=user)
        person.save()

    # create Person fullname
    print 'signal fullname creation reached'
    person = Person.objects.get(user_id=user.id)
    person.fullname = '%s %s' % (user.first_name, user.last_name)
    person.save()