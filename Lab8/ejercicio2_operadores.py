"""
Ejercicio 2: Operadores de Union, Interseccion y Complemento para conjuntos
difusos tipo 1 (una funcion por operador, implementadas en difuso.py).

Se aplican sobre dos terminos de la variable Temperatura del ejercicio 1:
  A = Templada (triangular)   y   B = Calida (gaussiana)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from difuso import union, interseccion, complemento
from ejercicio1_variables import crear_variables, SALIDA


def main():
    os.makedirs(SALIDA, exist_ok=True)
    temperatura, _, _ = crear_variables()
    x = temperatura.universo
    A, B = temperatura["Templada"], temperatura["Calida"]

    tipos_union = ["max", "suma_alg", "suma_acot", "drastica"]
    tipos_inter = ["min", "producto", "prod_acot", "drastica"]

    # --- Grafica principal: max / min / complemento ---
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ops = [
        ("Conjuntos A=Templada, B=Calida", None),
        ("Union A ∪ B (max)", union(A, B, "max")),
        ("Interseccion A ∩ B (min)", interseccion(A, B, "min")),
        ("Complemento ¬A = 1 - μA", complemento(A)),
    ]
    for ax, (titulo, res) in zip(axes.flat, ops):
        ax.plot(x, A, "--", color="tab:blue", label="A: Templada")
        if "Complemento" not in titulo:
            ax.plot(x, B, "--", color="tab:orange", label="B: Calida")
        if res is not None:
            ax.fill_between(x, res, color="tab:green", alpha=0.35)
            ax.plot(x, res, color="tab:green", linewidth=2.5, label="Resultado")
        ax.set_title(titulo)
        ax.set_xlabel("Temperatura (°C)")
        ax.set_ylabel("μ(x)")
        ax.set_ylim(-0.05, 1.08)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(SALIDA, "ej2_operadores.png"), dpi=130)
    plt.close(fig)

    # --- Comparacion de todas las T-conormas y T-normas ---
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 4.5))
    for t in tipos_union:
        a1.plot(x, union(A, B, t), linewidth=2, label=t)
    for t in tipos_inter:
        a2.plot(x, interseccion(A, B, t), linewidth=2, label=t)
    for ax, tit in [(a1, "Uniones (T-conormas)"), (a2, "Intersecciones (T-normas)")]:
        ax.plot(x, A, "k:", alpha=0.5)
        ax.plot(x, B, "k:", alpha=0.5)
        ax.set_title(tit + " de A=Templada y B=Calida")
        ax.set_xlabel("Temperatura (°C)")
        ax.set_ylim(-0.05, 1.08)
        ax.grid(alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(SALIDA, "ej2_comparacion_normas.png"), dpi=130)
    plt.close(fig)

    # --- Tabla numerica en puntos de muestra ---
    print("=== Ejercicio 2: Union, Interseccion y Complemento ===")
    puntos = [18, 22, 24, 26, 30]
    idx = [int(np.argmin(np.abs(x - p))) for p in puntos]
    print(f"\n{'x(°C)':>6} {'μA':>6} {'μB':>6} | " +
          " ".join(f"U_{t:<9}" for t in tipos_union) + "| " +
          " ".join(f"I_{t:<9}" for t in tipos_inter) + "| ¬A")
    for p, i in zip(puntos, idx):
        a, b = A[i], B[i]
        fila = f"{p:>6} {a:>6.3f} {b:>6.3f} | "
        fila += " ".join(f"{union(a, b, t):<11.3f}" for t in tipos_union) + "| "
        fila += " ".join(f"{interseccion(a, b, t):<11.3f}" for t in tipos_inter) + "| "
        fila += f"{complemento(a):.3f}"
        print(fila)

    # Verificacion de propiedades (con max/min/1-x)
    print("\nVerificacion de propiedades:")
    print("  Conmutatividad  A∪B = B∪A :", np.allclose(union(A, B), union(B, A)))
    print("  Conmutatividad  A∩B = B∩A :", np.allclose(interseccion(A, B), interseccion(B, A)))
    print("  Involucion      ¬¬A = A   :", np.allclose(complemento(complemento(A)), A))
    print("  De Morgan  ¬(A∪B)=¬A∩¬B  :",
          np.allclose(complemento(union(A, B)), interseccion(complemento(A), complemento(B))))
    print("  De Morgan  ¬(A∩B)=¬A∪¬B  :",
          np.allclose(complemento(interseccion(A, B)), union(complemento(A), complemento(B))))
    print("  Tercero excluido A∪¬A = X:", np.allclose(union(A, complemento(A)), 1),
          "(no se cumple en logica difusa)")
    print(f"\nGraficas guardadas en: {SALIDA}")


if __name__ == "__main__":
    main()
