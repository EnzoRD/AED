class PosicionMenorALimiteInferior(Exception):
    """Usado para posiciones que no deben ser menores que cero"""
    def __init__(self, posOriginal : int, limite_inferior: int, msj : str = 'La posición no puede ser menor que el limite inferior.') -> None:
        self.posOriginal = posOriginal
        self.limite_inferior = limite_inferior
        self.msj = msj
        super().__init__(self.msj)

    def __str__(self):
        return f'pos: {self.posOriginal}, limite: {self.limite_inferior} -> {self.msj}'
    
class PosicionMayorAlTamanio(Exception):
    """Usado para posiciones que exceden el tamaño de la lista"""
    def __init__(self, posOriginal : int, tamanio : int, msj : str = 'La posición no puede ser mayor al tamaño de la lista.') -> None:
        self.posOriginal = posOriginal
        self.tamanio = tamanio
        self.msj = msj
        super().__init__(self.msj)
        
    def __str__(self):
        return f'pos: {self.posOriginal}, tamaño: {self.tamanio} -> {self.msj}'

class ListaVacia(Exception):
    """Usado para métodos donde la lista no puede estar vacía"""
    def __init__(self, msj : str = 'La lista está vacía.') -> None:
        self.msj = msj
        
    def __str__(self):
        return f'{self.msj}'
