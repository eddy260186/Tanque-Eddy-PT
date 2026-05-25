from collections import defaultdict
from data.alimentos import alimentos_db
from data.ejercicios import rutinas_elite
from utils.logger import obtener_logger

logger = obtener_logger("PlanService")

def generar_menu_dinamico(
    p_g_total: float, 
    c_g_total: float, 
    g_g_total: float, 
    num_comidas: int, 
    num_opciones: int, 
    dieta_tipo: str, 
    pais: str
) -> tuple[dict, dict]:
    """
    Pieza 5A: Algoritmo de distribución de Macronutrientes y Menús Dinámicos.
    Calcula los gramos exactos por porción y genera opciones variadas sin repetir.
    También computa la lista de compras proyectada a 30 días.
    
    Devuelve: (diccionario_menus, lista_compras)
    """
    logger.info(f"🍽️ Iniciando algoritmo nutricional para Dieta: {dieta_tipo} | Comidas: {num_comidas}")
    
    diccionario_menus = {} 
    lista_compras = defaultdict(float)

    # Divisiones matemáticas de macros por cada plato individual
    p_com = p_g_total / num_comidas
    c_com = c_g_total / num_comidas
    g_com = g_g_total / num_comidas
    
    gramos_p = int(p_com / 0.25)
    gramos_g = int(g_com / 0.90)
    gramos_c = 0 if "Keto" in dieta_tipo else int(c_com / 0.25)

    # Mapa oficial de nombres de comidas según frecuencia diaria
    mapa_nombres = {
        1: ["Comida Única"], 
        2: ["Almuerzo", "Cena"], 
        3: ["Desayuno", "Almuerzo", "Cena"], 
        4: ["Desayuno", "Almuerzo", "Merienda", "Cena"], 
        5: ["Desayuno", "Media Mañana", "Almuerzo", "Merienda", "Cena"], 
        6: ["Desayuno", "Media Mañana", "Almuerzo", "Merienda", "Pre-Cena", "Cena"]
    }

    nombres_comidas = mapa_nombres.get(num_comidas, ["Comida"])

    for nombre_base in nombres_comidas:
        opciones_de_esta_comida = []
        es_mt = any(x in nombre_base for x in ["Desayuno", "Merienda", "Mañana"])
        
        for i in range(num_opciones):
            # 1. Selección de Proteína según tipo de restricción alimentaria
            if "Vegana" in dieta_tipo: 
                fp = alimentos_db["Prot_Vegana"][i % len(alimentos_db["Prot_Vegana"])]
            elif "Vegetariana" in dieta_tipo: 
                fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])] if es_mt else alimentos_db["Prot_Vegana"][i % len(alimentos_db["Prot_Vegana"])]
            elif "Pescetariana" in dieta_tipo: 
                fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])] if es_mt else alimentos_db["Prot_Pescado"][i % len(alimentos_db["Prot_Pescado"])]
            else: 
                fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])] if es_mt else alimentos_db["Prot_Principal"][i % len(alimentos_db["Prot_Principal"])]
            
            # 2. Selección de Carbohidratos según enfoque energético
            if "Keto" in dieta_tipo: 
                fc = alimentos_db["Verduras_Keto"][i % len(alimentos_db["Verduras_Keto"])]
                texto_carbo = "Libre"
            elif "Paleo" in dieta_tipo: 
                fc = alimentos_db["Carb_Vegetales"][i % len(alimentos_db["Carb_Vegetales"])]
                texto_carbo = f"{gramos_c}g"
            else: 
                fc = alimentos_db["Carb_Desayuno"][i % len(alimentos_db["Carb_Desayuno"])] if es_mt else alimentos_db["Carb_Principal"][i % len(alimentos_db["Carb_Principal"])]
                texto_carbo = f"{gramos_c}g"
            
            # 3. Grasas y Bebidas adaptadas regionalmente
            fg = alimentos_db["Grasas"][i % len(alimentos_db["Grasas"])]
            bebida = alimentos_db["Bebidas_Arg"][i % len(alimentos_db["Bebidas_Arg"])] if "Argentina" in pais else alimentos_db["Bebidas_Gral"][i % len(alimentos_db["Bebidas_Gral"])]
            
            # Construcción de la cadena de texto VIP para la interfaz y el PDF
            txt_op = f"Opcion {i+1}: {gramos_p}g {fp} + {texto_carbo} {fc} + {gramos_g}g {fg} | Infusion: {bebida}"
            opciones_de_esta_comida.append(txt_op)
            
            # Cálculo de la tracción de compras mensualizada
            dias_por_opcion = 30 / num_opciones
            lista_compras[fp] += gramos_p * dias_por_opcion
            if "Keto" not in dieta_tipo: 
                lista_compras[fc] += gramos_c * dias_por_opcion
            lista_compras[fg] += gramos_g * dias_por_opcion
            lista_compras[bebida] += dias_por_opcion
            
        diccionario_menus[nombre_base.upper()] = opciones_de_esta_comida

    return diccionario_menus, dict(lista_compras)


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