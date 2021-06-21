from django.conf.urls import url
from django.shortcuts import redirect, render
from django.contrib.messages import error
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import filters
from .serializers import ContactSerializer

import requests

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
    searchQuery = request.GET.get('search')

    if(searchQuery):
        contacts = contacts.filter(Q(contactFirstName__icontains=searchQuery) | Q(contactLastName__icontains=searchQuery) | Q(contactEmail__icontains=searchQuery))
    
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

# views past this point are actual webpages

def index(request):
    # this page will list all of the contacts

    searchQuery = request.GET.get('search')
    if(searchQuery==None):
        searchQuery = ''
    else:
        note = 'Search results for \'{}\''.format(searchQuery)
        error(request, note)

    # api call to GET the data
    url = 'http://127.0.0.1:8000/api/contact-list/?search=' + searchQuery
    contactList = requests.get(url).json()

    if(len(contactList)<=0):
        hasZeroContacts = True
    else:
        hasZeroContacts = False

    return render(request, 'contactbook/index.html', {'contacts': contactList, 'hasZeroContacts':hasZeroContacts, 'searchQuery':searchQuery})
 
def addContact(request):
    if request.method == 'POST': # if the user submitted the form
        filledForm = AddContactForm(request.POST)
        if filledForm.is_valid(): # validate data before saving
            
            # making the api call to POST the data
            url = 'http://127.0.0.1:8000/api/contact-create/'
            contactData = request.POST
            requests.post(url, contactData)

            note = '{} {} has been added to the contact book.'.format(filledForm.cleaned_data['contactFirstName'], filledForm.cleaned_data['contactLastName'])
            error(request, note)

            return redirect(index)
    else:
        form = AddContactForm()
        return render(request, 'contactbook/add-contact.html', {'addContactForm':form})

def editContact(request, pk):
    if request.method == 'POST': # if the user submitted the form
        filledForm = AddContactForm(request.POST)
        if filledForm.is_valid(): # validate data before saving
            # making the api call to POST the data
            url = 'http://127.0.0.1:8000/api/contact-update/' + pk
            contactData = request.POST
            requests.post(url, contactData)

            note = '{} {} has been updated.'.format(filledForm.cleaned_data['contactFirstName'], filledForm.cleaned_data['contactLastName'])
            error(request, note)

            return redirect(index)
    else:
        # make an api call to get the current data of the specific contact
        url = 'http://127.0.0.1:8000/api/contact-detail/' + pk
        contactData = requests.get(url).json()

        form = AddContactForm(initial=contactData) # create the form object with prefilled data
        return render(request, 'contactbook/edit-contact.html', {'editContactForm':form, 'contact':contactData})

def deleteContact(request, pk):
    if request.method == 'POST': # if the user submitted the form
        
        # make an api call to get the current data of the specific contact
        url = 'http://127.0.0.1:8000/api/contact-detail/' + pk
        contactData = requests.get(url).json()

        # making the api call to POST the data
        url = 'http://127.0.0.1:8000/api/contact-delete/' + pk
        requests.delete(url)

        note = '{} {} has been successfully deleted.'.format(contactData['contactFirstName'], contactData['contactLastName'])
        error(request, note)

        return redirect(index)
    else:
        # make an api call to get the current data of the specific contact
        url = 'http://127.0.0.1:8000/api/contact-detail/' + pk
        contactData = requests.get(url).json()

        return render(request, 'contactbook/delete-contact.html', {'contact':contactData})