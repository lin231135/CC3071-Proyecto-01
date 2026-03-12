class EstadoAFD:
    """Representa un estado del Autómata Finito Determinista (AFD)."""
    def __init__(self, id_estado, posiciones):
        self.id_estado = id_estado          # Ej: 'A', 'B', 'C'
        self.posiciones = set(posiciones)   # Conjunto de ID de posiciones del árbol
        self.es_aceptacion = False          # ¿Contiene el símbolo #?
        self.transiciones = {}              # Diccionario: {simbolo: id_estado_destino}