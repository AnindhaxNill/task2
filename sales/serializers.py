from django.db.models import fields
from rest_framework import serializers
from .models import salesdb


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = salesdb
        fields='__all__'
