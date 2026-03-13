# Laboratorio 01: Conversión Directa de Expresión Regular a AFD

**Universidad Valle de Guatemala**

**Curso:** CC3071 - Diseño de Lenguajes de Programación
**Laboratorio:** 01 - Conversión Directa de Expresiones Regulares a Autómatas Finitos Deterministas

---

## Descripción

Implementación de un compilador que convierte expresiones regulares directamente en Autómatas Finitos Deterministas (AFD) sin pasar por pasos intermedios. El sistema incluye:

- **Preprocesador:** Validación y normalización de expresiones regulares, conversión de notación infija a postfija
- **Construcción de Árbol Sintáctico:** Representación jerárquica de la expresión regular
- **Generador de AFD:** Implementación del algoritmo de construcción directa de Thompson
- **Simulador:** Evaluación de cadenas sobre el AFD generado
- **Interfaz Gráfica:** Visualización interactiva del árbol sintáctico, AFD y simulación de ejecución

---

## Estructura del Proyecto

```
CC3071-Proyecto-01/
├── main.py                      # Punto de entrada - Inicia la interfaz gráfica
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Configuración de Git
├── README.md                    # Este archivo
│
├── core/                        # Núcleo del compilador
│   ├── preprocesador.py         # Formateo y conversión infijo → postfijo
│   ├── arbol.py                 # Construcción del árbol sintáctico
│   ├── generador_afd.py         # Conversión directa de regex a AFD
│   └── simulador.py             # Motor de simulación de cadenas
│
├── gui/                         # Interfaz gráfica de usuario
│   ├── app.py                   # Aplicación principal (Tkinter/CustomTkinter)
│   └── visualizador.py          # Renderizado de grafos (árbol y AFD)
│
└── modelos/                     # Estructuras de datos
    ├── estado.py                # Definición de estados del AFD
    └── nodo.py                  # Definición de nodos del árbol sintáctico
```

---

## Operadores Soportados

| Operador | Símbolo | Descripción | Ejemplo |
|----------|---------|-------------|---------|
| Unión | `|` | Alternancia | `a|b` |
| Concatenación | Implícita | Secuencia | `ab` |
| Cerradura de Kleene | `*` | Cero o más | `a*` |
| Cerradura Positiva | `+` | Una o más | `a+` |
| Opcional | `?` | Cero o una | `a?` |

---

## Componentes del Sistema

### 1. Preprocesador (`core/preprocesador.py`)
- Formatea y valida expresiones regulares
- Convierte notación infija a postfija usando el algoritmo Shunting Yard
- Maneja parentización y precedencia de operadores

### 2. Árbol Sintáctico (`core/arbol.py`)
- Construye un árbol de sintaxis abstracta (AST) a partir de la notación postfija
- Nodos representan operadores y símbolos terminales
- Permite análisis estructurado de la expresión

### 3. Generador de AFD (`core/generador_afd.py`)
- Aplica el algoritmo de Thompson modificado
- Genera transiciones entre estados basadas en la estructura del árbol
- Produce un AFD completo sin necesidad de determinización posterior

### 4. Simulador (`core/simulador.py`)
- Ejecuta cadenas sobre el AFD generado
- Retorna si la cadena es aceptada o rechazada
- Soporta seguimiento paso a paso de la ejecución

### 5. Interfaz Gráfica (`gui/app.py`, `gui/visualizador.py`)
- Ingreso de expresiones regulares
- Generación y visualización del AFD con Graphviz
- Visualización del árbol sintáctico
- Simulación interactiva de cadenas con ejecución paso a paso

---

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Dependencias

```
customtkinter>=5.0
pillow>=9.0
networkx>=2.6
graphviz>=0.20
```

---

## Ejecución

```bash
python main.py
```

Se abrirá la interfaz gráfica donde es posible:
- Ingresar expresiones regulares
- Generar y visualizar el AFD correspondiente
- Validar la estructura del árbol sintáctico
- Simular la ejecución de cadenas paso a paso

---

## Flujo de Procesamiento

```
Expresión Regular (infija)
           ↓
   Preprocesador
           ↓
Expresión Regular (postfija)
           ↓
    Árbol Sintáctico
           ↓
   Generador de AFD
           ↓
    AFD Completo
           ↓
   Simulador
           ↓
Cadena Aceptada/Rechazada
```

---

## Expresiones de Prueba

[![Vista previa del video](https://img.youtube.com/vi/aTmgs1vn_Z4/maxresdefault.jpg)](https://youtu.be/aTmgs1vn_Z4)

https://youtu.be/aTmgs1vn_Z4?si=jZHxhAb-FJ0jdqgh

El sistema ha sido validado con:

- `(a|b)*abb` - Demuestra unión y cerradura de Kleene
- `0+1?0+` - Demuestra cerradura positiva y opcional
- `(x|y)?z+w*` - Combinación compleja de todos los operadores

---

## Detalles de Implementación

- El algoritmo maneja correctamente la precedencia de operadores
- La conversión a AFD se realiza sin requerir determinización posterior
- La interfaz permite visualizar cada etapa del proceso de compilación
- El código está estructurado para propósitos educativos

---

## Limitaciones Conocidas

- Solo soporta caracteres simples (a-z, 0-9)
- No incluye caracteres especiales expandidos (rangos como `[a-z]`)
- La visualización gráfica requiere que Graphviz esté instalado en el sistema

---
