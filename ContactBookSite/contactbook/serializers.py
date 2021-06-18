from rest_framework import serializers
from .models import Contact

# https://www.django-rest-framework.org/api-guide/serializers/
# this allows querysets and model instances (data) to be converted to native python types

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'