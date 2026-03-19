import customtkinter as ctk
from PIL import ImageTk
from core.preprocesador import formatear_regex, infijo_a_postfijo
from core.arbol import ArbolSintactico
from core.generador_afd import generar_afd
from core.minimizador import minimizar_afd
from gui.visualizador import generar_imagen_grafo

class InterfazLaboratorio(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Analizadores Léxicos - Laboratorio 01 y 02")
        self.geometry("1100x680")
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=2) 
        self.grid_rowconfigure(0, weight=1)
        
        self.afd_original = None
        self.afd_minimizado = None
        self.afd_actual = None
        self.viendo_minimizado = False
        self.cadena_simulacion = ""
        self.indice_simulacion = 0
        self.estado_simulacion = None
        self.mapa_estados = {}

        self.construir_columna_izquierda()
        self.construir_columna_derecha()
        self.construir_boton_ayuda()

    def construir_boton_ayuda(self):
        btn_help = ctk.CTkButton(self, text="?", width=35, height=35, corner_radius=17, 
                                 font=("Arial", 18, "bold"), fg_color="#4a4a4a", 
                                 hover_color="#2c2c2c", command=self.mostrar_ayuda)
        btn_help.place(relx=0.96, rely=0.03)

    def construir_columna_izquierda(self):
        frame_izq = ctk.CTkFrame(self)
        frame_izq.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # --- EXPRESIÓN REGULAR ---
        ctk.CTkLabel(frame_izq, text="1. Expresión Regular", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        self.entry_regex = ctk.CTkEntry(frame_izq, placeholder_text="Ej: (a|b)*abb", width=250)
        self.entry_regex.pack(pady=5)
        
        btn_generar = ctk.CTkButton(frame_izq, text="Generar AFD", command=self.procesar_regex)
        btn_generar.pack(pady=10)

        # --- SECCIÓN NUEVA: ESTADÍSTICAS Y MINIMIZACIÓN ---
        self.lbl_comparacion = ctk.CTkLabel(frame_izq, text="Estadísticas: -", font=("Arial", 12))
        self.lbl_comparacion.pack(pady=(0, 5))
        
        self.btn_toggle = ctk.CTkButton(frame_izq, text="Ver AFD Minimizado", command=self.toggle_afd, 
                                        fg_color="#2b8256", hover_color="#1e5c3d")
        self.btn_toggle.pack(pady=5)

        # --- TABLA DE TRANSICIONES ---
        ctk.CTkLabel(frame_izq, text="Tabla de Transiciones", font=("Arial", 14, "bold")).pack(pady=(10, 5))
        self.textbox_tabla = ctk.CTkTextbox(frame_izq, height=180, width=320, font=("Courier", 13), wrap="none")
        self.textbox_tabla.pack(pady=5, fill="x", padx=20)

        # --- SIMULACIÓN ---
        ctk.CTkLabel(frame_izq, text="2. Simulación de Cadenas", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        self.entry_cadena = ctk.CTkEntry(frame_izq, placeholder_text="Ej: abaabb", width=250)
        self.entry_cadena.pack(pady=5)
        
        frame_botones = ctk.CTkFrame(frame_izq, fg_color="transparent")
        frame_botones.pack(pady=5)
        
        ctk.CTkButton(frame_botones, text="Iniciar", width=80, command=self.iniciar_simulacion).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="Paso a Paso", width=100, command=self.paso_a_paso).grid(row=0, column=1, padx=5)

        self.lbl_resultado = ctk.CTkLabel(frame_izq, text="Esperando simulación...", font=("Arial", 14), wraplength=300)
        self.lbl_resultado.pack(pady=10)

    def construir_columna_derecha(self):
        self.frame_der = ctk.CTkFrame(self)
        self.frame_der.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_der.pack_propagate(False)
        
        self.lbl_titulo_grafo = ctk.CTkLabel(self.frame_der, text="Diagrama de Transición de Estados (ORIGINAL)", font=("Arial", 16, "bold"))
        self.lbl_titulo_grafo.pack(pady=10)
        
        self.lbl_imagen = ctk.CTkLabel(self.frame_der, text="Ingrese una expresión regular para generar el grafo.")
        self.lbl_imagen.pack(expand=True, fill="both")

    def mostrar_ayuda(self):
        ventana_ayuda = ctk.CTkToplevel(self)
        ventana_ayuda.title("Guía Rápida")
        ventana_ayuda.geometry("450x350")
        ventana_ayuda.attributes("-topmost", True) 

        texto = (
            " GUÍA DE USO - SIMULADOR Y MINIMIZADOR\n\n"
            "1. Crear el Autómata:\n"
            "• Escribe una expresión regular y presiona 'Generar AFD'.\n"
            "• Observa la comparación de estados en la pantalla.\n"
            "• Presiona 'Ver AFD Minimizado' para alternar la vista.\n\n"
            "2. Validar una Cadena:\n"
            "• La simulación recorrerá el autómata que estés visualizando en ese momento (Original o Minimizado).\n"
            "• Presiona 'Iniciar' y luego 'Paso a Paso'.\n\n"
            "3. Colores:\n"
            "• Celeste: Recorriendo la cadena.\n"
            "• Verde: Cadena ACEPTADA.\n"
            "• ojo: Cadena RECHAZADA."
        )

        lbl_ayuda = ctk.CTkLabel(ventana_ayuda, text=texto, font=("Arial", 14), justify="left", wraplength=400)
        lbl_ayuda.pack(padx=20, pady=20)
        ctk.CTkButton(ventana_ayuda, text="¡Entendido!", command=ventana_ayuda.destroy).pack(pady=10)

    def procesar_regex(self):
        regex = self.entry_regex.get()
        if not regex: return

        regex_format = formatear_regex(regex)
        regex_post = infijo_a_postfijo(regex_format)
        arbol = ArbolSintactico(regex_post)
        
        # Generar ambos autómatas
        self.afd_original = generar_afd(arbol)
        self.afd_minimizado = minimizar_afd(self.afd_original)
        
        # Calcular estadísticas para la rúbrica
        estados_orig = len(self.afd_original)
        trans_orig = sum(len(e.transiciones) for e in self.afd_original)
        estados_min = len(self.afd_minimizado)
        trans_min = sum(len(e.transiciones) for e in self.afd_minimizado)
        
        self.lbl_comparacion.configure(text=f"Original: {estados_orig} est. | {trans_orig} trans.\nMinimizado: {estados_min} est. | {trans_min} trans.", text_color="#f39c12")
        
        # Vista inicial
        self.viendo_minimizado = False
        self.btn_toggle.configure(text="Cambiar a AFD Minimizado")
        self.lbl_titulo_grafo.configure(text="Diagrama de Transición de Estados (ORIGINAL)")
        self.afd_actual = self.afd_original
        
        self.actualizar_vista()
        self.lbl_resultado.configure(text="AFD Generado Exitosamente", text_color="white")

    def toggle_afd(self):
        """Alterna dinámicamente entre el AFD original y el minimizado."""
        if not self.afd_original: return
        
        if self.viendo_minimizado:
            self.afd_actual = self.afd_original
            self.btn_toggle.configure(text="Cambiar a AFD Minimizado")
            self.lbl_titulo_grafo.configure(text="Diagrama de Transición de Estados (ORIGINAL)")
            self.viendo_minimizado = False
        else:
            self.afd_actual = self.afd_minimizado
            self.btn_toggle.configure(text="Cambiar a AFD Original")
            self.lbl_titulo_grafo.configure(text="Diagrama de Transición de Estados (MINIMIZADO)")
            self.viendo_minimizado = True
            
        self.actualizar_vista()

    def actualizar_vista(self):
        self.mapa_estados = {est.id_estado: est for est in self.afd_actual}
        
        self.textbox_tabla.delete("1.0", ctk.END)
        alfabeto = set()
        for est in self.afd_actual:
            alfabeto.update(est.transiciones.keys())
        alfabeto = sorted(list(alfabeto)) 

        encabezado = f"{'Estado':<8} | " + " | ".join([f"{simb:<3}" for simb in alfabeto]) + " | Aceptación"
        separador = "-" * len(encabezado)
        
        self.textbox_tabla.insert(ctk.END, encabezado + "\n")
        self.textbox_tabla.insert(ctk.END, separador + "\n")

        for est in self.afd_actual:
            fila = f"  {est.id_estado:<6} | "
            for simb in alfabeto:
                destino = est.transiciones.get(simb, "-") 
                fila += f"{destino:<3} | "
            acepta = "Sí" if est.es_aceptacion else "No"
            fila += f"  {acepta}"
            self.textbox_tabla.insert(ctk.END, fila + "\n")

        self.actualizar_grafo()

    def actualizar_grafo(self, estado_resaltado=None, color='#add8e6'):
        if not self.afd_actual: return
        img_pil = generar_imagen_grafo(self.afd_actual, estado_resaltado, color)
        img_pil.thumbnail((700, 500)) 
        img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=img_pil.size)
        self.lbl_imagen.configure(image=img_ctk, text="")
        self.lbl_imagen.image = img_ctk

    def iniciar_simulacion(self):
        if not self.afd_actual: return
        self.cadena_simulacion = self.entry_cadena.get()
        self.indice_simulacion = 0
        self.estado_simulacion = self.afd_actual[0] 
        self.lbl_resultado.configure(text=f"Simulando: Carácter '{self.cadena_simulacion[0]}'..." if self.cadena_simulacion else "Cadena vacía", text_color="white")
        self.actualizar_grafo(self.estado_simulacion.id_estado, '#add8e6')

    def paso_a_paso(self):
        if not self.estado_simulacion: return

        if self.indice_simulacion >= len(self.cadena_simulacion):
            if self.estado_simulacion.es_aceptacion:
                self.lbl_resultado.configure(text="[ACEPTADO] La cadena pertenece al lenguaje", text_color="#a8e6cf")
                self.actualizar_grafo(self.estado_simulacion.id_estado, '#a8e6cf') 
            else:
                self.lbl_resultado.configure(text="[RECHAZADO] Terminó en estado de no aceptación", text_color="#ff8b94")
                self.actualizar_grafo(self.estado_simulacion.id_estado, '#ff8b94') 
            self.estado_simulacion = None 
            return

        char_actual = self.cadena_simulacion[self.indice_simulacion]
        
        if char_actual in self.estado_simulacion.transiciones:
            id_siguiente = self.estado_simulacion.transiciones[char_actual]
            self.estado_simulacion = self.mapa_estados[id_siguiente]
            self.indice_simulacion += 1
            self.actualizar_grafo(self.estado_simulacion.id_estado, '#add8e6')
            
            if self.indice_simulacion < len(self.cadena_simulacion):
                self.lbl_resultado.configure(text=f"Avanzó con '{char_actual}'. Siguiente: '{self.cadena_simulacion[self.indice_simulacion]}'")
            else:
                self.lbl_resultado.configure(text="Fin de cadena. Presiona 'Paso a Paso' para ver el resultado.")
        else:
            self.lbl_resultado.configure(text=f"[RECHAZADO] No hay transición para el carácter '{char_actual}'", text_color="#ff8b94")
            self.actualizar_grafo(self.estado_simulacion.id_estado, '#ff8b94')
            self.estado_simulacion = None