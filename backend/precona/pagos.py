"""Procesamiento de avisos de pago de la pasarela (RF-09, RF-10, RN-03)."""

from dataclasses import dataclass
from typing import Protocol

from precona.cuit import validar_cuit


@dataclass(frozen=True)
class Orden:
    id_orden: str
    cuit: str
    importe: float


@dataclass(frozen=True)
class EstadoPago:
    estado: str
    importe: float


class Pasarela(Protocol):
    """Adaptador hacia la pasarela de pagos (en producción, Mercado Pago)."""

    def consultar_pago(self, id_pago: str) -> EstadoPago: ...


class Registro(Protocol):
    """Acceso a la base: pagos procesados y licencias."""

    def pago_ya_procesado(self, id_pago: str) -> bool: ...

    def registrar_licencia(self, id_pago: str, orden: Orden) -> None: ...


def decidir_accion(orden: Orden, pago: EstadoPago) -> str:
    """Devuelve la acción que corresponde al estado informado por la pasarela."""
    if pago.estado == "rejected":
        return "notificar_rechazo"
    if pago.estado != "approved":
        return "esperar"
    if pago.importe != orden.importe or not validar_cuit(orden.cuit):
        return "revisar_manual"
    return "entregar_licencia"


def procesar_aviso(id_pago: str, orden: Orden, pasarela: Pasarela, registro: Registro) -> str:
    """Procesa un aviso de pago una sola vez y entrega la licencia si corresponde.

    El estado se consulta siempre a la pasarela: el contenido del aviso no se
    considera confiable (RF-09). Un aviso repetido no genera nada nuevo (RF-10).
    """
    if registro.pago_ya_procesado(id_pago):
        return "duplicado"
    accion = decidir_accion(orden, pasarela.consultar_pago(id_pago))
    if accion == "entregar_licencia":
        registro.registrar_licencia(id_pago, orden)
    return accion
