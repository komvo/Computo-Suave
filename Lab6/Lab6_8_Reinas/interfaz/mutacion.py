import random


class MutacionOctal:
    def __init__(self, probabilidad=0.05):
        self.prob = probabilidad

    def mutacion_poblacion(self, poblacion):
        for cromosoma in poblacion:
            for i in range(cromosoma.n_genes):
                if random.random() < self.prob:
                    valor = cromosoma.genes[i]
                    cromosoma.genes[i] = random.choice([x for x in range(8) if x != valor])
