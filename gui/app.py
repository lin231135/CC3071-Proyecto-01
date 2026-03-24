import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import os

# Importaciones del Core (Asegúrate de que estas rutas coincidan con tu proyecto)
from core.preprocesador import formatear_regex, infijo_a_postfijo
from core.arbol import ArbolSintactico
from core.generador_afd import generar_afd
from core.minimizador import minimizar_afd
from gui.visualizador import generar_imagen_grafo

class InterfazPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Analizadores Léxicos - Proyecto 01")
        self.geometry("1280x720")
        
        # --- LAYOUT PRINCIPAL (Grid de 2 columnas: Sidebar y Contenido) ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Variables del core para Laboratorios
        self.afd_original = None
        self.afd_minimizado = None
        self.afd_actual = None
        self.viendo_minimizado = False
        self.cadena_simulacion = ""
        self.indice_simulacion = 0
        self.estado_simulacion = None
        self.mapa_estados = {}
        
        # Variables para Proyecto YALex
        self.ruta_archivo_yal = None
        self.ruta_archivo_txt = None

        self.crear_sidebar()
        
        # Contenedores de las vistas
        self.frame_vista_labs = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_vista_proyecto = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        self.construir_vista_labs()
        self.construir_vista_proyecto()

        # Iniciar en la vista del proyecto por defecto
        self.mostrar_vista_proyecto()

    # ==========================================
    # SIDEBAR (Navegación)
    # ==========================================
    def crear_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        lbl_logo = ctk.CTkLabel(self.sidebar_frame, text="Compiladores\nLexer Gen", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_nav_proyecto = ctk.CTkButton(self.sidebar_frame, text="💻 Proyecto YALex", command=self.mostrar_vista_proyecto)
        self.btn_nav_proyecto.grid(row=1, column=0, padx=20, pady=10)

        self.btn_nav_labs = ctk.CTkButton(self.sidebar_frame, text="🧪 Laboratorios (Regex)", command=self.mostrar_vista_labs, fg_color="transparent", border_width=1, text_color=("gray10", "#DCE4EE"))
        self.btn_nav_labs.grid(row=2, column=0, padx=20, pady=10)

    def mostrar_vista_proyecto(self):
        self.frame_vista_labs.grid_forget()
        self.frame_vista_proyecto.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.btn_nav_proyecto.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.btn_nav_labs.configure(fg_color="transparent")

    def mostrar_vista_labs(self):
        self.frame_vista_proyecto.grid_forget()
        self.frame_vista_labs.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.btn_nav_labs.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.btn_nav_proyecto.configure(fg_color="transparent")

    # ==========================================
    # VISTA 2: PROYECTO YALEX (Estilo VS Code)
    # ==========================================
    def construir_vista_proyecto(self):
        self.frame_vista_proyecto.grid_rowconfigure(1, weight=1)
        self.frame_vista_proyecto.grid_columnconfigure(0, weight=1)

        # --- TOOLBAR SUPERIOR ---
        toolbar = ctk.CTkFrame(self.frame_vista_proyecto, height=50)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        btn_cargar_yal = ctk.CTkButton(toolbar, text="📂 Cargar .yal", command=self.cargar_archivo_yal)
        btn_cargar_yal.pack(side="left", padx=10, pady=10)
        
        self.lbl_estado_yal = ctk.CTkLabel(toolbar, text="Ningún archivo YALex cargado", text_color="gray")
        self.lbl_estado_yal.pack(side="left", padx=10, pady=10)
        
        btn_ver_automata = ctk.CTkButton(toolbar, text="👁 Ver Autómata YALex", fg_color="#2b8256", hover_color="#1e5c3d", command=self.mostrar_automata_yalex)
        btn_ver_automata.pack(side="right", padx=10, pady=10)

        # --- ÁREA DE TRABAJO (Split View) ---
        workspace = ctk.CTkFrame(self.frame_vista_proyecto, fg_color="transparent")
        workspace.grid(row=1, column=0, sticky="nsew")
        workspace.grid_rowconfigure(0, weight=1)
        workspace.grid_columnconfigure(0, weight=2) # Editor de código
        workspace.grid_columnconfigure(1, weight=1) # Consola de tokens

        # Panel Izquierdo: Editor de Código
        panel_editor = ctk.CTkFrame(workspace)
        panel_editor.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        header_editor = ctk.CTkFrame(panel_editor, fg_color="transparent")
        header_editor.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(header_editor, text="📝 Editor (Archivo de Prueba)", font=("Arial", 14, "bold")).pack(side="left")
        
        btn_ejecutar = ctk.CTkButton(header_editor, text="▶ Ejecutar Lexer", width=120, fg_color="#b85a14", hover_color="#91450e", command=self.ejecutar_lexer_generado)
        btn_ejecutar.pack(side="right")
        
        self.editor_texto = ctk.CTkTextbox(panel_editor, font=("Consolas", 14), wrap="none")
        self.editor_texto.pack(expand=True, fill="both", padx=10, pady=10)

        # Panel Derecho: Consola de Salida
        panel_consola = ctk.CTkFrame(workspace)
        panel_consola.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        ctk.CTkLabel(panel_consola, text="🖥 Terminal / Tokens", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.consola_salida = ctk.CTkTextbox(panel_consola, font=("Consolas", 13), fg_color="#1e1e1e", text_color="#00ff00", wrap="word")
        self.consola_salida.pack(expand=True, fill="both", padx=10, pady=10)
        self.consola_salida.insert("0.0", "Carga un archivo .yal para generar el lexer...\n")
        self.consola_salida.configure(state="disabled")

    # --- LÓGICA DE LA VISTA PROYECTO ---
    def cargar_archivo_yal(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo YALex", filetypes=[("Archivos YAL", "*.yal"), ("Todos", "*.*")])
        if ruta:
            self.ruta_archivo_yal = ruta
            nombre_archivo = os.path.basename(ruta)
            self.lbl_estado_yal.configure(text=f"YALex Cargado: {nombre_archivo}", text_color="white")
            self.escribir_consola(f"[SISTEMA] Archivo cargado: {nombre_archivo}\n[SISTEMA] Compilando YALex y generando AFD gigante...\n")
            
            try:
                # Importaciones dinámicas de los módulos YALex
                from core.lector_yalex import LectorYALex
                from core.generador_codigo import generar_scanner_independiente
                
                self.lector = LectorYALex(ruta)
                
                # Unir todas las reglas del YALex en una super expresión regular separada por OR (|)
                regex_combinada = ""
                acciones = []
                
                for i, (regex_regla, accion) in enumerate(self.lector.rules):
                    regla_fmt = formatear_regex(regex_regla) 
                    regex_combinada += f"({regla_fmt})"
                    if i < len(self.lector.rules) - 1:
                        regex_combinada += "|"
                    acciones.append(accion)
                    
                regex_post = infijo_a_postfijo(regex_combinada)
                arbol = ArbolSintactico(regex_post, acciones)
                
                self.afd_proyecto_original = generar_afd(arbol)
                self.afd_proyecto_min = minimizar_afd(self.afd_proyecto_original)
                
                # Generar el archivo python independiente
                self.ruta_lexer = generar_scanner_independiente(self.afd_proyecto_min, self.lector.rules)
                self.escribir_consola(f"[ÉXITO] Analizador léxico 100% independiente generado en: {self.ruta_lexer}\n")
                
            except Exception as e:
                self.escribir_consola(f"[ERROR] Hubo un problema compilando el YALex:\n{str(e)}\n")

    def ejecutar_lexer_generado(self):
        codigo_fuente = self.editor_texto.get("1.0", "end-1c")
        if not self.ruta_archivo_yal:
            messagebox.showwarning("Advertencia", "Primero debes cargar un archivo .yal para generar el Lexer.")
            return
        if not codigo_fuente.strip():
            messagebox.showwarning("Advertencia", "El editor está vacío. Escribe código para analizar.")
            return
            
        self.escribir_consola("\n[EJECUTANDO LEXER INDEPENDIENTE]...\n")
        try:
            import importlib.util
            import sys
            
            # Forzamos la recarga del módulo por si generaste un lexer nuevo sin cerrar la app
            nombre_modulo = "scanner_generado"
            if nombre_modulo in sys.modules:
                del sys.modules[nombre_modulo]
                
            spec = importlib.util.spec_from_file_location(nombre_modulo, self.ruta_lexer)
            scanner = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(scanner)
            
            tokens = scanner.escanear(codigo_fuente)
            
            # --- AQUÍ CONFIGURAMOS EL COLOR ROJO ---
            self.consola_salida.tag_config("error", foreground="#ff4d4d")
            
            for lexema, accion in tokens:
                if "ERROR" in accion:
                    # Si es error, le pasamos la etiqueta "error" para que se pinte de rojo
                    self.escribir_consola(f"Lexema: '{lexema}' \t-> Acción: {accion}\n", "error")
                else:
                    # Si es normal, se imprime en su verde por defecto
                    self.escribir_consola(f"Lexema: '{lexema}' \t-> Acción: {accion}\n")
                    
        except Exception as e:
            self.escribir_consola(f"[ERROR DE EJECUCIÓN DEL LEXER]\n{str(e)}\n", "error")

    def mostrar_automata_yalex(self):
        if not hasattr(self, 'afd_proyecto_min') or not self.afd_proyecto_min:
            messagebox.showwarning("Advertencia", "Primero debes cargar un archivo .yal para generar el autómata.")
            return
        
        self.escribir_consola("\n[SISTEMA] Generando diagrama del autómata completo... (Esto puede tardar unos segundos)\n")
        try:
            # Genera la imagen y la abre en el visor de fotos predeterminado de Windows/Mac
            img_pil = generar_imagen_grafo(self.afd_proyecto_min)
            img_pil.show() 
            self.escribir_consola("[SISTEMA] Diagrama abierto en el visor de imágenes del sistema.\n")
        except Exception as e:
            self.escribir_consola(f"[ERROR] No se pudo renderizar el diagrama: {str(e)}\n")

    def escribir_consola(self, texto, tag=None):
        self.consola_salida.configure(state="normal")
        if tag:
            self.consola_salida.insert("end", texto, tag)
        else:
            self.consola_salida.insert("end", texto)
        self.consola_salida.configure(state="disabled")
        self.consola_salida.yview("end")

    # ==========================================
    # VISTA 1: LABORATORIOS (Lo que ya existía)
    # ==========================================
    def construir_vista_labs(self):
        self.frame_vista_labs.grid_rowconfigure(0, weight=1)
        self.frame_vista_labs.grid_columnconfigure(0, weight=1)
        self.frame_vista_labs.grid_columnconfigure(1, weight=2)

        # Copia exacta de tu código anterior empaquetado en este frame
        frame_izq = ctk.CTkFrame(self.frame_vista_labs)
        frame_izq.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(frame_izq, text="1. Expresión Regular", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        self.entry_regex = ctk.CTkEntry(frame_izq, placeholder_text="Ej: (a|b)*abb", width=250)
        self.entry_regex.pack(pady=5)
        ctk.CTkButton(frame_izq, text="Generar AFD", command=self.procesar_regex_labs).pack(pady=10)

        self.lbl_comparacion = ctk.CTkLabel(frame_izq, text="Estadísticas: -", font=("Arial", 12))
        self.lbl_comparacion.pack(pady=(0, 5))
        self.btn_toggle = ctk.CTkButton(frame_izq, text="Ver AFD Minimizado", command=self.toggle_afd, fg_color="#2b8256", hover_color="#1e5c3d")
        self.btn_toggle.pack(pady=5)

        ctk.CTkLabel(frame_izq, text="Tabla de Transiciones", font=("Arial", 14, "bold")).pack(pady=(10, 5))
        self.textbox_tabla = ctk.CTkTextbox(frame_izq, height=180, width=320, font=("Courier", 13), wrap="none")
        self.textbox_tabla.pack(pady=5, fill="x", padx=20)

        ctk.CTkLabel(frame_izq, text="2. Simulación de Cadenas", font=("Arial", 16, "bold")).pack(pady=(15, 5))
        self.entry_cadena = ctk.CTkEntry(frame_izq, placeholder_text="Ej: abaabb", width=250)
        self.entry_cadena.pack(pady=5)
        
        frame_botones = ctk.CTkFrame(frame_izq, fg_color="transparent")
        frame_botones.pack(pady=5)
        ctk.CTkButton(frame_botones, text="Iniciar", width=80, command=self.iniciar_simulacion).grid(row=0, column=0, padx=5)
        ctk.CTkButton(frame_botones, text="Paso a Paso", width=100, command=self.paso_a_paso).grid(row=0, column=1, padx=5)

        self.lbl_resultado = ctk.CTkLabel(frame_izq, text="Esperando simulación...", font=("Arial", 14), wraplength=300)
        self.lbl_resultado.pack(pady=10)

        self.frame_der = ctk.CTkFrame(self.frame_vista_labs)
        self.frame_der.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_der.pack_propagate(False)
        self.lbl_titulo_grafo = ctk.CTkLabel(self.frame_der, text="Diagrama de Transición (ORIGINAL)", font=("Arial", 16, "bold"))
        self.lbl_titulo_grafo.pack(pady=10)
        self.lbl_imagen = ctk.CTkLabel(self.frame_der, text="Grafo.")
        self.lbl_imagen.pack(expand=True, fill="both")

    # --- LÓGICA DE LABORATORIOS (Intacta) ---
    def procesar_regex_labs(self):
        regex_raw = self.entry_regex.get()
        if not regex_raw: return
        regex = regex_raw.replace(" ", "")
        
        regex_format = formatear_regex(regex)
        regex_post = infijo_a_postfijo(regex_format)
        arbol = ArbolSintactico(regex_post)
        
        self.afd_original = generar_afd(arbol)
        self.afd_minimizado = minimizar_afd(self.afd_original)
        
        estados_orig = len(self.afd_original)
        trans_orig = sum(len(e.transiciones) for e in self.afd_original)
        estados_min = len(self.afd_minimizado)
        trans_min = sum(len(e.transiciones) for e in self.afd_minimizado)
        
        self.lbl_comparacion.configure(text=f"Original: {estados_orig} est. | {trans_orig} trans.\nMinimizado: {estados_min} est. | {trans_min} trans.", text_color="#f39c12")
        self.viendo_minimizado = False
        self.btn_toggle.configure(text="Cambiar a AFD Minimizado")
        self.lbl_titulo_grafo.configure(text="Diagrama de Transición de Estados (ORIGINAL)")
        self.afd_actual = self.afd_original
        
        self.actualizar_vista_labs()
        self.lbl_resultado.configure(text="AFD Generado Exitosamente", text_color="white")

    def toggle_afd(self):
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
        self.actualizar_vista_labs()

    def actualizar_vista_labs(self):
        self.mapa_estados = {est.id_estado: est for est in self.afd_actual}
        self.textbox_tabla.delete("1.0", ctk.END)
        alfabeto = set()
        for est in self.afd_actual: alfabeto.update(est.transiciones.keys())
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
        self.actualizar_grafo_labs()

    def actualizar_grafo_labs(self, estado_resaltado=None, color='#add8e6'):
        if not self.afd_actual: return
        img_pil = generar_imagen_grafo(self.afd_actual, estado_resaltado, color)
        img_pil.thumbnail((600, 450)) 
        img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=img_pil.size)
        self.lbl_imagen.configure(image=img_ctk, text="")
        self.lbl_imagen.image = img_ctk

    def iniciar_simulacion(self):
        if not self.afd_actual: return
        self.cadena_simulacion = self.entry_cadena.get()
        self.indice_simulacion = 0
        self.estado_simulacion = self.afd_actual[0] 
        self.lbl_resultado.configure(text=f"Simulando: Carácter '{self.cadena_simulacion[0]}'..." if self.cadena_simulacion else "Cadena vacía", text_color="white")
        self.actualizar_grafo_labs(self.estado_simulacion.id_estado, '#add8e6')

    def paso_a_paso(self):
        if not self.estado_simulacion: return
        if self.indice_simulacion >= len(self.cadena_simulacion):
            if self.estado_simulacion.es_aceptacion:
                self.lbl_resultado.configure(text="[ACEPTADO] La cadena pertenece al lenguaje", text_color="#a8e6cf")
                self.actualizar_grafo_labs(self.estado_simulacion.id_estado, '#a8e6cf') 
            else:
                self.lbl_resultado.configure(text="[RECHAZADO] Terminó en estado de no aceptación", text_color="#ff8b94")
                self.actualizar_grafo_labs(self.estado_simulacion.id_estado, '#ff8b94') 
            self.estado_simulacion = None 
            return

        char_actual = self.cadena_simulacion[self.indice_simulacion]
        if char_actual in self.estado_simulacion.transiciones:
            id_siguiente = self.estado_simulacion.transiciones[char_actual]
            self.estado_simulacion = self.mapa_estados[id_siguiente]
            self.indice_simulacion += 1
            self.actualizar_grafo_labs(self.estado_simulacion.id_estado, '#add8e6')
            
            if self.indice_simulacion < len(self.cadena_simulacion):
                self.lbl_resultado.configure(text=f"Avanzó con '{char_actual}'. Siguiente: '{self.cadena_simulacion[self.indice_simulacion]}'")
            else:
                self.lbl_resultado.configure(text="Fin de cadena. Presiona 'Paso a Paso' para ver el resultado.")
        else:
            self.lbl_resultado.configure(text=f"[RECHAZADO] No hay transición para el carácter '{char_actual}'", text_color="#ff8b94")
            self.actualizar_grafo_labs(self.estado_simulacion.id_estado, '#ff8b94')
            self.estado_simulacion = None 

if __name__ == "__main__":
    app = InterfazPrincipal()
    app.mainloop()