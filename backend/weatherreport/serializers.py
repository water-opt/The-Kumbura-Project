from rest_framework import serializers
from .models import weather_report

class weatherReportSerializers(serializers.ModelSerializer):
    class Meta:
        model = weather_report
        fields = '__all__' 