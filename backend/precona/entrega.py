"""Entrega de una venta aprobada: licencia, factura y mail (RF-13, RF-14, RF-17)."""

from collections.abc import Callable

MENSAJES = {
    "unico": "Gracias por tu compra. Adjuntamos licencia y factura.",
    "semestral": "Gracias por tu suscripción. Adjuntamos licencia y factura.",
}


def tipo_factura(condicion_iva: str) -> str:
    """Conserva la regla de la versión inicial: A para Responsable Inscripto, B para el resto."""
    return "A" if condicion_iva == "RI" else "B"


def entregar(
    id_pago: str,
    cuit: str,
    modalidad: str,
    condicion_iva: str,
    email: str,
    guardar_licencia: Callable[[str, str], None],
    emitir_factura: Callable[[str, str], None],
    enviar_mail: Callable[[str, str, str], None],
) -> str:
    """Ejecuta la entrega una sola vez, sin repetir código por modalidad o condición."""
    if modalidad not in MENSAJES:
        return "modalidad_desconocida"
    guardar_licencia(id_pago, cuit)
    emitir_factura(id_pago, tipo_factura(condicion_iva))
    enviar_mail(email, "Tu licencia", MENSAJES[modalidad])
    return "entregado"
