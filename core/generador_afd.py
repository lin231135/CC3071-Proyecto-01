from modelos.estado import EstadoAFD

def generar_afd(arbol):
    """Aplica el Algoritmo 3.36 para crear los estados y transiciones del AFD."""
    estado_inicial_pos = frozenset(arbol.raiz.primera_pos)
    estado_inicial = EstadoAFD('A', estado_inicial_pos)
    
    estados_creados = {estado_inicial_pos: estado_inicial}
    cola_sin_marcar = [estado_inicial_pos]
    
    # Extraer el alfabeto e identificar el ID del marcador '#'
    alfabeto = set()
    id_fin = -1
    for pos, char in arbol.hojas.items():
        if char == '#': id_fin = pos
        else: alfabeto.add(char)
        
    letra_actual = ord('B') # Para nombrar los estados: A, B, C...
    
    while cola_sin_marcar:
        T = cola_sin_marcar.pop(0)
        estado_actual = estados_creados[T]
        
        if id_fin in T: # Si este estado contiene la posición del '#', es de aceptación
            estado_actual.es_aceptacion = True
            
        for char in alfabeto:
            U = set() # U es el nuevo conjunto de posiciones
            for pos in T:
                if arbol.hojas[pos] == char:
                    U.update(arbol.siguiente_pos[pos])
                    
            U_frozen = frozenset(U)
            if U_frozen: # Si el conjunto no está vacío, hay una transición
                if U_frozen not in estados_creados:
                    nuevo_estado = EstadoAFD(chr(letra_actual), U_frozen)
                    letra_actual += 1
                    estados_creados[U_frozen] = nuevo_estado
                    cola_sin_marcar.append(U_frozen)
                
                # Registrar la transición en el estado actual
                estado_actual.transiciones[char] = estados_creados[U_frozen].id_estado
                
    return list(estados_creados.values())