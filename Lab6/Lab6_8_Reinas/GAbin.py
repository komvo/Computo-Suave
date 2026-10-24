"""Laboratorio 6: ocho reinas, algoritmo genetico con cromosoma octal."""
import copy
import random
from CromosomaOct import CromosomaOctal
from interfaz import AptitudReinas, SeleccionTorneo, ReproduccionUnCruce, MutacionOctal


class GA:
    def __init__(self, num_inv=100, num_genes=8, prob_mutacion=0.05, por_remplazo=0.5):
        self.num_inv = num_inv
        self.num_genes = num_genes
        self.num_remplazo = int(num_inv * por_remplazo)
        self.evaluar = AptitudReinas()
        self.seleccion = SeleccionTorneo(3)
        self.reproducion = ReproduccionUnCruce(num_genes)
        self.mutacion = MutacionOctal(prob_mutacion)
        self.poblacion = [CromosomaOctal(num_genes) for _ in range(num_inv)]
        for c in self.poblacion:
            c.llenar_random_data()

    def buscar_solucion(self, max_generaciones=2000):
        historial = []
        for generacion in range(max_generaciones + 1):
            self.evaluar.evaluar_poblacion(self.poblacion)
            self.poblacion.sort(key=lambda c: c.score, reverse=True)
            mejor = self.poblacion[0]
            conflictos = self.evaluar.conflictos(mejor)
            promedio = sum(c.score for c in self.poblacion) / self.num_inv
            historial.append((generacion, mejor.score, conflictos, promedio, mejor.cadena()))
            if mejor.score == 28:  # solucion comprobada: cero ataques
                return copy.deepcopy(mejor), historial
            if generacion == max_generaciones:
                break
            padres = self.seleccion.seleccion_poblacion(self.poblacion)
            nuevos = copy.deepcopy(self.poblacion[:self.num_remplazo])
            self.reproducion.reproduccion_poblacion(nuevos, padres, self.num_inv)
            # Se mutan solo los descendientes, para conservar al mejor (elitismo).
            self.mutacion.mutacion_poblacion(nuevos[self.num_remplazo:])
            self.poblacion = nuevos
        return copy.deepcopy(self.poblacion[0]), historial


def tablero(cromosoma):
    lineas = ['    0 1 2 3 4 5 6 7']
    for fila in range(8):
        lineas.append(f'{fila} | ' + ' '.join('Q' if cromosoma.genes[col] == fila else '.' for col in range(8)))
    return '\n'.join(lineas)


def main():
    random.seed(3)  # repetir la demostracion
    algoritmo = GA()
    mejor, historial = algoritmo.buscar_solucion()
    print('LABORATORIO 6 - OCHO REINAS')
    print('Poblacion: 100 | torneo: 3 | cruce: 1 punto | mutacion: 0.05 | elitismo: 0.5')
    print('\nGeneracion | Mejor fitness | Conflictos | Promedio | Cromosoma')
    for g, score, conflictos, promedio, cadena in historial:
        if g == 0 or g == len(historial) - 1 or g % 10 == 0:
            print(f'{g:10d} | {score:13d} | {conflictos:10d} | {promedio:8.2f} | {cadena}')
    print('\nSolucion:', mejor.cadena())
    print('Filas por columna:', mejor.genes)
    print('Conflictos:', algoritmo.evaluar.conflictos(mejor))
    print('Fitness:', mejor.score, '/ 28')
    print('Generacion:', historial[-1][0])
    print('\n' + tablero(mejor))
    with open('resultados.txt', 'w', encoding='utf-8') as archivo:
        archivo.write('LABORATORIO 6 - OCHO REINAS\n')
        archivo.write('Semilla: 3\nPoblacion: 100\nTorneo: 3\nMutacion: 0.05\nReemplazo elite: 0.5\n')
        archivo.write('Generacion | Mejor fitness | Conflictos | Promedio fitness | Cromosoma\n')
        for registro in historial:
            g, score, conflictos, promedio, cadena = registro
            archivo.write(f'{g:10d} | {score:13d} | {conflictos:10d} | {promedio:16.2f} | {cadena}\n')
        archivo.write(f'\nCromosoma final: {mejor.cadena()}\nFilas por columna: {mejor.genes}\n')
        archivo.write(f'Conflictos: {algoritmo.evaluar.conflictos(mejor)}\nFitness: {mejor.score}/28\n')
        archivo.write('Generacion final: ' + str(historial[-1][0]) + '\n\n' + tablero(mejor) + '\n')
    if mejor.score != 28:
        raise RuntimeError('No se encontro solucion sin conflictos dentro del limite de generaciones')


if __name__ == '__main__':
    main()
