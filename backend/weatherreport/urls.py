from django.urls import path
from .views import reportSave, allReports, deleteReports, updateReport

urlpatterns = [
    path('report/save/', reportSave, name="weather-report"),
    path('report/all/', allReports, name="all-reports"),
    path('report/<int:id>/delete/', deleteReports, name="delete-report"),
    path('report/update/', updateReport, name="update-report")
]
