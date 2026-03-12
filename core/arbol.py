from modelos.nodo import Nodo

class ArbolSintactico:
    """Construye el árbol binario y calcula anulable, primera_pos, ultima_pos y siguiente_pos."""
    def __init__(self, regex_postfija):
        self.regex = regex_postfija
        self.raiz = None
        self.siguiente_pos = {}  # Diccionario: id_posicion -> set(id_posiciones)
        self.hojas = {}          # Diccionario: id_posicion -> caracter
        self.contador_pos = 1
        self.construir_arbol()
        
    def construir_arbol(self):
        pila = []
        for char in self.regex:
            if char in {'*', '+', '?'}: # Operadores unarios
                nodo = Nodo(char)
                nodo.hijo_izq = pila.pop()
                pila.append(nodo)
            elif char in {'.', '|'}:    # Operadores binarios
                nodo = Nodo(char)
                nodo.hijo_der = pila.pop()
                nodo.hijo_izq = pila.pop()
                pila.append(nodo)
            else:                       # Es una hoja (operando)
                if char == 'ε':
                    nodo = Nodo(char)
                else:
                    nodo = Nodo(char, self.contador_pos)
                    self.siguiente_pos[self.contador_pos] = set()
                    self.hojas[self.contador_pos] = char
                    self.contador_pos += 1
                pila.append(nodo)
        
        self.raiz = pila.pop()
        self.calcular_propiedades(self.raiz)

    def calcular_propiedades(self, nodo):
        """Recorre el árbol en Post-Orden (hijos primero, luego padre)."""
        if not nodo: return
        self.calcular_propiedades(nodo.hijo_izq)
        self.calcular_propiedades(nodo.hijo_der)
        
        # === REGLAS DEL LIBRO DEL DRAGÓN (y extensiones para + y ?) ===
        if nodo.hijo_izq is None and nodo.hijo_der is None: # Si es Hoja
            if nodo.valor == 'ε':
                nodo.anulable = True
            else:
                nodo.anulable = False
                nodo.primera_pos.add(nodo.id_posicion)
                nodo.ultima_pos.add(nodo.id_posicion)
                
        elif nodo.valor == '|': # Or
            nodo.anulable = nodo.hijo_izq.anulable or nodo.hijo_der.anulable
            nodo.primera_pos = nodo.hijo_izq.primera_pos.union(nodo.hijo_der.primera_pos)
            nodo.ultima_pos = nodo.hijo_izq.ultima_pos.union(nodo.hijo_der.ultima_pos)
            
        elif nodo.valor == '.': # Concatenación
            nodo.anulable = nodo.hijo_izq.anulable and nodo.hijo_der.anulable
            nodo.primera_pos = nodo.hijo_izq.primera_pos.union(nodo.hijo_der.primera_pos) if nodo.hijo_izq.anulable else set(nodo.hijo_izq.primera_pos)
            nodo.ultima_pos = nodo.hijo_der.ultima_pos.union(nodo.hijo_izq.ultima_pos) if nodo.hijo_der.anulable else set(nodo.hijo_der.ultima_pos)
            
            # Cálculo de siguiente_pos
            for i in nodo.hijo_izq.ultima_pos:
                self.siguiente_pos[i].update(nodo.hijo_der.primera_pos)
                
        elif nodo.valor == '*': # Kleene
            nodo.anulable = True
            nodo.primera_pos = set(nodo.hijo_izq.primera_pos)
            nodo.ultima_pos = set(nodo.hijo_izq.ultima_pos)
            # Cálculo de siguiente_pos
            for i in nodo.ultima_pos:
                self.siguiente_pos[i].update(nodo.primera_pos)
                
        elif nodo.valor == '+': # Cerradura Positiva (Agregada para el Lab)
            nodo.anulable = nodo.hijo_izq.anulable
            nodo.primera_pos = set(nodo.hijo_izq.primera_pos)
            nodo.ultima_pos = set(nodo.hijo_izq.ultima_pos)
            # Cálculo de siguiente_pos (Idéntico a Kleene)
            for i in nodo.ultima_pos:
                self.siguiente_pos[i].update(nodo.primera_pos)
                
        elif nodo.valor == '?': # Opcional (Agregada para el Lab)
            nodo.anulable = True
            nodo.primera_pos = set(nodo.hijo_izq.primera_pos)
            nodo.ultima_pos = set(nodo.hijo_izq.ultima_pos)
            # '?' no añade nada a siguiente_pos