import { expect, test } from "vitest";
import { mailValido, validarCuit } from "../src/validaciones";

test.each(["20-12345678-6", "20123456786", "20-20000003-0"])("acepta el CUIT %s", (cuit) => {
  expect(validarCuit(cuit)).toBe(true);
});

test.each(["20-12345678-5", "2012345678", "20-1234567A-6", "", "2020000009-1"])(
  "rechaza el CUIT %s",
  (cuit) => {
    expect(validarCuit(cuit)).toBe(false);
  },
);

test("valida el formato del mail", () => {
  expect(mailValido("demo@ejemplo.com")).toBe(true);
  expect(mailValido("demo@ejemplo")).toBe(false);
});
