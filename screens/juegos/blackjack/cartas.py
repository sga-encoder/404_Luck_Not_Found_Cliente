import random

# Diccionario de palos con sus símbolos y abreviaciones para nombres de variables, no afectaran a la puntuacion
palos = {
    'corazones': ('♥', 'Corazones'),
    'diamantes': ('♦', 'Diamantes'),
    'treboles': ('♣', 'Treboles'),
    'picas': ('♠', 'Picas')
}

valores = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

# Diccionario para almacenar todas las cartas y lista tipo mazo
cartas = {}
mazo = []

# Generar las 52 cartas
for palo, (simbolo, nombre_palo) in palos.items():
    for valor in valores:
        nombre_variable = valor
        valor_izq = valor.ljust(2) if len(valor) == 1 else valor
        valor_der = valor.rjust(2) if len(valor) == 1 else valor
        carta = (
                '┌─────────────┐'
        f'        │{valor_izq}           │'
        '        │             │'
        '        │             │'
        f'        │      {simbolo}      │'
        '        │             │'
        '        │             │'
        f'        │           {valor_der}│'
        '        └─────────────┘' 
        )
        cartas[nombre_variable] = carta
        mazo.append(carta)

# Barajar el mazo
random.shuffle(mazo)

# Mostrar varias cartas alineadas horizontalmente
def mostrar_cartas_en_linea(cartas_ascii):
    lineas_cartas = [carta.splitlines() for carta in cartas_ascii]
    for i in range(len(lineas_cartas[0])):
        print("  ".join(linea[i] for linea in lineas_cartas))

# Función para sacar una carta del mazo (como en un mazo real)
def sacar_carta():
    if mazo:
        return mazo.pop()
    else:
        return "No quedan cartas en el mazo."