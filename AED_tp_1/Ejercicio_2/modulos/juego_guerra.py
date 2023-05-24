from __future__ import annotations
from cola_doble import ColaDoble
import random as rd

class Carta:
    def __init__(self, valor : str, palo : str) -> None:
        self._valor = valor
        self._palo = palo
        self.boca_abajo = True
    
    @property
    def valor(self) -> str:
        return self._valor
    
    @property
    def palo(self) -> str:
        return self._palo
    
    @property
    def boca_abajo(self) -> bool:
        return self._boca_abajo
    
    @boca_abajo.setter
    def boca_abajo(self, new_valor: bool) -> None:
        self._boca_abajo = new_valor
        
    def __str__(self):
        return '-X' if self.boca_abajo else f'{self.valor}{self.palo}'
    
    def __eq__(self, otra_carta: Carta) -> bool:
        return self.valor == otra_carta.valor
    
    def __lt__(self, otra_carta: Carta) -> bool:
        valores = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        return valores.index(self.valor) < valores.index(otra_carta.valor)
    
    def __le__(self, otra_carta: Carta) -> bool:
        return self.__lt__(otra_carta) or self.__eq__(otra_carta)
    
    def __gt__(self, otra_carta: Carta) -> bool:
        return not self.__lt__(otra_carta) and not self.__eq__(otra_carta)
    
    def __ge__(self, otra_carta: Carta) -> bool:
        return self.__gt__(otra_carta) or self.__eq__(otra_carta)

class JuegoGuerra:
    def __init__(self, random_seed : int = 0) -> None:
        self._turnos_jugados = 0
        self._ganador = None
        self._empate = False
        self.en_guerra = False
        rd.seed(random_seed)
        
        # Generación de mazos
        valores = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        palos = ['♠', '♥', '♦', '♣']
        
        # Generamos el mazo con cada carta
        mazo = []
        for val in valores:
            for palo in palos:
                mazo.append(Carta(val, palo))
        
        # Mezclamos el mazo
        rd.shuffle(mazo)
        # Inicializamos una cola doble para el mazo
        mazo_inicial = ColaDoble()
        for carta in mazo:
            mazo_inicial.agregar_arriba(carta)
        
        # Ahora inicializamos los mazos de cada jugador
        self.mazo_jugador1 = ColaDoble()
        self.mazo_jugador2 = ColaDoble()
        # Damos las cartas de forma intercalada
        i = 0
        while mazo_inicial.tamanio != 0:
            self.mazo_jugador1.agregar_arriba(mazo_inicial.avanzar()) if i % 2 == 0 else self.mazo_jugador2.agregar_arriba(mazo_inicial.avanzar())
            i += 1
        
    @property
    def turnos_jugados(self) -> int:
        return self._turnos_jugados
    
    @property
    def ganador(self) -> str:
        return self._ganador
    
    @property
    def empate(self) -> bool:
        return self._empate
    
    def jugar_cartas(self, jugador : str, boca_abajo : bool = False) -> Carta:
        carta_jugada = None
        if jugador == 'j1':
            carta_jugada = self.mazo_jugador1.avanzar()
            carta_jugada.boca_abajo = boca_abajo
            self.mesa_j1.append(carta_jugada)
        else:
            carta_jugada = self.mazo_jugador2.avanzar()
            carta_jugada.boca_abajo = boca_abajo
            self.mesa_j2.append(carta_jugada)
        
        return carta_jugada
    
    def decidir_ganador_del_turno(self) -> str:
        # Retorna un string del ganador o empate.
        # Verificamos solamente las cartas del final de cada lista mesa
        carta_j1 = self.mesa_j1[-1]
        carta_j2 = self.mesa_j2[-1]
        resultado = 'empate'
        if carta_j1 > carta_j2:
            resultado = 'j1'
        elif carta_j1 < carta_j2:
            resultado = 'j2'
            
        return resultado
    
    def repartir_botin(self, ganador : str) -> None:
        # Otorga las cartas de ambas mesas de forma alternada para el jugador ganador
        # La longitud de las mesas debe ser iguales a este punto, solo usamos mesa_j1
        for i in range(len(self.mesa_j1)):
            if ganador == 'j1':
                carta = self.mesa_j1[i]
                # Hacemos que la carta vuelva a estar boca abajo
                carta.boca_abajo = True
                self.mazo_jugador1.agregar(carta)
                carta = self.mesa_j2[i]
                # Hacemos que la carta vuelva a estar boca abajo
                carta.boca_abajo = True
                self.mazo_jugador1.agregar(carta)
            else:
                # No deberia de haber un empate acá, simplemente pasamos como else
                carta = self.mesa_j1[i]
                # Hacemos que la carta vuelva a estar boca abajo
                carta.boca_abajo = True
                self.mazo_jugador2.agregar(carta)
                carta = self.mesa_j2[i]
                # Hacemos que la carta vuelva a estar boca abajo
                carta.boca_abajo = True
                self.mazo_jugador2.agregar(carta)
            
    def iniciar_juego(self) -> None:
        # Loop de juego
        # Las cartas en la mesa de cada jugador
        self.mesa_j1 = []
        self.mesa_j2 = []
        self.en_guerra = False
        # Loop de juego
        while self._turnos_jugados < 10000:
            # Para cada inicio del turno verificamos los mazos de cada jugador
            # Vamos a terminar el loop con un break cuando sea necesario.
            if not self.mazo_jugador1.tamanio:
                self._ganador = 'jugador 2'
            if not self.mazo_jugador2.tamanio:
                self._ganador = 'jugador 1'
            # Chequeamos si hay ganador, si lo hay cortamos el loop
            if self._ganador:
                break
            
            # Solamente aumentamos el turno si no estamos en guerra
            if not self.en_guerra:
                self._turnos_jugados += 1
            
            # Procedemos a jugar las cartas correspondientes, dependiendo de si estamos en guerra o no
            if self.en_guerra:
                # Si estamos en guerra debemos jugar 3 cartas boca abajo para cada jugador
                # Pero antes debemos chequear si los jugadores tienen las cartas suficientes
                # para la guerra
                if self.mazo_jugador1.tamanio < 4:
                    self._ganador = 'jugador 2'
                    break
                elif self.mazo_jugador2.tamanio < 4:
                    self._ganador = 'jugador 1'
                    break
                # Jugamos las 3 cartas boca abajo
                for _ in range(3):
                    self.jugar_cartas('j1', True)
                    self.jugar_cartas('j2', True)
                    
            # Jugamos las cartas boca arriba y decidimos
            self.jugar_cartas('j1')
            self.jugar_cartas('j2')
            
            # Mostramos la mesa
            print(self)
            
            # Ahora procedemos a verificar los resultados de la mesa y
            # decidimos el ganador del turno
            resultado = self.decidir_ganador_del_turno()
            if resultado != 'empate':
                # Si estabamos en guerra, ya no lo estamos.
                self.en_guerra = False
                # Repartimos las cartas al ganador
                self.repartir_botin(resultado)
                # Limpiamos la mesa
                self.mesa_j1.clear()
                self.mesa_j2.clear()
            else:
                # Continuamos con la ejecucion del loop
                self.en_guerra = True
                
        if self.turnos_jugados == 10000 and not self._ganador:
            self._empate = True
        
        print(self)

    def __str__(self):
        result = f"{'-' * 36}\n"
        if self.ganador:
            return result + f'***** {self.ganador} gana la partida *****'.center(64, ' ')
        elif self.empate:
            return result + '***** Empate *****'.center(64, ' ')
        
        turno = f'Turno: {self.turnos_jugados}\n'
        guerra = '**** Guerra!! ****'.center(64, ' ')
        mazo_1 = ''
        idx = 0
        for carta in self.mazo_jugador1:
            mazo_1 += f'{(carta.dato)} '
            idx += 1
            if idx % 10 == 0 and idx < self.mazo_jugador1.tamanio:
                mazo_1 += '\n'
        mesa = ''
        for i in range(len(self.mesa_j1)):
            mesa += f' {str(self.mesa_j1[i])} {str(self.mesa_j2[i])}'
        mesa.center(64, ' ')
        mazo_2 = ''
        idx = 0
        for carta in self.mazo_jugador2:
            mazo_2 += f'{(carta.dato)} '
            idx += 1
            if idx % 10 == 0 and idx < self.mazo_jugador2.tamanio:
                mazo_2 += '\n'
        if self.en_guerra:
            result += guerra + '\n'
        result += turno
        result += f'jugador 1:\n{mazo_1} \n\n'
        result += f'        {mesa}        \n\n'
        result += f'jugador 2:\n{mazo_2}\n'
        return result
        
if __name__ == '__main__':
    
    juego = JuegoGuerra(random_seed=547)
    juego.iniciar_juego()
    pass