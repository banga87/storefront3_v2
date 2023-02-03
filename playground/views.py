from django.shortcuts import render
from .tasks import notify_customers


def say_hello(request):
    notify_customers.delay('MESSAGE!!')
    return render(request, 'hello.html', {'name': 'Angus'})
