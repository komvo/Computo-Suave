"""
Ejercicio 4: Composicion del ultimo ejemplo de la presentacion (diap. 66)
usando la T-norma = Producto (composicion max-producto), y comparacion con
la T-norma minimo (max-min).

    mu_c(u, v)   = [[0.9, 0.4, 0.1],        mu_mb(v, w) = [[0.0, 0.0],
                    [0.1, 0.4, 0.9]]                       [0.6, 0.0],
                                                           [1.0, 0.7]]
    Realizar mu_{C o MB}(u, w)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from difuso import composicion, imprimir_matriz
from ejercicio1_variables import SALIDA


def heatmap(ax, M, titulo):
    ax.imshow(M, cmap="Greens", vmin=0, vmax=1)
    for (i, j), v in np.ndenumerate(M):
        ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                color="white" if v > 0.6 else "black", fontsize=13)
    ax.set_xticks(range(M.shape[1]), [f"w{j + 1}" for j in range(M.shape[1])])
    ax.set_yticks(range(M.shape[0]), [f"u{i + 1}" for i in range(M.shape[0])])
    ax.set_title(titulo)


def main():
    print("=== Ejercicio 4: Composicion con T-norma = Producto ===\n")
    C = np.array([[0.9, 0.4, 0.1],
                  [0.1, 0.4, 0.9]])
    MB = np.array([[0.0, 0.0],
                   [0.6, 0.0],
                   [1.0, 0.7]])
    imprimir_matriz("mu_c(u,v)", C, "u", "v")
    imprimir_matriz("mu_mb(v,w)", MB, "v", "w")

    print("\nComposicion max-producto, paso a paso:")
    T_prod = composicion(C, MB, "producto", detalle=True)
    print()
    imprimir_matriz("mu_{C o MB}(u,w)  [max-producto]", T_prod)

    print("\nComparacion: composicion max-min, paso a paso:")
    T_min = composicion(C, MB, "min", detalle=True)
    print()
    imprimir_matriz("mu_{C o MB}(u,w)  [max-min]", T_min)

    esperado = np.array([[0.24, 0.07],
                         [0.90, 0.63]])
    print("\nResultado max-producto correcto (verificado a mano):",
          np.allclose(T_prod, esperado))
    print("Observacion: max-producto <= max-min en cada elemento:",
          bool(np.all(T_prod <= T_min + 1e-12)))

    os.makedirs(SALIDA, exist_ok=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.8))
    heatmap(a1, T_prod, "C ∘ MB  (max-producto)")
    heatmap(a2, T_min, "C ∘ MB  (max-min)")
    fig.tight_layout()
    fig.savefig(os.path.join(SALIDA, "ej4_composicion.png"), dpi=130)
    plt.close(fig)
    print(f"\nGrafica guardada en: {SALIDA}")
    return T_prod


if __name__ == "__main__":
    main()
