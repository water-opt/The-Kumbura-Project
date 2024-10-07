from rest_framework import serializers
from .models import prediction_pest

class pestPredictionSerializers(serializers.ModelSerializer):
    class Meta:
        model = prediction_pest
        fields = '__all__' 