from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from ticketexchange.models import Person, Event, Ticket
from ticketexchange.forms import PersonForm, UserForm


@staff_member_required
def person_index(request):
    persons = Person.objects.filter(user__is_superuser=False)
    return render(request, 'ticketexchange/Person/person_index.html', {'persons': persons})


@staff_member_required
def person_detail(request, person_pk):
    person = Person.objects.get(id=person_pk)
    return render(request, 'ticketexchange/Person/person_detail.html', {'person': person})


@staff_member_required
def person_edit(request, person_pk):
    user = get_object_or_404(User, pk=request.user.id)
    person = get_object_or_404(Person, pk=request.user.person.id)

    if request.method == "POST":

        if "cancel" in request.POST:
            return redirect('person_index')

        user_form = UserForm(request.POST, instance=user)
        person_form = PersonForm(request.POST, instance=person)

        if person_form.is_valid() and user_form.is_valid():
            person_form.save()
            user_form.save()
            return redirect('person_detail', person_pk=person.pk)

    else:
        person_form = PersonForm(instance=person)
        user_form = UserForm(instance=user)


    return render(request, 'ticketexchange/Person/person_edit.html', {'person_form': person_form, 'user_form': user_form})
