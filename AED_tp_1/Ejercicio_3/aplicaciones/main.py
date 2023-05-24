import os
import time
from modulos.mezcla_natural import crear_archivo_de_datos, ordenar_por_mezcla_natural, verificar_ordenado

if __name__ == '__main__':
    # Creamos el archivo con los datos
    crear_archivo_de_datos('datos.txt')
    # Obtenemos el tamaño original del archivo
    file_size_original = os.path.getsize(r'datos.txt') 
    print('File Size:', file_size_original, 'bytes')
    # Iniciamos un contador
    start = time.perf_counter_ns()
    # Llamada al algoritmo para que ordene el archivo previamente creado.
    ordenar_por_mezcla_natural('datos.txt')
    # Terminamos el contador
    end = time.perf_counter_ns()
    res = end-start
    print(f"Tiempo empleado: {str(res//10**9) + 's' if res // 10**9 > 0 else str(res//10**6) + 'ms'}")
    # Verificamos el orden
    if verificar_ordenado('datos.txt'):
        print("Esta ordenado")
    else:
        print("No esta ordenado")
    # Obtenemos el tamaño del archivo ya ordenado
    file_size_2 = os.path.getsize(r'datos.txt') 
    print('File Size:', file_size_2, 'bytes')
    if file_size_original == file_size_2:
        print('El archivo no varió su tamaño.')
    else:
        print('El archivo sufrió una variación en su tamaño.')