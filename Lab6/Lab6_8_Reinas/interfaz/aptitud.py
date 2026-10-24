class AptitudReinas:
    """f(x) = 28 - conflictos; cada pareja de reinas cuenta una vez."""

    @staticmethod
    def conflictos(cromosoma):
        conflictos = 0
        for columna_a in range(8):
            for columna_b in range(columna_a + 1, 8):
                fila_a = cromosoma.genes[columna_a]
                fila_b = cromosoma.genes[columna_b]
                if fila_a == fila_b or abs(fila_a - fila_b) == abs(columna_a - columna_b):
                    conflictos += 1
        return conflictos

    def evaluar_poblacion(self, poblacion):
        for cromosoma in poblacion:
            cromosoma.score = 28 - self.conflictos(cromosoma)
