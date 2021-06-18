from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ContactSerializer

from .models import Contact
from .forms import AddContactForm

@api_view(['GET']) # only allow get method here
def apiOverview(request):
    apiUrls = {
        'List': '/contact-list/',
        'Detailed View': '/contact-detail/<str:pk>/',
        'Create': '/contact-create/',
        'Update': '/contact-update/<str:pk>/',
        'Delete': '/contact-delete/<str:pk>/',
    }

    return Response(apiUrls)

@api_view(['GET']) 
def contactList(request):
    contacts = Contact.objects.all()
    serializer = ContactSerializer(contacts, many=True) # make the data python friendly
    return Response(serializer.data)

@api_view(['GET']) 
def contactDetail(request, pk):
    contacts = Contact.objects.get(id=pk) # get specific contact via id
    serializer = ContactSerializer(contacts, many=False) # many=false because i am only getting one object
    return Response(serializer.data)

@api_view(['POST']) 
def contactCreate(request):
    serializer = ContactSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['POST']) 
def contactUpdate(request, pk):
    contact = Contact.objects.get(id=pk)
    serializer = ContactSerializer(instance=contact, data=request.data)
    
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE']) 
def contactDelete(request, pk):
    contact = Contact.objects.get(id=pk)
    contact.delete()

    return Response('Contact successfully deleted!')

def index(request):
    return render(request, 'contactbook/index.html')

def addContact(request):
    if request.method == 'POST': # if the user submitted the form
        filledForm = AddContactForm(request.POST)
        if filledForm.is_valid(): # validate data before saving
            filledForm.save()
            note = '{} {} has been added to the contact book.'.format(filledForm.cleaned_data['contactFirstName'], filledForm.cleaned_data['contactLastName'])
            newForm = AddContactForm()
            return render(request, 'contactbook/addContact.html', {'addContactForm':newForm, 'note':note})
    else:
        form = AddContactForm()
        return render(request, 'contactbook/addContact.html', {'addContactForm':form})