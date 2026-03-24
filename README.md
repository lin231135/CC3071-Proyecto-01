# Generador de analizadores léxicos

### Universidad del Valle de Guatemala - Diseño de Lenguajes de Programación



* Cindy Gualim (21226)
* Javier Linares (231135)
* Gadiel Ocaña (231270)

---

Este proyecto implementa un generador de analizadores léxicos desde cero, basado en la especificación YALex. El sistema lee un archivo de reglas léxicas (.yal), construye los autómatas finitos deterministas (AFD) correspondientes utilizando algoritmos fundamentales de la teoría de compiladores, y genera un programa ejecutable capaz de escanear texto plano.

**Nota importante:** El sistema fue diseñado desde cero sin utilizar librerías nativas o externas de expresiones regulares, implementando todo el análisis a través de árboles sintácticos y autómatas.

---

##  Características Principales

* **Pipeline de Compilación Completo:** Cubre desde la lectura y parsing del archivo `.yal`, hasta la generación de código independiente.
* **Interfaz Gráfica (GUI) Moderna:** Entorno tipo IDE desarrollado con CustomTkinter que incluye panel de edición y consola. Utiliza la filosofía *Fail Fast* para resaltar errores léxicos.
* **Algoritmo Maximal Munch:** El escáner generado aplica la estrategia de la coincidencia más larga para extraer el lexema.
* **Visualización de Grafos:** Integración con la librería externa Graphviz para exportar diagramas de transición de alta calidad de los autómatas compilados.

---

##  Fundamentos Teóricos y Algoritmos

El motor de compilación se fundamenta estrictamente en la literatura del "Libro del Dragón" (Aho, Lam, Sethi y Ullman). Implementa los siguientes algoritmos:

* **Algoritmo Shunting Yard (Dijkstra):** Para convertir la expresión de notación infija a postfija respetando la precedencia de operadores.
* **Cálculo de Funciones de Posición:** Recorrido en post-orden sobre el árbol sintáctico para calcular `anulable`, `primera_pos`, `ultima_pos` y la tabla `siguiente_pos`.
* **Construcción Directa de AFD:** Generación directa de los estados del Autómata Finito Determinista utilizando la tabla `siguiente_pos`, evitando construir el AFN de Thompson.
* **Minimización de Estados:** Optimización del autómata reduciendo estados redundantes mediante un algoritmo de particionamiento iterativo.

---

##  Arquitectura del Sistema

El software sigue una arquitectura modular en capas:

* `lector_yalex.py`: Análisis léxico manual del archivo `.yal` y aislamiento de reglas.
* `preprocesador.py`: Acondiciona las expresiones y las convierte a notación postfija.
* `arbol.py`: Construcción del Árbol Sintáctico y cálculo de las cuatro funciones matemáticas.
* `generador_afd.py`: Transformación del árbol sintáctico en un AFD.
* `minimizador.py`: Optimización del AFD agrupando estados equivalentes.
* `generador_codigo.py`: Inyección de la matriz de transiciones en la plantilla ejecutable final (`scanner_generado.py`).

---

##  Casos de Prueba Incluidos

Se diseñaron tres pares de archivos de prueba incrementando progresivamente la complejidad:

* **Baja (`baja.yal`):** Enfocada en operaciones aritméticas elementales y operadores básicos.
* **Media (`media.yal`):** Detección de palabras reservadas, números con decimales y cadenas de texto.
* **Alta (`alta.yal`):** Simula el analizador de un lenguaje tipo C/Java incorporando tipos de datos y operadores lógicos.

---

##  Tecnologías Utilizadas

* Python 3.x
* CustomTkinter (GUI)
* Graphviz (Visualización de Autómatas)






