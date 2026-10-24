import random


class SeleccionTorneo:
    def __init__(self, participantes=3):
        self.participantes = participantes

    def seleccion_poblacion(self, poblacion):
        ganadores = []
        for _ in range(len(poblacion)):
            competidores = random.sample(poblacion, self.participantes)
            ganadores.append(max(competidores, key=lambda cromosoma: cromosoma.score))
        return ganadores
