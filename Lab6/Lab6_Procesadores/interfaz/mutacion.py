"""Cambio aleatorio del procesador con probabilidad por gen."""
import random

class MutacionDecimal:
    def __init__(self, probabilidad=0.05):
        self.probabilidad = probabilidad

    def mutacion_poblacion(self, poblacion):
        for cromosoma in poblacion:
            for i, actual in enumerate(cromosoma.genes):
                if random.random() < self.probabilidad:
                    # Elegir uno de los otros dos procesadores garantiza cambio.
                    cromosoma.genes[i] = random.choice([p for p in (1, 2, 3) if p != actual])
