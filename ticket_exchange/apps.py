from django.apps import AppConfig

class AppNameConfig(AppConfig):
    name = 'ticket_exchange'
    verbose_name = "Ticket Exchange"

    def ready(self):
        import ticket_exchange.signals