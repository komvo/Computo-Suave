"""Laboratorio 7 - Algoritmo neurogenetico.

Este es el UNICO archivo que hay que modificar para cambiar el experimento.
Todos los notebooks y GAneuro.py leen sus valores desde aqui.
"""

# ---------------------------------------------------------------
# 1. Reproducibilidad y division de datos (igual que en el Lab 4)
# ---------------------------------------------------------------
SEMILLA = 1288703          # semilla del algoritmo genetico (random)
SEMILLA_RED = 42           # random_state de la division 60/40 y de la red
TEST_SIZE = 0.40           # 60 % entrenamiento / 40 % prueba

# ---------------------------------------------------------------
# 2. Parametros del algoritmo genetico
# ---------------------------------------------------------------
GA_PARAMS = {
    'num_inv': 24,             # individuos por generacion
    'max_generaciones': 20,    # generaciones maximas
    'torneo': 3,               # participantes del torneo
    'prob_mutacion': 0.15,     # probabilidad de mutar cada gen
    'por_remplazo': 0.3,       # fraccion elite que pasa directo (elitismo)
    'folds': 3,                # validacion cruzada interna para la aptitud
}

# ---------------------------------------------------------------
# 3. Espacio de busqueda de la red (cada gen elige un indice de la lista)
# ---------------------------------------------------------------
ESPACIO_RED = {
    'capas':            [1, 2, 3],
    'neuronas1':        [4, 8, 16, 32, 64, 128],
    'neuronas2':        [4, 8, 16, 32, 64, 128],
    'neuronas3':        [4, 8, 16, 32, 64, 128],
    'activacion':       ['relu', 'tanh', 'logistic'],
    'tasa_aprendizaje': [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03],
    'alpha':            [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 3.0, 10.0],
    'batch':            [16, 32, 64, 128],
}

# Entrenamiento de cada red (igual que en el Lab 4)
MAX_ITER = 3000
PACIENCIA = 100            # n_iter_no_change del early stopping

# ---------------------------------------------------------------
# 4. Redes base del Laboratorio 4 (punto de comparacion)
# ---------------------------------------------------------------
BASE_SOYBEAN = {
    'variables': ['PH', 'IFP', 'NLP', 'NGP', 'NGL', 'NS', 'MHG'],
    'ocultas': (64, 32, 16), 'activacion': 'relu',
    'tasa_aprendizaje': 0.001, 'alpha': 0.0001, 'batch': 'auto',
}
BASE_HYDRO = {
    'variables': ['plant_height', 'shoot_length', 'root_length', 'stem_diameter', 'leaves'],
    'ocultas': (32, 16, 8), 'activacion': 'relu',
    'tasa_aprendizaje': 0.001, 'alpha': 0.0001, 'batch': 'auto',
}

# Semillas para comprobar que la mejora no depende de la inicializacion
SEMILLAS_ROBUSTEZ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
