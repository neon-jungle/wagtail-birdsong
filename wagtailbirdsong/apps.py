from django.apps import AppConfig

class BirdsongApp(AppConfig):
    name = 'wagtailbirdsong'

    def ready(self):
        import wagtailbirdsong.signals