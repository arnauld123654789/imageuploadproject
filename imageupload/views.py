import uuid
from pathlib import Path

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import os
from .models import ImageModel
from django.core.files.base import ContentFile
import base64


from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as imageTensor
import numpy as np




def upload_image(request):
    if request.method == 'POST':
        # Get the uploaded image from the request
        image = request.FILES['image']

        # Create a unique filename for the image
        filename = f"{request.POST['name']}_{image.name}"

        # Save the image to the 'imageformodel' directory
        image_path = os.path.join(settings.MEDIA_ROOT, filename)
        with open(image_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Save the image information to the database
        image_model = ImageModel(name=request.POST['name'], image=filename)
        image_model.save()

        # Redirect the user to a success page
        return redirect('success')

    # If the request method is GET, render the upload form
    return render(request, 'upload.html')
def success(request):
    return render(request, 'success.html')

def ok(request):
    return render(request, 'ok.html')

def image_list(request):
    images = ImageModel.objects.all()
    return render(request, 'image_list.html', {'images': images})
def index(request):
    return render(request, 'pages/index.html')
def pageDiagnostic(request):
    return render(request, 'pages/pageDiagnostic.html')


def faireDiagnostic(request):
    if request.method == 'POST':
        # Get the image data from the hidden input field
        image_data = request.POST.get('image_data')

        # Decode the base64-encoded image data and save it to a file
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]

        nameImage = f'{uuid.uuid4()}.{ext}'
        data = ContentFile(base64.b64decode(imgstr), name=nameImage)

        # Create a new ImageModel instance and save it to the database
        image = ImageModel(image=data, name=nameImage)
        image.save()

        # Redirect the user to the success page

        # # Charger le modèle enregistré
        model = load_model(Path(__file__).resolve().parent.parent / 'improved_model.h5')

        # Charger et prétraiter une image pour les tests
        img_path = Path(__file__).resolve().parent.parent / 'media/imageformodel/' / image.name
        img = imageTensor.load_img(img_path, target_size=(256, 256))
        img_array = imageTensor.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalisation des pixels

        # Faire une prédiction avec le modèle chargé
        predictions = model.predict(img_array)

        # Charger les noms des classes (à adapter en fonction de votre modèle)
        class_names = {0: 'acarien rouge', 1: 'alternariose', 2: 'bonne_santé',
                       3: 'enroulement_jaune_foliaire_de_la_tomate', 4: 'mildiou_de_la_tomate',
                       5: 'mildiou_du_feuillage_de_la_tomate', 6: 'mosaïque_de_la_tomate', 7: 'septoriose',
                       8: 'tache_bacterienne_de_la_tomate',
                       9: 'tavelure(tache_cerclé)'}  # Dictionnaire d'indices vers noms de classes

        # Obtenir l'indice de la classe prédite
        predicted_class_index = np.argmax(predictions)

        # Afficher le nom de la classe prédite et le pourcentage de prédiction
        predicted_class_name = class_names[predicted_class_index]
        predicted_percentage = predictions[0][predicted_class_index] * 100

        print("Classe prédite:", predicted_class_name)
        print("Pourcentage de prédiction:", predicted_percentage)

        data = {"Classepredite": predicted_class_name}
        data['imageMaladie'] = Path(__file__).resolve().parent.parent / 'media/imageformodel/' / image.name

        return render(request=request, template_name='pages/pageResultatDiagnostic.html', context=data)

    # If the request method is GET, render the upload form
    return render(request, 'pages/faireDiagnostic.html')





















    # If the request method is GET, render the upload form
    return render(request, 'pages/faireDiagnostic.html')