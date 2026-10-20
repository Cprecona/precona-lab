import { describe, expect, test } from "vitest";
import { validarFormularioCompra } from "../src/compra";

// Datos ficticios (RN-07)
const base = {
  estudio: "Estudio Demo SRL",
  cuit: "20-12345678-6",
  mail: "demo@ejemplo.com",
  condicionIva: "Responsable Inscripto",
};

describe("validarFormularioCompra (RF-06)", () => {
  test("rechaza datos incompletos", () => {
    expect(validarFormularioCompra({ ...base, estudio: "" }).mensaje).toBe(
      "Completá todos los datos.",
    );
  });
  test("rechaza si falta la condición frente al IVA", () => {
    expect(validarFormularioCompra({ ...base, condicionIva: "" }).puedePagar).toBe(false);
  });
  test("rechaza un CUIT con dígito verificador incorrecto", () => {
    expect(validarFormularioCompra({ ...base, cuit: "20-12345678-5" }).mensaje).toBe(
      "El CUIT ingresado no es válido.",
    );
  });
  test("rechaza un mail mal formado", () => {
    expect(validarFormularioCompra({ ...base, mail: "demo@ejemplo" }).mensaje).toBe(
      "Revisá el mail ingresado.",
    );
  });
  test("habilita el pago con todos los datos válidos", () => {
    expect(validarFormularioCompra(base)).toEqual({ puedePagar: true, mensaje: "" });
  });
});
