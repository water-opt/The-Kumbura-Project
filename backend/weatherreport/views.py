from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import weather_report
from .serializers import weatherReportSerializers
from rest_framework import status

@api_view(['POST'])
def reportSave(request):
    data = request.data
    user = request.user
    city = data.get('city')
    temperature = data.get('temperature')
    phValue = data.get('phValue')
    windSpeed = data.get('windSpeed')
    rainfall = data.get('rainfall')
    
    report = weather_report(
        user=user, 
        city=city, 
        temperature=temperature, 
        ph_value=phValue, 
        wind_speed=windSpeed, 
        rainfall=rainfall
    )
    report.save()

    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def allReports(request):
    user = request.user
    reports = weather_report.objects.filter(user=user)
    serializer = weatherReportSerializers(reports, many=True)

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteReports(request, id):
    report = weather_report.objects.get(id=id)
    report.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def updateReport(request):
    user = request.user
    report_id = request.data.get('id')

    try:
        report = weather_report.objects.get(id=report_id, user=user)

        report.temperature = request.data.get('temperature', report.temperature)
        report.ph_value = request.data.get('ph_value', report.ph_value)
        report.wind_speed = request.data.get('wind_speed', report.wind_speed)
        report.rainfall = request.data.get('rainfall', report.rainfall)

        report.save()
        serializer = weatherReportSerializers(report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except weatherReportSerializers.DoesNotExist:
        return Response({'error': 'Report not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

