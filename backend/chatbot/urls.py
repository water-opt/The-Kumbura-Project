from django.urls import path
from .views import _user_query

urlpatterns = [
    path('user/query/', _user_query, name='user-query')
]
