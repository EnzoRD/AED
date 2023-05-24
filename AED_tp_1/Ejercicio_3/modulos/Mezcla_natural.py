from random import randint

def crear_archivo_de_datos(nombre: str) -> None:
    f = 10**6
    N = 5*f
    cifras = 20
    tam_bloque = f # 1 M de valores por bloque a escribir
    
    print('Cantidad de valores a escribir:', N)
    
    # truncar archivo si existe
    with open(nombre, 'w') as archivo:
        pass
    
    # escribir datos
    N_restantes = N
    while N_restantes > 0:
        cif = cifras
        r = N_restantes % tam_bloque
        c = N_restantes // tam_bloque
        if c > 0:
            t = tam_bloque
        elif c == 0:
            t = r
        N_restantes -= t
        print('t =', t, ', N_restantes =', N_restantes)
        bloque = [str(randint(10**(cif-1), 10**cif-1))+'\n'
                  for i in range(t)]        
        with open(nombre, 'a+') as archivo:
            archivo.writelines(bloque)

def dividir(archivo: str = 'datos.txt') -> None:
    """
    Función que divide el archivo en dos subarchivos copiando las listas naturales ordenadas del archivo alternativamente
    Parameters
    ----------
    archivo : str, optional
        Nombre del archivo a dividir. El valor por defecto es 'datos.txt'.

    Returns
    -------
    None
    """
    # Abrimos y/o creamos los archivos auxiliares y el archivo de datos         
    with open('Auxiliar_1.txt', 'w') as auxiliar_uno, open('Auxiliar_2.txt', 'w') as auxiliar_dos, open(archivo) as archi:
        primer_elemento = archi.readline().rstrip('\n')
        segundo_elemento= archi.readline().rstrip('\n')
        # Siempre se escribe el primer elemento en el auxiliar uno
        auxiliar_uno.write(primer_elemento + '\n')
        bandera = False # Si la bandera tiene estado "false" se escribe en auxiliar_1 de lo contrario en auxiliar_2
        while segundo_elemento != '':
            # Condicional que establece el estado de bandera para saber donde escribir
            if primer_elemento > segundo_elemento:
                bandera = not bandera
            # Condicional para escribir donde corresponde
            auxiliar_dos.write(segundo_elemento + '\n') if bandera else auxiliar_uno.write(segundo_elemento + '\n')
            primer_elemento = segundo_elemento
            segundo_elemento = archi.readline().rstrip('\n')

def mezcla(aux_1: str = 'Auxiliar_1.txt', aux_2: str = 'Auxiliar_2.txt', archivo : str = 'datos.txt') -> int:
    """
    Mezcla las sublistas ordenadas de los ficheros aux_1 y aux_2 para producir el fichero archivo.
    Parameters
    ----------
    aux_1 : str, optional
        Nombre del archivo auxiliar 1. El valor por defecto es 'Auxiliar_1.txt'.
    aux_2 : str, optional
        Nombre del archivo auxiliar 2. El valor por defecto es 'Auxiliar_2.txt'.
    archivo : str, optional
        Nombre del archivo resultante. El valor por defecto es 'datos.txt'.

    Returns
    -------
    int
        Número de sublistas restantes por ordenar.
    """
    # Abrimos los archivos de partición para lectura y el archivo de datos para escritura
    with open(aux_1, 'r') as aux1, open(aux_2, 'r') as aux2, open(archivo,'w') as archi:
        # Etapa de inicialización, donde leemos los primer elementos de los archivos auxiliares, la bandera en false y el contador de sublistas en cero
        primer_elemento = aux1.readline().rstrip('\n')
        segundo_elemento = aux2.readline().rstrip('\n')
        numSublistas = 0
        ultimo_insertado = '0'
        """Mientras los archivos no lean el string vacio se seguira ejecutando"""
        # Comparamos siempre con el último elemento ingresado, pero teniendo en cuenta el menor de ambos archivos
        # Optimización: Esto se realiza para generar una sublista ordenada lo más grande posible.
        while segundo_elemento != '' and primer_elemento != '':
            if primer_elemento <= segundo_elemento:
                if ultimo_insertado <= primer_elemento:
                    archi.write(primer_elemento + '\n')
                    ultimo_insertado = primer_elemento
                    primer_elemento = aux1.readline().rstrip('\n')
                elif ultimo_insertado <= segundo_elemento:
                    archi.write(segundo_elemento + '\n')
                    ultimo_insertado = segundo_elemento
                    segundo_elemento = aux2.readline().rstrip('\n')
                else:
                    numSublistas += 1
                    archi.write(primer_elemento + '\n')
                    ultimo_insertado = primer_elemento
                    primer_elemento = aux1.readline().rstrip('\n')
            else:
                if ultimo_insertado <= segundo_elemento:
                    archi.write(segundo_elemento + '\n')
                    ultimo_insertado = segundo_elemento
                    segundo_elemento = aux2.readline().rstrip('\n')
                elif ultimo_insertado <= primer_elemento:
                    archi.write(primer_elemento + '\n')
                    ultimo_insertado = primer_elemento
                    primer_elemento = aux1.readline().rstrip('\n')
                else:
                    numSublistas += 1
                    archi.write(segundo_elemento + '\n')
                    ultimo_insertado = segundo_elemento
                    segundo_elemento = aux2.readline().rstrip('\n')
        
        # Es necesario incrementar el valor de las sublistas acá.
        numSublistas += 1
        # En caso de que una de las dos listas sea mas corta y finalice se termina de copiar en el archivo el resto de elementos de la lista sobrante      
        while primer_elemento != '':
            if ultimo_insertado > primer_elemento:
                numSublistas += 1
            archi.write(primer_elemento +'\n')
            ultimo_insertado = primer_elemento
            primer_elemento = aux1.readline().rstrip('\n')
        while segundo_elemento != '':
            if ultimo_insertado > segundo_elemento:
                numSublistas += 1
            archi.write(segundo_elemento +'\n')
            ultimo_insertado = segundo_elemento
            segundo_elemento = aux2.readline().rstrip('\n')
        # Retorna el numero de sublistas para contralar el bucle de la funcion ordenar_por_mezcla_natural
    return numSublistas

def ordenar_por_mezcla_natural(archivo: str = 'datos.txt') -> None:
    """
    Función que llama las n veces necesarias a las funciones dividir y mezcla
    Parameters
    ----------
    archivo : str, optional
        Nombre del archivo a ordenar. El valor por defecto es 'datos.txt'.

    Returns
    -------
    None
    """
    numSublistas= 0
    while numSublistas != 1:
        dividir(archivo)
        numSublistas = mezcla('Auxiliar_1.txt','Auxiliar_2.txt',archivo)

def verificar_ordenado(archivo: str = 'datos.txt') -> bool:
    """
    Recorre el archivo comparando 2 lineas contiguas, verificando que la primer
    linea sea menor a la siguiente comparada.

    Parameters
    ----------
    archivo : str, optional
        Nombre del archivo a verificar el orden. El valor por defecto es 'datos.txt'.

    Returns
    -------
    bool
        True: El archivo está ordenado
        False: El archivo no está ordenado
    """
    with open('datos.txt','r') as datos:
        aux_primero = datos.readline().rstrip('\n')
        aux_segundo = datos.readline().rstrip('\n')
        while aux_segundo != '':
            if aux_primero > aux_segundo:
                return False
            aux_primero = aux_segundo
            aux_segundo = datos.readline().rstrip('\n')
    return True
