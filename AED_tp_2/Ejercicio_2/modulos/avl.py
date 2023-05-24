from __future__ import annotations
from typing import Any

class NodoArbol:
    def __init__(self, clave: Any, valor: Any, izquierdo : NodoArbol = None, derecho : NodoArbol = None, padre : NodoArbol = None, factor_equilibrio: int = 0) -> None:
        self.clave = clave
        self.carga_util = valor
        self.hijo_izquierdo = izquierdo
        self.hijo_derecho = derecho
        self.padre = padre
        self.factor_equilibrio = factor_equilibrio
        
    @property
    def clave(self) -> Any:
        """
        Getter de la clave del nodo
        """
        return self._clave
    
    @clave.setter
    def clave(self, new_clave : Any) -> None:
        """
        Setter de la clave del nodo
        """
        self._clave = new_clave
    
    @property
    def carga_util(self) -> Any:
        """
        Getter de la carga util del nodo
        """
        return self._carga_util
    
    @carga_util.setter
    def carga_util(self, new_carga_util: Any) -> None:
        """
        Setter de la carga util del nodo
        """
        self._carga_util = new_carga_util
    
    @property
    def hijo_izquierdo(self) -> NodoArbol:
        """
        Getter del hijo izquierdo del nodo
        """
        return self._hijo_izquierdo
    
    @hijo_izquierdo.setter
    def hijo_izquierdo(self, new_hijo_izquierdo: NodoArbol) -> None:
        """
        Setter del hijo izquierdo del nodo
        """
        self._hijo_izquierdo = new_hijo_izquierdo
    
    @property
    def hijo_derecho(self) -> NodoArbol:
        """
        Getter del hijo derecho del nodo
        """
        return self._hijo_derecho
    
    @hijo_derecho.setter
    def hijo_derecho(self, new_hijo_derecho: NodoArbol) -> None:
        """
        Setter del hijo derecho del nodo
        """
        self._hijo_derecho = new_hijo_derecho
    
    @property
    def padre(self) -> NodoArbol:
        """
        Getter del padre del nodo
        """
        return self._padre
    
    @padre.setter
    def padre(self, new_padre: NodoArbol) -> None:
        """
        Setter del padre del nodo
        """
        self._padre = new_padre
    
    @property
    def factor_equilibrio(self) -> int:
        """
        Getter del factor de equilibrio
        """
        return self._factor_equilibrio
    
    @factor_equilibrio.setter
    def factor_equilibrio(self, new_factor_equilibrio: int) -> None:
        """
        Setter del factor de equilibrio
        """
        self._factor_equilibrio = new_factor_equilibrio
    
    def tiene_hijo_izquierdo(self) -> bool:
        return self.hijo_izquierdo
    
    def tiene_hijo_derecho(self) -> bool:
        return self.hijo_derecho
    
    def es_hijo_izquierdo(self) -> bool:
        return self.padre and self.padre.hijo_izquierdo == self
    
    def es_hijo_derecho(self) -> bool:
        return self.padre and self.padre.hijo_derecho == self
    
    def es_raiz(self) -> bool:
        return not self.padre
    
    def es_hoja(self) -> bool:
        return not (self.hijo_izquierdo or self.hijo_derecho)
    
    def tiene_algun_hijo(self) -> bool:
        return not self.es_hoja()
    
    def tiene_ambos_hijos(self) -> bool:
        return self.hijo_izquierdo and self.hijo_derecho
    
    def reemplazar_dato_de_nodo(self, clave : Any, valor : Any, h_izq : NodoArbol, h_der : NodoArbol) -> None:
        """
        Reemplaza todos los datos del nodo con los valores proporcionados.

        Parameters
        ----------
        clave : Any
            Nueva clave del nodo.
        valor : Any
            Nueva carga útil del nodo.
        h_izq : NodoArbol
            Nuevo hijo izquierdo del nodo.
        h_der : NodoArbol
            Nuevo hijo derecho del nodo.

        Returns
        -------
        None

        """
        self.clave = clave
        self.carga_util = valor
        self.hijo_izquierdo = h_izq
        self.hijo_derecho = h_der
        if self.tiene_hijo_izquierdo():
            self.hijo_izquierdo.padre = self
        if self.tiene_hijo_derecho():
            self.hijo_derecho.padre = self
            
    def encontrar_sucesor(self) -> NodoArbol:
        """
        Busca el mínimo nodo posible yendo por el hijo derecho.

        Returns
        -------
        NodoArbol
            Nodo sucesor del nodo actual.

        """
        sucesor = None
        if self.tiene_hijo_derecho():
            sucesor = self.hijo_derecho.encontrar_minimo()
        else:
            if self.padre:
                if self.es_hijo_izquierdo():
                    sucesor = self.padre
                else:
                    self.padre.hijo_derecho = None
                    sucesor = self.padre.encontrar_sucesor()
                    self.padre.hijo_derecho = self
        return sucesor
    
    def encontrar_minimo(self) -> NodoArbol:
        """
        Encuentra el mínimo nodo a partir del nodo actual por el cual se llamó el método.

        Returns
        -------
        NodoArbol
            Nodo mínimo del árbol.

        """
        actual = self
        while actual.tiene_hijo_izquierdo():
            actual = self.hijo_izquierdo
        return actual
    
    def empalmar(self) -> None:
        """
        Desasigna el nodo actual, asignando su ancestro con sus descendencias.

        Returns
        -------
        None

        """
        if self.es_hoja():
            if self.es_hijo_izquierdo():
                self.padre.hijo_izquierdo = None
            else:
                self.padre.hijo_derecho = None
        elif self.tiene_algun_hijo():
            if self.tiene_hijo_izquierdo():
                if self.es_hijo_izquierdo():
                    self.padre.hijo_izquierdo = self.hijo_izquierdo
                else:
                    self.padre.hijo_derecho = self.hijo_izquierdo
                self.hijo_izquierdo.padre = self.padre
            else:
                if self.es_hijo_izquierdo():
                    self.padre.hijo_izquierdo = self.hijo_derecho
                else:
                    self.padre.hijo_derecho = self.hijo_derecho
                self.hijo_derecho.padre = self.padre
    
    def __iter__(self):
        if self:
            if self.tiene_hijo_izquierdo():
                for elem in self.hijo_izquierdo:
                    yield elem
            yield self.clave
            if self.tiene_hijo_derecho():
                for elem in self.hijo_derecho:
                    yield elem
class AVL:
    def __init__(self) -> None:
        self._raiz = None
        self._tam = 0
    
    ############## Métodos BST
    
    @property
    def tamanio(self) -> int:
        return self._tam
    
    @property
    def raiz(self) -> NodoArbol:
        return self._raiz
    
    def __len__(self):
        return self._tam
    
    def __iter__(self):
        return self._raiz.__iter__()
    
    # Helpers para representar el árbol en consola
    def _altura(self, nodo : NodoArbol, n : int):
        if not nodo:
            return n
        altura = n
        if nodo:
            altura += 1
        return max(self._altura(nodo.hijo_izquierdo, altura), self._altura(nodo.hijo_derecho, altura))
    
    def altura_maxima_arbol(self) -> int:
        """
        Devuelve la altura máxima del árbol desde la raíz.

        Returns
        -------
        int
            Altura máxima del árbol desde la raíz.

        """
        if not self.raiz:
            return 0
        return self._altura(self.raiz, 0)
        
    # Representación en consola del arbol, más o menos...
    def __repr__(self):
        if self.raiz == None: return 'Empty'
        content='\n' # to hold final string
        cur_nodes=[self.raiz] # all nodes at current level
        cur_height=self.altura_maxima_arbol() # height of nodes at current level
        sep=' '*(2**(cur_height-1)) # variable sized separator between elements
        while True:
            cur_height+=-1 # decrement current height
            if len(cur_nodes)==0: break
            cur_row=' '
            next_row=''
            next_nodes=[]

            if all(n is None for n in cur_nodes):
                break

            for n in cur_nodes:

                if n==None:
                    cur_row+='   '+sep
                    next_row+='   '+sep
                    next_nodes.extend([None,None])
                    continue

                if n.carga_util!=None:       
                    buf=' '*int((5-len(str(n.carga_util)))/2)
                    cur_row+='%s%s%s'%(buf,str(n.carga_util),buf)+sep
                else:
                    cur_row+=' '*5+sep

                if n.hijo_izquierdo!=None:  
                    next_nodes.append(n.hijo_izquierdo)
                    next_row+=' /'+sep
                else:
                    next_row+='  '+sep
                    next_nodes.append(None)

                if n.hijo_derecho!=None: 
                    next_nodes.append(n.hijo_derecho)
                    next_row+='\ '+sep
                else:
                    next_row+='  '+sep
                    next_nodes.append(None)

            content+=(cur_height*'   '+cur_row+'\n'+cur_height*'   '+next_row+'\n')
            cur_nodes=next_nodes
            sep=' '*int(len(sep)/2) # cut separator size in half
        return content
    
    def __getitem__(self, clave: Any) -> Any:
        return self.obtener(clave)
    
    def __setitem__(self, c : Any, v : Any) -> None:
        self.agregar(c,v)
    
    def __contains__(self, clave : Any) -> Any:
        return self._obtener(clave, self._raiz)
    
    def __delitem__(self, clave : Any) -> None:
        self.eliminar(clave)
        
    def recorrer_inorden(self) -> list:
        """
        Recorre el árbol inorden

        Returns
        -------
        list
            Lista de elementos del árbol en inorden (ordenado).

        """
        return self._inorden(self.raiz)
    
    def _inorden(self, nodo : NodoArbol) -> list:
        """
        Helper para recorrer_inorden, método recursivo para agregar los nodos recorridos a la lista.

        Parameters
        ----------
        nodo : NodoArbol
            nodo actual que se está recorriendo.

        Returns
        -------
        list
            lista de elementos del árbol en inorden.

        """
        if not nodo:
            return []
        
        result = [] + self._inorden(nodo.hijo_izquierdo)
        result.append(nodo.carga_util)
        result += self._inorden(nodo.hijo_derecho)
    
        return result
        
    def obtener(self, clave : Any) -> Any:
        """
        Obtiene el elemento con la clave requerida

        Parameters
        ----------
        clave : Any
            Clave a buscar en el árbol.

        Returns
        -------
        Any
            Carga útil del nodo buscado.

        """
        if self._raiz:
            res = self._obtener(clave, self._raiz)
            return res.carga_util if res else None
        else:
            return None
    
    def _obtener(self, clave : Any, nodo_actual : NodoArbol) -> Any:
        """
        Helper recursivo para el método obtener

        Parameters
        ----------
        clave : Any
            Clave a buscar en el árbol.
        nodo_actual : NodoArbol
            Nodo que se está recorriendo.

        Returns
        -------
        Any
            Carga útil del nodo buscado.

        """
        # Si tenemos None en el nodo actual, entonces significa que la clave no se encuentra en el árbol
        if not nodo_actual:
            return None
        # Si la clave que buscamos está en el nodo actual, retornamos su carga útil
        elif nodo_actual.clave == clave:
            return nodo_actual
        # Decidimos que camino tomar dependiendo de la clave del nodo actual
        elif clave < nodo_actual.clave:
            return self._obtener(clave, nodo_actual.hijo_izquierdo)
        else:
            return self._obtener(clave, nodo_actual.hijo_derecho)
        
    def agregar(self, clave : Any, valor : Any) -> None:
        """
        Inserta una clave en el árbol junto con su valor

        Parameters
        ----------
        clave : Any
            Clave del elemento a insertar.
        valor : Any
            Carga útil del elemento a insertar.

        Returns
        -------
        None

        """
        # Si el árbol no está vacío, buscamos la posición donde se debe insertar, sino simplemente asignamos la raiz
        # a nuestro nodo
        if self.raiz:
            self._agregar(clave, valor, self.raiz)
        else:
            self._raiz = NodoArbol(clave, valor)
        self._tam += 1
    
    def eliminar(self, clave : Any) -> None:
        """
        Elimina la clave y su carga útil del árbol.

        Parameters
        ----------
        clave : Any
            Elemento a eliminar.

        Raises
        ------
        ValueError
            En caso de intentar eliminar una clave que no se encuentre en el árbol.

        Returns
        -------
        None

        """
        # Si el tamaño de la lista es mayor a 1, debemos buscar recursivamente el nodo que contenga la clave a eliminar
        if self.tamanio > 1:
            nodo_elim = self._obtener(clave, self.raiz)
            if nodo_elim:
                self._remover(nodo_elim)
                self._tam -= 1
            else:
                # Clave no encontrada, excepción
                raise ValueError(f'La clave a eliminar {clave} no se encuentra en el árbol.')
        elif self.tamanio == 1 and self.raiz.clave == clave:
            self._raiz = None
            self._tam -= 1
        else:
            raise ValueError('El arbol está vacío o la clave {clave} no se encuentra en el árbol.')
        
    # Modificado para AVL
    def _agregar(self, clave : Any, valor : Any, nodo_actual : NodoArbol):
        """
        Helper recursivo para el método agregar, es el método responsable de buscar la ubicación donde se debe insertar.

        Parameters
        ----------
        clave : Any
            Clave del elemento a insertar.
        valor : Any
            Carga útil del elemento a insertar.
        nodo_actual : NodoArbol
            Nodo actual del árbol que se está analizando.

        Returns
        -------
        None.

        """
        # Si la clave del nuevo nodo es menor a la del nodo actual, debemos insertarla a la izquierda del mismo
        if clave < nodo_actual.clave:
            if nodo_actual.tiene_hijo_izquierdo():
                # Si la posición se encuentra ocupada por otro nodo, debemos insertarlo dependiendo el hijo izquierdo del nodo
                self._agregar(clave, valor, nodo_actual.hijo_izquierdo)
            else:
                nodo_actual.hijo_izquierdo = NodoArbol(clave, valor, padre=nodo_actual)
                # Una vez insertado el nodo, actualizamos el equilibrio del mismo
                self._actualizar_equilibrio(nodo_actual.hijo_izquierdo)
        else:
            if nodo_actual.tiene_hijo_derecho():
                # Si la posición se encuentra ocupada por otro nodo, debemos insertarlo dependiendo el hijo derecho del nodo
                self._agregar(clave, valor, nodo_actual.hijo_derecho)
            else:
                nodo_actual.hijo_derecho = NodoArbol(clave, valor, padre=nodo_actual)
                # Una vez insertado el nodo, actualizamos el equilibrio del mismo
                self._actualizar_equilibrio(nodo_actual.hijo_derecho)
    
    # Modificado para AVL
    def _remover(self, nodo_actual : NodoArbol) -> None:
        """
        Helper recursivo para el método eliminar, es el método responsable de eliminar el elemento y modificar
        los factores de equilibrio de sus ancestros.

        Parameters
        ----------
        nodo_actual : NodoArbol
            Nodo a eliminar.

        Returns
        -------
        None

        """
        # Bandera booleana que indica si debemos actualizar los factores de equilibrio
        # Solamente se pondrá en False si el nodo a eliminar tenga ambos hijos.
        act_eq = True
        # Primer caso: El nodo a eliminar es hoja
        if nodo_actual.es_hoja():
            if nodo_actual.es_hijo_izquierdo():
                # Desvinculamos el nodo actual del padre
                nodo_actual.padre.hijo_izquierdo = None
                # Al ser hijo izquierdo debemos disminuir el factor de equilibrio del padre.
                nodo_actual.padre.factor_equilibrio -= 1
            else:
                # Desvinculamos el nodo actual del padre
                nodo_actual.padre.hijo_derecho = None
                # Al ser hijo derecho debemos aumentar el factor de equilibrio del padre.
                nodo_actual.padre.factor_equilibrio += 1
        # Segundo caso: El nodo a eliminar tiene ambos hijos
        elif nodo_actual.tiene_ambos_hijos():
            # Buscamos el sucesor del nodo actual
            sucesor = nodo_actual.encontrar_sucesor()
            # Empalmamos el nodo actual con el sucesor y reemplazamos para su posterior eliminación.
            sucesor.empalmar()
            nodo_actual.clave = sucesor.clave
            nodo_actual.carga_util = sucesor.carga_util
            # No debemos actualizar el factor de equilibrio
            act_eq = False
        # Tercer caso: El nodo a eliminar tiene algún hijo
        else:
            # En caso de tener un hijo izquierdo
            if nodo_actual.tiene_hijo_izquierdo():
                if nodo_actual.es_hijo_izquierdo():
                    # Asignamos como padre del hijo del nodo actual al padre del nodo actual, y viceversa
                    nodo_actual.hijo_izquierdo.padre = nodo_actual.padre
                    nodo_actual.padre.hijo_izquierdo = nodo_actual.hijo_izquierdo
                    # En caso de que el nodo actual haya sido un hijo izquierdo, disminuimos el factor de equilibrio del padre
                    nodo_actual.padre.factor_equilibrio -= 1
                elif nodo_actual.es_hijo_derecho():
                    # Asignamos como padre del hijo del nodo actual al padre del nodo actual, y viceversa
                    nodo_actual.hijo_izquierdo.padre = nodo_actual.padre
                    nodo_actual.padre.hijo_derecho = nodo_actual.hijo_izquierdo
                    # En caso de que el nodo actual haya sido un hijo derecho, aumentamos el factor de equilibrio del padre
                    nodo_actual.padre.factor_equilibrio += 1
                else:
                    nodo_actual.reemplazar_dato_de_nodo(nodo_actual.hijo_izquierdo.clave, nodo_actual.hijo_izquierdo.carga_util, nodo_actual.hijo_izquierdo.hijo_izquierdo, nodo_actual.hijo_izquierdo.hijo_derecho)
            # En caso de tener un hijo derecho
            else:
                if nodo_actual.es_hijo_izquierdo():
                    # Asignamos como padre del hijo del nodo actual al padre del nodo actual, y viceversa
                    nodo_actual.hijo_derecho.padre = nodo_actual.padre
                    nodo_actual.padre.hijo_izquierdo = nodo_actual.hijo_derecho
                    # En caso de que el nodo actual haya sido un hijo izquierdo, disminuimos el factor de equilibrio del padre
                    nodo_actual.padre.factor_equilibrio -= 1
                elif nodo_actual.es_hijo_derecho():
                    # Asignamos como padre del hijo del nodo actual al padre del nodo actual, y viceversa
                    nodo_actual.hijo_derecho.padre = nodo_actual.padre
                    nodo_actual.padre.hijo_derecho = nodo_actual.hijo_derecho
                    # En caso de que el nodo actual haya sido un hijo derecho, aumentamos el factor de equilibrio del padre
                    nodo_actual.padre.factor_equilibrio += 1
                else:
                    nodo_actual.reemplazar_dato_de_nodo(nodo_actual.hijo_derecho.clave, nodo_actual.hijo_derecho.carga_util, nodo_actual.hijo_derecho.hijo_izquierdo, nodo_actual.hijo_derecho.hijo_derecho)
        # Actualizamos el equilibrio del padre del nodo eliminado solamente de ser necesario.
        if act_eq:
            self._actualizar_equilibrio_rem(nodo_actual.padre)
    
                
    ############## Métodos AVL
    def _actualizar_equilibrio_rem(self, nodo : NodoArbol) -> None:
        """
        Actualiza el equilibrio del nodo al remover un nodo y, de ser necesario, reequilibra el árbol.

        Parameters
        ----------
        nodo : NodoArbol
            Nodo actual a actualizar el factor de equilibrio.

        Returns
        -------
        None

        """
        # Si el nodo está desequilibrado, lo volvemos a reequilibrar
        if abs(nodo.factor_equilibrio) > 1:
            self._reequilibrar(nodo)
            return
        
        # Si tenemos padre y el balance del nodo cambió, debemos "quitarle peso" al padre
        # Es decir, si ahora tenemos 0 es porque antes teniamos -1 o bien 1, por lo que ya no está pesado de algún lado
        # En caso de tener -1 o 1, significa que el nodo estaba balanceado y ahora se encuentra pesado, pero no debemos
        # aumentar o disminuir el peso del padre
        if nodo.padre and nodo.factor_equilibrio == 0:
            if nodo.es_hijo_izquierdo():
                # En este caso es al revés que el de insertar, ahora al ser izquierdo debemos restar 1 al factor de equilibrio del padre.
                nodo.padre.factor_equilibrio -= 1
            elif nodo.es_hijo_derecho():
                # En caso de que sea derecho, debemos sumar uno al factor de equilibrio del padre.
                nodo.padre.factor_equilibrio += 1
            
            # Actualizamos el del padre solamente en caso de que lo necesitemos
            if nodo.padre.factor_equilibrio != 0:
                self._actualizar_equilibrio_rem(nodo.padre)
        
    def _actualizar_equilibrio(self, nodo : NodoArbol) -> None:
        """
        Actualiza el equilibrio del nodo al insertar un nodo y, de ser necesario, reequilibra el árbol.

        Parameters
        ----------
        nodo : NodoArbol
            Nodo actual a actualizar el factor de equilibrio.

        Returns
        -------
        None

        """
        # Si el nodo está desequilibrado, lo volvemos a reequilibrar
        if abs(nodo.factor_equilibrio) > 1:
            self._reequilibrar(nodo)
            return
        
        # Si tenemos padre, debemos actualizar el factor de equilibrio del mismo
        if nodo.padre:
            if nodo.es_hijo_izquierdo():
                # Sumamos 1 en caso de ser hijo izquierdo
                nodo.padre.factor_equilibrio += 1
            elif nodo.es_hijo_derecho():
                # Restamos 1 en caso de ser hijo derecho
                nodo.padre.factor_equilibrio -= 1
            
            # Si no está balanceado el padre, actualizamos el factor de equilibrio del padre.
            if nodo.padre.factor_equilibrio != 0:
                self._actualizar_equilibrio(nodo.padre)
    
    def _reequilibrar(self, nodo : NodoArbol) -> None:
        """
        Reequilibra el nodo, generando rotaciones según se crea conveniente.

        Parameters
        ----------
        nodo : NodoArbol
            Nodo actual que se está reequilibrando.

        Returns
        -------
        None

        """
        if nodo.factor_equilibrio < 0:
            # Si el hijo derecho tiene diferente símbolo que el padre, primero debemos realizar una rotación hacia la derecha
            if nodo.hijo_derecho.factor_equilibrio > 0:
                self._rotar_derecha(nodo.hijo_derecho)
            # El else que estaba acá era redundante, siempre se hace una rotación a la izquierda en este caso
            self._rotar_izquierda(nodo)
        elif nodo.factor_equilibrio > 0:
            # Si el hijo izquierdo tiene diferente símbolo que el padre, primero debemos realizar una rotación hacia la izquierda
            if nodo.hijo_izquierdo.factor_equilibrio < 0:
                self._rotar_izquierda(nodo.hijo_izquierdo)
            # El else que estaba acá era redundante, siempre se hace una rotación a la derecha en este caso
            self._rotar_derecha(nodo)
    
    def _rotar_izquierda(self, rot_raiz : NodoArbol) -> None:
        """
        Rotación a la izquierda para los nodos desequilibrados.

        Parameters
        ----------
        rot_raiz : NodoArbol
            Nodo pivote de la rotación.

        Returns
        -------
        None

        """
        # Empezamos asignando a la nueva raíz del subarbol que se generará
        nueva_raiz = rot_raiz.hijo_derecho
        # El hijo derecho de la raíz será el hijo izquierdo de nuestra nueva raíz
        rot_raiz.hijo_derecho = nueva_raiz.hijo_izquierdo
        # Si el hijo derecho de la raíz anterior (ahora nuestra nueva raiz) tiene un hijo izquierdo
        # el padre de ese hijo ahora será la raíz anterior
        if nueva_raiz.hijo_izquierdo:
            nueva_raiz.hijo_izquierdo.padre = rot_raiz
        # Finalmente asignamos como padre de nuestra nueva raíz al padre de la raíz anterior.
        nueva_raiz.padre = rot_raiz.padre
        # Si era la raíz del árbol general, asignamos a la raiz nueva como raíz de nuestro árbol
        if rot_raiz.es_raiz():
            self._raiz = nueva_raiz
        else:
            # Caso contrario, nos fijamos qué hijo era y hacemos las asignaciones pertinentes.
            if rot_raiz.es_hijo_izquierdo():
                rot_raiz.padre.hijo_izquierdo = nueva_raiz
            else:
                rot_raiz.padre.hijo_derecho = nueva_raiz
        # Asignamos como hijo izquierdo a la raíz anterior y como padre de la raíz anterior a la nueva raíz
        nueva_raiz.hijo_izquierdo = rot_raiz
        rot_raiz.padre = nueva_raiz
        # Actualizamos los factores de equilibrio teniendo en cuenta los viejos factores de equilibrio.
        rot_raiz.factor_equilibrio = rot_raiz.factor_equilibrio + 1 - min(nueva_raiz.factor_equilibrio, 0)
        nueva_raiz.factor_equilibrio = nueva_raiz.factor_equilibrio + 1 + max(rot_raiz.factor_equilibrio, 0)
    
    def _rotar_derecha(self, rot_raiz : NodoArbol) -> None:
        """
        Rotación a la derecha para los nodos desequilibrados.

        Parameters
        ----------
        rot_raiz : NodoArbol
            Nodo pivote de la rotación.

        Returns
        -------
        None

        """
        # Empezamos asignando a la nueva raíz del subarbol que se generará
        nueva_raiz = rot_raiz.hijo_izquierdo
        # El hijo izquierdo de la raíz será el hijo derecho de nuestra nueva raíz
        rot_raiz.hijo_izquierdo = nueva_raiz.hijo_derecho
        # Si el hijo izquierdo de la raíz anterior (ahora nuestra nueva raiz) tiene un hijo derecho
        # el padre de ese hijo ahora será la raíz anterior
        if nueva_raiz.hijo_derecho:
            nueva_raiz.hijo_derecho.padre = rot_raiz
        # Finalmente asignamos como padre de nuestra nueva raíz al padre de la raíz anterior.
        nueva_raiz.padre = rot_raiz.padre
        # Si era la raíz del árbol general, asignamos a la raiz nueva como raíz de nuestro árbol
        if rot_raiz.es_raiz():
            self._raiz = nueva_raiz
        else:
            # Caso contrario, nos fijamos qué hijo era y hacemos las asignaciones pertinentes.
            if rot_raiz.es_hijo_izquierdo():
                rot_raiz.padre.hijo_izquierdo = nueva_raiz
            else:
                rot_raiz.padre.hijo_derecho = nueva_raiz
        # Asignamos como hijo derecho a la raíz anterior y como padre de la raíz anterior a la nueva raíz
        nueva_raiz.hijo_derecho = rot_raiz
        rot_raiz.padre = nueva_raiz
        # Actualizamos los factores de equilibrio teniendo en cuenta los viejos factores de equilibrio.
        rot_raiz.factor_equilibrio = rot_raiz.factor_equilibrio - 1 - max(nueva_raiz.factor_equilibrio, 0)
        nueva_raiz.factor_equilibrio = nueva_raiz.factor_equilibrio - 1 + min(rot_raiz.factor_equilibrio, 0)
        
    def obtener_clave_y_carga_util_entre(self, clave_inicio : Any, clave_final : Any) -> list:
        """
        Devuelve una lista de tuplas, donde se tendrán las claves con su carga útil, de forma ordenada

        Parameters
        ----------
        clave_inicio : Any
            Clave inicial a buscar.
        clave_final : Any
            Clave final.

        Returns
        -------
        list
            Lista de tuplas con las claves y cargas útiles.

        """
        lista = []
        iterador = Iterador(self, clave_inicio)
        for nodo in iterador:
            if clave_inicio <= nodo.clave <= clave_final:
                lista.append((nodo.clave, nodo.carga_util))
        
        return lista
        
class Iterador:
    def __init__(self, arbol: AVL, clave_inicial: Any) -> None:
        self.nodo = arbol._obtener(clave_inicial, arbol.raiz)
        
    def __iter__(self):
        return self
    
    def __next__(self):
        salida = self.nodo
        if not self.nodo:
            raise StopIteration()
        
        self.nodo = self.nodo.encontrar_sucesor()
        return salida