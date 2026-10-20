import { validarCuit, mailValido } from "./validaciones";

export interface DatosCompra {
  estudio: string;
  cuit: string;
  mail: string;
  condicionIva: string;
}

export function validarFormularioCompra(d: DatosCompra): { puedePagar: boolean; mensaje: string } {
  let mensaje = "";
  if (d.estudio.trim() !== "" && d.condicionIva !== "") {
    // Decisión 1
    if (!validarCuit(d.cuit)) {
      // Decisión 2
      mensaje = "El CUIT ingresado no es válido.";
    } else if (!mailValido(d.mail)) {
      // Decisión 3
      mensaje = "Revisá el mail ingresado.";
    }
  } else {
    mensaje = "Completá todos los datos.";
  }
  return { puedePagar: mensaje === "", mensaje };
}
