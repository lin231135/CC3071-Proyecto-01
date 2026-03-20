# Laboratorio 02: Minimización de AFD

**Universidad Valle de Guatemala**

**Curso:** CC3071 - Diseño de Lenguajes de Programación
**Laboratorio:** 02 - Minimización de Autómatas Finitos Deterministas

---

## Descripción

Implementación del Laboratorio 02: Conversión de expresiones regulares a AFD y minimización de estados.
El proyecto mantiene una estructura modular para el preprocesamiento, generación, simulación y minimización.

- **Preprocesador:** Valida y normaliza la expresión regular, convierte infijo a postfijo.
- **Árbol sintáctico:** Construye el árbol de la expresión regular a partir de postfijo.
- **Generador de AFD:** Genera un AFD directo desde el árbol sintáctico.
- **Simulador:** Evalúa cadenas y determina aceptación/rechazo.
- **Minimizador:** Reduce el AFD a su versión mínima conservando el lenguaje.
- **Interfaz gráfica:** Permite ingresar expresiones, generar AFD, y comparar con versión minimizada.

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
│   ├── minimizador.py           # Minimización de AFD
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

## Requisitos

- Python 3.8 o superior
- pip

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

La aplicación permite:
- Ingresar expresiones regulares
- Generar y visualizar el AFD y su versión minimizada
- Simular cadenas paso a paso
- Ver y comparar estados antes y después de minimización

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
  Minimización
           ↓
 AFD Minimizado
```

---

## Laboratorio 02: Minimización de AFD

[![Video del laboratorio 2](https://img.youtube.com/vi/_9mDtbiSLpc/maxresdefault.jpg)](https://www.youtube.com/watch?v=_9mDtbiSLpc)

Video del Lab 02: https://www.youtube.com/watch?v=_9mDtbiSLpc

### Cambios implementados

- Se agregó `core/minimizador.py`
- Se modificó `gui/app.py` para mostrar minimización y pruebas

### Expresiones y pruebas realizadas

#### Expresión 1: "Ya Mínima"
- Expresión: `(a|b)*abb`
- Pruebas:
  - Acepta: `abaabb`
  - Rechaza: `abba`

#### Expresión 2: "Se Reduce"
- Expresión: `a(c|d)z|b(c|d)z`
- Pruebas:
  - Acepta: `bdz`
  - Rechaza: `abz`

---

## Detalles de Implementación

- El algoritmo maneja correctamente la precedencia de operadores
- La conversión a AFD se realiza sin requerir determinización posterior
- El minimizador encuentra clases equivalentes de estados y genera un AFD mínimo
- La interfaz permite visualizar cada etapa del proceso

---

## Limitaciones Conocidas

- Solo soporta caracteres simples (a-z, 0-9)
- No incluye caracteres especiales expandidos (rangos como `[a-z]`)
- La visualización gráfica requiere que Graphviz esté instalado en el sistema

---