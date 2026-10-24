"""Pruebas de la entrega con mocks: se audita qué se llama y con qué datos."""

from unittest.mock import Mock

import pytest

from precona.entrega import entregar, tipo_factura


@pytest.mark.parametrize("condicion, tipo", [("RI", "A"), ("MT", "B"), ("CF", "B")])
def test_tipo_factura(condicion: str, tipo: str) -> None:
    assert tipo_factura(condicion) == tipo


def test_entrega_llama_una_vez_a_cada_servicio() -> None:
    guardar, facturar, mail = Mock(), Mock(), Mock()

    resultado = entregar(
        "TEST-001", "20123456786", "semestral", "RI", "demo@ejemplo.com", guardar, facturar, mail
    )

    assert resultado == "entregado"
    guardar.assert_called_once_with("TEST-001", "20123456786")
    facturar.assert_called_once_with("TEST-001", "A")
    mail.assert_called_once_with(
        "demo@ejemplo.com",
        "Tu licencia",
        "Gracias por tu suscripción. Adjuntamos licencia y factura.",
    )


def test_modalidad_desconocida_no_entrega_nada() -> None:
    guardar, facturar, mail = Mock(), Mock(), Mock()

    resultado = entregar(
        "TEST-002", "20123456786", "mensual", "CF", "demo@ejemplo.com", guardar, facturar, mail
    )

    assert resultado == "modalidad_desconocida"
    guardar.assert_not_called()
    facturar.assert_not_called()
    mail.assert_not_called()
