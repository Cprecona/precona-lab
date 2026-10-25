const PESOS = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2];
export function validarCuit(cuit: string): boolean {
  const n = cuit.replace(/[\s.-]/g, "");
  if (!/^\d{11}$/.test(n)) return false;
  const suma = PESOS.reduce((acc, p, i) => acc + p * Number(n[i]), 0);
  let dv = 11 - (suma % 11);
  if (dv === 11) dv = 0;
  return dv !== 10 && dv === Number(n[10]);
}
export function mailValido(mail: string): boolean {
  return /^[^\s@]+@[^\s@.]+(\.[^\s@.]+)+$/.test(mail);
}
