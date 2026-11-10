from abc import ABC, abstractmethod

import numpy as np
from joblib import Parallel, delayed
from sklearn.model_selection import KFold, cross_val_score

import configuracion as cfg
from redes import columnas, crear_red, decodificar


class Aptitud(ABC):
    @abstractmethod
    def evaluar_poblacion(self, poblacion):
        pass


def _r2_validacion(genes, grupos, X, y, folds):
    params = decodificar(genes, grupos)
    if not params['variables']:          # una red sin entradas no sirve
        return -1.0
    cols = columnas(params, grupos)
    kf = KFold(n_splits=folds, shuffle=True, random_state=cfg.SEMILLA_RED)
    r2 = cross_val_score(crear_red(params), X[cols], y, cv=kf, scoring='r2')
    return float(np.mean(r2))


class AptitudRedNeuronal(Aptitud):
    """f(x) = R2 promedio de validacion cruzada SOLO sobre el 60 % de entrenamiento.

    El 40 % de prueba nunca se usa durante la busqueda; asi la comparacion final es justa.
    Se guarda un cache para no reentrenar cromosomas repetidos.
    """

    def __init__(self, X, y, grupos, folds=3, n_jobs=-1):
        self.X, self.y, self.grupos = X, y, grupos
        self.folds = folds
        self.n_jobs = n_jobs
        self.cache = {}

    def evaluar_poblacion(self, poblacion):
        nuevos = list({c.clave() for c in poblacion if c.clave() not in self.cache})
        scores = Parallel(n_jobs=self.n_jobs)(
            delayed(_r2_validacion)(list(k), self.grupos, self.X, self.y, self.folds) for k in nuevos)
        self.cache.update(zip(nuevos, scores))
        for c in poblacion:
            c.score = self.cache[c.clave()]
