import random


class CromosomaRN:
    """Cromosoma entero: cada gen guarda el indice de una opcion.

    Ejemplo de genes: [capas, neuronas1, neuronas2, neuronas3, activacion,
    tasa_aprendizaje, alpha, batch, usar_var1, usar_var2, ...].
    """

    def __init__(self, nombres, opciones):
        self.nombres = list(nombres)          # nombre de cada gen
        self.opciones = list(opciones)        # cuantas opciones tiene cada gen
        self.n_genes = len(self.nombres)
        self.genes = [0] * self.n_genes
        self.score = -1.0

    def llenar_random_data(self):
        self.genes = [random.randrange(n) for n in self.opciones]

    def get_bits(self, gen):
        return self.genes[gen - 1]

    def set_bits(self, valor, gen):
        if not 0 <= valor < self.opciones[gen - 1]:
            raise ValueError(f'El gen {gen} debe estar entre 0 y {self.opciones[gen - 1] - 1}')
        self.genes[gen - 1] = valor

    def cadena(self):
        return '-'.join(str(g) for g in self.genes)

    def clave(self):
        return tuple(self.genes)
