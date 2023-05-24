from __future__ import annotations
from typing import Any
from modulos.paciente import Paciente

class ColaPrioridad:
    # Constructor
    def __init__(self) -> None:
        self.__lista_interna = [0]
        self.__tamanio = 0
        
    @property
    def tamanio(self) -> int:
        return self.__tamanio
    
    def __str__(self) -> str:
        res = ''
        for idx, item in enumerate(self.__lista_interna):
            if idx == 0:
                continue
            res += str(item)
            if idx + 1 <= self.tamanio:
                res += '\n'
        return res
    
    def __iter__(self):
        return self.__lista_interna[1:].__iter__()
    
    def __len__(self):
        return self.tamanio
    
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
        if self.__lista_interna[posicion] < self.__lista_interna[posicion // 2]:
            # Si tiene mayor prioridad (ya que es un montículo de mínimos), movemos
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
    
    def hijo_minimo(self, pos: int) -> int:
        """
        Compara los hijos del nodo en la posición pos para devolver el mínimo de ambos.

        Parameters
        ----------
        pos : int
            Posición del padre

        Returns
        -------
        int
            Posición del hijo mínimo
        """
        # Verificamos si tiene un hijo derecho
        if pos * 2 + 1 > self.__tamanio:
            # La comprobación de que en esta posicion este al menos un hijo izquierdo está antes
            # de la ejecución de este código
            return pos * 2
        else:
            return pos * 2 if self.__lista_interna[pos * 2] < self.__lista_interna[pos * 2 + 1] else pos * 2 + 1

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
        
        # Buscamos el hijo minimo del nodo
        hijo_minimo = self.hijo_minimo(pos)
        if self.__lista_interna[pos] > self.__lista_interna[hijo_minimo]:
            aux = self.__lista_interna[pos]
            self.__lista_interna[pos] = self.__lista_interna[hijo_minimo]
            self.__lista_interna[hijo_minimo] = aux
        
        self.infiltrar_abajo(hijo_minimo)
        
    def avanzar(self) -> Any:
        """
        Elimina el primer elemento de la cola de prioridad.

        Returns
        -------
        Any
            Item eliminado
        """
        # Posicion 1, la posición 0 jamás se toca.
        eliminado = self.__lista_interna[1]
        # Intercambiamos la posicion del último nodo de la lista interna
        self.__lista_interna[1] = self.__lista_interna[self.__tamanio]
        self.__tamanio -= 1
        # Eliminamos el elemento que movimos
        self.__lista_interna.pop()
        # Infiltramos el elemento que quedó en la cabeza para ponerlo en su posición correspondiente
        self.infiltrar_abajo(1)
        
        return eliminado
    
if __name__ == '__main__':
    prio = ColaPrioridad()
    for i in range(5):
        p = Paciente(i)
        prio.insertar(p)
    atendidos = []
    for i in range(5):
        atendido = prio.avanzar()
        atendidos.append(atendido)
    for item in atendidos:
        print(item)