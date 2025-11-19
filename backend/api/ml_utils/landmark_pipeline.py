# landmark_pipeline.py

import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial.distance import euclidean

# Inicializar MediaPipe Hands UNA SOLA VEZ
mp_hands = mp.solutions.hands
# Usamos min_detection_confidence más bajo para mayor robustez
HANDS_DETECTOR = mp.solutions.hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.35 
)

def apply_clahe(image):
    """Aplica la Ecualización de Histograma CLAHE para mejorar el contraste."""
    if image is None:
        return None
        
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    channels = list(cv2.split(ycrcb))
    
    # Aplicar CLAHE a la luminancia (canal 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    channels[0] = clahe.apply(channels[0]) 
    
    cv2.merge(channels, ycrcb) 
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR) 

def calculate_geometric_features(landmarks):
    """
    Calcula un vector de características geométricas (distancias) 
    invariantes a la traslación y escala.
    """
    if landmarks is None or len(landmarks) == 0:
        return None

    # Normalización: Traslación (Muñeca L0 a origen)
    wrist = landmarks[0]
    normalized_landmarks = landmarks - wrist
    
    # Normalización: Escala (Factor L0 a L9)
    scale_factor = euclidean(normalized_landmarks[0], normalized_landmarks[9])
    if scale_factor < 1e-6: 
        return None
        
    scaled_landmarks = normalized_landmarks / scale_factor

    # --- Cálculo de Características ---
    features = []
    finger_tips = [4, 8, 12, 16, 20]
    
    # 1. Distancias entre Puntas de Dedos (10 características)
    for i in range(len(finger_tips)):
        for j in range(i + 1, len(finger_tips)):
            dist = euclidean(scaled_landmarks[finger_tips[i]], scaled_landmarks[finger_tips[j]])
            features.append(dist)
            
    # 2. Distancia de Puntas de Dedos a la Muñeca L0 (5 características)
    for tip_index in finger_tips:
        dist = euclidean(scaled_landmarks[tip_index], [0, 0]) 
        features.append(dist)
        
    # 3. Flexión de Nudillos (Distancia de L8, L12, L16, L20 a sus bases) (4 características)
    bases = [5, 9, 13, 17]
    for tip, base in zip(finger_tips[1:], bases):
        dist = euclidean(scaled_landmarks[tip], scaled_landmarks[base])
        features.append(dist)

    # 4. Coordenadas de las puntas (10 características)
    for tip_index in finger_tips:
        features.extend(scaled_landmarks[tip_index].tolist())
        
    return features


def landmark_pipeline(image_path):
    """
    Implementa el pipeline completo: Carga -> Ecualización -> Detección -> Características.
    """
    image = cv2.imread(image_path)
    if image is None:
        return None

    # Paso 1: Ecualización (para robustez de iluminación)
    image_eq = apply_clahe(image)

    # Paso 2: Detección de Landmarks
    results = HANDS_DETECTOR.process(cv2.cvtColor(image_eq, cv2.COLOR_BGR2RGB))
    
    if not results.multi_hand_landmarks:
        return None

    # Convertir a array de 21x2
    landmarks_raw = []
    for lm in results.multi_hand_landmarks[0].landmark:
        landmarks_raw.extend([lm.x, lm.y])
    landmarks = np.array(landmarks_raw).reshape(21, 2)
    
    # Paso 3: Cálculo de Características
    return calculate_geometric_features(landmarks)

# Liberar los recursos de MediaPipe al cerrar la aplicación (Buena práctica)
# HANDS_DETECTOR.close() # Se descomenta si se usa en un entorno de servidor