Laboratorio 7 - Algoritmo neurogenetico - Computo Suave
Valdez Meza Kevin Osmar - 1288703

Requiere Python 3 con: numpy, pandas, matplotlib, scikit-learn, openpyxl, jupyter
   pip install numpy pandas matplotlib scikit-learn openpyxl jupyter

COMO EJECUTAR
1. Abrir la carpeta "Lab 7" en VS Code / Jupyter.
2. Abrir 01_Soybean_NeuroGenetico.ipynb y ejecutar todo (Run All).
3. Abrir 02_HydroGrowNet_NeuroGenetico.ipynb y ejecutar todo.
   (Cada GA tarda unos minutos.) Tambien desde terminal:
   python GAneuro.py soybean
   python GAneuro.py hydro

ARCHIVOS
configuracion.py   UNICO archivo a editar: parametros del GA, espacio de busqueda y redes base.
GAneuro.py         clase GA: evaluar -> ordenar -> torneo -> elitismo -> cruce -> mutacion.
CromosomaRN.py     cromosoma de genes enteros (cada gen = indice de una opcion).
interfaz/aptitud.py      f(x) = R2 promedio de validacion cruzada (3 pliegues) con el 60 % de entrenamiento.
interfaz/seleccion.py    torneo de 3 participantes.
interfaz/reproducion.py  cruce de un punto.
interfaz/mutacion.py     cambia un gen por otra opcion valida.
redes.py           carga de datasets, decodificacion cromosoma -> MLPRegressor, metricas.
graficas.py        graficas (se guardan en figuras/).
resultados_*.json  resultados numericos de la ultima ejecucion.
datasets/          datos usados (soy = Forty Soybean Cultivars, hydro = HydroGrowNet).

QUE SE PUEDE CAMBIAR (configuracion.py)
GA_PARAMS['num_inv']           tamano de la poblacion (24)
GA_PARAMS['max_generaciones']  generaciones (20)
GA_PARAMS['prob_mutacion']     probabilidad de mutar cada gen (0.15)
GA_PARAMS['por_remplazo']      elitismo: fraccion que pasa directo (0.3)
GA_PARAMS['torneo']            participantes del torneo (3)
GA_PARAMS['folds']             pliegues de validacion cruzada (3)
ESPACIO_RED[...]               listas de opciones de capas, neuronas, activacion, lr, alpha, batch
BASE_SOYBEAN / BASE_HYDRO      red de comparacion (la del Laboratorio 4)
SEMILLA                        cambiarla da otra corrida del GA (otro resultado posible)
TEST_SIZE                      0.40 = division 60/40 del Lab 4

Despues de cambiar algo: Kernel -> Restart & Run All (para que se recargue configuracion.py).

Dataset IoT del Lab 4: no se usa. Sus variables son ruido uniforme independiente
(correlacion con EC ~0.003 y autocorrelacion ~0), por lo que ninguna red ni GA puede predecir EC.
