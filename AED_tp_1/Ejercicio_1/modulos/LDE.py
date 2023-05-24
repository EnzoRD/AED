from __future__ import annotations
from typing import Any
import Excepciones as ex

class Nodo:
    def __init__(self, p_dato: Any = None, p_nodo_siguiente: Nodo = None, p_nodo_anterior: Nodo = None) -> None:
        self.dato = p_dato
        self.anterior = p_nodo_anterior
        self.siguiente = p_nodo_siguiente
        
    @property
    def dato(self) -> Any:
        """Getter del dato del nodo"""
        return self._dato
    
    @dato.setter
    def dato(self, p_dato: Any) -> None:
        """Setter del dato del nodo"""
        self._dato = p_dato
    
    @property
    def anterior(self) -> Nodo:
        """Getter del nodo anterior"""
        return self._anterior
    
    @anterior.setter
    def anterior(self, p_nodo_anterior: Nodo) -> None:
        """Setter del nodo anterior"""
        self._anterior = p_nodo_anterior
    
    @property
    def siguiente(self) -> Nodo:
        """Getter del nodo siguiente"""
        return self._siguiente
    
    @siguiente.setter
    def siguiente(self, p_nodo_siguiente: Nodo) -> None:
        """Setter del nodo siguiente"""
        self._siguiente = p_nodo_siguiente

class ListaDobleEnlazada:
    def __init__(self) -> None:
        self.cabeza = None
        self.cola = None
        self._tamanio = 0
        
    @property
    def cabeza(self) -> Nodo:
        """Getter de la cabeza de la lista"""
        return self._cabeza
    
    @cabeza.setter
    def cabeza(self, p_cabeza: Nodo) -> None:
        """Setter de la cabeza de la lista"""
        self._cabeza = p_cabeza
        
    @property
    def cola(self) -> Nodo:
        """Getter de la cola de la lista"""
        return self._cola
    
    @cola.setter
    def cola(self, p_cola: Nodo) -> Nodo:
        """Setter de la cola de la lista"""
        self._cola = p_cola
    
    @property
    def tamanio(self) -> int:
        """Getter del tamaño de la lista"""
        return self._tamanio
        
    def iniciar_lista_vacia(self, data: Any) -> None:
        """
        Inicia la lista con un dato

        Parameters
        ----------
        data : Any
            Dato que contendrá la lista inicializada.

        Returns
        -------
        None
        """
        new_nodo = Nodo(data)
        self.cabeza = new_nodo
        self.cola = new_nodo
        self._tamanio += 1 
        
    def esta_vacia(self) -> bool:
        """
        Chequea si la lista está vacía.

        Returns
        -------
        bool
        """
        return self._tamanio == 0
    
    def agregar(self, item: Any) -> None:
        """
        Agrega un nodo al principio de la lista

        Parameters
        ----------
        item : Any
            Dato a agregar a la lista

        Returns
        -------
        None
        """
        # Si la lista está vacía, directamente inicializamos una lista vacia con el dato
        if self.esta_vacia():
            self.iniciar_lista_vacia(item)
            return
        
        new_nodo = Nodo(item)
        # El nodo siguiente al dato ingresado será la cabeza de la lista
        new_nodo.siguiente = self.cabeza
        # El anterior de la cabeza es el nodo recién insertado
        self.cabeza.anterior = new_nodo
        # La cabeza ahora es el nodo insertado
        self.cabeza = new_nodo
        # Aumentamos el tamaño
        self._tamanio += 1
    
    def anexar(self, item: Any) -> None:
        """
        Inserta un nodo en el final de la lista.

        Parameters
        ----------
        item : Any
            Dato a agregar a la lista.

        Returns
        -------
        None
        """
        if self.esta_vacia():
            self.iniciar_lista_vacia(item)
            return
        
        new_nodo = Nodo(item)
        # El nodo anterior al dato insertado es la cola
        new_nodo.anterior = self.cola
        # El siguiente de la cola es el nodo a insertar
        self.cola.siguiente = new_nodo
        # La cola ahora es el nodo insertado
        self.cola = new_nodo
        # Aumentamos el tamaño
        self._tamanio += 1
    
    def insertar(self, pos: int, item: Any) -> None:
        """
        Inserta un dato la posición de la lista

        Parameters
        ----------
        pos : int
            Posición de la lista a la cual el item se insertará.
        item : Any
            Dato a insertar.

        Raises
        ------
        ex.PosicionMenorALimiteInferior
            En caso de que la posición sea menor a 0.
        ex.PosicionMayorAlTamanio
            En caso de que la posición sea mayor al tamaño de la lista.

        Returns
        -------
        None
        """
        # Excepciones para los limites de inserción de la lista.
        if pos < 0:
            raise ex.PosicionMenorALimiteInferior(pos, 0)
        if pos > self.tamanio:
            raise ex.PosicionMayorAlTamanio(pos, self.tamanio)
        # Si la posición es 0, insertamos en el inicio de la lista
        if pos == 0:
            self.agregar(item)
        # Si la posición es igual al tamaño de la lista, insertamos al final.
        elif pos == self._tamanio:
            self.anexar(item)
        # Sino, hay que ingresarlo en un nodo interno.
        else:
            # Vamos hasta la posición deseada
            current_pos = 0
            current_nodo = self.cabeza
            while (current_pos != pos):
                current_nodo = current_nodo.siguiente
                current_pos += 1
            
            # Si por algún motivo estamos en la cola, anexamos el item al final
            if current_nodo is None:
                self.anexar(item)
                return
            
            # Creamos el nodo con el dato a ingresar.
            new_nodo = Nodo(item)
            # El anterior del nodo a insertar, es el nodo anterior de la posición actual
            new_nodo.anterior = current_nodo.anterior
            # El siguiente del nodo a insertar es el nodo de la posición actual
            new_nodo.siguiente = current_nodo
            # Si existe un nodo anterior, el siguiente del anterior es el nodo a insertar
            if current_nodo.anterior:
                current_nodo.anterior.siguiente = new_nodo
            # El anterior del nodo en la posición actual, es el nuevo nodo.
            current_nodo.anterior = new_nodo
            
            # Aumentamos el tamaño de la lista.
            self._tamanio += 1
    
    def extraer(self, pos: int = None) -> Nodo:
        """
        Extrae un nodo en una posición dada.
        Parameters
        ----------
        pos : int, optional
            Posición del nodo a eliminar

        Raises
        ------
        ex.PosicionMayorAlTamanio
            La posición fue mayor al tamaño de la lista.
        ex.PosicionMenorALimiteInferior
            La posición fue menor -1, que es el menor valor aceptado
        ex.ListaVacia
            La lista de la que se intentó extraer un elemento, está vacía.
        Returns
        -------
        Nodo
            Nodo eliminado en la posición deseada.
        """
        # Excepciones para los limites de extracción de la lista.
        if pos and pos > self.tamanio:
            raise ex.PosicionMayorAlTamanio(pos, self.tamanio)
        if pos and pos < -1:
            raise ex.PosicionMenorALimiteInferior(pos, -1)
        if self.esta_vacia():
            raise ex.ListaVacia()
        # Si la posición es 0, debemos eliminar la cabeza de la lista
        if pos == 0:
            item_eliminado = self.cabeza
            # Si este if se cumple, la lista solo tenía un solo elemento.
            if not self.cabeza.siguiente:
                self.cabeza = None
            else:
                # El siguiente de la cabeza es la cabeza.
                self.cabeza = self.cabeza.siguiente
                # El anterior de la cabeza ya no existe.
                self.cabeza.anterior = None
            # Decrementamos el tamaño
            self._tamanio -= 1
            return item_eliminado
        # Si estas condiciones se cumplen, se debe insertar al final
        if pos is None or pos == -1 or pos == self._tamanio-1:
            item_eliminado = self.cola
            # La lista tiene un solo item si esto se cumple
            if self.cola.anterior:
                self.cola.anterior.siguiente = None
            # La cola ahora es el elemento anterior a la cola
            self.cola = self.cola.anterior
            # Decrementamos el tamaño
            self._tamanio -= 1
            return item_eliminado
        else:
            # Extraemos un nodo interior
            # Nos movemos hasta la posición que se quiere extraer
            current_pos = 0
            current_nodo = self.cabeza
            while current_pos != pos:
                current_pos += 1
                current_nodo = current_nodo.siguiente
            
            # Si existe el anterior del nodo actual (no es la cabeza), asignamos
            # el siguiente del anterior al siguiente del nodo actual
            if current_nodo.anterior:
                current_nodo.anterior.siguiente = current_nodo.siguiente
            # Misma situación con la cola, si existe el siguiente del nodo actual
            # asignamos como anterior del siguiente al nodo anterior del nodo actual
            if current_nodo.siguiente:
                current_nodo.siguiente.anterior = current_nodo.anterior
            
            # Si de algún modo estamos en la cabeza, asignamos la cabeza como el nodo siguiente
            if current_pos == 0:
                self.cabeza = current_nodo.siguiente
            # Decrementamos el tamaño
            self._tamanio -= 1
            return current_nodo
    
    def copiar(self) -> ListaDobleEnlazada:
        """
        Hace una copia de la lista, permitiendo deepcopy para listas de python y para
        variables que sean instancia de nuestra lista.

        Returns
        -------
        ListaDobleEnlazada
            Copia de la lista actual.

        """
        nueva_lista = ListaDobleEnlazada()
        # Creamos una nueva lista, recorremos la actual, e insertamos en la lista nueva
        nodo_actual = self.cabeza
        while nodo_actual:
            # si es una instancia de lista, llamamos al método de copy del dato (deepcopy)
            if isinstance(nodo_actual.dato, ListaDobleEnlazada):
                nueva_lista.anexar(nodo_actual.dato.copiar())
            # si es una instancia de lista de Python, hacemos una copia de lista de Python
            elif isinstance(nodo_actual.dato, list):
                nueva_lista.anexar(nodo_actual.dato[:])
            else:
                # Simplemente anexamos el dato del nodo
                nueva_lista.anexar(nodo_actual.dato)
            nodo_actual = nodo_actual.siguiente
        
        return nueva_lista
    
    def invertir(self) -> None:
        """
        Invierte la lista, haciendo que lo que antes era la cabeza sea ahora la cola.

        Returns
        -------
        None
        """
        # Si está vacía no hacemos nada.
        if self.esta_vacia():
            return
        
        # Empezamos desde la cabeza
        current = self.cabeza
        # Guardamos el siguiente de la lista
        siguiente = current.siguiente
        # Hacemos que el siguiente de donde estamos parados sea None, la cabeza será la cola
        current.siguiente = None
        # El anterior del nodo actual será el siguiente
        current.anterior = siguiente
        # La cola ahora es el nodo actual
        self.cola = current
        
        while siguiente:
            # Ahora recorremos la lista normalmente e invertimos los nodos
            # El anterior es ahora el siguiente
            siguiente.anterior = siguiente.siguiente
            # El siguiente del siguiente es el nodo actual
            siguiente.siguiente = current
            # Guardamos el siguiente como el actual
            current = siguiente
            # Siguiente es el anterior
            siguiente = siguiente.anterior
        # Una vez que terminamos, estamos en lo que debería ser nuestra cabeza
        self.cabeza = current
    
    def insertar_ordenado(self, cabeza_ord : Nodo, cola_ord : Nodo, dato : Any) -> tuple:
        """
        Método auxiliar para el método de ordenar. Inserta el dato en una posición ordenada.

        Parameters
        ----------
        cabeza_ord : Nodo
            Cabeza de la lista ordenada.
        cola_ord : Nodo
            Cola de la lista ordenada.
        dato : Any
            Dato a insertar

        Returns
        -------
        tuple
            Contiene la cabeza y la cola de la lista ordenada actualizada.

        """
        # Creamos el nodo con el dato
        new_nodo = Nodo(dato)
        # Si la lista ordenada está vacía, la inicializamos.
        if cabeza_ord == None:
            cabeza_ord = new_nodo
            cola_ord = cabeza_ord
        elif cabeza_ord.dato >= new_nodo.dato:
            # Insertamos en la cabeza
            new_nodo.siguiente = cabeza_ord
            new_nodo.siguiente.anterior = new_nodo
            if not cabeza_ord.siguiente:
                # La lista ordenada tiene un solo elemento, actualizamos la cola
                cola_ord = cabeza_ord
            # La cabeza ordenada es el nodo insertado
            cabeza_ord = new_nodo
        else:
            # Iteramos hasta encontrar la posición en la que se debe insertar.
            current = cabeza_ord
            while current.siguiente and current.siguiente.dato < new_nodo.dato:
                current = current.siguiente
            # El nodo siguiente al insertado va a ser el siguiente del nodo actual
            new_nodo.siguiente = current.siguiente
            # Si no estamos en la cola, hacemos que el anterior del siguiente sea el nodo a insertar
            if current.siguiente:
                new_nodo.siguiente.anterior = new_nodo
            # El siguiente del nodo actual será el nodo insertado
            current.siguiente = new_nodo
            # El anterior del nodo insertado será el nodo actual
            new_nodo.anterior = current
            # Si estamos en la cola, la cola ordenada será el nodo insertado
            if not new_nodo.siguiente:
                cola_ord = new_nodo
        # Retornamos los extremos de la lista ordenada actualizados.
        return cabeza_ord, cola_ord
    
    def ordenar(self) -> None:
        """
        Ordena la lista de menor a mayor, con el método de inserción

        Returns
        -------
        None
        """
        # Inicializamos la cabeza y la cola ordenada, junto con el iterador.
        cabeza_ord = None
        cola_ord = None
        current = self.cabeza
        while current:
            # Guardamos el siguiente al dato actual
            siguiente = current.siguiente
            # Borramos las referencias del nodo actual
            current.anterior = current.siguiente = None
            # Actualizamos los punteros de la cabeza ordenada y la cola ordenada,
            # una vez que se inserta el dato actual.
            cabeza_ord, cola_ord = self.insertar_ordenado(cabeza_ord, cola_ord, current.dato)
            # Avanzamos
            current = siguiente
        # Sobreescribimos la cabeza y la cola actual por la cabeza y la cola ordenada.
        self.cabeza = cabeza_ord
        self.cola = cola_ord
    
    def concatenar(self, l1: ListaDobleEnlazada) -> ListaDobleEnlazada:
        """
        Inserta al final de la lista una lista pasada por parámetro

        Parameters
        ----------
        l1 : ListaDobleEnlazada
            Lista a insertar al final de la lista.

        Returns
        -------
        ListaDobleEnlazada
            Lista actualizada con las 2 listas concatenadas.

        """
        # Agarramos la cabeza de la lista a concatenar
        head_lista = l1.cabeza
        # El siguiente de la cola actual será la cabeza de la lista
        self.cola.siguiente = head_lista
        # El anterior de la lista a concatenar es la cola de la lista
        head_lista.anterior = self.cola
        # La cola de la lista concatenada es la cola de la lista a concatenar
        self.cola = l1.cola
        # Sumamos los tamaños de las 2 listas.
        self._tamanio += l1.tamanio
        return self
        
    def __add__(self, l1: ListaDobleEnlazada) -> ListaDobleEnlazada:
        """Simplemente llama al método de concatenar"""
        return self.concatenar(l1)
    
    def __str__(self):
        """Devuelve a la lista como un string"""
        # Recorremos la lista y la copiamos en una lista de Python, luego simplemente retornamos
        # el string de la lista de Python
        current = self.cabeza
        aux= []
        while current != None:
            aux.append(current.dato)
            current = current.siguiente
        return str(aux)
    
    def __iter__(self):
        """Iterador de la lista"""
        nodo = self.cabeza
        while nodo:
            yield nodo
            nodo = nodo.siguiente
    
if __name__ == "__main__":
    lista = ListaDobleEnlazada()
    lista.anexar(1)
    lista.anexar(2)
    lista.anexar(3)
    lista.anexar(4)
    
    print(lista, lista.tamanio)
    lista.extraer(0)
    print(lista, lista.tamanio)
    lista.extraer(0)
    print(lista, lista.tamanio)
    lista.extraer(0)
    print(lista, lista.tamanio)
    lista.extraer(0)
    print(lista, lista.tamanio)
    lista.anexar(2)
    print(lista, lista.tamanio)
    pass
