"""Un gen por tarea. Valores 1, 2 o 3 (procesadores)."""
import random

class CromosomaDecimal:
    def __init__(self, num_genes=6):
        self.genes = [0] * num_genes
        self.score = 0.0

    def llenar_random_data(self):
        self.genes = [random.randint(1, 3) for _ in self.genes]

    def cadena(self):
        return ''.join(str(gen) for gen in self.genes)
