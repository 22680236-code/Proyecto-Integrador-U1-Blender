import bpy
import math
import random

# ==============================================================================
# PROYECTO INTEGRADOR U1: Generador de Escenario Procedural Animado
# ==============================================================================
# Descripción:
# Este script genera proceduralmente un pasillo curvo utilizando funciones seno.
# Crea paredes con materiales alternados y variaciones de altura.
# Finalmente, configura una cámara y un objetivo (Empty) y los anima automáticamente
# para recorrer el camino generado.
# ==============================================================================


def crear_material_simple(nombre, color_rgb):
    """
    Función auxiliar para crear materiales básicos.
    Si el material ya existe, lo elimina para asegurar una creación limpia.
    """
    if nombre in bpy.data.materials:
        bpy.data.materials.remove(bpy.data.materials[nombre])
        
    mat = bpy.data.materials.new(name=nombre)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (*color_rgb, 1.0) # Añade Alpha=1.0
    return mat

def generar_y_animar():
    # --- 1. LIMPIEZA DE ESCENA ---
    # Aseguramos estar en modo objeto antes de seleccionar y borrar
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # --- 2. DEFINICIÓN DE MATERIALES ---
    mat_pared_oscura = crear_material_simple("ParedOscura", (0.1, 0.1, 0.15)) # Gris azulado oscuro
    mat_pared_acento = crear_material_simple("ParedAcento", (0.85, 0.25, 0.05)) # Naranja intenso
    mat_suelo = crear_material_simple("SueloAsfalto", (0.25, 0.25, 0.3))      # Gris medio

    # --- 3. PARÁMETROS DE CONFIGURACIÓN ---
    num_pasos = 120           # Longitud total del recorrido en segmentos
    ancho_mitad = 4.5         # Distancia del centro a la pared
    avance_z = 2.0            # Distancia entre cada segmento (avance hacia adelante)
    
    # Parámetros de la curva (Matemáticos)
    amplitud_curva = 18.0     # Qué tan ancha es la oscilación lateral (Eje X)
    frecuencia_curva = 0.06   # Velocidad de la oscilación (menor = curvas más suaves)

    # Parámetros de animación
    frames_por_paso = 5       # Velocidad del recorrido (menor = más rápido)
    altura_camara = 2.2       # Altura de los "ojos" del espectador

    # --- 4. CONFIGURACIÓN INICIAL DE CÁMARA Y OBJETIVO ---
    
    # Crear el objetivo (Empty) que la cámara mirará
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, altura_camara))
    objetivo = bpy.context.active_object
    objetivo.name = "ObjetivoCamara"

    # Crear la cámara
    bpy.ops.object.camera_add(location=(0, -5, altura_camara))
    camara = bpy.context.active_object
    camara.name = "CamaraPrincipal"
    bpy.context.scene.camera = camara # Establecer como cámara activa

    # Aplicar restricción "Track To" para que la cámara siempre mire al objetivo
    restriccion = camara.constraints.new(type='TRACK_TO')
    restriccion.target = objetivo
    restriccion.track_axis = 'TRACK_NEGATIVE_Z' # La cámara mira hacia su eje -Z local
    restriccion.up_axis = 'UP_Y'                # El eje Y define "arriba"

    # Ajustar la duración total de la animación en Blender
    bpy.context.scene.frame_end = num_pasos * frames_por_paso

    # --- 5. BUCLE PRINCIPAL DE GENERACIÓN Y ANIMACIÓN ---
    for i in range(num_pasos):
        
        # A. CÁLCULOS MATEMÁTICOS (El corazón de la curva)
        pos_y_actual = i * avance_z
        # Fórmula del seno para determinar el desplazamiento lateral en X
        centro_x_actual = amplitud_curva * math.sin(pos_y_actual * frecuencia_curva)
        altura_base = 1.0

        # B. GENERACIÓN GEOMÉTRICA (Procedural)
        
        # -- Suelo (Segmento actual) --
        bpy.ops.mesh.primitive_cube_add(location=(centro_x_actual, pos_y_actual, 0.0))
        suelo = bpy.context.active_object
        suelo.data.materials.append(mat_suelo)
        # Escalamos para cubrir el ancho del pasillo
        suelo.scale = (ancho_mitad + 1.5, 1.0, 0.1) 

        # -- Pared Izquierda --
        bpy.ops.mesh.primitive_cube_add(location=(centro_x_actual - ancho_mitad, pos_y_actual, altura_base))
        pared_izq = bpy.context.active_object
        
        # Lógica de alternancia (basada en si 'i' es par o impar)
        if i % 2 == 0:
            pared_izq.data.materials.append(mat_pared_oscura)
        else:
            pared_izq.data.materials.append(mat_pared_acento)
            # Variación procedural: hacer la pared acento más alta
            pared_izq.scale.z = 1.6
            pared_izq.location.z = altura_base * 1.6

        # -- Pared Derecha (Siempre oscura en este diseño) --
        bpy.ops.mesh.primitive_cube_add(location=(centro_x_actual + ancho_mitad, pos_y_actual, altura_base))
        pared_der = bpy.context.active_object
        pared_der.data.materials.append(mat_pared_oscura)
        
        # C. ANIMACIÓN (Inserción de Keyframes)
        
        frame_key = i * frames_por_paso
        
        # 1. Animar Cámara: Se coloca en la posición calculada actual
        camara.location = (centro_x_actual, pos_y_actual, altura_camara)
        camara.keyframe_insert(data_path="location", frame=frame_key)
        
        # 2. Animar Objetivo: Se calcula una posición futura para guiar la mirada
        pasos_adelante = i + 5 # Mira 5 segmentos hacia adelante
        pos_y_futura = pasos_adelante * avance_z
        # ¡Importante! El objetivo también debe seguir la curva seno futura
        centro_x_futuro = amplitud_curva * math.sin(pos_y_futura * frecuencia_curva)
        
        objetivo.location = (centro_x_futuro, pos_y_futura, altura_camara)
        objetivo.keyframe_insert(data_path="location", frame=frame_key)

    print("Generación procedural y animación completadas.")

# Ejecutar la función principal
generar_y_animar()
