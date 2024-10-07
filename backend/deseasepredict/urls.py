from django.urls import path
from .views import predict, history, delete, updateDate

urlpatterns = [
    path('predict/', predict, name='predict'),
    path('pest/all/', history, name='history'),
    path('pest/<int:id>/delete/', delete, name='delete'),
    path('pest/<int:id>/update/', updateDate, name='update')
]