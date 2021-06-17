from django.db import models

class Contact(models.Model):
    contactFirstName = models.CharField(max_length=30)
    contactLastName = models.CharField(max_length=30)
    contactEmail = models.EmailField(max_length=254)
    contactPhoneNumber = models.CharField(max_length=12)

    def __str__(self):
        return "{} {}".format(self.contactFirstName, self.contactLastName)