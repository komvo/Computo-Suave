"""Selección por ruleta, no por torneo."""
import random

class SeleccionRuleta:
    def seleccion_poblacion(self, poblacion):
        # Cada individuo tiene probabilidad proporcional a su fitness.
        pesos = [c.score for c in poblacion]
        return random.choices(poblacion, weights=pesos, k=len(poblacion))
