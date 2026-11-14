"""
Ejercicio 1: Tres variables linguisticas con 3 o mas terminos cada una,
mezclando las funciones de membresia vistas en clase
(triangular, trapezoidal, gaussiana, gaussiana acampanada y sigmoidal).

Contexto: control de clima de un invernadero.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from difuso import (VariableLinguistica, trimf, trapmf, gaussmf, gbellmf,
                    sigmf)

SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficas")


def crear_variables():
    # 1) Temperatura [0, 45] C  -> trapezoidal + triangular + gaussiana + trapezoidal
    temperatura = VariableLinguistica("Temperatura", np.linspace(0, 45, 901), "°C")
    temperatura.agregar_termino("Fria", trapmf, 0, 0, 8, 16)
    temperatura.agregar_termino("Templada", trimf, 12, 20, 28)
    temperatura.agregar_termino("Calida", gaussmf, 4, 30)
    temperatura.agregar_termino("Caliente", trapmf, 32, 38, 45, 45)

    # 2) Humedad relativa [0, 100] %  -> sigmoidal + campana + gaussiana + sigmoidal
    humedad = VariableLinguistica("Humedad relativa", np.linspace(0, 100, 1001), "%")
    humedad.agregar_termino("Seca", sigmf, -0.25, 30)
    humedad.agregar_termino("Normal", gbellmf, 15, 3, 50)
    humedad.agregar_termino("Humeda", gaussmf, 8, 72)
    humedad.agregar_termino("Saturada", sigmf, 0.3, 88)

    # 3) Velocidad del ventilador [0, 100] %  -> trapezoidal + triangular + campana + trapezoidal
    ventilador = VariableLinguistica("Velocidad del ventilador", np.linspace(0, 100, 1001), "%")
    ventilador.agregar_termino("Apagado", trapmf, 0, 0, 5, 15)
    ventilador.agregar_termino("Lenta", trimf, 5, 25, 45)
    ventilador.agregar_termino("Media", gbellmf, 12, 2.5, 55)
    ventilador.agregar_termino("Rapida", trapmf, 65, 85, 100, 100)

    return temperatura, humedad, ventilador


def graficar(variable, ax):
    for termino, (desc, mu) in variable.terminos.items():
        ax.plot(variable.universo, mu, linewidth=2, label=f"{termino}  [{desc}]")
    ax.set_title(f"Variable linguistica: {variable.nombre}")
    ax.set_xlabel(f"{variable.nombre} ({variable.unidad})")
    ax.set_ylabel("Grado de membresia μ(x)")
    ax.set_ylim(-0.05, 1.08)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="center right")


def main():
    os.makedirs(SALIDA, exist_ok=True)
    variables = crear_variables()

    fig, axes = plt.subplots(3, 1, figsize=(10, 11))
    for var, ax in zip(variables, axes):
        graficar(var, ax)
        # Grafica individual tambien
        f2, a2 = plt.subplots(figsize=(10, 4))
        graficar(var, a2)
        f2.tight_layout()
        nombre = var.nombre.lower().replace(" ", "_")
        f2.savefig(os.path.join(SALIDA, f"ej1_{nombre}.png"), dpi=130)
        plt.close(f2)
    fig.tight_layout()
    fig.savefig(os.path.join(SALIDA, "ej1_variables_linguisticas.png"), dpi=130)
    plt.close(fig)

    print("=== Ejercicio 1: Variables linguisticas ===")
    for var in variables:
        print(f"\n{var.nombre} ({var.unidad}), universo [{var.universo[0]:g}, {var.universo[-1]:g}]")
        for t, (desc, _) in var.terminos.items():
            print(f"  - {t:<10} {desc}")

    # Ejemplo de fusificacion
    ejemplos = [(variables[0], 26), (variables[1], 65), (variables[2], 50)]
    print("\nEjemplos de fusificacion:")
    for var, x in ejemplos:
        grados = ", ".join(f"{t}={g:.3f}" for t, g in var.fusificar(x).items())
        print(f"  {var.nombre} = {x}{var.unidad}: {grados}")
    print(f"\nGraficas guardadas en: {SALIDA}")
    return variables


if __name__ == "__main__":
    main()
