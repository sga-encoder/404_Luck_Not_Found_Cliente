from cliente.utils.events import add_key_listener
from cliente.utils.printers import print_text,print_button,print_card
from asciimatics.screen import Screen
import pyfiglet
from cliente.screens.juegos.blackjack.cartas import sacar_carta
from . import blackjack_shared
from cliente.utils.async_wrapper import AsyncScreenManager

# Importar el backend del BlackJack
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../servidor'))
from servidor.src.model.salaDeJuego.juego.juegosDeCartas.BlackJack import BlackJack
from servidor.src.model.usuario.Usuario import Usuario
from servidor.src.model.salaDeJuego.SalaDeJuegoServicio import SalaDeJuegoServicio
import asyncio
from datetime import datetime

def blackjack_juego(screen):
    screen.clear()
    screen.mouse=True
    
    # Usar AsyncScreenManager para manejar el event loop de forma segura
    async_manager = AsyncScreenManager()
    
    # Obtener la instancia del juego desde el estado compartido (YA DEBE EXISTIR)
    game_state = blackjack_shared.get_game_state()
    
    # Verificar que game_state no sea None y que sea una tupla/lista
    if game_state is None:
        print("❌ Error: No hay estado de juego. Volviendo a inicio...")
        async_manager.close()
        return 'blackjack_inicio'
    
    if not isinstance(game_state, (tuple, list)):
        print("❌ Error: Estado de juego inválido (no es tupla). Volviendo a inicio...")
        async_manager.close()
        return 'blackjack_inicio'
    
    if len(game_state) < 2:
        print("❌ Error: Estado de juego incompleto. Volviendo a inicio...")
        async_manager.close()
        return 'blackjack_inicio'
    
    # Ahora sí desempaquetar de forma segura
    try:
        if len(game_state) >= 3:
            blackjack_instance, jugador_actual_usuario, sala_id = game_state
        else:
            blackjack_instance, jugador_actual_usuario = game_state[:2]
            sala_id = None
            
        # Verificar que las instancias no sean None
        if blackjack_instance is None or jugador_actual_usuario is None:
            print("❌ Error: Instancias de juego inválidas. Volviendo a inicio...")
            async_manager.close()
            return 'blackjack_inicio'
            
        print(f"🎮 Usando juego existente para usuario: {jugador_actual_usuario.get_nombre()}")
        
        # Si ya tenemos sala_id, usarlo directamente
        if sala_id:
            print(f"✅ Usando sala existente: {sala_id}")
        
    except (ValueError, TypeError, AttributeError) as e:
        print(f"❌ Error desempaquetando estado de juego: {e}")
        print("❌ Volviendo a inicio...")
        async_manager.close()
        return 'blackjack_inicio'
    
    # Servicio para gestionar Firestore
    servicio_sala = SalaDeJuegoServicio()
    
    def ejecutar_asyncio(coro):
        """Ejecuta una corrutina de forma síncrona usando AsyncScreenManager"""
        try:
            return async_manager.run_async(coro)
        except Exception as e:
            print(f"Error en asyncio: {e}")
            return None
    
    async def obtener_sala_activa():
        """Obtiene la sala activa del usuario desde Firestore"""
        try:
            salas_activas = await servicio_sala.obtener_collection_salas_de_juego()
            
            # Verificar que jugador_actual_usuario no sea None
            if jugador_actual_usuario is None:
                print("❌ Error: Usuario no válido")
                return None
            
            # Buscar sala activa del usuario
            for sala in salas_activas:
                if (sala.get('tipo_juego') == 'BlackJack' and 
                    jugador_actual_usuario.get_id() in sala.get('jugadores', [])):
                    return sala.get('id')
            return None
        except Exception as e:
            print(f"Error obteniendo sala activa: {e}")
            return None
    
    # Solo buscar sala si no la tenemos ya
    if not sala_id:
        print("🔍 Buscando sala activa...")
        sala_id = ejecutar_asyncio(obtener_sala_activa())
        
        if not sala_id:
            print("❌ No se encontró sala activa. Volviendo a inicio...")
            async_manager.close()
            return 'blackjack_inicio'
        
        print(f"✅ Sala encontrada: {sala_id}")
        
        # Actualizar el estado compartido con la sala_id encontrada
        blackjack_shared.set_game_state(blackjack_instance, jugador_actual_usuario, sala_id)
    
    async def actualizar_estado_firestore():
        """Actualiza el estado del juego en Firestore"""
        if sala_id:
            try:
                datos_actualizacion = {
                    'manos_jugadores': {f'jugador_{i+1}': manos_backend[i] for i in range(4)},
                    'mano_crupier': mano_crupier_backend,
                    'turno_actual': jugador_actual,
                    'jugadores_plantados': plantados,
                    'cartas_reveladas': cartas_reveladas,
                    'juego_terminado': juego_terminado,
                    'resultados': resultados if juego_terminado else []
                }
                
                await servicio_sala.actualizar_sala_de_juego(sala_id, datos_actualizacion)
                print(f"🔄 Estado actualizado en Firestore")
                
            except Exception as e:
                print(f"❌ Error actualizando estado: {e}")

    async def finalizar_sala():
        """Finaliza el juego y elimina la sala de Firestore"""
        if sala_id:
            try:
                # Verificar que blackjack_instance no sea None
                fecha_fin = datetime.now().isoformat() if blackjack_instance is None else str(blackjack_instance._fechaHoraInicio)
                
                # Guardar registro final en historial
                await servicio_sala.guardar_registro_sala_de_juego(sala_id, {
                    'id': sala_id,
                    'tipo_juego': 'BlackJack',
                    'estado': 'finalizada',
                    'resultados_finales': resultados,
                    'fecha_hora_fin': fecha_fin,
                    'jugadores_participantes': [f'jugador_{i+1}' for i in range(4)]
                })
                
                # Eliminar de salas activas
                await servicio_sala.eliminar_sala_de_juego(sala_id)
                print(f"🏁 Sala {sala_id} finalizada y eliminada de Firestore")
                
            except Exception as e:
                print(f"❌ Error finalizando sala: {e}")

    async def crear_nueva_sala():
        """Crea una nueva sala para nueva ronda"""
        try:
            # Verificar que las instancias no sean None
            if jugador_actual_usuario is None or blackjack_instance is None:
                print("❌ Error: Instancias no válidas para crear sala")
                return None
                
            fecha_inicio = datetime.now().isoformat() if blackjack_instance._fechaHoraInicio is None else str(blackjack_instance._fechaHoraInicio)
            
            datos_sala = {
                'tipo_juego': 'BlackJack',
                'capacidad': 4,
                'capacidad_minima': 1,
                'jugadores': [jugador_actual_usuario.get_id()],
                'estado': 'activa',
                'valor_entrada_mesa': 100,
                'apuestas': {},
                'historial': [],
                'fecha_hora_inicio': fecha_inicio,
                'creador': jugador_actual_usuario.get_id(),
                'manos_inicializadas': True
            }
            
            nueva_sala_id = await servicio_sala.crear_sala_de_juego_activa(datos_sala)
            print(f"🆕 Nueva sala creada: {nueva_sala_id}")
            return nueva_sala_id
            
        except Exception as e:
            print(f"❌ Error creando nueva sala: {e}")
            return None
    
    # Definir funciones de respaldo ANTES de usarlas
    def extraer_valor_fallback(carta_frontend):
        """Función de respaldo para extraer valor de carta si blackjack_instance es None"""
        import re
        
        # Buscar patrones de valores en el texto de la carta
        match_10 = re.search(r'│10', carta_frontend)
        if match_10:
            return '10'
        
        match = re.search(r'│([A-K2-9])', carta_frontend)
        if match:
            valor = match.group(1)
            # Verificar que sea un valor válido
            cartas_validas = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
                             "J":10,"Q":10,"K":10,"A":11}
            if valor in cartas_validas:
                return valor
        
        # Si no se encuentra, retornar valor por defecto
        import random
        return random.choice(['2','3','4','5','6','7','8','9','10','J','Q','K','A'])

    def calcular_puntos_fallback(mano):
        """Función de respaldo para calcular puntos si blackjack_instance es None"""
        cartas_valores = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
                         "J":10,"Q":10,"K":10,"A":11}
        
        puntos = sum(cartas_valores.get(carta, 0) for carta in mano)
        # Si hay un As y los puntos son mayores a 21, resta 10 puntos
        if 'A' in mano and puntos > 21:
            puntos -= 10
        return puntos
    
    mesa = {
        'text': 'Mesa BlackJack',
        'x-center': 0,
        'y-center': -20,
        'font': 'elite',
        'justify': 'center',
        'color': Screen.COLOUR_CYAN,
    }

    boton_pedirCarta ={
        'text': '┌─────────────┐\n'
                '│ PEDIR CARTA │\n'
                '└─────────────┘',
        'x-center': -70,
        'y-center': 18,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_GREEN,
    }

    boton_plantarse ={
        'text': '┌─────────────┐\n'
                '│  PLANTARSE  │\n'
                '└─────────────┘',
        'x-center': -70,
        'y-center': 22,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_RED,
    }

    boton_revelar_cartas = {
        'text': '┌─────────────┐\n'
                '│REVELAR CARTA│\n'
                '└─────────────┘',
        'x-center': -70,
        'y-center': 26,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_YELLOW,
    }

    boton_jugadorActivo ={
        'text': '[JUGADOR ACTIVO]',
        'x-center': 0,
        'y-center': 0,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_BLUE,
       }
    
    boton_jugadorEspera ={
        'text': '[JUGADOR ESPERANDO]',
        'x-center': 0,
        'y-center': 0,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_MAGENTA,
       }

    # Inicializar 4 jugadores backend
    jugadores_backend = [
        Usuario.crear_usuario_local(f"Jugador {i+1}", f"Apellido {i+1}") 
        for i in range(4)
    ]
    
    # Inicializar manos sincronizando frontend y backend
    manos_backend = []
    jugadores = []
    
    for i in range(4):
        # Generar cartas del frontend primero
        mano_frontend = [sacar_carta(), sacar_carta()]
        jugadores.append(mano_frontend)
        
        # Extraer valores del frontend y crear mano backend correspondiente
        mano_backend = []
        for carta_frontend in mano_frontend:
            # Verificar que blackjack_instance no sea None antes de usar sus métodos
            if blackjack_instance is not None:
                valor_backend = blackjack_instance.extraer_valor_carta(carta_frontend)
            else:
                # Fallback: extraer valor manualmente
                valor_backend = extraer_valor_fallback(carta_frontend)
            mano_backend.append(valor_backend)
        manos_backend.append(mano_backend)
    
    # Mano del crupier sincronizada
    crupier = [sacar_carta(), sacar_carta()]  # Frontend
    mano_crupier_backend = []  # Backend correspondiente
    for carta_frontend in crupier:
        if blackjack_instance is not None:
            valor_backend = blackjack_instance.extraer_valor_carta(carta_frontend)
        else:
            valor_backend = extraer_valor_fallback(carta_frontend)
        mano_crupier_backend.append(valor_backend)

    plantados = [False] * 4
    cartas_reveladas = False
    juego_terminado = False
    resultados = []

    posiciones = [
        (-65, -5),  # Jugador 1
        (-47, 15),   # Jugador 2
        (25, 15),    # Jugador 3
        (30, -5),   # Jugador 4
    ]
    posicion_crupier = (-15, -5)

    jugador_actual = 0

    # Actualizar estado inicial en Firestore
    ejecutar_asyncio(actualizar_estado_firestore())

    def avanzar_turno():
        nonlocal jugador_actual, juego_terminado, cartas_reveladas
        if jugador_actual < len(jugadores)-1:
            jugador_actual += 1
        else:
            # Si llegamos al final, todos han jugado
            if all(plantados):
                # Turno del crupier automático
                turno_crupier()
                cartas_reveladas = True
                juego_terminado = True
        
        # Actualizar estado en Firestore
        ejecutar_asyncio(actualizar_estado_firestore())

    def pedir_carta_backend():
        """Pedir carta usando la lógica del backend"""
        if not plantados[jugador_actual] and not juego_terminado:
            # Generar carta del frontend
            nueva_carta_frontend = sacar_carta()
            jugadores[jugador_actual].append(nueva_carta_frontend)
            
            # Extraer valor y agregarlo al backend
            if blackjack_instance is not None:
                valor_backend = blackjack_instance.extraer_valor_carta(nueva_carta_frontend)
            else:
                valor_backend = extraer_valor_fallback(nueva_carta_frontend)
            manos_backend[jugador_actual].append(valor_backend)
            
            # Verificar puntos usando método del backend con valores reales
            if blackjack_instance is not None:
                puntos = blackjack_instance.calcular_puntos(manos_backend[jugador_actual])
            else:
                puntos = calcular_puntos_fallback(manos_backend[jugador_actual])
                
            if puntos >= 21:
                plantados[jugador_actual] = True
                avanzar_turno()
            else:
                # Actualizar estado en Firestore
                ejecutar_asyncio(actualizar_estado_firestore())

    def plantarse_backend():
        """Plantarse usando la lógica del backend"""
        if not juego_terminado:
            plantados[jugador_actual] = True
            avanzar_turno()
            return 'PLANTADO'

    def revelar_cartas_crupier():
        """Revelar las cartas del crupier manualmente"""
        nonlocal cartas_reveladas, juego_terminado
        if not cartas_reveladas:
            turno_crupier()
            cartas_reveladas = True
            juego_terminado = True
        return 'REVELADO'

    def turno_crupier():
        """Lógica del turno del crupier"""
        nonlocal mano_crupier_backend, crupier, resultados
        
        # El crupier debe sacar cartas hasta tener 17 o más puntos
        if blackjack_instance is not None:
            puntos_crupier = blackjack_instance.calcular_puntos(mano_crupier_backend)
        else:
            puntos_crupier = calcular_puntos_fallback(mano_crupier_backend)
            
        while puntos_crupier < 17:
            # Agregar nueva carta
            nueva_carta_frontend = sacar_carta()
            crupier.append(nueva_carta_frontend)
            
            if blackjack_instance is not None:
                valor_backend = blackjack_instance.extraer_valor_carta(nueva_carta_frontend)
            else:
                valor_backend = extraer_valor_fallback(nueva_carta_frontend)
            mano_crupier_backend.append(valor_backend)
            
            if blackjack_instance is not None:
                puntos_crupier = blackjack_instance.calcular_puntos(mano_crupier_backend)
            else:
                puntos_crupier = calcular_puntos_fallback(mano_crupier_backend)
        
        # Determinar ganadores
        determinar_ganadores()
        
        # Actualizar estado final en Firestore
        ejecutar_asyncio(actualizar_estado_firestore())

    def determinar_ganadores():
        """Determina quién gana y quién pierde"""
        nonlocal resultados
        resultados = []
        
        if blackjack_instance is not None:
            puntos_crupier = blackjack_instance.calcular_puntos(mano_crupier_backend)
        else:
            puntos_crupier = calcular_puntos_fallback(mano_crupier_backend)
        
        for i in range(4):
            if blackjack_instance is not None:
                puntos_jugador = blackjack_instance.calcular_puntos(manos_backend[i])
            else:
                puntos_jugador = calcular_puntos_fallback(manos_backend[i])
            
            if puntos_jugador > 21:
                resultado = "PERDIÓ (Se pasó)"
                color = Screen.COLOUR_RED
            elif puntos_crupier > 21:
                resultado = "GANÓ (Crupier se pasó)"
                color = Screen.COLOUR_GREEN
            elif puntos_jugador > puntos_crupier:
                resultado = "GANÓ"
                color = Screen.COLOUR_GREEN
            elif puntos_jugador < puntos_crupier:
                resultado = "PERDIÓ"
                color = Screen.COLOUR_RED
            else:
                resultado = "EMPATE"
                color = Screen.COLOUR_YELLOW
            
            resultados.append({
                'texto': f"J{i+1}: {puntos_jugador} pts - {resultado}",
                'color': color
            })

    def nueva_ronda():
        """Reinicia el juego para una nueva ronda"""
        nonlocal jugadores, manos_backend, crupier, mano_crupier_backend, sala_id
        nonlocal plantados, cartas_reveladas, juego_terminado, resultados, jugador_actual
        
        # Finalizar sala actual
        ejecutar_asyncio(finalizar_sala())
        
        # Crear nueva sala
        nueva_sala_id = ejecutar_asyncio(crear_nueva_sala())
        
        if not nueva_sala_id:
            print("❌ Error creando nueva sala")
            return 'blackjack_inicio'
        
        # Actualizar sala_id global
        sala_id = nueva_sala_id
        
        # Actualizar estado compartido con nueva sala_id
        blackjack_shared.set_game_state(blackjack_instance, jugador_actual_usuario, sala_id)
        
        screen.clear()
        
        # Reinicializar todo
        manos_backend = []
        jugadores = []
        
        for i in range(4):
            mano_frontend = [sacar_carta(), sacar_carta()]
            jugadores.append(mano_frontend)
            
            mano_backend = []
            for carta_frontend in mano_frontend:
                if blackjack_instance is not None:
                    valor_backend = blackjack_instance.extraer_valor_carta(carta_frontend)
                else:
                    valor_backend = extraer_valor_fallback(carta_frontend)
                mano_backend.append(valor_backend)
            manos_backend.append(mano_backend)
        
        # Nueva mano del crupier
        crupier = [sacar_carta(), sacar_carta()]
        mano_crupier_backend = []
        for carta_frontend in crupier:
            if blackjack_instance is not None:
                valor_backend = blackjack_instance.extraer_valor_carta(carta_frontend)
            else:
                valor_backend = extraer_valor_fallback(carta_frontend)
            mano_crupier_backend.append(valor_backend)

        plantados = [False] * 4
        cartas_reveladas = False
        juego_terminado = False
        resultados = []
        jugador_actual = 0
        
        # Actualizar estado inicial en nueva sala
        ejecutar_asyncio(actualizar_estado_firestore())
        
        return 'NUEVA_RONDA'

    def salir_del_juego():
        """Maneja la salida del juego"""
        # Finalizar y eliminar sala de Firestore
        print("🚪 Saliendo del juego...")
        ejecutar_asyncio(finalizar_sala())
        blackjack_shared.clear_game_state()
        async_manager.close()
        return 'salir'

    try:
        while True:
            screen.refresh()
            print_text(screen, mesa, True)
            
            # Mostrar ID de sala
            sala_info = {
                'text': f'Sala ID: {sala_id}',
                'x-center': 0,
                'y-center': -15,
                'color': Screen.COLOUR_GREEN,
            }
            print_text(screen, sala_info)
            
            # Mostrar todas las cartas del jugador alineadas horizontalmente
            for idx, mano in enumerate(jugadores):
                x_base, y_base = posiciones[idx]
                for j, carta_texto in enumerate(mano):
                    carta = {
                        'text': carta_texto,
                        'x-center': x_base + (j * 18),
                        'y-center': y_base,
                        'color': Screen.COLOUR_BLACK,
                        'bg': Screen.COLOUR_WHITE,
                        'height': 10,
                        'width': 15,
                    }
                    print_card(screen, carta)

                # Mostrar estado del jugador
                if idx == jugador_actual and not plantados[jugador_actual] and not juego_terminado:
                    boton_jugadorActivo['x-center'] = x_base
                    boton_jugadorActivo['y-center'] = y_base - 8
                    print_button(screen, boton_jugadorActivo)
                else:
                    boton_jugadorEspera['x-center'] = x_base
                    boton_jugadorEspera['y-center'] = y_base - 8
                    print_button(screen, boton_jugadorEspera)

            # Mostrar cartas del crupier
            for i, carta_texto in enumerate(crupier):
                if i == 0 or cartas_reveladas:
                    # Mostrar carta real
                    carta_config = {
                        'text': carta_texto,
                        'x-center': posicion_crupier[0] + (i * 18),
                        'y-center': posicion_crupier[1],
                        'color': Screen.COLOUR_BLACK,
                        'bg': Screen.COLOUR_WHITE,
                        'height': 10,
                        'width': 15
                    }
                else:
                    # Carta oculta
                    carta_config = {
                    'text':
                        '┌─────────────┐'
                '        │ ?           │'
                '        │             │'
                '        │             │'
                '        │      #      │'
                '        │             │'
                '        │             │'
                '        │           ? │'
                '        └─────────────┘',
                        'x-center': posicion_crupier[0] + (i * 18),
                        'y-center': posicion_crupier[1],
                        'color': Screen.COLOUR_WHITE,
                        'bg': Screen.COLOUR_RED,
                        'height': 10,
                        'width': 15
                    }
                print_card(screen, carta_config)

            # Mostrar puntos del crupier si están reveladas
            if cartas_reveladas:
                if blackjack_instance is not None:
                    puntos_crupier = blackjack_instance.calcular_puntos(mano_crupier_backend)
                else:
                    puntos_crupier = calcular_puntos_fallback(mano_crupier_backend)
                    
                puntos_crupier_text = {
                    'text': f'Crupier: {puntos_crupier} puntos',
                    'x-center': posicion_crupier[0],
                    'y-center': posicion_crupier[1] + 8,
                    'color': Screen.COLOUR_CYAN,
                }
                print_text(screen, puntos_crupier_text)

            # Mostrar resultados si el juego terminó
            if juego_terminado and resultados:
                for i, resultado in enumerate(resultados):
                    x_base, y_base = posiciones[i]
                    resultado_text = {
                        'text': resultado['texto'],
                        'x-center': x_base + 20,
                        'y-center': y_base - 10,
                        'color': resultado['color'],
                    }
                    print_text(screen, resultado_text)
                
                # Mostrar instrucciones para nueva ronda
                instruccion_nueva_ronda = {
                    'text': 'Presiona N para Nueva Ronda | F para Salir',
                    'x-center': 0,
                    'y-center': 25,
                    'color': Screen.COLOUR_WHITE,
                    'bg': Screen.COLOUR_BLUE,
                }
                print_text(screen, instruccion_nueva_ronda)

            event = screen.get_event()

            # Botones según el estado del juego
            if not juego_terminado:
                # Solo mostrar botones de juego si el jugador actual no está plantado
                if not plantados[jugador_actual]:
                    print_button(
                        screen,
                        boton_pedirCarta,
                        event,
                        click=pedir_carta_backend
                    )

                    print_button(
                        screen,
                        boton_plantarse,
                        event,
                        click=plantarse_backend,
                    )
                
                # Botón para revelar cartas manualmente (disponible cuando todos estén plantados)
                if all(plantados) and not cartas_reveladas:
                    print_button(
                        screen,
                        boton_revelar_cartas,
                        event,
                        click=revelar_cartas_crupier
                    )
            
            # Key listeners
            # Salir con tecla F
            salir = add_key_listener(ord('f'), event, salir_del_juego)
            if salir == 'salir':
                return 'salir'
            
            # Nueva ronda con tecla N (solo cuando el juego haya terminado)
            if juego_terminado:
                nueva_ronda_key = add_key_listener(ord('n'), event, nueva_ronda)
                if nueva_ronda_key == 'NUEVA_RONDA':
                    pass  # La función nueva_ronda() ya reinicia todo
    
    except KeyboardInterrupt:
        print("🛑 Juego interrumpido por el usuario")
        async_manager.close()
        return 'salir'
    except Exception as e:
        print(f"❌ Error inesperado en el juego: {e}")
        async_manager.close()
        return 'salir'
    finally:
        # Asegurar que el async manager se cierre al salir
        async_manager.close()