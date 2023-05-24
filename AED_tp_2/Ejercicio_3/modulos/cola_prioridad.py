from __future__ import annotations
from typing import Any
import random

class ColaPrioridad:
    # Constructor
    def __init__(self, de_maximos : bool = True) -> None:
        self.__lista_interna = [(0, 0)]
        self.__tamanio = 0
        self.__de_maximos = de_maximos
        
    @property
    def tamanio(self) -> int:
        return self.__tamanio
    
    def esta_vacia(self) -> bool:
        return self.__tamanio == 0
    
    def __str__(self) -> str:
        res = ''
        for idx, item in enumerate(self.__lista_interna):
            if idx == 0:
                continue
            res += str(item[0]) + ' ' + str(item[1])
            if idx + 1 <= self.tamanio:
                res += '\n'
        return res
    
    def __iter__(self):
        return iter(self.__lista_interna[1:])
    
    def __len__(self):
        return self.tamanio
    
    def __contains__(self, val: Any):
        for par in self.__lista_interna:
            if par[1] == val:
                return True
        return False
    
    def infiltrar_arriba(self, posicion: int) -> None:
        """
        Infiltra el elemento de en la posicion que recibe el parametro e intenta infiltrarla
        hacia arriba.

        Parameters
        ----------
        posicion : int
            Posicion del nodo a infiltrar.

        Returns
        -------
        None
        """
        if posicion // 2 == 0:
            return
        
        # Comparo el elemento a infiltrar con el padre del submonticulo
        if self.__de_maximos:
            if self.__lista_interna[posicion][0] > self.__lista_interna[posicion // 2][0]:
                # Si tiene mayor prioridad (ya que es un montículo de máximos), movemos
                aux = self.__lista_interna[posicion // 2]
                self.__lista_interna[posicion // 2] = self.__lista_interna[posicion]
                self.__lista_interna[posicion] = aux
        else:
            if self.__lista_interna[posicion][0] < self.__lista_interna[posicion // 2][0]:
                # Si tiene mayor prioridad (ya que es un montículo de mínimos}), movemos
                aux = self.__lista_interna[posicion // 2]
                self.__lista_interna[posicion // 2] = self.__lista_interna[posicion]
                self.__lista_interna[posicion] = aux
            
        self.infiltrar_arriba(posicion // 2)
    
    def insertar(self, item: Any) -> None:
        """
        Inserta un elemento en la cola de prioridad, manteniendo la propiedad de orden

        Parameters
        ----------
        item : Any
            Elemento a insertar en la cola de prioridad.

        Returns
        -------
        None
        """
        # Se añade a la lista interna
        self.__lista_interna.append(item)
        self.__tamanio += 1
        # Se infiltra el elemento para reposicionarlo si es necesario
        self.infiltrar_arriba(self.tamanio)
    
    def hijo_maximo_minimo(self, pos: int) -> int:
        """
        Compara los hijos del nodo en la posición pos para devolver el máximo o mínimo de ambos.

        Parameters
        ----------
        pos : int
            Posición del padre

        Returns
        -------
        int
            Posición del hijo máximo/mínimo
        """
        # Verificamos si tiene un hijo derecho
        if pos * 2 + 1 > self.__tamanio:
            # La comprobación de que en esta posicion este al menos un hijo izquierdo está antes
            # de la ejecución de este código
            return pos * 2
        else:
            if self.__de_maximos:
                return pos * 2 if self.__lista_interna[pos * 2][0] > self.__lista_interna[pos * 2 + 1][0] else pos * 2 + 1
            else:
                return pos * 2 if self.__lista_interna[pos * 2][0] < self.__lista_interna[pos * 2 + 1][0] else pos * 2 + 1

    def infiltrar_abajo(self, pos: int) -> None:
        """
        Infiltra hacia abajo el elemento de la raiz.

        Parameters
        ----------
        pos : int
            Posición del elemento a infiltrar.

        Returns
        -------
        None
        """
        # Condicion de corte
        if 2 * pos > self.__tamanio:
            return
        
        # Buscamos el hijo máximo/mínimo del nodo
        hijo_maximo_minimo = self.hijo_maximo_minimo(pos)
        if self.__de_maximos:
            if self.__lista_interna[pos][0] < self.__lista_interna[hijo_maximo_minimo][0]:
                aux = self.__lista_interna[pos]
                self.__lista_interna[pos] = self.__lista_interna[hijo_maximo_minimo]
                self.__lista_interna[hijo_maximo_minimo] = aux
        else:
            if self.__lista_interna[pos][0] > self.__lista_interna[hijo_maximo_minimo][0]:
                aux = self.__lista_interna[pos]
                self.__lista_interna[pos] = self.__lista_interna[hijo_maximo_minimo]
                self.__lista_interna[hijo_maximo_minimo] = aux
        
        self.infiltrar_abajo(hijo_maximo_minimo)
        
    def avanzar(self) -> Any:
        """
        Elimina el primer elemento de la cola de prioridad.

        Returns
        -------
        Any
            Item eliminado
        """
        # Posicion 1, la posición 0 jamás se toca.
        eliminado = self.__lista_interna[1][1]
        # Intercambiamos la posicion del último nodo de la lista interna
        self.__lista_interna[1] = self.__lista_interna[self.__tamanio]
        self.__tamanio -= 1
        # Eliminamos el elemento que movimos
        self.__lista_interna.pop()
        # Infiltramos el elemento que quedó en la cabeza para ponerlo en su posición correspondiente
        self.infiltrar_abajo(1)
        
        return eliminado
    
    def construir_monticulo(self, lista : list) -> None:
        """
        Construye un montículo a partir de una lista
        
        Parameters
        ----------
        lista : list
            Lista del cual se armará el montículo

        Returns
        -------
        None
        """
        i = len(lista) // 2
        self.__tamanio = len(lista)
        self.__lista_interna = [(0, 0)] + lista[:]
        while (i > 0):
            self.infiltrar_abajo(i)
            i -= 1
            
    def buscar_posicion(self, a_buscar: Any) -> int:
        pos = None
        i = 1
        while i <= self.tamanio:
            if self.__lista_interna[i][1] == a_buscar:
                pos = i
                break
            i += 1
        
        return pos
            
    def decrementar_clave(self, valor: Any, new_val: int) -> None:
        pos = self.buscar_posicion(valor)
        # print('##############\n', pos, valor, new_val, '\n##############')
        if not pos:
            # raise ValueError('El vértice buscado no se encuentra en el gráfo.')
            return
        
        old_clave = self.__lista_interna[pos][0]
        self.__lista_interna[pos] = (new_val, self.__lista_interna[pos][1])
        
        if self.__de_maximos:
            if old_clave < new_val:
                self.infiltrar_arriba(pos)
            else:
                self.infiltrar_abajo(pos)
        else:
            if old_clave < new_val:
                self.infiltrar_abajo(pos)
            else:
                self.infiltrar_arriba(pos)
    
if __name__ == '__main__':
    prio = ColaPrioridad(de_maximos=True)
    lista = [(3, 4), (5, 4), (5, 1), (6, 5), (7, 3)]
    # for i in range(5):
    #     rand = (random.randint(1,10), 8)
    #     prio.insertar(rand)
    prio.construir_monticulo(lista)
    prio.decrementar_clave(5, 99)
    
    ya_eliminados = []
    for i in range(5):
        eliminado = prio.avanzar()
        ya_eliminados.append(eliminado)
    
    print(f'Fue: {ya_eliminados}')
    pass