from __future__ import annotations
from avl import AVL
from operator import itemgetter
import datetime as dt

class TemperaturasDB:
    def __init__(self):
        self._avl = AVL()
    
    def guardar_temperatura(self, temperatura : int, fecha : str) -> None:
        """
        Guarda la medida de temperatura asociada a  la fecha.

        Parameters
        ----------
        temperatura : int
            Temperatura a guardar.
        fecha : str
            Fecha en la cual se guarda la temperatura.

        Returns
        -------
        None

        """
        fecha_dt = dt.datetime.strptime(fecha, "%d/%m/%Y").date()
        self._avl.agregar(fecha_dt, temperatura)
        # print(self._avl)
    
    def devolver_temperatura(self, fecha : str) -> int:
        """
        Devuelve la medida de temperatura en la fecha determinada.

        Parameters
        ----------
        fecha : str
            Fecha de la medición buscada.

        Returns
        -------
        int
            Temperatura en la fecha correspondiente.
            En caso de no encontrarse la fecha buscada, retorna None

        """
        fecha_dt = dt.datetime.strptime(fecha, "%d/%m/%Y").date()
        return self._avl.obtener(fecha_dt)
    
    def max_temp_rango(self, fecha_1 : str, fecha_2 : str) -> int:
        """
        Devuelve la temperatura máxima entre los rangos fecha_1 y fecha_2, ambos extremos inclusive.

        Parameters
        ----------
        fecha_1 : str
            Fecha de inicio.
        fecha_2 : str
            Fecha final.

        Returns
        -------
        int
            Temperatura máxima en el rango dado.

        """
        fecha_1_dt = dt.datetime.strptime(fecha_1, "%d/%m/%Y").date()
        fecha_2_dt = dt.datetime.strptime(fecha_2, "%d/%m/%Y").date()
        temp_rango = self._avl.obtener_clave_y_carga_util_entre(fecha_1_dt, fecha_2_dt)
        return max(temp_rango, key=itemgetter(1))[1]
    
    def min_temp_rango(self, fecha_1 : str, fecha_2 : str) -> int:
        """
        Devuelve la temperatura mínima entre los rangos fecha_1 y fecha_2, ambos extremos inclusive.

        Parameters
        ----------
        fecha_1 : str
            Fecha de inicio.
        fecha_2 : str
            Fecha final.

        Returns
        -------
        int
            Temperatura mínima en el rango dado.

        """
        fecha_1_dt = dt.datetime.strptime(fecha_1, "%d/%m/%Y").date()
        fecha_2_dt = dt.datetime.strptime(fecha_2, "%d/%m/%Y").date()
        temp_rango = self._avl.obtener_clave_y_carga_util_entre(fecha_1_dt, fecha_2_dt)
        return min(temp_rango, key=itemgetter(1))[1]
    
    def temp_extremos_rango(self, fecha_1 : str, fecha_2 : str) -> tuple:
        """
        Devuelve la temperatura mínima y máxima entre los rangos de fecha_1 y fecha_2, ambos extremos inclusive.

        Parameters
        ----------
        fecha_1 : str
            Fecha de inicio.
        fecha_2 : str
            Fecha final.

        Returns
        -------
        tuple
            Temperatura mínima y máxima en el rango dado, como una tupla según el orden ya mencionado.

        """
        minimo = self.min_temp_rango(fecha_1, fecha_2)
        maximo = self.max_temp_rango(fecha_1, fecha_2)        
        return minimo, maximo
    
    def borrar_temperatura(self, fecha : str) -> None:
        """
        Elimina de la base de datos la medición correspondiente a la fecha dada.

        Parameters
        ----------
        fecha : str
            Fecha de la temperatura a eliminar.

        Returns
        -------
        None

        """
        fecha_dt = dt.datetime.strptime(fecha, "%d/%m/%Y").date()
        self._avl.eliminar(fecha_dt)
        # print(self._avl)
    
    def mostrar_temperaturas(self, fecha_1 : str, fecha_2 : str) -> None:
        """
        Muestra por consola el listado de las mediciones de temperatura en el rango recibido por parámetro
        Formato: "dd/mm/aaaa: temperatura ªC" ordenado por fechas

        Parameters
        ----------
        fecha_1 : str
            Fecha de inicio.
        fecha_2 : str
            Fecha final.

        Returns
        -------
        None

        """
        fecha_1_dt = dt.datetime.strptime(fecha_1, "%d/%m/%Y").date()
        fecha_2_dt = dt.datetime.strptime(fecha_2, "%d/%m/%Y").date()
        temps = self._avl.obtener_clave_y_carga_util_entre(fecha_1_dt, fecha_2_dt)
        
        for fecha, temp in temps:
            print(f"{fecha.strftime('%d/%m/%Y')}: {temp} ºC")
    
    def mostrar_cantidad_muestras(self) -> None:
        """
        Muestra por consola la cantidad de muestras presentes en la base de datos.

        Returns
        -------
        None
        
        """
        print(self._avl.tamanio)
    
if __name__ == '__main__':
    pass