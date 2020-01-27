import time

from django.contrib.staticfiles.management.commands.runserver import Command as StaticfilesRunserverCommand
from worker.worker import Worker
from django.conf import settings


class Command(StaticfilesRunserverCommand):
    help = "Starts a lightweight Web server for development and also serves static files."

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

    def get_handler(self, *args, **options):
        handler = super(Command, self).get_handler(*args, **options)
        #custom_handler = options.get('custom_handler', True)
        w = Worker(settings.WORKER_PORT)


        return handler


