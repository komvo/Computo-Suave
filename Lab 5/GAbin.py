import random
import copy
from CromosomaBin import CromosomaBinario
from interfaz import AptitudMochila, SeleccionTorneo, ReproduccionUnCruce, MutacionFlip

class GA:
    def __init__(self, num_inv: int, num_genes: int, hyperparams: dict):
        self.poblacion = [CromosomaBinario(num_genes) for _ in range(num_inv)]
        self.num_inv = num_inv
        self.hyperparams = hyperparams
        self.evaluar = hyperparams['Aptitud']
        self.seleccion = hyperparams['Seleccion']
        self.reproducion = hyperparams['Reproduccion']
        self.mutacion = hyperparams['Mutacion']
        self.num_remplazo = int(hyperparams['por remplazo'] * num_inv)
        for individuo in self.poblacion:
            individuo.llenar_random_data()

    def buscar_solucion(self, tolerancia: float, var: dict):
        sum_score_prev = 0
        fail_score = None
        fail_count = 0
        generacion = 1
        # Se limita el número de generaciones para evitar bucles interminables.
        while generacion <= 2000:
            self.evaluar.evaluar_poblacion(self.poblacion, var)
            promedio = sum(c.score for c in self.poblacion) / self.num_inv
            avg_tol = abs(promedio - sum_score_prev) / max(1, abs(promedio))
            sum_score_prev = promedio
            if (generacion + 1) % 100 == 0:
                print(f'[{generacion:04d}] avg_err: {avg_tol:.5f} avg_score: {promedio:.5f}')
            if fail_score is not None and fail_score == avg_tol:
                fail_count += 1
            else:
                fail_count = 0
            if fail_count >= 10 or avg_tol < tolerancia:
                break
            fail_score = avg_tol
            self.poblacion.sort(key=lambda c: c.score, reverse=True)
            mating_pool = self.seleccion.seleccion_poblacion(self.poblacion)
            generacion_nueva = copy.deepcopy(self.poblacion[:self.num_remplazo])
            self.reproducion.reproduccion_poblacion(generacion_nueva, mating_pool, self.num_inv)
            self.mutacion.mutacion_poblacion(generacion_nueva)
            self.poblacion = generacion_nueva
            generacion += 1
        self.evaluar.evaluar_poblacion(self.poblacion, var)
        return generacion

def sum_pesos_test(pesos, cromosoma):
    return sum(pesos[i] for i in range(cromosoma.n_genes) if cromosoma.get_bits(i + 1) == 1)

def sum_valores_test(valores, cromosoma):
    return sum(valores[i] for i in range(cromosoma.n_genes) if cromosoma.get_bits(i + 1) == 1)

def ejecutar_prueba(nombre, variables, semilla=2026):
    random.seed(semilla)
    num_genes = 32
    cant_ind = 100
    gaparams = {
        'Aptitud': AptitudMochila(),
        'Seleccion': SeleccionTorneo(3),
        'Reproduccion': ReproduccionUnCruce(num_genes),
        'Mutacion': MutacionFlip(0.05),
        'por remplazo': 0.5
    }
    algoritmoGA = GA(cant_ind, num_genes, gaparams)
    generaciones = algoritmoGA.buscar_solucion(1e-4, variables)
    solucion = sorted(algoritmoGA.poblacion, key=lambda c: c.score, reverse=True)
    print(f'\n{nombre} | capacidad: {variables["capacidad"]} kg | generaciones: {generaciones}')
    print(f'{"id":^6} {"Cromosoma":^32} Score / Peso / Valor')
    for i, cromosoma in enumerate(solucion[:10]):
        peso = sum_pesos_test(variables['pesos'], cromosoma)
        valor = sum_valores_test(variables['valores'], cromosoma)
        print(f'[{i+1:^4d}] {cromosoma.bits:032b} : {cromosoma.score} -> {peso} kg / {valor}')
    # Para el reporte se usa la mejor solución que sí cabe en la mochila.
    factibles = [c for c in solucion if sum_pesos_test(variables['pesos'], c) <= variables['capacidad']]
    mejor = max(factibles, key=lambda c: c.score) if factibles else None
    if mejor:
        objetos = [i + 1 for i in range(num_genes) if mejor.get_bits(i + 1)]
        print(f'MEJOR FACTIBLE: objetos {objetos}; peso={sum_pesos_test(variables["pesos"],mejor)}; valor={sum_valores_test(variables["valores"],mejor)}')
    return mejor, generaciones

if __name__ == '__main__':
    random.seed(1288703)
    pesos = [random.randint(1, 10) for _ in range(32)]
    valores = [random.randint(10, 100) for _ in range(32)]
    print('Pesos:', pesos)
    print('Valores:', valores)
    variables = {'pesos': pesos, 'valores': valores, 'capacidad': 80}
    ejecutar_prueba('Prueba 1: original', variables)
    variables['capacidad'] = 60
    ejecutar_prueba('Prueba 2: capacidad modificada', variables)
    variables['capacidad'] = 80
    variables['pesos'] = [p + 2 if i < 8 else p for i, p in enumerate(pesos)]
    ejecutar_prueba('Prueba 3: pesos modificados', variables)
