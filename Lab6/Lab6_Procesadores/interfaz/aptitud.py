"""f(x) = 1/(1 + M(x)); M = mayor carga de procesador."""
class AptitudProcesadores:
    def __init__(self, tiempos):
        self.tiempos = tiempos

    def cargas(self, cromosoma):
        cargas = [0, 0, 0]
        for tarea, procesador in enumerate(cromosoma.genes):
            cargas[procesador - 1] += self.tiempos[tarea]
        return cargas

    def evaluar_poblacion(self, poblacion):
        for cromosoma in poblacion:
            cromosoma.score = 1.0 / (1 + max(self.cargas(cromosoma)))
