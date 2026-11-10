"""Graficas usadas en los notebooks; cada una se guarda tambien en la carpeta figuras/."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

FIG = Path(__file__).resolve().parent / 'figuras'
FIG.mkdir(exist_ok=True)
AZUL, NARANJA, GRIS = '#2a6fb0', '#e07b24', '#888888'


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(FIG / f'{nombre}.png', dpi=150, bbox_inches='tight')
    plt.show()


def mapa_correlacion(df, cols, titulo, nombre):
    c = df[cols].corr()
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    im = ax.imshow(c, vmin=-1, vmax=1, cmap='RdBu_r')
    ax.set_xticks(range(len(cols)), cols, rotation=45, ha='right')
    ax.set_yticks(range(len(cols)), cols)
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f'{c.iloc[i, j]:.2f}', ha='center', va='center', fontsize=8,
                    color='white' if abs(c.iloc[i, j]) > 0.6 else 'black')
    fig.colorbar(im, ax=ax)
    ax.set_title(titulo)
    _guardar(fig, nombre)
    return c


def histograma(serie, xlabel, titulo, nombre):
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.hist(serie, bins=20, color=AZUL, edgecolor='white')
    ax.axvline(serie.mean(), color=NARANJA, ls='--', label=f'media = {serie.mean():.1f}')
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Observaciones')
    ax.set_title(titulo)
    ax.legend()
    _guardar(fig, nombre)


def cajas_por_grupo(df, grupo, objetivo, ylabel, titulo, nombre, rotar=90):
    orden = df.groupby(grupo)[objetivo].median().sort_values().index
    datos = [df.loc[df[grupo] == g, objetivo] for g in orden]
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.boxplot(datos, patch_artist=True, boxprops=dict(facecolor='#cfe0f1'))
    ax.set_xticks(range(1, len(orden) + 1), orden, rotation=rotar, fontsize=7)
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    _guardar(fig, nombre)


def curva_perdida(curvas, titulo, nombre):
    fig, ax = plt.subplots(figsize=(8, 3.8))
    for etiqueta, curva, color in curvas:
        ax.plot(curva, label=etiqueta, color=color)
    ax.set_xlabel('Epoca')
    ax.set_ylabel('Perdida (MSE escalado)')
    ax.set_title(titulo)
    ax.legend()
    _guardar(fig, nombre)


def real_vs_predicho(y, predicciones, unidad, titulo, nombre):
    fig, axes = plt.subplots(1, len(predicciones), figsize=(5.2 * len(predicciones), 4.6))
    axes = np.atleast_1d(axes)
    lo = min(y.min(), *(p.min() for _, p, _ in predicciones))
    hi = max(y.max(), *(p.max() for _, p, _ in predicciones))
    for ax, (etiqueta, p, color) in zip(axes, predicciones):
        ax.scatter(y, p, alpha=.65, color=color, s=22)
        ax.plot([lo, hi], [lo, hi], '--', color=GRIS)
        ax.set_xlabel(f'Real ({unidad})')
        ax.set_ylabel(f'Predicho ({unidad})')
        ax.set_title(etiqueta)
    fig.suptitle(titulo)
    _guardar(fig, nombre)


def evolucion_ga(historial, titulo, nombre, base_cv=None):
    g = [h['generacion'] for h in historial]
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(g, [h['mejor'] for h in historial], 'o-', color=NARANJA, label='Mejor individuo')
    ax.plot(g, [h['promedio'] for h in historial], 's--', color=AZUL, label='Promedio poblacion')
    if base_cv is not None:
        ax.axhline(base_cv, color=GRIS, ls=':', label=f'Red base (R2 cv = {base_cv:.3f})')
    ax.set_xlabel('Generacion')
    ax.set_ylabel('Aptitud = R2 validacion cruzada')
    ax.set_title(titulo)
    ax.legend()
    _guardar(fig, nombre)


def barras_comparacion(tabla, metricas, titulo, nombre):
    fig, axes = plt.subplots(1, len(metricas), figsize=(4.2 * len(metricas), 3.8))
    colores = [GRIS, AZUL, NARANJA][-len(tabla):]
    for ax, m in zip(axes, metricas):
        vals = tabla[m].values
        ax.bar(tabla.index, vals, color=colores)
        for i, v in enumerate(vals):
            ax.text(i, v, f'{v:.3f}' if abs(v) < 10 else f'{v:.1f}', ha='center', va='bottom', fontsize=9)
        ax.set_title(m)
        ax.tick_params(axis='x', rotation=15)
    fig.suptitle(titulo)
    _guardar(fig, nombre)
