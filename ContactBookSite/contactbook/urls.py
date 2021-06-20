from functools import partial
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', views.apiOverview, name='api'),
    path('api/contact-list/', views.contactList, name='contact-list'),
    path('api/contact-detail/<str:pk>/', views.contactDetail, name='contact-detail'),
    path('api/contact-create/', views.contactCreate, name='contact-create'),
    path('api/contact-update/<str:pk>', views.contactUpdate, name='contact-update'),
    path('api/contact-delete/<str:pk>', views.contactDelete, name='contact-delete'),
    path('add-contact', views.addContact, name='addContact'),
    path('edit-contact/<str:pk>', views.editContact, name='editContact'),
]