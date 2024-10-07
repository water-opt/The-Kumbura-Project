from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from .models import predictions_yield
from rest_framework import status
from .serializers import yieldPredictionSerializers
import numpy as np

weights = np.array([-51.63070152, -24.01388075, -6.13184188])
bias = 592.49028889047

def predict_yield(soil_quality, environment_factors, irrigation):
    input_features = np.array([soil_quality, environment_factors, irrigation])
    predicted_yield = np.dot(input_features, weights) + bias
    
    return predicted_yield

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def yield_data(request):
    user = request.user
    data = request.data
    soil_quality = data.get('soil_quality')
    environment_factors = data.get('environment_factors')
    irrigation = data.get('irrigation')
    
    soil_quality_mapping = {'Good': 1, 'Bad': 2, 'Moderate': 3}
    environment_factors_mapping = {'Dry': 1, 'Rainy': 2, 'Humid': 3}
    irrigation_mapping = {'Yala': 1, 'Maha': 2}

    soil_quality_num = soil_quality_mapping.get(soil_quality)
    environment_factors_num = environment_factors_mapping.get(environment_factors)
    irrigation_num = irrigation_mapping.get(irrigation)

    predict = predict_yield(soil_quality_num, environment_factors_num, irrigation_num)

    prediction_record = predictions_yield(
        user=user,
        soil_quality=soil_quality,
        environment_factors=environment_factors,
        irrigation=irrigation,
        prediction=str(predict)
    )

    prediction_record.save()

    return Response({'result': predict})

@api_view(['GET'])
def history(request):
    user = request.user
    predictions = predictions_yield.objects.filter(user=user)
    serializer = yieldPredictionSerializers(predictions, many=True)
    
    return Response(serializer.data) 

@api_view(['DELETE'])
def delete(request, id):
    prediction = predictions_yield.objects.get(id=id)
    prediction.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def updateDate(request, id):
    user = request.user
    date = request.data.get('date_added')
    prediction = predictions_yield.objects.get(id=id, user=user)
    prediction.date_added = date
    prediction.save()

    return Response(status=status.HTTP_200_OK)