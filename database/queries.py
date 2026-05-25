from database.conexion import supabase
from utils.logger import obtener_logger
from datetime import datetime

logger = obtener_logger("DatabaseQueries")

# =========================================================================
# 1. CONSULTAS DE CONTROL DEL ENTRENADOR (Módulo Multiusuario)
# =========================================================================

def obtener_alumnos_por_entrenador(staff_id: str) -> list:
    """
    Trae únicamente los alumnos asignados a un entrenador específico.
    Cumple con el aislamiento multi-inquilino.
    """
    try:
        respuesta = supabase.table("perfiles_atletas")\
            .select("id, nombre_completo, genero, objetivo_principal, creditos_ia")\
            .eq("entrenador_id", staff_id)\
            .execute()
        return respuesta.data
    except Exception as e:
        logger.error(f"❌ Error al obtener alumnos para el staff {staff_id}: {str(e)}")
        return []

def registrar_nuevo_profesional(perfil_id: str, rol: str, whatsapp: str, limite: int) -> bool:
    """
    Inserta un nuevo miembro del staff (entrenador/nutricionista) en roles_staff.
    Llamado exclusivamente por el Panel de Admin.
    """
    try:
        datos = {
            "perfil_id": perfil_id,
            "rol": rol,
            "whatsapp_comercial": whatsapp,
            "limite_alumnos": limite,
            "activo": True
        }
        supabase.table("roles_staff").insert(datos).execute()
        logger.info(f"✅ Nuevo profesional registrado con éxito: Rol {rol} para Perfil {perfil_id}")
        return True
    except Exception as e:
        logger.error(f"❌ Error al registrar profesional en roles_staff: {str(e)}")
        return False

def registrar_log_whatsapp(alumno_id: str, entrenador_id: str, direccion: str, contenido: str) -> None:
    """
    Guarda el historial de mensajes de WhatsApp para el sistema de auditoría y debugging.
    """
    try:
        log = {
            "alumno_id": alumno_id,
            "entrenador_id": entrenador_id,
            "direccion": direccion, # 'entrante' o 'saliente'
            "contenido": contenido,
            "estado_envio": "enviado"
        }
        supabase.table("mensajes_whatsapp").insert(log).execute()
    except Exception as e:
        logger.error(f"❌ Error al escribir log de WhatsApp: {str(e)}")


# =========================================================================
# 2. CONSULTAS PARA LA SUITE DE ADMINISTRACIÓN GENERAL (Dashboard Maestro)
# =========================================================================

def obtener_metricas_globales_saas() -> dict:
    """
    Calcula métricas globales para el dashboard del dueño de la plataforma.
    """
    try:
        total_atletas = supabase.table("perfiles_atletas").select("id", count="exact").execute()
        total_staff = supabase.table("roles_staff").select("id, rol").execute()
        
        entrenadores = len([x for x in total_staff.data if x["rol"] == "entrenador"])
        nutricionistas = len([x for x in total_staff.data if x["rol"] == "nutricionista"])
        
        return {
            "total_alumnos": total_atletas.count or 0,
            "total_entrenadores": entrenadores,
            "total_nutricionistas": nutricionistas,
            "mensajes_hoy": 0  # Se conectará dinámicamente con mensajes_whatsapp más adelante
        }
    except Exception as e:
        logger.error(f"❌ Error al obtener métricas globales: {str(e)}")
        return {"total_alumnos": 0, "total_entrenadores": 0, "total_nutricionistas": 0, "mensajes_hoy": 0}

def buscar_perfil_por_email_exacto(email: str) -> dict:
    """
    Busca un usuario en perfiles_atletas mediante su email para poder promoverlo.
    """
    try:
        respuesta = supabase.table("perfiles_atletas").select("id, nombre_completo, email").eq("email", email).execute()
        if respuesta.data:
            return respuesta.data[0]
        return {}
    except Exception as e:
        logger.error(f"❌ Error al buscar perfil por email {email}: {str(e)}")
        return {}

def obtener_lista_staff_detallada() -> list:
    """
    Trae todo el personal activo en la tabla roles_staff cruzando datos básicos de su perfil.
    """
    try:
        respuesta = supabase.table("roles_staff").select(
            "id, rol, whatsapp_comercial, plan_saas, limite_alumnos, activo, perfiles_atletas(nombre_completo, email)"
        ).execute()
        return respuesta.data
    except Exception as e:
        logger.error(f"❌ Error al obtener lista de staff: {str(e)}")
        return []