"""Laboratorio 7: algoritmo neurogenetico (GA que optimiza una red neuronal MLP).

Uso desde terminal:  python GAneuro.py soybean   |   python GAneuro.py hydro
"""
import copy
import random
import sys
import time

from sklearn.model_selection import train_test_split

import configuracion as cfg
from CromosomaRN import CromosomaRN
from interfaz import AptitudRedNeuronal, MutacionEntera, ReproduccionUnCruce, SeleccionTorneo
from redes import (cargar_hydro, cargar_soybean, decodificar, describir, entrenar_y_evaluar,
                   genes_del_problema)


class GA:
    def __init__(self, X, y, grupos, num_inv=20, prob_mutacion=0.15, por_remplazo=0.3,
                 torneo=3, folds=3, **_):
        self.num_inv = num_inv
        self.grupos = grupos
        self.num_remplazo = max(1, int(num_inv * por_remplazo))
        self.evaluar = AptitudRedNeuronal(X, y, grupos, folds)
        self.seleccion = SeleccionTorneo(torneo)
        self.reproducion = ReproduccionUnCruce()
        self.mutacion = MutacionEntera(prob_mutacion)
        nombres, opciones = genes_del_problema(grupos)
        self.poblacion = [CromosomaRN(nombres, opciones) for _ in range(num_inv)]
        for c in self.poblacion:
            c.llenar_random_data()

    def buscar_solucion(self, max_generaciones=15, verbose=True):
        historial = []
        for generacion in range(max_generaciones + 1):
            inicio = time.time()
            self.evaluar.evaluar_poblacion(self.poblacion)
            self.poblacion.sort(key=lambda c: c.score, reverse=True)
            mejor = self.poblacion[0]
            promedio = sum(max(c.score, -1) for c in self.poblacion) / self.num_inv
            historial.append({'generacion': generacion, 'mejor': mejor.score, 'promedio': promedio,
                              'cromosoma': mejor.cadena(),
                              'red': describir(decodificar(mejor.genes, self.grupos), self.grupos)})
            if verbose:
                print(f'[{generacion:02d}] mejor R2_cv={mejor.score:.4f} | promedio={promedio:.4f} | '
                      f'{describir(decodificar(mejor.genes, self.grupos), self.grupos)} | {time.time() - inicio:.1f}s')
            if generacion == max_generaciones:
                break
            padres = self.seleccion.seleccion_poblacion(self.poblacion)
            nuevos = copy.deepcopy(self.poblacion[:self.num_remplazo])        # elitismo
            self.reproducion.reproduccion_poblacion(nuevos, padres, self.num_inv)
            self.mutacion.mutacion_poblacion(nuevos[self.num_remplazo:])    # no se muta a la elite
            self.poblacion = nuevos
        return copy.deepcopy(self.poblacion[0]), historial


def main(nombre='soybean'):
    random.seed(cfg.SEMILLA)
    df, X, y, grupos = cargar_soybean() if nombre == 'soybean' else cargar_hydro()
    base = cfg.BASE_SOYBEAN if nombre == 'soybean' else cfg.BASE_HYDRO
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=cfg.TEST_SIZE, random_state=cfg.SEMILLA_RED)
    _, _, mb = entrenar_y_evaluar(base, grupos, Xtr, ytr, Xte, yte)
    print('BASE   :', describir(base, grupos), '| R2 prueba =', round(mb['R2'], 4))
    ga = GA(Xtr, ytr, grupos, **cfg.GA_PARAMS)
    mejor, _ = ga.buscar_solucion(cfg.GA_PARAMS['max_generaciones'])
    params = decodificar(mejor.genes, grupos)
    _, _, mo = entrenar_y_evaluar(params, grupos, Xtr, ytr, Xte, yte)
    print('GA     :', describir(params, grupos), '| variables:', params['variables'], '| R2 prueba =', round(mo['R2'], 4))


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'soybean')
