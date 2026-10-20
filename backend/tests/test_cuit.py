"""Pruebas unitarias de validar_cuit. Todos los CUIT son ficticios (RN-07)."""

import pytest

from precona.cuit import calcular_digito_verificador, validar_cuit


@pytest.mark.parametrize(
    "cuit",
    ["20-12345678-6", "20123456786", "30-71234567-1", "27 11111111 7"],
)
def test_acepta_cuit_validos(cuit: str) -> None:
    assert validar_cuit(cuit)


@pytest.mark.parametrize(
    "cuit, motivo",
    [
        ("20-12345678-5", "dígito verificador incorrecto"),
        ("2012345678", "tiene 10 dígitos"),
        ("201234567860", "tiene 12 dígitos"),
        ("20-1234567A-6", "contiene una letra"),
        ("", "está vacío"),
        ("99-12345678-6", "prefijo inexistente"),
    ],
)
def test_rechaza_cuit_invalidos(cuit: str, motivo: str) -> None:
    assert not validar_cuit(cuit), motivo


def test_resultado_11_da_digito_cero() -> None:
    # 11 - (suma % 11) = 11 -> el dígito verificador es 0
    assert calcular_digito_verificador("2020000003") == 0
    assert validar_cuit("20-20000003-0")


@pytest.mark.parametrize("ultimo", "0123456789")
def test_resultado_10_no_tiene_digito_valido(ultimo: str) -> None:
    # 11 - (suma % 11) = 10 -> ningún dígito final es válido
    assert calcular_digito_verificador("2020000009") is None
    assert not validar_cuit("2020000009" + ultimo)
