from django.urls import path
from .views import yield_data, history, delete, updateDate

urlpatterns = [
    path('yield-predict/', yield_data, name='predict-yield'),
    path('yield-all/', history, name='yield-history'),
    path('yield/<int:id>/delete/', delete, name='yield-delete'),
    path('yield/<int:id>/update/', updateDate, name='yield-update')
]
