from modelos.estado import EstadoAFD

def minimizar_afd(estados_afd):
    """
    Implementa el Algoritmo de Minimización de Estados de un AFD (Hopcroft).
    """
    if not estados_afd: return []
    
    # 1. Obtener el alfabeto dinámicamente
    alfabeto = set()
    for e in estados_afd:
        alfabeto.update(e.transiciones.keys())
    alfabeto = sorted(list(alfabeto))
    
    # Mapa rápido para buscar objetos estado por su ID
    mapa_estados = {e.id_estado: e for e in estados_afd}
    id_inicial_original = estados_afd[0].id_estado
    
    # 2. Partición inicial: Separar IDs de estados de aceptación y no aceptación
    aceptacion = {e.id_estado for e in estados_afd if e.es_aceptacion}
    no_aceptacion = {e.id_estado for e in estados_afd if not e.es_aceptacion}
    
    particion = []
    if no_aceptacion: particion.append(no_aceptacion)
    if aceptacion: particion.append(aceptacion)
    
    def obtener_grupo(id_est, particion_actual):
        for i, g in enumerate(particion_actual):
            if id_est in g: return i
        return -1

    # 3. Bucle de partición (agrupar estados equivalentes)
    while True:
        nueva_particion = []
        for grupo in particion:
            subgrupos = {}
            for id_est in grupo:
                estado = mapa_estados[id_est]
                firma = []
                for simb in alfabeto:
                    dest = estado.transiciones.get(simb)
                    if dest:
                        firma.append(obtener_grupo(dest, particion))
                    else:
                        firma.append(-1)
                firma = tuple(firma)
                
                if firma not in subgrupos:
                    subgrupos[firma] = set()
                subgrupos[firma].add(id_est)
            nueva_particion.extend(subgrupos.values())
        
        # Si la partición no cambió, terminamos de dividir
        if len(nueva_particion) == len(particion):
            break
        particion = nueva_particion
        
    # 4. Ordenar para que el grupo con el estado inicial quede de primero
    particion.sort(key=lambda g: 0 if id_inicial_original in g else 1)
    
    # 5. Construir el nuevo AFD Minimizado
    estados_min = []
    mapa_nuevos_ids = {}
    letra = ord('A')
    
    for grupo in particion:
        nuevo_id = chr(letra)
        letra += 1
        posiciones_combinadas = set()
        es_acept = False
        representante_id = list(grupo)[0] 
        representante_obj = mapa_estados[representante_id]
        
        for id_est in grupo:
            est_obj = mapa_estados[id_est]
            posiciones_combinadas.update(est_obj.posiciones)
            if est_obj.es_aceptacion:
                es_acept = True
            mapa_nuevos_ids[id_est] = nuevo_id
            
        nuevo_estado = EstadoAFD(nuevo_id, posiciones_combinadas)
        nuevo_estado.es_aceptacion = es_acept
        nuevo_estado._representante_temp = representante_obj # Guardar temporalmente para copiar transiciones
        estados_min.append(nuevo_estado)
        
    # 6. Reasignar las transiciones hacia los nuevos IDs
    for est in estados_min:
        for simb, dest_original in est._representante_temp.transiciones.items():
            est.transiciones[simb] = mapa_nuevos_ids[dest_original]
            
    return estados_min