from modulos.cola_prioridad import ColaPrioridad
from modulos.grafo import Grafo, Vertice
# Descomentar en caso de tener pyvis
# from modulos.grafo import VisualizadorGrafo
import numpy as np

def abrir_archivo_de_rutas(name: str = 'rutas.txt') -> list:
    """
    Abre un archivo de nombre name y devuelve una lista de elementos.

    Parameters
    ----------
    name : str, optional
        Nombre del archivo a abrir. The default is 'rutas.txt'.

    Returns
    -------
    list
        Lista de aristas.

    """
    datos = []
    with open(name, 'r') as arch:
        for line in arch:
            ciudad, conexion, peso, costo = line.rstrip('\n').split(',')
            datos.append((ciudad, conexion, int(peso), int(costo)))
    
    return datos

def dijkstra_pesos(grafo: Grafo, inicio : Vertice) -> None:
    """
    Algoritmo de dijkstra de pesos máximos (cuello de botella)

    Parameters
    ----------
    grafo : Grafo
        Grafo a realizar el dijkstra.
    inicio : Vertice
        Vértice de inicio con el cuál se generarán los pesos.

    Returns
    -------
    None

    """
    cp = ColaPrioridad()
    inicio.dist = np.Inf
    cp.construir_monticulo([(v.dist, v) for v in grafo])
    while not cp.esta_vacia():
        vertice_actual = cp.avanzar()
        for vertice_siguiente in vertice_actual.obtener_conexiones():
            distancia = min(vertice_actual.dist, vertice_actual.obtener_ponderacion(vertice_siguiente))
            if distancia > vertice_siguiente.dist:
                vertice_siguiente.dist = distancia
                vertice_siguiente.predecesor = vertice_actual
                cp.decrementar_clave(vertice_siguiente, distancia)

def dijkstra_costo(grafo: Grafo, inicio : Vertice) -> None:
    """
    Algoritmo de dijkstra para caminos mínimos.

    Parameters
    ----------
    grafo : Grafo
        Grafo a realizar el dijkstra.
    inicio : Vertice
        Vértice de inicio con el cuál se generarán los pesos.

    Returns
    -------
    None

    """
    cp = ColaPrioridad(de_maximos=False)
    
    # Seteamos la distancia de los vertices en infinito
    for v in grafo:
        v.dist = np.Inf
    
    inicio.dist = 0
    cp.construir_monticulo([(v.dist, v) for v in grafo])
    while not cp.esta_vacia():
        vertice_actual = cp.avanzar()
        for vertice_siguiente in vertice_actual.obtener_conexiones():
            nuevo_costo = vertice_actual.dist + vertice_actual.obtener_ponderacion(vertice_siguiente)
            if nuevo_costo < vertice_siguiente.dist:
                vertice_siguiente.dist = nuevo_costo
                vertice_siguiente.predecesor = vertice_actual
                cp.decrementar_clave(vertice_siguiente, nuevo_costo)

def calcular_cuello_de_botella(grafo: Grafo, de: str, a: str) -> int:
    """
    Calcula el máximo cuello de botella para el camino de cierta ubicación a cierto destino.

    Parameters
    ----------
    grafo : Grafo
        Grafo del cual se calculará.
    de : str
        Origen.
    a : str
        Destino.

    Raises
    ------
    ValueError
        El destino del camino no se encuentra en el grafo.

    Returns
    -------
    int
        Cuello de botella máximo para el camino.

    """
    dijkstra_pesos(grafo, grafo.obtener_vertice(de))
    vertice_destino = grafo.obtener_vertice(a)
    if vertice_destino:
        return vertice_destino.dist
    else:
        raise ValueError('La ciudad {a} no se encuentra en las rutas!')

def calcular_costo_minimo(grafo: Grafo, de: str, a: str) -> int:
    """
    Calcula el camino de costo mínimo posible para un destino

    Parameters
    ----------
    grafo : Grafo
        Grafo del cual se calculará.
    de : str
        Origen.
    a : str
        Destino.

    Returns
    -------
    int
        Costo mínimo para el camino.

    """
    dijkstra_costo(grafo, grafo.obtener_vertice(de))
    return grafo.obtener_vertice(a).dist

def calcular_opciones_de_transporte(de: str, a: str, arch: str = 'rutas.txt') -> tuple:
    """
    Calcula el camino con el máximo cuello de botella y mínimo costo para un origen y un destino.s

    Parameters
    ----------
    de : str
        Origen del camino.
    a : str
        Destino del camino.
    arch : str, optional
        Nombre del archivo del cual tenemos datos. The default is 'rutas.txt'.

    Returns
    -------
    tuple
        Tupla que contiene el máximo cuello de botella, el mínimo costo y el camino en cuestión.

    """
    grafo_pesos_maximos = Grafo()
    datos = abrir_archivo_de_rutas(arch)
    for _de, _a, _peso, _ in datos:
        grafo_pesos_maximos.agregar_arista(_de, _a, _peso)
    
    # VisualizadorGrafo(grafo_pesos_maximos, 'grafo_pesos_maximos.html')
    
    bottleneck = calcular_cuello_de_botella(grafo_pesos_maximos, de, a)
    
    # Luego de calcular el peso máximo permitido, armamos nuevamente el grafo obviando las aristas que no cumplan con este requisito
    grafo_costo_minimo = Grafo()
    for _de, _a, _peso, _costo in datos:
        if _peso >= bottleneck:
            grafo_costo_minimo.agregar_arista(_de, _a, _costo)
    
    # VisualizadorGrafo(grafo_costo_minimo, 'grafo_costo_minimo.html')
    
    costo_minimo = calcular_costo_minimo(grafo_costo_minimo, de, a)
    
    it = grafo_costo_minimo.obtener_vertice(a)
    camino = [it.clave]
    while it.predecesor:
        camino.append(it.predecesor.clave)
        it = it.predecesor
    
    camino.reverse()
    return bottleneck, costo_minimo, camino

if __name__ == '__main__':
    ciudad_destino = input('Ingrese una ciudad de destino: ')
    bottleneck, costo_minimo, camino = calcular_opciones_de_transporte('CiudadBs.As.', ciudad_destino, 'rutas.txt')
    print(f'Máximo peso permitido: {bottleneck}kg\nCosto mínimo: ${costo_minimo*1000}\nRuta a realizar: {camino}')

    