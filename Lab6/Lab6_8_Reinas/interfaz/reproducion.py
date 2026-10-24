import random
from CromosomaOct import CromosomaOctal


class ReproduccionUnCruce:
    def __init__(self, num_genes=8):
        self.num_genes = num_genes

    def reproduccion_poblacion(self, poblacion, potencial, max_poblacion):
        while len(poblacion) < max_poblacion:
            padre_a, padre_b = random.sample(potencial, 2)
            punto = random.randint(1, self.num_genes - 1)
            hijo_a = CromosomaOctal(self.num_genes)
            hijo_b = CromosomaOctal(self.num_genes)
            hijo_a.genes = padre_a.genes[:punto] + padre_b.genes[punto:]
            hijo_b.genes = padre_b.genes[:punto] + padre_a.genes[punto:]
            poblacion.append(hijo_a)
            if len(poblacion) < max_poblacion:
                poblacion.append(hijo_b)
