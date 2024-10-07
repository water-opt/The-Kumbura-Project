from django.db import models
from django.contrib.auth.models import User

class prediction_pest(models.Model):
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    predicted_class = models.CharField(max_length=50)  
    summary = models.TextField()
