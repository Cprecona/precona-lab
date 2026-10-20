# Versión inicial del procesamiento de pagos (antes de la refactorización)
import json
import requests

TOKEN_MP = "TEST-0000000000000000-000000-00000000000000000000000000000000-000000000"
procesados = []


def procesar_aviso_mp(datos, enviar_mail, guardar_licencia, emitir_factura):
    global procesados
    id_pago = datos["data"]["id"]
    if id_pago in procesados:
        return "duplicado"
    try:
        r = requests.get("https://api.mercadopago.com/v1/payments/" + str(id_pago),
                         headers={"Authorization": "Bearer " + TOKEN_MP}, verify=False)
        pago = json.loads(r.text)
    except:
        return "error"
    cuit = pago["metadata"]["cuit"].replace("-", "")
    if len(cuit) == 11 and cuit.isdigit():
        pesos = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        suma = 0
        for i in range(10):
            suma = suma + int(cuit[i]) * pesos[i]
        dv = 11 - (suma % 11)
        if dv == 11:
            dv = 0
        if dv == 10 or dv != int(cuit[10]):
            return "cuit_invalido"
    else:
        return "cuit_invalido"
    if pago["status"] == "approved":
        if pago["transaction_amount"] == pago["metadata"]["importe_orden"]:
            if pago["metadata"]["modalidad"] == "unico":
                guardar_licencia(id_pago, cuit)
                if pago["metadata"]["condicion_iva"] == "RI":
                    emitir_factura(id_pago, "A")
                    enviar_mail(pago["payer"]["email"], "Tu licencia", "Gracias por tu compra. Adjuntamos licencia y factura.")
                else:
                    emitir_factura(id_pago, "B")
                    enviar_mail(pago["payer"]["email"], "Tu licencia", "Gracias por tu compra. Adjuntamos licencia y factura.")
            elif pago["metadata"]["modalidad"] == "semestral":
                guardar_licencia(id_pago, cuit)
                if pago["metadata"]["condicion_iva"] == "RI":
                    emitir_factura(id_pago, "A")
                    enviar_mail(pago["payer"]["email"], "Tu licencia", "Gracias por tu suscripción. Adjuntamos licencia y factura.")
                else:
                    emitir_factura(id_pago, "B")
                    enviar_mail(pago["payer"]["email"], "Tu licencia", "Gracias por tu suscripción. Adjuntamos licencia y factura.")
            else:
                return "modalidad_desconocida"
            procesados.append(id_pago)
            return "entregado"
        else:
            return "importe_distinto"
    elif pago["status"] == "rejected":
        enviar_mail(pago["payer"]["email"], "Pago rechazado", "Tu pago fue rechazado.")
        return "rechazado"
    else:
        return "esperar"
