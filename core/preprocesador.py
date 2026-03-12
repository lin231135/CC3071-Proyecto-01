def formatear_regex(regex):
    """
    Agrega el operador de concatenación explícita ('.') y el marcador final ('#').
    Ejemplo: '(a|b)*abb' -> '((a|b)*.a.b.b).#'
    """
    res = ""
    for i in range(len(regex)):
        c1 = regex[i]
        res += c1
        if i + 1 < len(regex):
            c2 = regex[i + 1]
            # Condiciones para que exista concatenación implícita entre dos caracteres
            if c1 not in {'(', '|', '.'} and c2 not in {')', '|', '*', '+', '?', '.'}:
                res += '.'
    
    return f"({res}).#"

def infijo_a_postfijo(regex):
    """
    Algoritmo Shunting Yard para convertir de notación infija a postfija.
    """
    precedencia = {'|': 1, '.': 2, '*': 3, '+': 3, '?': 3}
    salida = []
    pila = []
    
    for char in regex:
        # Si es un operando (letra, número o el hashtag)
        if char.isalnum() or char == '#' or (char not in precedencia and char not in {'(', ')'}):
            salida.append(char)
        elif char == '(':
            pila.append(char)
        elif char == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop() # Eliminar el '(' de la pila
        else: # Es un operador
            while pila and pila[-1] != '(' and precedencia.get(pila[-1], 0) >= precedencia.get(char, 0):
                salida.append(pila.pop())
            pila.append(char)
            
    while pila:
        salida.append(pila.pop())
        
    return "".join(salida)