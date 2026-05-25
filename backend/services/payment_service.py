import requests
import streamlit as st
from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("PaymentService")

def validar_comprobante_pago(nro_operacion: str, email_usuario: str) -> tuple[bool, str]:
    """
    Pieza 4: Servicio Financiero de Mercado Pago y Cupones VIP.
    Verifica el número de operación contra la API oficial de Mercado Pago o valida el cupón TANQUEVIP.
    Evita fraudes chequeando duplicados en la tabla 'pagos_verificados' de Supabase.
    
    Devuelve: (True, mensaje_exito) o (False, mensaje_error)
    """
    if not nro_operacion:
        return False, "⚠️ Por favor, ingresá un número de operación."

    # Limpieza estricta del string enviado por el usuario
    nro_limpio = nro_operacion.replace("#", "").strip()

    # =========================================================================
    # 1. VALIDACIÓN DE CUPÓN SECRETO ULTRA ELITE
    # =========================================================================
    if nro_limpio == "TANQUEVIP":
        logger.info(f"🎟️ Cupón VIP de acceso total utilizado por: {email_usuario}")
        return True, "✅ ¡Acceso VIP concedido por Cupón! Tu Plan Elite ha sido desbloqueado."

    # =========================================================================
    # 2. CONECTIVIDAD CON LA API OFICIAL DE MERCADO PAGO
    # =========================================================================
    try:
        # Extraemos el token desde los secretos para mantener compatibilidad absoluta
        if "MERCADO_PAGO_TOKEN" not in st.secrets:
            logger.error("❌ Error de infraestructura: 'MERCADO_PAGO_TOKEN' no configurado en st.secrets.")
            return False, "❌ Error de configuración interna en el servidor de pagos. Contactá a soporte."

        token = st.secrets["MERCADO_PAGO_TOKEN"]
        url = f"https://api.mercadopago.com/v1/payments/{nro_limpio}"
        headers = {"Authorization": f"Bearer {token}"}

        logger.info(f"🔍 Consultando estado de transacción MP-{nro_limpio} en la API de Mercado Pago...")
        respuesta = requests.get(url, headers=headers, timeout=10)

        if respuesta.status_code == 200:
            datos_pago = respuesta.json()
            status = datos_pago.get("status")

            if status == "approved":
                # =========================================================================
                # 3. ESCUDO ANTI-FRAUDE: Bloqueo de reutilización de comprobantes
                # =========================================================================
                chequeo_duplicado = supabase.table("pagos_verificados")\
                    .select("*")\
                    .eq("id_pago", nro_limpio)\
                    .execute()

                if len(chequeo_duplicado.data) == 0:
                    # El pago es real y nadie lo usó, registramos la firma en Supabase
                    supabase.table("pagos_verificados").insert({
                        "id_pago": nro_limpio,
                        "usuario": email_usuario
                    }).execute()
                    
                    logger.info(f"💳 Transacción validada y grabada con éxito: MP-{nro_limpio} asignado a {email_usuario}")
                    return True, "✅ ¡Pago aprobado! Tu Plan Elite ha sido desbloqueado con éxito."
                else:
                    logger.warning(f"🚨 ALERTA DE FRAUDE: Intento de reutilización del ID MP-{nro_limpio} por el usuario {email_usuario}")
                    return False, "❌ Este comprobante de pago ya fue utilizado por otro usuario en la plataforma."
            else:
                logger.warning(f"⚠️ Transacción MP-{nro_limpio} rechazada por Mercado Pago. Estado actual: {status}")
                return False, f"❌ El pago figura como: {status}. Para desbloquear el plan debe estar 'approved'."
        else:
            logger.warning(f"🔍 El ID de operación MP-{nro_limpio} no existe en los registros de Mercado Pago.")
            return False, "❌ Número de operación no encontrado en Mercado Pago. Verificá los dígitos."

    except Exception as e:
        logger.error(f"🚨 Fallo crítico de red en el módulo de Mercado Pago: {str(e)}")
        return False, f"❌ Error técnico de pasarela: {str(e)}"