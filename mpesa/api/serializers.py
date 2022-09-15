from rest_framework import serializers
from mpesa.models import LNMLoan

class LNMOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LNMLoan
        fields = ['id']