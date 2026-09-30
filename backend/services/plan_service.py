from data.ejercicios import rutinas_elite
from utils.logger import obtener_logger
from backend.services.nutrition_service import generar_menu_nutricional, formatear_opcion

logger = obtener_logger("PlanService")


def generar_menu_dinamico(p_g_total, c_g_total, g_g_total, num_comidas,
                         num_opciones, dieta_tipo, pais,
                         restricciones_alimentarias="") -> tuple[dict, dict]:
    """Adaptador compatible con la interfaz/PDF: opciones de texto y compras."""
    menus, compras = generar_menu_nutricional(
        p_g_total, c_g_total, g_g_total, num_comidas, num_opciones,
        dieta_tipo, pais, restricciones_alimentarias)
    return {nombre: [formatear_opcion(op, i + 1) for i, op in enumerate(opciones)]
            for nombre, opciones in menus.items()}, compras


def generar_rutina_entrenamiento(
    tipo_entreno: str, 
    nivel_experiencia: str, 
    dias_entreno: int, 
    variante_nombre: str = None
) -> dict:
    """
    Pieza 5B: Slicing modular de Rutinas de Entrenamiento Elite.
    Filtra los bloques de ejercicios según disponibilidad semanal del atleta.
    """
    logger.info(f"🏋️‍♂️ Armándolo bloque deportivo: {tipo_entreno} | Nivel: {nivel_experiencia} | Días: {dias_entreno}")
    
    diccionario_rutinas = {}
    
    if dias_entreno == 0:
        return {"Descanso Activo": ["Día libre. Priorizar hidratación, sueño y caminatas ligeras."]}

    contenido_nivel = rutinas_elite.get(tipo_entreno, {}).get(nivel_experiencia, [])
    
    # Manejo de variantes indexadas si la disciplina es un diccionario complejo de opciones
    if isinstance(contenido_nivel, dict):
        if variante_nombre and variante_nombre in contenido_nivel:
            rutina_seleccionada = contenido_nivel[variante_nombre]
        else:
            # Fallback seguro: toma la primera variante disponible si no se especifica
            primer_key = list(contenido_nivel.keys())[0]
            rutina_seleccionada = contenido_nivel[primer_key]
    else:
        rutina_seleccionada = contenido_nivel

    if rutina_seleccionada:
        # Hacemos el slicing exacto por la cantidad de días que el alumno puede entrenar
        for bloque in rutina_seleccionada[:dias_entreno]:
            diccionario_rutinas[bloque[0]] = bloque[1:]
    else:
        diccionario_rutinas = {"Aviso": ["Rutina en construcción para esta disciplina y nivel."]}

    return diccionario_rutinas
