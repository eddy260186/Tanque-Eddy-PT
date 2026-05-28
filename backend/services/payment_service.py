import requests
import os
from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("PaymentService")

def validar_comprobante_pago(nro_operacion: str, email_usuario: str) -> tuple[bool, str]:
    """
    Pieza 4: Servicio Financiero de Mercado Pago y Cupones VIP.
    Verifica el número de operación contra la API oficial de Mercado Pago o valida el cupón TANQUEVIP.
    Evita fraudes chequeando duplicados en la tabla 'pagos_verificados' de Supabase.

    Devuelve:
    (True, mensaje_exito) o (False, mensaje_error)
    """

    if not nro_operacion:
        return False, "⚠️ Por favor, ingresá un número de operación."

    # =========================================================================
    # LIMPIEZA DEL NÚMERO DE OPERACIÓN
    # =========================================================================
    nro_limpio = nro_operacion.replace("#", "").strip()

    # =========================================================================
    # CUPÓN VIP ESPECIAL
    # =========================================================================
    if nro_limpio == "TANQUEVIP":
        logger.info(f"🎟️ Cupón VIP utilizado por: {email_usuario}")
        return True, "✅ ¡Acceso VIP concedido! Tu Plan Elite fue desbloqueado."

    # =========================================================================
    # VALIDACIÓN OFICIAL MERCADO PAGO
    # =========================================================================
    try:

        # TOKEN DESDE RAILWAY
        token = os.getenv("MERCADO_PAGO_TOKEN")

        if not token:
            logger.error("❌ MERCADO_PAGO_TOKEN no configurado en Railway.")
            return False, "❌ Error interno del sistema de pagos. Contactá soporte."

        # API MERCADO PAGO
        url = f"https://api.mercadopago.com/v1/payments/{nro_limpio}"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        logger.info(f"🔍 Consultando pago MP-{nro_limpio} en Mercado Pago...")

        respuesta = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        # =========================================================================
        # RESPUESTA EXITOSA
        # =========================================================================
        if respuesta.status_code == 200:

            datos_pago = respuesta.json()

            status = datos_pago.get("status")

            logger.info(f"💳 Estado actual del pago MP-{nro_limpio}: {status}")

            # =========================================================================
            # PAGO APROBADO
            # =========================================================================
            if status == "approved":

                # =========================================================================
                # ESCUDO ANTI FRAUDE
                # =========================================================================
                chequeo_duplicado = (
                    supabase
                    .table("pagos_verificados")
                    .select("*")
                    .eq("id_pago", nro_limpio)
                    .execute()
                )

                # =========================================================================
                # PAGO NO UTILIZADO
                # =========================================================================
                if len(chequeo_duplicado.data) == 0:

                    supabase.table("pagos_verificados").insert({
                        "id_pago": nro_limpio,
                        "usuario": email_usuario
                    }).execute()

                    logger.info(
                        f"✅ Pago MP-{nro_limpio} validado correctamente para {email_usuario}"
                    )

                    return True, "✅ ¡Pago aprobado! Tu Plan Elite fue desbloqueado con éxito."

                # =========================================================================
                # PAGO DUPLICADO
                # =========================================================================
                else:

                    logger.warning(
                        f"🚨 Intento de reutilización detectado: MP-{nro_limpio}"
                    )

                    return False, "❌ Este comprobante ya fue utilizado anteriormente."

            # =========================================================================
            # PAGO NO APROBADO
            # =========================================================================
            else:

                logger.warning(
                    f"⚠️ Pago MP-{nro_limpio} no aprobado. Estado: {status}"
                )

                return False, f"❌ El pago figura como: {status}. Debe estar aprobado."

        # =========================================================================
        # PAGO NO EXISTE
        # =========================================================================
        elif respuesta.status_code == 404:

            logger.warning(
                f"❌ El pago MP-{nro_limpio} no existe en Mercado Pago."
            )

            return False, "❌ Número de operación inexistente en Mercado Pago."

        # =========================================================================
        # ERROR API
        # =========================================================================
        else:

            logger.error(
                f"❌ Error API Mercado Pago: {respuesta.status_code} - {respuesta.text}"
            )

            return False, "❌ Error consultando Mercado Pago. Intentá nuevamente."

    # =========================================================================
    # ERROR GENERAL
    # =========================================================================
    except Exception as e:

        logger.error(
            f"🚨 Error crítico Mercado Pago: {str(e)}"
        )

        return False, f"❌ Error técnico del sistema de pagos: {str(e)}"