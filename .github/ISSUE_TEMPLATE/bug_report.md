---
name: "🐞 Reporte de incidencia"
about: "Informar un fallo del sitio, el backend o una herramienta HTML"
title: "[BUG] <componente>: <qué falla, en pocas palabras>"
labels: ["bug", "a-triar"]
assignees: []
---

<!--
ANTES DE COMPLETAR
- Usar SOLO datos ficticios (RN-07). Nunca adjuntar CUIT, comprobantes, mails ni
  archivos de clientes reales.
- No pegar códigos de licencia reales, claves, tokens ni secretos (RNF-02).
- Buscar primero si ya existe una incidencia igual. Una incidencia = un problema.
- Borrar los comentarios de ayuda (como este) antes de enviar.

Ejemplo de buen título:
[BUG] Backend: un webhook duplicado genera dos licencias para el mismo pago
-->

## 1. Identificación

| Campo | Valor |
|---|---|
| **Componente** | <!-- Sitio público / Backend / Base de datos / Herramienta HTML: nombre / Mails --> |
| **Requerimiento afectado** | <!-- ID del documento de requerimientos, ej. RF-10, RNF-03. "Ninguno" si no aplica --> |
| **Entorno** | <!-- Local / Prueba (staging) / Producción --> |
| **Versión** | <!-- Commit, tag o versión de la herramienta, ej. v1.2.0 o a1b2c3d --> |
| **Navegador y sistema** | <!-- Solo si aplica, ej. Chrome 129 en Windows 11 --> |
| **Fecha y hora del fallo** | <!-- AAAA-MM-DD HH:MM (hora de Argentina) --> |
| **Frecuencia** | <!-- Siempre / A veces (indicar cada cuánto) / Una sola vez --> |

## 2. Severidad

<!-- Marcar UNA con [x] -->
- [ ] **Crítica**: bloquea la venta o la entrega, compromete datos o seguridad (ej. pago aprobado sin licencia).
- [ ] **Alta**: una función principal no anda y no hay alternativa.
- [ ] **Media**: falla una función, pero hay una forma de seguir.
- [ ] **Baja**: problema visual, de texto o de comodidad.

## 3. Descripción técnica del problema

<!--
Qué falla, dónde y en qué condiciones, en 2 a 5 oraciones.
Describir hechos, no suposiciones. Si hay una hipótesis de la causa, va en la sección 8.
-->

## 4. Pasos exactos para reproducir

<!--
Numerados, uno por acción, desde un estado inicial claro. Otra persona debe poder
seguirlos sin preguntar nada. Indicar los datos de prueba exactos (ficticios) que se usaron.
-->

**Estado inicial:** <!-- ej. sesión cerrada, base de prueba recién restaurada, herramienta sin licencia cargada -->

**Datos de prueba usados:** <!-- ej. CUIT ficticio de prueba, usuario de prueba de Mercado Pago, archivo demo_compras_10k.csv -->

1.
2.
3.

## 5. Comportamiento esperado vs. observado

| Esperado | Observado |
|---|---|
| <!-- Qué debería pasar, según el requerimiento o el criterio de aceptación --> | <!-- Qué pasa en realidad. Copiar textual los mensajes de error --> |

## 6. Evidencias

<!--
Adjuntar lo que corresponda arrastrando archivos a esta caja:
- Capturas de pantalla o video corto del fallo.
- Log del backend (recortado al fragmento relevante, sin secretos).
- Consola del navegador (F12 → Consola) y pestaña Red, si es una herramienta o el sitio.
- Archivo de entrada FICTICIO que provoca el fallo.
- ID del pago de prueba en Mercado Pago, si aplica.
-->

```text
Pegar aquí logs o mensajes de error
```

## 7. Impacto

<!-- A quién afecta y cuánto: ¿clientes que compran?, ¿una herramienta?, ¿solo la administradora?
     ¿Hay ventas, licencias o facturas afectadas? ¿Cuántas? -->

## 8. Información adicional (opcional)

<!-- Hipótesis de causa, alternativa temporal (workaround), incidencias o PR relacionados (#123). -->

---

### Lista de control de quien reporta

- [ ] El título indica componente y síntoma.
- [ ] Los pasos permiten reproducir el fallo desde cero.
- [ ] Esperado y observado están separados y son concretos.
- [ ] Indiqué el requerimiento afectado (o "Ninguno").
- [ ] Las evidencias usan solo datos ficticios y no contienen secretos.
