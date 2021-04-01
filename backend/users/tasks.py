from django.core import management

def clearsessions():
    management.call_command('clearsessions')
