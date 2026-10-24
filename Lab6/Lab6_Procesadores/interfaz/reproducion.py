"""Cruce de un punto, tomado como operador de las prácticas previas."""
import random
from CromosomaDecimal import CromosomaDecimal

class ReproduccionUnCruce:
    def reproduccion_poblacion(self, nueva, padres, max_poblacion):
        while len(nueva) < max_poblacion:
            padre_a, padre_b = random.sample(padres, 2)
            punto = random.randint(1, len(padre_a.genes) - 1)
            hijo_a = CromosomaDecimal(len(padre_a.genes))
            hijo_b = CromosomaDecimal(len(padre_a.genes))
            hijo_a.genes = padre_a.genes[:punto] + padre_b.genes[punto:]
            hijo_b.genes = padre_b.genes[:punto] + padre_a.genes[punto:]
            nueva.append(hijo_a)
            if len(nueva) < max_poblacion:
                nueva.append(hijo_b)
