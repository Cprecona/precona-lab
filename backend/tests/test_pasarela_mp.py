"""Prueba del adaptador sin red: httpx.MockTransport reemplaza a la API real."""

import httpx
import pytest

from precona.pasarela_mp import PasarelaMercadoPago


def test_consulta_el_pago_con_token_del_entorno(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MP_ACCESS_TOKEN", "TOKEN-DE-PRUEBA")
    pedidos: list[httpx.Request] = []

    def responder(pedido: httpx.Request) -> httpx.Response:
        pedidos.append(pedido)
        return httpx.Response(200, json={"status": "approved", "transaction_amount": 50000})

    cliente = httpx.Client(transport=httpx.MockTransport(responder))
    estado = PasarelaMercadoPago(cliente).consultar_pago("TEST-001")

    assert (estado.estado, estado.importe) == ("approved", 50000.0)
    assert pedidos[0].url.path == "/v1/payments/TEST-001"
    assert pedidos[0].headers["Authorization"] == "Bearer TOKEN-DE-PRUEBA"
