"""Porciones y restricciones: funciones puras, sin acceso a BD ni servicios IA."""
from collections import defaultdict
from itertools import product
import math
import re
import unicodedata

import numpy as np
from data.alimentos_nutricionales import ALIMENTOS_NUTRICIONALES


class ErrorPlanNutricional(ValueError):
    """Un plan inválido no debe publicarse ni guardarse como correcto."""


def _normalizar(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', str(texto or '').lower())
                   if not unicodedata.combining(c)).strip()


DIETAS = {
    'clasica / equilibrada': 'clasica', 'clasica': 'clasica',
    'hiperproteica (fitness)': 'hiperproteica', 'hiperproteica': 'hiperproteica',
    'cetogenica (keto)': 'keto', 'cetogenica': 'keto', 'keto': 'keto',
    'low carb': 'low_carb', 'vegana (100% vegetal)': 'vegana', 'vegana': 'vegana',
    'vegetariana': 'vegetariana', 'pescetariana': 'pescetariana',
    'paleolitica': 'paleo', 'paleo': 'paleo', 'mediterranea': 'mediterranea',
    'dash': 'dash', 'fodmap': 'fodmap', 'libre de gluten': 'sin_gluten',
    'sin gluten': 'sin_gluten', 'sin lactosa': 'sin_lactosa',
    'flexitariana': 'flexitariana',
}

# Restricciones estructuradas reconocidas. El texto desconocido requiere revisión;
# nunca se interpreta por coincidencias parciales o se ignora una alergia.
RESTRICCIONES = {
    'sin gluten': {'gluten'}, 'gluten': {'gluten'}, 'celiaquia': {'gluten'},
    'celiaco': {'gluten'}, 'celiaca': {'gluten'}, 'libre de gluten': {'gluten'},
    'sin lactosa': {'lacteos'}, 'lactosa': {'lacteos'},
    'sin lacteos': {'lacteos'}, 'lacteos': {'lacteos'}, 'leche': {'lacteos'},
    'huevo': {'huevo'}, 'huevos': {'huevo'}, 'sin huevo': {'huevo'},
    'soja': {'soja'}, 'soya': {'soja'}, 'sin soja': {'soja'},
    'pescado': {'pescado'}, 'pescados': {'pescado'}, 'sin pescado': {'pescado'},
    'mariscos': {'mariscos'}, 'mani': {'mani'}, 'cacahuete': {'mani'},
    'frutos secos': {'frutos_secos'}, 'nueces': {'frutos_secos'},
    'almendras': {'frutos_secos'}, 'semillas': {'semillas'},
    'sin carne': {'carne'}, 'carne': {'carne'}, 'cerdo': {'cerdo'},
    'sin cerdo': {'cerdo'}, 'pollo': {'pollo'}, 'vacuno': {'vacuno'},
    'carne de vaca': {'vacuno'}, 'legumbres': {'legumbre'},
}


def filtros_alimentarios(dieta_tipo, restricciones_alimentarias=''):
    dieta = DIETAS.get(_normalizar(dieta_tipo))
    if not dieta:
        raise ErrorPlanNutricional('Tipo de dieta no reconocido. Seleccioná una dieta del catálogo.')
    if dieta in {'dash', 'fodmap'}:
        raise ErrorPlanNutricional(
            f'{dieta.upper()} requiere un plan revisado por tu profesional; '
            'el generador todavía no valida sodio ni porciones FODMAP.')
    excluidas = set()
    if dieta == 'vegana':
        excluidas.update({'carne', 'pescado', 'lacteos', 'huevo'})
    elif dieta == 'vegetariana':
        excluidas.update({'carne', 'pescado'})
    elif dieta == 'pescetariana':
        excluidas.add('carne')
    elif dieta == 'paleo':
        excluidas.update({'lacteos', 'cereal', 'legumbre'})
    elif dieta == 'sin_gluten':
        excluidas.add('gluten')
    elif dieta == 'sin_lactosa':
        excluidas.add('lacteos')
    texto = _normalizar(restricciones_alimentarias)
    if texto in {'', 'ninguna', 'ninguno', 'sin restricciones', 'no tengo alergias'}:
        return dieta, excluidas
    for parte in re.split(r'[,;\n]+|\s+y\s+', texto):
        parte = parte.strip()
        parte = re.sub(r'^(?:alergia|alergico|alergica|intolerancia)\s+(?:a\s+la|a\s+los|a\s+las|al|a)\s+', '', parte).strip()
        if parte not in RESTRICCIONES:
            raise ErrorPlanNutricional(
                f'Restricción pendiente de revisión: «{parte}». '
                'Usá restricciones reconocidas separadas por comas o consultá a tu profesional.')
        excluidas.update(RESTRICCIONES[parte])
    return dieta, excluidas


def validar_macros(p_g_total, c_g_total, g_g_total):
    valores = []
    for nombre, valor in [('proteína', p_g_total), ('carbohidratos', c_g_total), ('grasas', g_g_total)]:
        try:
            numero = float(valor)
        except (ValueError, TypeError, OverflowError):
            raise ErrorPlanNutricional(f'La cantidad de {nombre} debe ser un número.') from None
        if isinstance(valor, bool) or not math.isfinite(numero) or numero < 0:
            raise ErrorPlanNutricional(f'La cantidad de {nombre} debe ser finita y no negativa. Revisá la meta y el plazo.')
        valores.append(numero)
    if sum(valores) <= 0:
        raise ErrorPlanNutricional('El plan debe aportar energía. Revisá la meta y el plazo.')
    return tuple(valores)


def calcular_macros_objetivo(peso, calorias, dieta_tipo):
    """Conserva la política previa; impide que una meta genere macros negativos."""
    dieta, _ = filtros_alimentarios(dieta_tipo)
    try:
        peso, calorias = float(peso), float(calorias)
    except (ValueError, TypeError, OverflowError):
        raise ErrorPlanNutricional('Peso y calorías deben ser números positivos.') from None
    if not all(math.isfinite(x) and x > 0 for x in (peso, calorias)):
        raise ErrorPlanNutricional('Peso y calorías deben ser números positivos. Revisá la meta y el plazo.')
    p = peso * (2.2 if dieta == 'hiperproteica' else 1.8)
    if dieta == 'keto':
        c = 30.0
        g = (calorias - 4 * p - 4 * c) / 9
    else:
        g = calorias * 0.30 / 9
        c = (calorias - 4 * p - 9 * g) / 4
    return validar_macros(p, c, g)


NOMBRES_COMIDAS = {
    1: ['COMIDA ÚNICA'], 2: ['ALMUERZO', 'CENA'],
    3: ['DESAYUNO', 'ALMUERZO', 'CENA'],
    4: ['DESAYUNO', 'ALMUERZO', 'MERIENDA', 'CENA'],
    5: ['DESAYUNO', 'MEDIA MAÑANA', 'ALMUERZO', 'MERIENDA', 'CENA'],
    6: ['DESAYUNO', 'MEDIA MAÑANA', 'ALMUERZO', 'MERIENDA', 'PRE-CENA', 'CENA'],
}


def _porcionar(ids, objetivos):
    # Cada columna aporta TODOS los macros del ingrediente por gramo.
    alimentos = [ALIMENTOS_NUTRICIONALES[i] for i in ids]
    matriz = np.array([[a[k] / 100 for a in alimentos]
                       for k in ['proteina_100g', 'carbos_100g', 'grasa_100g']])
    try:
        gramos = np.linalg.solve(matriz, objetivos)
    except np.linalg.LinAlgError:
        return None
    if not np.isfinite(gramos).all() or (gramos < -1e-7).any():
        return None
    # Se recalculan los nutrientes DESPUÉS de redondear el peso mostrado.
    gramos = np.round(np.maximum(gramos, 0), 1)
    totales = matriz @ gramos
    if any(abs(real - meta) > max(0.1, meta * 0.01)
           for real, meta in zip(totales, objetivos)):
        return None
    ingredientes = [{'id': i, 'nombre': a['nombre'], 'estado': a['estado'], 'gramos': float(g)}
                    for i, a, g in zip(ids, alimentos, gramos) if g > 0]
    kcal = sum(a['kcal_100g'] * g / 100 for a, g in zip(alimentos, gramos))
    return {'ingredientes': ingredientes, 'kcal': round(float(kcal), 1),
            'proteina_g': round(float(totales[0]), 1),
            'carbos_g': round(float(totales[1]), 1),
            'grasa_g': round(float(totales[2]), 1)}


def generar_menu_nutricional(p_g_total, c_g_total, g_g_total, num_comidas,
                             num_opciones, dieta_tipo, pais,
                             restricciones_alimentarias=''):
    macros = validar_macros(p_g_total, c_g_total, g_g_total)
    if type(num_comidas) is not int or num_comidas not in NOMBRES_COMIDAS:
        raise ErrorPlanNutricional('Elegí entre 1 y 6 comidas diarias.')
    if type(num_opciones) is not int or not 1 <= num_opciones <= 10:
        raise ErrorPlanNutricional('Elegí entre 1 y 10 opciones por comida.')
    dieta, excluidas = filtros_alimentarios(dieta_tipo, restricciones_alimentarias)
    permitidos = {i: a for i, a in ALIMENTOS_NUTRICIONALES.items()
                 if not excluidas.intersection(a['etiquetas'])}
    objetivos = np.array(macros) / num_comidas
    menus, compras = {}, defaultdict(float)
    bebida = 'Mate amargo o agua' if _normalizar(pais) == 'argentina' else 'Agua o té sin azúcar'
    for nombre in NOMBRES_COMIDAS[num_comidas]:
        desayuno = nombre in {'DESAYUNO', 'MEDIA MAÑANA', 'MERIENDA'}
        gp = 'proteina_desayuno' if desayuno else 'proteina_principal'
        gc = 'carbo_keto' if dieta == 'keto' else ('carbo_desayuno' if desayuno else 'carbo_principal')
        grupos = [[i for i, a in permitidos.items() if grupo in a['grupos']]
                  for grupo in [gp, gc, 'grasa']]
        candidatas = []
        for ids in product(*grupos):
            opcion = _porcionar(ids, objetivos)
            if opcion:
                candidatas.append(opcion)
        # Primero los platos cuya energía tabulada más se acerca a la meta.
        energia_meta = 4 * objetivos[0] + 4 * objetivos[1] + 9 * objetivos[2]
        candidatas.sort(key=lambda op: abs(op['kcal'] - energia_meta))
        opciones, vistos = [], set()
        # Alternar ingredientes principales antes de repetir la misma proteína.
        while candidatas and len(opciones) < num_opciones:
            disponibles = [o for o in candidatas if o['ingredientes'][0]['id'] not in vistos]
            opcion = (disponibles or candidatas)[0]
            candidatas.remove(opcion)
            firma = tuple((x['id'], x['gramos']) for x in opcion['ingredientes'])
            if any(tuple((x['id'], x['gramos']) for x in o['ingredientes']) == firma for o in opciones):
                continue
            vistos.add(opcion['ingredientes'][0]['id'])
            opcion['bebida'] = bebida
            opciones.append(opcion)
        if len(opciones) < num_opciones:
            raise ErrorPlanNutricional(
                f'No hay {num_opciones} opciones compatibles para {nombre.lower()} '
                'con estos macros y restricciones. Reducí las opciones o pedí un ajuste a tu profesional.')
        menus[nombre] = opciones
        for opcion in opciones:
            for item in opcion['ingredientes']:
                # Estimación para elegir UNA alternativa cada día, rotadas por igual.
                etiqueta = f"{item['nombre']} ({item['estado']})"
                compras[etiqueta] += item['gramos'] * 30 / len(opciones)
    return menus, {k: round(v, 1) for k, v in compras.items()}


def formatear_opcion(opcion, indice=None):
    prefijo = f'Opcion {indice}: ' if indice is not None else ''
    platos = ' + '.join(f"{i['gramos']:g}g {i['nombre']} ({i['estado']})"
                        for i in opcion['ingredientes'])
    return (f"{prefijo}{platos} | Infusion: {opcion['bebida']} | "
            f"Aprox: {opcion['kcal']:.1f} kcal; P: {opcion['proteina_g']:.1f}g; "
            f"C: {opcion['carbos_g']:.1f}g; G: {opcion['grasa_g']:.1f}g")


def resumen_energia(menus):
    """Rango diario al seleccionar una opción por comida."""
    return (round(sum(min(o['kcal'] for o in ops) for ops in menus.values()), 1),
            round(sum(max(o['kcal'] for o in ops) for ops in menus.values()), 1))


def nutrientes_opcion_texto(texto):
    """Lee el resumen de una opción nueva; los planes antiguos usan el fallback."""
    match = re.search(
        r'\| Aprox: ([0-9.]+) kcal; P: ([0-9.]+)g; C: ([0-9.]+)g; G: ([0-9.]+)g$',
        str(texto or ''))
    if not match:
        return None
    return dict(zip(['kcal', 'proteina_g', 'carbos_g', 'grasa_g'], map(float, match.groups())))


def validar_objetivo_energia(cal_objetivo, p_g_total, c_g_total, g_g_total):
    macros = validar_macros(p_g_total, c_g_total, g_g_total)
    try:
        kcal = float(cal_objetivo)
    except (ValueError, TypeError, OverflowError):
        raise ErrorPlanNutricional('La meta de calorías debe ser positiva.') from None
    energia_macros = 4 * macros[0] + 4 * macros[1] + 9 * macros[2]
    if not math.isfinite(kcal) or kcal <= 0 or abs(kcal - energia_macros) > max(5, kcal * 0.01):
        raise ErrorPlanNutricional('La meta de calorías no coincide con los macros. Recalculá el plan antes de guardarlo.')


def compras_desde_menus_texto(menus):
    """Proyección mensual de UNA alternativa por comida; soporta menús antiguos.

    Usa el peso servido del estado descrito, no una conversión de compra en crudo.
    Solo lee ingredientes anteriores a '|'; ignora bebidas y resúmenes de macros.
    """
    compras = defaultdict(float)
    for opciones in (menus or {}).values():
        if not isinstance(opciones, list) or not opciones:
            continue
        for opcion in opciones:
            ingredientes = str(opcion).split('|', 1)[0]
            ingredientes = re.sub(r'^Opcion\s*\d+:\s*', '', ingredientes, flags=re.I)
            for ingrediente in ingredientes.split('+'):
                match = re.match(r'^\s*(\d+(?:[.,]\d+)?)\s*g\s+(.+?)\s*$', ingrediente)
                if match:
                    compras[match[2]] += float(match[1].replace(',', '.')) * 30 / len(opciones)
    return {k: round(v, 1) for k, v in compras.items()}
