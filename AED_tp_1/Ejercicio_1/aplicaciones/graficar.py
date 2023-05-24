from modulos.LDE import ListaDobleEnlazada as Lista
import time
import numpy as np
from functools import wraps
import matplotlib.pyplot as plt

def calcular_tiempo(func: callable) -> callable:
    """Se pasa una función o método para medir el tiempo que toma una función o método en ejecutarse.
        Para utilizarse, se puede o bien decorar el método que se quiere medir,
        o bien llamar a la función pasando el método como parámetro.
    Args:
        func (callable): función/método a cronometrar.
    Return:
        tuple[tiempo en nanosegundos, return de la función/método en sí]
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        fun_return = func(*args, **kwargs)
        final = time.perf_counter_ns()
        time_result = final - start
        return (time_result, fun_return)
    
    return wrapper

if __name__ == '__main__':
    # Lista de tiempos del sort utilizado en la ListaDobleEnlazada
    lista_sort_res = []
    # Lista de ns
    ns = [10, 100, 1000, 2000, 5000, 10000, 20000]
    for n in ns:
        # Generamos una lista de n elementos aleatorios entre 0 y 1000
        rand_list = list(np.random.randint(low = 0, high = 1000, size = n))
        # Inicializamos las listas correspondientes y las llenamos con los valores randomizados.
        lista_python = rand_list
        lista_doble = Lista()
        for numero in rand_list:
            lista_doble.anexar(numero)
        
        # Tomamos el tiempo del sort de ListaDobleEnlazada
        tiempo, _ = calcular_tiempo(lista_doble.ordenar)()
        lista_sort_res.append(tiempo/10**9)
        
    # Graficamos
    figura = plt.figure()
    ejes = plt.axes()
    
    
    ejes.plot(ns, lista_sort_res)
    plt.title('Curva de orden de complejidad en función al número de elementos')
    plt.xlabel('Número de elementos')
    plt.ylabel('Tiempo (s)')
    figura.savefig('orden_ejecucion.png', dpi=500)
    plt.close(figura)