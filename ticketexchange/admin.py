from django.contrib import admin
from ticketexchange.models import Event, Ticket, Person
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.


# class TicketInline(admin.TabularInline):
#     model = Person.tickets.through


class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False
    filter_horizontal = ('tickets',)


# Define a new User admin
class CustomUserAdmin(BaseUserAdmin):
    # save_on_top = True
    inlines = (PersonInline, )

# Re-register UserAdmin



class EventAdmin(admin.ModelAdmin):
    # fields = ['name', 'location', 'start_date', 'end_date']
    fieldsets = [
        ('Festival Info', {'fields': ['name', 'location']}),
        ('Date Info', {'fields': ['start_date', 'end_date']})
    ]
    list_display = ('name', 'location', 'start_date', 'end_date')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'seller', 'buyer', 'price')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# admin.site.register(Person, PersonAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)


