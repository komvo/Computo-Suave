"""
Ejercicio 3: Proceso de composicion sup-star (max-min) y comprobacion con
    R = [[1, 0], [0, 1]]   y   S = [[1, 0, 0], [1, 0, 1]]

Ademas se valida con el ejemplo crisp de la presentacion (diapositiva 62).
"""
import numpy as np
from difuso import composicion, imprimir_matriz


def main():
    print("=== Ejercicio 3: Composicion sup-star (max-min) ===\n")
    R = np.array([[1, 0],
                  [0, 1]])
    S = np.array([[1, 0, 0],
                  [1, 0, 1]])
    imprimir_matriz("R(U,V)", R, "u", "v")
    imprimir_matriz("S(V,W)", S, "v", "w")
    print("\nCalculo paso a paso:")
    T = composicion(R, S, "min", detalle=True)
    print()
    imprimir_matriz("R o S (U,W)", T)
    print("\nComo R es la matriz identidad, R o S debe ser igual a S:",
          np.array_equal(T, S))

    # Validacion con el ejemplo de la presentacion
    print("\n--- Validacion con el ejemplo de la presentacion (diap. 62) ---")
    R1 = np.array([[0, 1, 0, 1],
                   [1, 0, 0, 0],
                   [0, 0, 1, 1]])
    R2 = np.array([[1, 0, 0, 0],
                   [0, 0, 0, 1],
                   [1, 1, 0, 0],
                   [0, 0, 1, 0]])
    esperado = np.array([[0, 0, 1, 1],
                         [1, 0, 0, 0],
                         [1, 1, 1, 0]])
    R3 = composicion(R1, R2, "min")
    imprimir_matriz("R1 o R2", R3)
    print("Coincide con T de la presentacion:", np.array_equal(R3, esperado))
    return T


if __name__ == "__main__":
    main()
