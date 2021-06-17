from django.forms import fields
from .models import Contact
from django import forms

# class AddContactForm(forms.Form):
#     contactFirstName = forms.CharField(label='First Name', max_length=30)
#     contactLastName = forms.CharField(label='Last Name', max_length=30)
#     contactEmail = forms.EmailField(label='Email', max_length=254)
#     contactPhoneNumber = forms.CharField(label='Phone Number', max_length=11)

class AddContactForm(forms.ModelForm):

    contactEmail = forms.EmailField(label='Email', max_length=254)
    class Meta:
        model = Contact
        fields = '__all__'
        labels = {'contactFirstName':'First Name',
                   'contactLastName':'Last Name',
                   'contactEmail':'Email',
                   'contactPhoneNumber':'Phone Number' }