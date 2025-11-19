import os
import tempfile
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Importamos tu pipeline y el cargador
from .ml_utils.landmark_pipeline import landmark_pipeline
from .ml_utils.model_loader import cargar_modelo

class PrediccionSenasView(APIView):
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({"error": "No se proporcionó imagen"}, status=status.HTTP_400_BAD_REQUEST)
            
        imagen_archivo = request.FILES['image']
        
        modelo = cargar_modelo()
        if modelo is None:
            return Response({"error": "El modelo de IA no está disponible"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 3. Guardar imagen en un archivo temporal
        # Tu función landmark_pipeline pide un 'path' (ruta), así que creamos uno temporal
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                for chunk in imagen_archivo.chunks():
                    temp_file.write(chunk)
                temp_path = temp_file.name

            features = landmark_pipeline(temp_path)
            
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

        if features is None:
            return Response({
                "mensaje": "No se detectó ninguna mano en la imagen",
                "prediccion": None
            }, status=status.HTTP_200_OK)

        features_array = np.array([features])
        
        prediccion = modelo.predict(features_array)
        
        return Response({
            "exito": True,
            "prediccion": prediccion[0], # Retornamos el primer (y único) resultado
            "mensaje": "Seña detectada correctamente"
        })
