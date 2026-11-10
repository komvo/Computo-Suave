import random
from abc import ABC, abstractmethod
from CromosomaRN import CromosomaRN


class Reproduccion(ABC):
    @abstractmethod
    def reproduccion_poblacion(self, poblacion, potencial, max_poblacion):
        pass


class ReproduccionUnCruce(Reproduccion):
    """Cruce de un punto: el hijo A toma los primeros genes del padre A y el resto del padre B."""

    def reproduccion_poblacion(self, poblacion, potencial, max_poblacion):
        while len(poblacion) < max_poblacion:
            padreA, padreB = random.sample(potencial, 2)
            n = padreA.n_genes
            punto_cruce = random.randint(1, n - 1)
            hijoA = CromosomaRN(padreA.nombres, padreA.opciones)
            hijoB = CromosomaRN(padreA.nombres, padreA.opciones)
            hijoA.genes = padreA.genes[:punto_cruce] + padreB.genes[punto_cruce:]
            hijoB.genes = padreB.genes[:punto_cruce] + padreA.genes[punto_cruce:]
            poblacion.append(hijoA)
            if len(poblacion) < max_poblacion:
                poblacion.append(hijoB)
