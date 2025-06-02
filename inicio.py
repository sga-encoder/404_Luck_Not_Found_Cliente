from asciimatics.screen import Screen
import time
import pyfiglet


from screens.home import home
from screens.juegos.poker import poker
from screens.juegos.blackjack import blackjack
from screens.juegos.knucklebones.knucklebones import knucklebones
from screens.forms.login import login_form
from screens.forms.login_avanzado import advanced_login_form
from utils.events import add_key_listener
from utils.helpers import create_card, font_tester, font_tester_recomded
from utils.printers import print_button, print_text

def inicio(screen):
    screen.mouse = True
    contador = [0]
    text = {
        'text': '404-LUCK-NOT FOUND',
        'x-center': 0,
        'y-center': -5,
        'font': 'big_money-ne',
        'justify': 'center',
        'max-width': 130,
    }
    boton_text = {
        'text': '[  INICIAR JUEGO  ]',
        'x-center': 0,
        'y-center': 5,
        'color': Screen.COLOUR_WHITE,
        'bg': Screen.COLOUR_BLUE
    }
    while True:
        screen.refresh()
        print_text(screen, text, True)
        event = screen.get_event()  # Solo aquí
        button_inicio = print_button(
            screen,
            boton_text,
            event,
            click=lambda: True
        )
        print_text(screen, {'text': f'Contador: {contador[0]}', 'x-center': 0, 'y-center': 8})
        if button_inicio['result']:
            return button_inicio['result']
        # Escuchar Enter como 10 y 13
        add_key_listener([10, 13], event, lambda: (contador.__setitem__(0, contador[0] + 1)))

def main(screen):
    resultado = inicio(screen)
    if resultado:
        card = home(screen)
        if card == 'poker':
            poker(screen)
        elif card == 'blackjack':
            blackjack(screen)
        elif card == 'knucklebones':
            knucklebones(screen)

def main_dev(screen):
    """
    Función de desarrollo para probar formularios de login
    """
    screen.clear()
    print_text(screen, {
        'text': '=== MODO DESARROLLO ===',
        'x-center': 0,
        'y-center': -15,
        'color': Screen.COLOUR_YELLOW
    })
    
    print_text(screen, {
        'text': 'Presiona 1 para Login Básico, 2 para Login Avanzado, ESC para salir',
        'x-center': 0,
        'y-center': -13,
        'color': Screen.COLOUR_CYAN
    })
    
    screen.refresh()
    screen.clear()
    
    while True:
        event = screen.get_event()
        
        if event and hasattr(event, 'key_code'):
            if event.key_code == ord('1'):
                # Probar login básico
                resultado = login_form(screen)
                mostrar_resultado_login(screen, resultado, "BÁSICO")
            elif event.key_code == ord('2'):
                # Probar login avanzado
                resultado = advanced_login_form(screen)
                mostrar_resultado_login(screen, resultado, "AVANZADO")
                
            elif event.key_code == 27:  # ESC
                break
        
        # screen.clear()
        print_text(screen, {
            'text': '=== MODO DESARROLLO ===',
            'x-center': 0,
            'y-center': -15,
            'color': Screen.COLOUR_YELLOW
        })
        
        print_text(screen, {
            'text': 'Presiona 1 para Login Básico, 2 para Login Avanzado, ESC para salir',
            'x-center': 0,
            'y-center': -13,
            'color': Screen.COLOUR_CYAN
        })
        
        screen.refresh()

def mostrar_resultado_login(screen, resultado, tipo):
    """
    Muestra el resultado del login de manera detallada
    """
    screen.clear()
    
    if resultado and resultado.get('action') == 'login':
        print_text(screen, {
            'text': f'✅ LOGIN EXITOSO ({tipo})',
            'x-center': 0,
            'y-center': -5,
            'color': Screen.COLOUR_GREEN
        })
        
        print_text(screen, {
            'text': f"Usuario: {resultado['usuario']}",
            'x-center': 0,
            'y-center': -3,
            'color': Screen.COLOUR_WHITE
        })
        
        print_text(screen, {
            'text': f"Contraseña: {'*' * len(resultado['password'])}",
            'x-center': 0,
            'y-center': -2,
            'color': Screen.COLOUR_WHITE
        })
        
        if 'recordar' in resultado:
            recordar_texto = "SÍ" if resultado['recordar'] else "NO"
            print_text(screen, {
                'text': f"Recordar usuario: {recordar_texto}",
                'x-center': 0,
                'y-center': -1,
                'color': Screen.COLOUR_WHITE
            })
            
    else:
        print_text(screen, {
            'text': '❌ LOGIN CANCELADO',
            'x-center': 0,
            'y-center': -3,
            'color': Screen.COLOUR_RED
        })
    
    print_text(screen, {
        'text': 'Presiona cualquier tecla para continuar...',
        'x-center': 0,
        'y-center': 2,
        'color': Screen.COLOUR_CYAN
    })
    
    screen.refresh()
    screen.get_event()  # Esperar entrada del usuario



if __name__ == "__main__":
    # font_tester('v.s',2)
    # font_tester_recomded('404-LUCK-NOT FOUND')
    # Screen.wrapper(main)
    Screen.wrapper(main_dev)  # Cambiar a main_dev para probar login
    # print(create_card({
    #     'width': 55,
    #     'height': 27,
    #     'text': '',
    #     'ascii_x': '│',
    #     'ascii_y': '─',
    #     'grid_divider_x': 3,
    #     'grid_divider_y': 3,
    #     'corner': ['╭', '╮', '╰', '╯'],
    #     'grid': True,
    # }))