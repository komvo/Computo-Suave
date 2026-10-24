"""Laboratorio 6, problema 2: distribuir seis tareas entre tres procesadores."""
import copy
import random
from CromosomaDecimal import CromosomaDecimal
from interfaz import AptitudProcesadores, SeleccionRuleta, ReproduccionUnCruce, MutacionDecimal

TIEMPOS = [8, 5, 7, 3, 6, 4]
SEMILLA = 1288703

class GA:
    def __init__(self, tiempos, num_inv=30, prob_mutacion=0.05, por_remplazo=0.5):
        self.tiempos = tiempos
        self.num_inv = num_inv
        self.num_remplazo = int(num_inv * por_remplazo)
        self.aptitud = AptitudProcesadores(tiempos)
        self.seleccion = SeleccionRuleta()
        self.reproduccion = ReproduccionUnCruce()
        self.mutacion = MutacionDecimal(prob_mutacion)
        self.poblacion = [CromosomaDecimal(len(tiempos)) for _ in range(num_inv)]
        for crom in self.poblacion:
            crom.llenar_random_data()

    def buscar_solucion(self, max_generaciones=1000):
        historial = []
        # 33 unidades de trabajo; ningún reparto puede terminar en menos de 11.
        cota_inferior = (sum(self.tiempos) + 2) // 3
        for generacion in range(max_generaciones + 1):
            self.aptitud.evaluar_poblacion(self.poblacion)
            self.poblacion.sort(key=lambda c: c.score, reverse=True)
            mejor = self.poblacion[0]
            cargas = self.aptitud.cargas(mejor)
            historial.append((generacion, mejor.cadena(), cargas, max(cargas), mejor.score))
            if max(cargas) == cota_inferior or generacion == max_generaciones:
                return copy.deepcopy(mejor), historial
            padres = self.seleccion.seleccion_poblacion(self.poblacion)
            nuevos = copy.deepcopy(self.poblacion[:self.num_remplazo])
            self.reproduccion.reproduccion_poblacion(nuevos, padres, self.num_inv)
            self.mutacion.mutacion_poblacion(nuevos[self.num_remplazo:])
            self.poblacion = nuevos

def detalle(cromosoma, tiempos):
    lineas = []
    for proc in (1, 2, 3):
        indices = [i for i, x in enumerate(cromosoma.genes) if x == proc]
        tareas = ', '.join('T' + str(i + 1) for i in indices) or '(ninguna)'
        total = sum(tiempos[i] for i in indices)
        lineas.append(f'P{proc}: {tareas} | carga={total}')
    return '\n'.join(lineas)

def main():
    random.seed(SEMILLA)
    algoritmo = GA(TIEMPOS)
    mejor, historial = algoritmo.buscar_solucion()
    cargas = algoritmo.aptitud.cargas(mejor)
    texto = [
        'LABORATORIO 6 - PROBLEMA 2: DISTRIBUCION DE TAREAS',
        f'Semilla: {SEMILLA}',
        f'Tiempos: {TIEMPOS}',
        'Poblacion: 30 | seleccion: ruleta | cruce: un punto | mutacion: 0.05 | elite: 50%',
        'Generacion | Cromosoma | Cargas P1/P2/P3 | M(x) | Fitness',
    ]
    for gen, cadena, cs, makespan, score in historial:
        texto.append(f'{gen:10d} | {cadena} | {str(cs):17s} | {makespan:4d} | {score:.8f}')
    texto.extend([
        '', 'RESULTADO FINAL',
        f'Cromosoma decimal: {mejor.cadena()}',
        detalle(mejor, TIEMPOS),
        f'Tiempo total para terminar: {max(cargas)} (maximo de cargas)',
        f'Fitness: {mejor.score:.8f} = 1/(1+{max(cargas)})',
        f'Generacion final: {historial[-1][0]}',
        'Cota inferior teorica: ceil(33/3)=11',
        f'Optimo comprobado por cota: {max(cargas)==11}',
    ])
    salida = '\n'.join(texto) + '\n'
    print(salida)
    with open('resultados.txt', 'w', encoding='utf-8') as f:
        f.write(salida)
    assert len(mejor.genes)==6 and all(x in (1, 2, 3) for x in mejor.genes)
    assert sum(cargas)==sum(TIEMPOS)

if __name__ == '__main__':
    main()
