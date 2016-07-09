from django.apps import AppConfig

class AppNameConfig(AppConfig):
    name = 'ticketexchange'
    verbose_name = "Ticket Exchange"

    def ready(self):
        import ticketexchange.signals