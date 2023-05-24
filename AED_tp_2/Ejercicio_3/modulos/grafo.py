from __future__ import annotations
from typing import Any
# Descomentar en caso de tener pyvis
# from pyvis.network import Network

class Vertice:
    """Representa cada vertice en el grafo, usa un diccionario para seguir a los vertices 
    que esta conectado"""
    def __init__(self, clave : Any) -> None:
        self._id = clave
        self.conectado_a = {}
        self._dist = 0
        self._predecesor = None
    
    def agregar_vecino(self, vecino : Any , ponderacion : int = 0):
        """
        Agrega como vecino a una clave como vértice con una ponderación 

        Parameters
        ----------
        vecino : Any
            Clave del vértice vecino.
        ponderacion : int, optional
            Ponderación de la arista que conecta ambos nodos. The default is 0.

        Returns
        -------
        None

        """
        self.conectado_a[vecino] = ponderacion
    
    def __str__(self) -> str:
        return str(self._id) + 'conectado' + str([x._id for x in self.conectado_a])
    
    def obtener_conexiones(self) -> list:
        """
        Obtiene las claves de los vértices vecinos del vértice actual.

        Returns
        -------
        list
            Lista de claves de vértices.

        """
        return self.conectado_a.keys()
    
    @property
    def clave(self) -> Any:
        return self._id
    
    @property
    def dist(self) -> int:
        return self._dist
    
    @dist.setter
    def dist(self, new_dist: int) -> None:
        self._dist = new_dist
        
    @property
    def predecesor(self) -> Vertice:
        return self._predecesor
    
    @predecesor.setter
    def predecesor(self, new_predecesor) -> None:
        self._predecesor = new_predecesor
    
    def obtener_ponderacion(self, vecino : Any) -> int:
        """
        Obtiene la ponderación de una arista dada la clave de un vecino del vértice actual.

        Parameters
        ----------
        vecino : Any
            Clave del vértice vecino a buscar.

        Returns
        -------
        int
            Ponderación de la arista.

        """
        return self.conectado_a[vecino]
    
class Grafo:
    def __init__(self) -> None:
        self.lista_vertices = {}
        self.num_vertices = 0
    
    def agregar_vertice(self, clave : Any) -> Vertice:
        """
        Agrega un vértice con clave "clave" al grafo.

        Parameters
        ----------
        clave : Any
            Clave del vértice a agregar.

        Returns
        -------
        Vertice
            Vertice agregado.

        """
        self.num_vertices += 1
        new_vertice = Vertice(clave)
        self.lista_vertices[clave] = new_vertice
        return new_vertice
    
    def obtener_vertice(self, clave : Any) -> Vertice:
        """
        Obtiene el vértice que contiene la clave dada.

        Parameters
        ----------
        clave : Any
            Clave del vértice a buscar.

        Returns
        -------
        Vertice
            Vertice buscado.

        """
        if clave in self.lista_vertices:
            return self.lista_vertices[clave]
        else:
            return None
    
    def __contains__(self, n : Any):
        return n in self.lista_vertices
    
    def agregar_arista(self, de : Any, a : Any, costo : int = 0) -> None:
        """
        Agrega una arista que une a ambos vértices de las claves dadas con cierta ponderación. En caso de no existir
        alguno de los dos vértices, se agregarán al grafo.

        Parameters
        ----------
        de : Any
            Clave del vértice del cual se agregará el vecino.
        a : Any
            Clave del vértice del vecino a agregar.
        costo : int, optional
            Ponderación de la arista agregada. The default is 0.

        Returns
        -------
        None

        """
        if de not in self.lista_vertices:
            self.agregar_vertice(de)
        if a not in self.lista_vertices:
            self.agregar_vertice(a)
        self.lista_vertices[de].agregar_vecino(self.lista_vertices[a], costo)
        
    def obtener_vertices(self):
        return self.lista_vertices.keys()
    
    def __iter__(self):
        return iter(self.lista_vertices.values())

########## 
# Visualizador de grafos usando pyvis, en caso de descomentar el código de abajo, asegurarse de tener instalado
# pyvis. Para instalarlo desde anaconda, utilizar el siguiente comando: conda install -c conda-forge pyvis
# Para instalarlo usando pip: pip install pyvis

# class VisualizadorGrafo:
#     """
#     Visualizador de grafos interactivos, se creará en la carpeta un archivo html que contendrá el grafo a visualizar.
#     Para utilizarlo, instanciar la clase dando como parámetro el grafo.
#     """
#     def __init__(self, grafo : Grafo, nombre : str = 'grafo.html', dirigido = True):
#         self.__network = Network(directed = dirigido, height = '900px')
#         self.__grafo = grafo
        
#         # Vertices
#         for v in self.__grafo:
#             self.__network.add_node(v.clave, shape='circle')
        
#         # Aristas
#         for v in self.__grafo:
#             for c in v.obtener_conexiones():
#                 self.__network.add_edge(v.clave, c.clave, value = v.obtener_ponderacion(c), title = str(v.obtener_ponderacion(c)), arrowStrikethrough=False)
        
#         self.__network.show(nombre)
    