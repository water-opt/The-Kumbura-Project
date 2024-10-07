from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class predictions_yield(models.Model):
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    soil_quality = models.CharField(max_length=20)
    environment_factors = models.CharField(max_length=20)
    irrigation = models.CharField(max_length=20)
    prediction = models.FloatField()