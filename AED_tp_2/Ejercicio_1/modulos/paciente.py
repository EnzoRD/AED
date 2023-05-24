# -*- coding: utf-8 -*-

from __future__ import annotations
from random import randint, choices

nombres = ['Leandro', 'Mariela', 'Gastón', 'Andrea', 'Antonio', 'Estela', 'Jorge', 'Agustina']
apellidos = ['Perez', 'Colman', 'Rodriguez', 'Juarez', 'García', 'Belgrano', 'Mendez', 'Lopez']

niveles_de_riesgo = [1, 2, 3]
descripciones_de_riesgo = ['crítico', 'moderado', 'bajo']
# probabilidades de aparición de cada tipo de paciente
probabilidades = [0.1, 0.3, 0.6] 

class Paciente:
    def __init__(self, orden_llegada: int) -> None:
        n = len(nombres)
        self.__nombre = nombres[randint(0, n-1)]
        self.__apellido = apellidos[randint(0, n-1)]
        self.__riesgo = choices(niveles_de_riesgo, probabilidades)[0]
        self.__descripcion = descripciones_de_riesgo[self.__riesgo-1]
        self.__orden_llegada = orden_llegada

    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def apellido(self) -> str:
        return self.__apellido
    
    @property
    def riesgo(self) -> int:
        return self.__riesgo
    
    @property
    def descripcion_riesgo(self) -> str:
        return self.__descripcion
    
    @property
    def orden_llegada(self) -> int:
        return self.__orden_llegada
    
    def __str__(self) -> str:
        cad = self.__nombre + ' '
        cad += self.__apellido + '\t -> '
        cad += str(self.__riesgo) + '-' + self.__descripcion + '\t'
        cad += f'Orden: {str(self.orden_llegada)}'
        return cad
    
    def __eq__(self, other: Paciente) -> bool:
        return self.riesgo == other.riesgo
    
    def __lt__(self, other: Paciente) -> bool:
        if self.__eq__(other):
            # Tienen el mismo riesgo, pero procedemos a fijarnos en el orden de llegada de cada uno
            # Orden de llegada no puede ser nunca igual
            return self.orden_llegada < other.orden_llegada
        else:
            # Sino simplemente vemos el riesgo
            return self.riesgo < other.riesgo
