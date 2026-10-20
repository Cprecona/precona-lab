"""Validación de CUIT/CUIL argentinos."""

import re

PESOS = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)
PREFIJOS_VALIDOS = {"20", "23", "24", "27", "30", "33", "34"}


def normalizar_cuit(cuit: str) -> str:
    """Quita guiones, puntos y espacios. Ej.: '20-12345678-6' -> '20123456786'."""
    return re.sub(r"[\s.\-]", "", cuit)


def calcular_digito_verificador(primeros_diez: str) -> int | None:
    """Calcula el dígito verificador por módulo 11.

    Multiplica cada uno de los 10 primeros dígitos por su peso
    (5, 4, 3, 2, 7, 6, 5, 4, 3, 2), suma los productos y hace
    11 - (suma % 11). Si da 11, el dígito es 0. Si da 10, el número
    no tiene dígito válido y se devuelve None.
    """
    suma = sum(int(d) * p for d, p in zip(primeros_diez, PESOS, strict=True))
    resultado = 11 - (suma % 11)
    if resultado == 11:
        return 0
    if resultado == 10:
        return None
    return resultado


def validar_cuit(cuit: str) -> bool:
    """Devuelve True si el CUIT tiene formato, prefijo y dígito verificador válidos."""
    numero = normalizar_cuit(cuit)
    if not re.fullmatch(r"\d{11}", numero):
        return False
    if numero[:2] not in PREFIJOS_VALIDOS:
        return False
    return calcular_digito_verificador(numero[:10]) == int(numero[10])
