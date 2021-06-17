from django.shortcuts import render
from django.http import HttpResponse

from .forms import AddContactForm


def index(request):
    return render(request, 'contactbook/index.html')

def addContact(request):
    if request.method == 'POST': # if the user submitted the form
        filledForm = AddContactForm(request.POST)
        if filledForm.is_valid():
            filledForm.save()
            note = '{} {} has been added to the contact book.'.format(filledForm.cleaned_data['contactFirstName'], filledForm.cleaned_data['contactLastName'])
            newForm = AddContactForm()
            return render(request, 'contactbook/addContact.html', {'addContactForm':newForm, 'note':note})
    else:
        form = AddContactForm()
        return render(request, 'contactbook/addContact.html', {'addContactForm':form})