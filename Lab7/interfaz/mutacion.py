import random
from abc import ABC, abstractmethod


class Mutacion(ABC):
    @abstractmethod
    def mutacion_poblacion(self, poblacion):
        pass


class MutacionEntera(Mutacion):
    """Cambia un gen por otra opcion valida distinta a la actual."""

    def __init__(self, probabilidad=0.15):
        self.prob = probabilidad

    def mutacion_poblacion(self, poblacion):
        for crom in poblacion:
            for i in range(crom.n_genes):
                if random.random() < self.prob and crom.opciones[i] > 1:
                    actual = crom.genes[i]
                    crom.genes[i] = random.choice([x for x in range(crom.opciones[i]) if x != actual])
