import random


class CromosomaOctal:
    """Ocho genes octales: indice = columna, valor = fila (0..7)."""

    def __init__(self, genes=8):
        if genes != 8:
            raise ValueError('La practica requiere exactamente ocho genes')
        self.n_genes = genes
        self.genes = [0] * genes
        self.score = 0

    def llenar_random_data(self):
        self.genes = [random.randint(0, 7) for _ in range(self.n_genes)]

    def get_bits(self, gen):
        return self.genes[gen - 1]

    def set_bits(self, valor, gen):
        if not 0 <= valor <= 7:
            raise ValueError('Cada gen debe estar entre 0 y 7')
        self.genes[gen - 1] = valor

    def cadena(self):
        return ''.join(str(n) for n in self.genes)
