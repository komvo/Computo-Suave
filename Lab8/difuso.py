"""
Libreria propia de conjuntos difusos tipo 1.

Contiene:
  - Funciones de membresia (MF): triangular, trapezoidal, gaussiana,
    gaussiana acampanada (bell) y sigmoidal.
  - Clase VariableLinguistica (quintupla v, T, X, g, m simplificada).
  - Operadores: union, interseccion y complemento (una funcion por operador).
  - Composicion sup-star (max-T) de relaciones difusas.
"""
import numpy as np


# ---------------------------------------------------------------------------
# Funciones de membresia
# ---------------------------------------------------------------------------
def trimf(x, a, b, c):
    """MF triangular  mu(x; a, b, c)."""
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    if b > a:
        m = (a <= x) & (x <= b)
        y[m] = (x[m] - a) / (b - a)
    if c > b:
        m = (b <= x) & (x <= c)
        y[m] = (c - x[m]) / (c - b)
    y[x == b] = 1.0
    return y


def trapmf(x, a, b, c, d):
    """MF trapezoidal  mu(x; a, b, c, d)."""
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    if b > a:
        m = (a <= x) & (x < b)
        y[m] = (x[m] - a) / (b - a)
    y[(b <= x) & (x <= c)] = 1.0
    if d > c:
        m = (c < x) & (x <= d)
        y[m] = (d - x[m]) / (d - c)
    return y


def gaussmf(x, sigma, c):
    """MF gaussiana  mu(x; sigma, c) = exp(-(x - c)^2 / (2 sigma^2))."""
    x = np.asarray(x, dtype=float)
    return np.exp(-((x - c) ** 2) / (2.0 * sigma ** 2))


def gbellmf(x, a, b, c):
    """MF gaussiana acampanada  mu(x; a, b, c) = 1 / (1 + |(x - c)/a|^(2b))."""
    x = np.asarray(x, dtype=float)
    return 1.0 / (1.0 + np.abs((x - c) / a) ** (2 * b))


def sigmf(x, a, c):
    """MF sigmoidal  mu(x; a, c) = 1 / (1 + exp(-a (x - c)))."""
    x = np.asarray(x, dtype=float)
    return 1.0 / (1.0 + np.exp(-a * (x - c)))


# ---------------------------------------------------------------------------
# Variable linguistica
# ---------------------------------------------------------------------------
class VariableLinguistica:
    """Variable linguistica: nombre, universo X y terminos {nombre: MF}."""

    def __init__(self, nombre, universo, unidad=""):
        self.nombre = nombre
        self.universo = np.asarray(universo, dtype=float)
        self.unidad = unidad
        self.terminos = {}  # nombre -> (descripcion de la MF, vector mu)

    def agregar_termino(self, nombre, mf, *params):
        desc = f"{mf.__name__}{tuple(params)}"
        self.terminos[nombre] = (desc, mf(self.universo, *params))
        return self

    def __getitem__(self, termino):
        return self.terminos[termino][1]

    def fusificar(self, valor):
        """Grado de membresia de un valor crisp en cada termino (interpolado)."""
        return {t: float(np.interp(valor, self.universo, mu))
                for t, (_, mu) in self.terminos.items()}


# ---------------------------------------------------------------------------
# Operadores para conjuntos difusos tipo 1
# ---------------------------------------------------------------------------
def union(mu_a, mu_b, tipo="max"):
    """Union (T-conorma / s-norma).

    tipo:
      'max'        -> max(mu_a, mu_b)
      'suma_alg'   -> mu_a + mu_b - mu_a*mu_b      (suma algebraica)
      'suma_acot'  -> min(1, mu_a + mu_b)          (suma acotada)
      'drastica'   -> mu_a si mu_b=0, mu_b si mu_a=0, 1 en otro caso
    """
    a = np.asarray(mu_a, dtype=float)
    b = np.asarray(mu_b, dtype=float)
    if tipo == "max":
        return np.maximum(a, b)
    if tipo == "suma_alg":
        return a + b - a * b
    if tipo == "suma_acot":
        return np.minimum(1.0, a + b)
    if tipo == "drastica":
        return np.where(b == 0, a, np.where(a == 0, b, 1.0))
    raise ValueError(f"Tipo de union desconocido: {tipo}")


def interseccion(mu_a, mu_b, tipo="min"):
    """Interseccion (T-norma).

    tipo:
      'min'        -> min(mu_a, mu_b)
      'producto'   -> mu_a * mu_b                  (producto algebraico)
      'prod_acot'  -> max(0, mu_a + mu_b - 1)      (producto acotado / Lukasiewicz)
      'drastica'   -> mu_a si mu_b=1, mu_b si mu_a=1, 0 en otro caso
    """
    a = np.asarray(mu_a, dtype=float)
    b = np.asarray(mu_b, dtype=float)
    if tipo == "min":
        return np.minimum(a, b)
    if tipo == "producto":
        return a * b
    if tipo == "prod_acot":
        return np.maximum(0.0, a + b - 1.0)
    if tipo == "drastica":
        return np.where(b == 1, a, np.where(a == 1, b, 0.0))
    raise ValueError(f"Tipo de interseccion desconocido: {tipo}")


def complemento(mu_a):
    """Complemento estandar: 1 - mu_a."""
    return 1.0 - np.asarray(mu_a, dtype=float)


# ---------------------------------------------------------------------------
# Composicion sup-star (max-T)
# ---------------------------------------------------------------------------
def composicion(R, S, tnorma="min", detalle=False):
    """Composicion sup-star:  mu_{R o S}(u, w) = max_v [ mu_R(u, v) * mu_S(v, w) ]

    R: matriz |U| x |V|,  S: matriz |V| x |W|.
    tnorma: 'min' o 'producto' (cualquier tipo aceptado por `interseccion`).
    Si detalle=True, imprime el calculo de cada elemento.
    """
    R = np.asarray(R, dtype=float)
    S = np.asarray(S, dtype=float)
    if R.shape[1] != S.shape[0]:
        raise ValueError(f"Dimensiones incompatibles: R{R.shape} y S{S.shape}")

    n_u, n_v = R.shape
    n_w = S.shape[1]
    T = np.zeros((n_u, n_w))
    for i in range(n_u):
        for j in range(n_w):
            terminos = interseccion(R[i, :], S[:, j], tnorma)  # vector sobre v
            T[i, j] = terminos.max()
            if detalle:
                pares = ", ".join(
                    f"{tnorma}({R[i, k]:g},{S[k, j]:g})={terminos[k]:.2f}"
                    for k in range(n_v))
                print(f"  T(u{i + 1},w{j + 1}) = max[{pares}] = {T[i, j]:.2f}")
    return T


def imprimir_matriz(nombre, M, filas="u", cols="w"):
    M = np.asarray(M, dtype=float)
    print(f"{nombre} =")
    print("       " + "".join(f"{cols}{j + 1:<6}" for j in range(M.shape[1])))
    for i, fila in enumerate(M):
        print(f"  {filas}{i + 1}  " + "".join(f"{v:<7.2f}" for v in fila))
