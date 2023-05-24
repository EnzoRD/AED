import unittest
from unittest.mock import patch
from modulos.temperaturas_db import TemperaturasDB
import io

class TestTemperaturaDB(unittest.TestCase):
    
    def setUp(self):
        self.db = TemperaturasDB()
        self.temp_dict = {}
        # El órden de la temperatura se condice con el órden de las fechas
        self.temp_dict['30/10/2022'] = 10
        self.temp_dict['1/10/2022'] = 5
        self.temp_dict['24/12/2022'] = 15
        self.temp_dict['1/12/2022'] = 12
        self.temp_dict['1/05/2022'] = 2
        self.temp_dict['7/10/2022'] = 7
        self.temp_dict['5/10/2022'] = 6
        
    def test_guardar(self):
        """ Se va a testear el método de guardar comparando el tamaño del árbol avl interno """
        self.assertEqual(self.db._avl.tamanio, 0)
        for fecha, temp in self.temp_dict.items():
            self.db.guardar_temperatura(temp, fecha)
        
        self.assertEqual(self.db._avl.tamanio, len(self.temp_dict))
    
    def test_eliminar_devolver(self):
        """ 
        Se va a testear el método de eliminar comparando el tamaño del árbol avl interno e
        intentando obtener la temperatura en la fecha luego de ser eliminada
        """
        for fecha, temp in self.temp_dict.items():
            self.db.guardar_temperatura(temp, fecha)
        self.assertEqual(self.db.devolver_temperatura('1/12/2022'), self.temp_dict['1/12/2022'])
        self.db.borrar_temperatura('1/12/2022')
        self.assertEqual(self.db.devolver_temperatura('1/12/2022'), None)
        self.assertEqual(self.db._avl.tamanio, 6)
        
    def test_minimos_maximos(self):
        """
        El método de temp_extremos_rango internamente usa min_temp_rango y max_temp_rango
        Se va a testear primero en la totalidad de los elementos y luego en un rango arbitrario
        """
        for fecha, temp in self.temp_dict.items():
            self.db.guardar_temperatura(temp, fecha)
        fecha_inicio = '1/05/2022'; fecha_final_1 = '24/12/2022'; fecha_final_2 = '7/10/2022'
        min_total = self.temp_dict[min(self.temp_dict, key=self.temp_dict.get)]
        max_total = self.temp_dict[max(self.temp_dict, key=self.temp_dict.get)]
        # El rango total es el árbol entero, donde las temperaturas se encuentran en los extremos
        self.assertEqual(self.db.temp_extremos_rango(fecha_inicio, fecha_final_1), (min_total, max_total))
        self.assertEqual(self.db.temp_extremos_rango(fecha_inicio, fecha_final_2), (min_total, 7))
        #  Añadimos una fecha en el medio del rango
        self.db.guardar_temperatura(400, '12/11/2022')
        self.assertEqual(self.db.temp_extremos_rango(fecha_inicio, fecha_final_1), (min_total, 400))
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_mostrar_temperaturas(self, mock_stdout):
        """
        Se usa mock para comprobar lo que se printee por consola.
        """
        for fecha, temp in self.temp_dict.items():
            self.db.guardar_temperatura(temp, fecha)
        
        out = "01/05/2022: 2 ºC\n01/10/2022: 5 ºC\n05/10/2022: 6 ºC\n07/10/2022: 7 ºC\n"
        self.db.mostrar_temperaturas('1/05/2022', '7/10/2022')
        self.assertMultiLineEqual(mock_stdout.getvalue(), out)
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_mostrar_cantidad_muestras(self, mock_stdout):
        """
        Se usa mock para comprobar lo que se printee por consola.
        """
        for fecha, temp in self.temp_dict.items():
            self.db.guardar_temperatura(temp, fecha)
            
        self.db.mostrar_cantidad_muestras()
        len_str = str(len(self.temp_dict)) + '\n'
        self.assertEqual(mock_stdout.getvalue(), len_str)
        
if __name__ == '__main__':
    unittest.main()