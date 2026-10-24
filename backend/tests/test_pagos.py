"""Pruebas de procesar_aviso con dobles de prueba. Datos ficticios (RN-07)."""

from unittest.mock import Mock

import pytest

from precona.pagos import EstadoPago, Orden, decidir_accion, procesar_aviso

ORDEN = Orden(id_orden="ORD-TEST-1", cuit="20-12345678-6", importe=50000.0)


class PasarelaStub:
    """Stub: inyecta la respuesta de la pasarela sin conexión real."""

    def __init__(self, estado: str, importe: float = 50000.0) -> None:
        self._respuesta = EstadoPago(estado=estado, importe=importe)

    def consultar_pago(self, id_pago: str) -> EstadoPago:
        return self._respuesta


class RegistroEnMemoria:
    def __init__(self) -> None:
        self.licencias: list[str] = []

    def pago_ya_procesado(self, id_pago: str) -> bool:
        return id_pago in self.licencias

    def registrar_licencia(self, id_pago: str, orden: Orden) -> None:
        self.licencias.append(id_pago)


def test_pago_aprobado_entrega_una_licencia() -> None:
    # Arrange
    registro = RegistroEnMemoria()
    # Act
    accion = procesar_aviso("TEST-001", ORDEN, PasarelaStub("approved"), registro)
    # Assert
    assert accion == "entregar_licencia"
    assert registro.licencias == ["TEST-001"]


def test_aviso_duplicado_no_genera_segunda_licencia() -> None:
    registro = RegistroEnMemoria()
    pasarela = PasarelaStub("approved")
    procesar_aviso("TEST-001", ORDEN, pasarela, registro)

    accion = procesar_aviso("TEST-001", ORDEN, pasarela, registro)

    assert accion == "duplicado"
    assert registro.licencias == ["TEST-001"]


def test_duplicado_no_vuelve_a_consultar_la_pasarela() -> None:
    # Mock: se audita la interacción con la pasarela
    registro = RegistroEnMemoria()
    registro.licencias.append("TEST-001")
    pasarela = Mock()

    procesar_aviso("TEST-001", ORDEN, pasarela, registro)

    pasarela.consultar_pago.assert_not_called()


def test_aviso_nuevo_consulta_la_pasarela_una_vez() -> None:
    pasarela = Mock()
    pasarela.consultar_pago.return_value = EstadoPago("approved", 50000.0)

    procesar_aviso("TEST-002", ORDEN, pasarela, RegistroEnMemoria())

    pasarela.consultar_pago.assert_called_once_with("TEST-002")


@pytest.mark.parametrize(
    "estado, importe, cuit, esperado",
    [
        ("rejected", 50000.0, "20-12345678-6", "notificar_rechazo"),
        ("pending", 50000.0, "20-12345678-6", "esperar"),
        ("in_process", 50000.0, "20-12345678-6", "esperar"),
        ("approved", 45000.0, "20-12345678-6", "revisar_manual"),
        ("approved", 50000.0, "20-12345678-5", "revisar_manual"),
        ("approved", 50000.0, "20-12345678-6", "entregar_licencia"),
    ],
)
def test_decidir_accion(estado: str, importe: float, cuit: str, esperado: str) -> None:
    orden = Orden(id_orden="ORD-TEST-1", cuit=cuit, importe=50000.0)
    assert decidir_accion(orden, EstadoPago(estado, importe)) == esperado


def test_pago_rechazado_no_registra_licencia() -> None:
    registro = RegistroEnMemoria()

    accion = procesar_aviso("TEST-003", ORDEN, PasarelaStub("rejected"), registro)

    assert accion == "notificar_rechazo"
    assert registro.licencias == []
