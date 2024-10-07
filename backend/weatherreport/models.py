from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class weather_report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=50)
    temperature = models.IntegerField(validators=[MinValueValidator(-50), MaxValueValidator(50)])
    ph_value = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(14)])
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    rainfall = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
