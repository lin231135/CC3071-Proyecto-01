import graphviz
from PIL import Image
import os

def generar_imagen_grafo(estados_afd, estado_resaltado=None, color_resaltado='#add8e6'):
    """
    Genera una imagen PNG del autómata. 
    Si se envía un 'estado_resaltado', lo pinta del 'color_resaltado'.
    Por defecto, el color resaltado es celeste (#add8e6).
    """
    dot = graphviz.Digraph(format='png')
    dot.attr(rankdir='LR', bgcolor='transparent') 

    # 1. Dibujar los Nodos (Estados)
    for est in estados_afd:
        shape = 'doublecircle' if est.es_aceptacion else 'circle'
        fillcolor = 'white'
        
        # Si este estado es el paso actual, lo pintamos del color que nos indique el simulador
        if estado_resaltado and est.id_estado == estado_resaltado:
            fillcolor = color_resaltado

        dot.node(est.id_estado, est.id_estado, shape=shape, style='filled', fillcolor=fillcolor)

    # Nodo invisible para la flecha de inicio
    dot.node('inicio', '', shape='none')
    if estados_afd:
        dot.edge('inicio', estados_afd[0].id_estado)

    # 2. Dibujar las Transiciones (Flechas)
    for est in estados_afd:
        for char, dest in est.transiciones.items():
            dot.edge(est.id_estado, dest, label=char)

    # 3. Renderizar a imagen
    nombre_archivo = 'temp_grafo'
    dot.render(nombre_archivo, format='png', cleanup=True)
    
    img = Image.open(f"{nombre_archivo}.png")
    return img