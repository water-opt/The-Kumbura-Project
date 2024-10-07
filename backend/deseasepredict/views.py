import numpy as np
import tensorflow as tf
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from keras.preprocessing import image
from PIL import Image as PILImage
from .models import prediction_pest
from rest_framework import status
from .serializers import pestPredictionSerializers
import wikipedia 

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
NUM_CLASSES = 12  
LEARNING_RATE = 1e-3
LOSS_FUNCTION = 'sparse_categorical_crossentropy'

def create_model(num_classes):
    inputs = tf.keras.Input(shape=(224, 224, 3))

    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical"),
        tf.keras.layers.RandomRotation(0.2),
    ])

    x = data_augmentation(inputs)
    x = tf.keras.layers.Rescaling(1.0 / 255)(x)

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False 

    x = base_model(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss=LOSS_FUNCTION,
        metrics=['accuracy']
    )
    return model

model = create_model(NUM_CLASSES)

class_names = [
    'ants', 'bees', 'beetle', 'caterpillar', 'earthworms', 'earwig',
    'grasshopper', 'moth', 'slug', 'snail', 'wasp', 'weevil'
]

@api_view(['POST'])
def predict(request):
    user = request.user
    if request.method == 'POST':
        img_file = request.FILES['image']

        img = PILImage.open(img_file)
        img = img.resize(IMAGE_SIZE)  
        img_array = image.img_to_array(img) / 255.0  
        img_array = np.expand_dims(img_array, axis=0)  

        predictions = model.predict(img_array)

        predicted_class_index = np.argmax(predictions[0])
        predicted_class_name = class_names[predicted_class_index]

        try:
            summary = wikipedia.summary(predicted_class_name, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            summary = f"Disambiguation error. Multiple pages found: {e.options}"
        except wikipedia.exceptions.PageError:
            summary = "No page found for the predicted class."
        

        prediction_instance = prediction_pest(user=user, predicted_class=predicted_class_name, summary=summary)
        prediction_instance.save()

        return JsonResponse({
            'predicted_class': predicted_class_name,
            'summary': summary
        })
    
@api_view(['GET'])
def history(request):
    predictions = prediction_pest.objects.all()
    serializer = pestPredictionSerializers(predictions, many=True)
    
    return Response(serializer.data)


@api_view(['DELETE'])
def delete(request, id):
    prediction = prediction_pest.objects.get(id=id)
    prediction.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def updateDate(request, id):
    user = request.user
    prediction = prediction_pest.objects.get(id=id, user=user)
    prediction.date_added = request.data.get('date_added')
    prediction.save()

    return Response(status=status.HTTP_200_OK)