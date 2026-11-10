"""Carga de datasets, construccion de redes y metricas (comun a los dos notebooks)."""
import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import TransformedTargetRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import configuracion as cfg

warnings.filterwarnings('ignore')
CARPETA = Path(__file__).resolve().parent
DATOS = CARPETA / 'datasets'


# ------------------------------------------------------------------
# Datasets
# ------------------------------------------------------------------
def cargar_soybean():
    """Forty Soybean Cultivars (UCI). Salida: GY (kg/ha)."""
    df = pd.read_csv(DATOS / 'soy' / 'data.csv')
    df['Cultivar'] = df['Cultivar'].str.strip()
    numericas = ['PH', 'IFP', 'NLP', 'NGP', 'NGL', 'NS', 'MHG']
    dummies = pd.get_dummies(df['Cultivar'], prefix='Cult').astype(float)
    X = pd.concat([df[numericas + ['Season']], dummies], axis=1)
    # Cada "variable" que el GA puede activar/desactivar y las columnas que representa.
    grupos = {v: [v] for v in numericas}
    grupos['Cultivar'] = list(dummies.columns)
    grupos['Season'] = ['Season']
    return df, X, df['GY'], grupos


def _diametro(v):
    nums = re.findall(r'\d+(?:\.\d+)?', str(v))
    return np.mean([float(x) for x in nums]) if nums else np.nan


def _cosecha(archivo, experimento):
    x = pd.ExcelFile(archivo)
    hoja = [s for s in x.sheet_names if 'Harvest' in s][0]
    raw = pd.read_excel(archivo, sheet_name=hoja, header=None)
    h = next(i for i, row in raw.iterrows()
             if row.astype(str).str.contains('Total weight', case=False, na=False).any())
    headers = [str(v).strip() if pd.notna(v) else f'c{j}' for j, v in enumerate(raw.iloc[h])]
    t = raw.iloc[h + 1:].copy()
    t.columns = headers

    def buscar(s):
        return next((c for c in t.columns if s.lower() in str(c).lower()), None)

    mapa = {'total_weight': buscar('Total weight'), 'plant_height': buscar('Plant height'),
            'shoot_length': buscar('Shoot length'), 'root_length': buscar('Root length'),
            'head_diameter': buscar('Head diameter') or buscar('H.D'),
            'stem_diameter': buscar('Stem diameter'), 'leaves': buscar('leaves')}
    o = pd.DataFrame({k: t[v] for k, v in mapa.items() if v})
    o['head_diameter'] = o['head_diameter'].map(_diametro)
    for c in ['total_weight', 'plant_height', 'shoot_length', 'root_length', 'stem_diameter', 'leaves']:
        o[c] = pd.to_numeric(o[c], errors='coerce')
    o['experimento'] = experimento
    return o.dropna(subset=['total_weight', 'plant_height', 'shoot_length',
                            'root_length', 'stem_diameter', 'leaves'])


def cargar_hydro():
    """HydroGrowNet - lechuga Batavia. Salida: peso total de la cosecha (g)."""
    archivos = sorted((DATOS / 'hydro').glob('*.xlsx'))
    df = pd.concat([_cosecha(f, i + 1) for i, f in enumerate(archivos)], ignore_index=True)
    variables = ['plant_height', 'shoot_length', 'root_length', 'stem_diameter', 'leaves', 'head_diameter']
    X = df[variables].astype(float)
    grupos = {v: [v] for v in variables}
    return df, X, df['total_weight'].astype(float), grupos


# ------------------------------------------------------------------
# Cromosoma <-> red neuronal
# ------------------------------------------------------------------
def genes_del_problema(grupos):
    """Nombres de los genes y cuantas opciones tiene cada uno."""
    nombres = list(cfg.ESPACIO_RED) + [f'usar_{g}' for g in grupos]
    opciones = [len(v) for v in cfg.ESPACIO_RED.values()] + [2] * len(grupos)
    return nombres, opciones


def decodificar(genes, grupos):
    """Convierte la lista de indices del cromosoma en hiperparametros legibles."""
    e = cfg.ESPACIO_RED
    n_red = len(e)
    valor = {k: e[k][genes[i]] for i, k in enumerate(e)}
    capas = valor['capas']
    ocultas = tuple(valor[f'neuronas{i + 1}'] for i in range(capas))
    usadas = [g for j, g in enumerate(grupos) if genes[n_red + j] == 1]
    return {'variables': usadas, 'ocultas': ocultas, 'activacion': valor['activacion'],
            'tasa_aprendizaje': valor['tasa_aprendizaje'], 'alpha': valor['alpha'],
            'batch': valor['batch']}


def columnas(params, grupos):
    return [c for v in params['variables'] for c in grupos[v]]


def crear_red(params, semilla=cfg.SEMILLA_RED):
    """Imputacion -> estandarizacion -> MLP; la salida tambien se estandariza (como en el Lab 4)."""
    red = Pipeline([
        ('imputador', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('nn', MLPRegressor(hidden_layer_sizes=params['ocultas'], activation=params['activacion'],
                            solver='adam', learning_rate_init=params['tasa_aprendizaje'],
                            alpha=params['alpha'], batch_size=params['batch'],
                            max_iter=cfg.MAX_ITER, early_stopping=True, validation_fraction=0.2,
                            n_iter_no_change=cfg.PACIENCIA, random_state=semilla)),
    ])
    return TransformedTargetRegressor(regressor=red, transformer=StandardScaler())


def describir(params, grupos=None):
    """Texto corto de la red; la primera cifra es el numero real de entradas (columnas)."""
    arq = '-'.join(str(n) for n in params['ocultas'])
    entradas = len(columnas(params, grupos)) if grupos else len(params['variables'])
    return (f"{entradas}-{arq}-1 | {params['activacion']} | lr={params['tasa_aprendizaje']} | "
            f"alpha={params['alpha']} | batch={params['batch']}")


# ------------------------------------------------------------------
# Metricas
# ------------------------------------------------------------------
def metricas(y, p):
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    return {'R2': float(r2_score(y, p)), 'R': float(np.corrcoef(y, p)[0, 1]),
            'MAE': float(mean_absolute_error(y, p)), 'RMSE': float(np.sqrt(mean_squared_error(y, p))),
            'MSE': float(mean_squared_error(y, p))}


def entrenar_y_evaluar(params, grupos, Xtr, ytr, Xte, yte, semilla=cfg.SEMILLA_RED):
    """Entrena con el 60 % y evalua con el 40 %. Devuelve modelo, prediccion y metricas.

    'loss_final' es la perdida (MSE/2 escalado + L2) del ultimo epoch de entrenamiento;
    'MSE' es la perdida total en el conjunto de prueba en unidades originales.
    """
    cols = columnas(params, grupos)
    modelo = crear_red(params, semilla).fit(Xtr[cols], ytr)
    pred = modelo.predict(Xte[cols])
    m = metricas(yte, pred)
    nn = modelo.regressor_['nn']
    m['loss_final'] = float(nn.loss_curve_[-1])
    m['epocas'] = int(nn.n_iter_)
    m['parametros'] = int(sum(w.size for w in nn.coefs_) + sum(b.size for b in nn.intercepts_))
    return modelo, pred, m


def robustez(params, grupos, Xtr, ytr, Xte, yte):
    """Repite el entrenamiento con varias inicializaciones de pesos."""
    filas = []
    for s in cfg.SEMILLAS_ROBUSTEZ:
        _, _, m = entrenar_y_evaluar(params, grupos, Xtr, ytr, Xte, yte, semilla=s)
        filas.append({'semilla': s, 'R2': m['R2'], 'MAE': m['MAE'], 'RMSE': m['RMSE']})
    return pd.DataFrame(filas)
