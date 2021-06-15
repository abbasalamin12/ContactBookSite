from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'contactbook/index.html')

def addContact(request):
    return render(request, 'contactbook/addContact.html')