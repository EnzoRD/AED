from Ejercicio_1.modulos.LDE import ListaDobleEnlazada as Lista
from typing import Any

class ColaDoble:
    def __init__(self) -> None:
        self._lista_interna = Lista()
        
    def agregar(self, item : Any) -> None:
        self._lista_interna.anexar(item)
        
    def agregar_arriba(self, item : Any) -> None:
        self._lista_interna.agregar(item)
        
    def avanzar(self) -> Any:
        return self._lista_interna.extraer(0).dato
    
    def remover_al_final(self) -> Any:
        return self._lista_interna.extraer().dato
    
    def esta_vacia(self) -> bool:
        return self._lista_interna.esta_vacia()
    
    @property
    def tamanio(self) -> int:
        return self._lista_interna.tamanio
    
    def __str__(self) -> str:
        res = ''
        for nodo in self._lista_interna:
            res += str(nodo.dato) + ' '
        return res
    
    def __iter__(self):
        return self._lista_interna.__iter__()

if __name__ == '__main__':
    cola = ColaDoble()
    
    cola.agregar(0)
    cola.agregar(1)
    cola.agregar(2)
    cola.agregar(3)
    
    eliminado = cola.avanzar()
    cola.agregar(4)
    print(cola, cola.tamanio)
    cola.avanzar()
    print(cola, cola.tamanio)
    cola.avanzar()
    print(cola, cola.tamanio)
    cola.avanzar()
    print(cola, cola.tamanio)
    cola.avanzar()
    print(cola, cola.tamanio)
    cola.agregar(2)
    print(cola, cola.tamanio)
    cola.agregar_arriba(19)
    print(cola, cola.tamanio)
    