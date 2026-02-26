# Proyecto Integrador Unidad 1: Escenario Procedural Animado en Blender

Este repositorio contiene el proyecto integrador para la Unidad 1 de Programación para Arte Digital. El proyecto demuestra el uso de la API de Python en Blender (`bpy`) para la generación procedural de geometría y la automatización de animaciones de cámara.

## Descripción del Proyecto

El objetivo es crear un script de Python que, al ejecutarse en Blender, genere automáticamente un escenario 3D y una animación de recorrido. El proyecto se basa en la tarea anterior de "Escenario Procedural" (un pasillo recto con paredes alternas) y le añade complejidad mediante:

1.  **Geometría Curva:** Uso de funciones matemáticas (seno) para curvar el camino.
2.  **Animación Automática:** Generación de fotogramas clave (keyframes) vía código para que una cámara recorra el camino generado suavemente.

### Resultado Visual

*(Si subiste la imagen en el Paso 3, se verá aquí automáticamente)*
![Vista del Escenario Generado](resultado_escenario.png)

---

## Características Técnicas

El script (`generador_escenario_animado.py`) implementa las siguientes funcionalidades:

* **Limpieza de Escena:** Borrado automático de todos los objetos previos antes de iniciar la generación.
* **Generación de Materiales:** Creación procedural de materiales con colores definidos (pared oscura, pared acento naranja, suelo).
* **Uso de Matemáticas (`math.sin`):** La curvatura del pasillo no se modela manualmente, sino que se calcula usando una función sinusoidal para determinar la posición X en función del avance en Y.
* **Lógica Condicional:** Uso de `if i % 2 == 0:` para alternar materiales y altura de las paredes en cada paso del bucle, creando variación visual.
* **Setup de Cámara Avanzado:**
    * Creación de una Cámara y un objeto "Empty" (Objetivo).
    * Aplicación de una restricción (constraint) **'TRACK_TO'** a la cámara, forzándola a mirar siempre al objeto Objetivo.
* **Animación Procedural:** El bucle `for` principal no solo coloca cubos, sino que también inserta `keyframes` de posición para la cámara y su objetivo en la línea de tiempo, creando el recorrido automáticamente.

---

## Requisitos y Ejecución

### Requisitos Software
* Blender 3.0 o superior (Probado en 4.x).

### ¿Cómo ejecutar el script?

1.  Abre Blender.
2.  Ve a la pestaña superior de espacio de trabajo llamada **"Scripting"**.
3.  Haz clic en **"New"** (Nuevo) en el editor de texto para crear un bloque de texto vacío.
4.  Copia el contenido completo del archivo `generador_escenario_animado.py` de este repositorio.
5.  Pega el código en el editor de texto de Blender.
6.  Haz clic en el botón de **"Run Script"** (icono de Play ▶️) en la barra del editor de texto.
7.  Para ver el resultado:
    * Mueve el ratón a la vista 3D.
    * Presiona la tecla `0` (cero) en el teclado numérico para entrar en la vista de cámara.
    * Presiona la **Barra Espaciadora** para reproducir la animación generada.

