"""Adaptador real hacia la API de Mercado Pago."""

import os

import httpx

from precona.pagos import EstadoPago

URL_PAGOS = "https://api.mercadopago.com/v1/payments/"


class PasarelaMercadoPago:
    """Consulta el estado de un pago. El token se lee del entorno, nunca del código (RNF-02)."""

    def __init__(self, cliente: httpx.Client | None = None) -> None:
        token = os.environ["MP_ACCESS_TOKEN"]
        self._cliente = cliente or httpx.Client(timeout=10.0)
        self._encabezados = {"Authorization": f"Bearer {token}"}

    def consultar_pago(self, id_pago: str) -> EstadoPago:
        respuesta = self._cliente.get(URL_PAGOS + id_pago, headers=self._encabezados)
        respuesta.raise_for_status()
        datos = respuesta.json()
        return EstadoPago(estado=datos["status"], importe=float(datos["transaction_amount"]))
