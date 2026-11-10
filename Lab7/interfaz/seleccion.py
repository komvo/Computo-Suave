import random
from abc import ABC, abstractmethod


class Seleccion(ABC):
    @abstractmethod
    def seleccion_poblacion(self, poblacion):
        pass


class SeleccionTorneo(Seleccion):
    def __init__(self, participantes=3):
        self.participantes = participantes

    def seleccion_poblacion(self, poblacion):
        ganadores = []
        for _ in range(len(poblacion)):
            competidores = random.sample(poblacion, self.participantes)
            ganadores.append(max(competidores, key=lambda c: c.score))
        return ganadores
