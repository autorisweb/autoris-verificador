# Autoris - Verificador de Estampillas OTS

Este microservicio permite verificar la validez de una estampilla de tiempo generada por OpenTimestamps (.ots) utilizando una API simple basada en Flask.

## ¿Cómo funciona?

Envías un archivo .ots a través de una solicitud POST y el microservicio responde con el estado de verificación.

## Endpoint

`POST /verificar`

**Parámetros:**
- `file` (archivo .ots): Archivo que deseas verificar.

**Respuesta esperada:**

```json
{
  "estado": "pending" | "verified" | "invalid",
  "mensaje": "Descripción del estado"
}
