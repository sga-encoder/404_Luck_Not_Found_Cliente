from asciimatics.screen import Screen

from cliente.utils.user_session import UserSessionManager
from servidor.src.model.salaDeJuego.juego import KnuckleBones
from servidor.src.model.usuario import Usuario

from ....utils.events import add_key_listener
from ....utils.printers import print_button, print_text

async def knucklebones_inicio(screen):
    screen.mouse = True
    text = {
        'text': 'KNUCKLEBONES',
        'x-center': 0,
        'y-center': -5,
        'font': 'big_money-ne',
        'justify': 'center',
        'max-width': 120,
    }
    boton_text = {
        'text': '[  INICIAR JUEGO  ]',
        'x-center': 0,
        'y-center': 5,
        'color': Screen.COLOUR_WHITE,
        'bg': Screen.COLOUR_CYAN
    }
    
    error_text = {
        'text': 'Error: No se pudieron cargar los datos del usuario',
        'x-center': 0,
        'y-center': 0,
        'color': Screen.COLOUR_RED,
        'bg': Screen.COLOUR_BLACK
    }
    
    screen.clear()
    auth = UserSessionManager()
    
    try:
        data_user = await auth.load_user_session()
        
        # Verificar si los datos del usuario son válidos
        if data_user is None:
            # Mostrar mensaje de error en pantalla
            while True:
                screen.clear()
                print_text(screen, error_text, True)
                screen.refresh()
                
                event = screen.get_event()
                if event and hasattr(event, 'key') and event.key:
                    return False
        
        user = Usuario.from_dict(data_user)
    except Exception as e:
        # Mostrar error específico
        error_text['text'] = f'Error al cargar sesión: {str(e)}'
        while True:
            screen.clear()
            print_text(screen, error_text, True)
            screen.refresh()
            
            event = screen.get_event()
            if event and hasattr(event, 'key') and event.key:
                return False
    
    while True:
        # screen.clear()
        print_text(screen, text, True)
        screen.refresh()
        
        event = screen.get_event()
        button_inicio = print_button(
            screen,
            boton_text,
            event,
            click=lambda: True
        )
        
        if button_inicio['result']:
            try:
                juego = KnuckleBones()
                # Verificar que el juego se haya inicializado correctamente
                if juego is None:
                    print("Error: No se pudo inicializar el juego KnuckleBones")
                    return False
                
                # Intentar entrar a la sala de juego (usando await porque es async)
                resultado = await juego.entrar_sala_de_juego(user, juego.to_dict())
                if resultado:
                    return button_inicio['result']
                else:
                    print("Error: No se pudo entrar a la sala de juego")
                    return False
            except Exception as e:
                print(f"Error al inicializar KnuckleBones: {str(e)}")
                return False
        
        # add_key_listener(screen, button_inicio)
        
        if button_inicio['result']:
            return button_inicio['result']