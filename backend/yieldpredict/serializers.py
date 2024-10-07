from rest_framework import serializers
from .models import predictions_yield

class yieldPredictionSerializers(serializers.ModelSerializer):
    class Meta:
        model = predictions_yield
        fields = '__all__' 