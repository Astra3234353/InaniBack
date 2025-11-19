import joblib
import os
from django.conf import settings

modelo_ia = None

def cargar_modelo():
    global modelo_ia
    if modelo_ia is None:
        path = os.path.join(settings.BASE_DIR, 'api', 'ml_utils', 'signsense_knn_model.pkl')
        try:
            modelo_ia = joblib.load(path)
            print("✅ Modelo de IA cargado correctamente")
        except Exception as e:
            print(f"❌ Error cargando el modelo: {e}")
            modelo_ia = None
    return modelo_ia

