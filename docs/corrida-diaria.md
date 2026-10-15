# Corrida diaria

La ejecuta la tarea programada de lunes a viernes. Cada corrida arranca en una sesión nueva.

## 1. Descargar

```bash
python3 scripts/bora.py            # fecha de hoy (hora Argentina)
```

Leé `runs/<AAAAMMDD>.json`. Si `total_avisos` es 0 (feriado o edición aún no publicada), terminá: sin mail ni mensajes, y explicá el motivo en la respuesta final.

## 2. Commitear

```bash
git add organismos temas runs && git commit -m "corrida: <AAAAMMDD> descarga" && git push origin main
```

## 3. Repartir

Con los IDs de `config/sesiones.json`, mandá un mensaje (`send_message`) a:

- cada especialista de organismo que tenga normas nuevas en `runs/<AAAAMMDD>.json` → `organismos.<slug>`;
- el Analista de Temas, si `temas_candidatos` no está vacío.

Formato del mensaje:

```
Corrida <AAAAMMDD>. Normas nuevas de <slug>:
- <titulo> — <archivo>
Seguí docs/especialista.md (o docs/analista-temas.md).
```

No mandes mensaje a quien no tiene novedades.

## 4. Esperar los informes

Corré en segundo plano (`run_in_background`), con los slugs a los que escribiste (`temas` para el Analista):

```bash
python3 scripts/esperar_informes.py <AAAAMMDD> cnv bcra temas --minutos 45
```

## 5. Enviar el mail

Con la herramienta de Gmail, enviá un mail a **pedro.rossaroli@mitranicaballero.com**:

- Asunto: `BORA <DD/MM/AAAA> — <n> normas de organismos seguidos, <m> temas relevantes` (o `BORA <DD/MM/AAAA> — sin novedades`).
- Cuerpo, en este orden:
  1. **Organismos**: por organismo (CNV, ATEP, BCRA Com. "A", AAIP), cada norma con número, firmantes y el resumen del informe del especialista. Si un organismo no publicó nada, una línea "Sin publicaciones".
  2. **Temas de interés**: los relevantes y tangenciales según `informes/<AAAAMMDD>/temas.md`. Mencioná cuántos falsos positivos se descartaron.
  3. Link a cada norma en el Boletín Oficial (campo `url`).
- Si algún informe no llegó a tiempo, armá esa parte con los datos de `runs/<AAAAMMDD>.json` (número, firmantes, link) y aclarala como "sin análisis del especialista".

Si no hubo normas de organismos ni candidatos, mandá igual el mail "sin novedades" con la cantidad total de avisos de la edición.

## 6. Cierre

Respondé con un resumen de 3 a 5 líneas (se usa como notificación push).
