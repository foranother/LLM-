from rest_framework import serializers
from disease.models import Disease


class DiseaseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = ['id', 'kr', 'en']
        read_only_fields = ['id']
