# Corrida diaria

La ejecuta la tarea programada de lunes a viernes a las 05:55 (hora Argentina). Cada corrida arranca en una sesión nueva.

**Objetivo horario:** el mail tiene que salir entre las 07:00 y las 07:30. Nunca después de las 07:30: si algo se demora, mandá lo que tengas.

## 1. Descargar

```bash
python3 scripts/bora.py --esperar-minutos 50   # fecha de hoy (hora Argentina)
```

Si la edición todavía no está publicada, el script reintenta cada 5 minutos hasta 50 minutos. Corrélo en segundo plano (`run_in_background`) para no chocar con el timeout de comandos.

Leé `runs/<AAAAMMDD>.json`. Si `total_avisos` es 0 después de esperar (feriado o edición demorada), terminá sin mensajes a especialistas y mandá un mail corto: "BORA <DD/MM/AAAA> — edición no publicada a las <hora>".

## 2. Commitear

```bash
git add organismos temas runs && git commit -m "corrida: <AAAAMMDD> descarga" && git push origin main
```

## 3. Repartir

Con los IDs de `config/sesiones.json`, mandá un mensaje con la herramienta **`mcp__claude-code-remote__send_message`** (`session_id` + `message`) a los destinatarios de abajo. `SendMessage` es otro canal y no llega a esas sesiones.

**Plan B, si `mcp__claude-code-remote__send_message` no está disponible:** lanzá un subagente (herramienta `Agent`) por cada destinatario, con el mismo mensaje y la instrucción de leer `CLAUDE.md` y su doc de rol (`docs/especialista.md` o `docs/analista-temas.md`). La memoria está en el repo, así que el resultado es equivalente. Aclaralo en el resumen final.

Destinatarios:

- cada especialista de organismo que tenga normas nuevas en `runs/<AAAAMMDD>.json` → `organismos.<slug>`;
- el Analista de Temas, si `temas_candidatos` no está vacío.

Formato del mensaje:

```
Corrida <AAAAMMDD>. Normas nuevas de <slug>:
- <titulo> — <archivo>
Seguí docs/especialista.md (o docs/analista-temas.md).
```

No mandes mensaje a quien no tiene novedades, con una excepción: el Especialista CNV.

### Especialista CNV: vigencias y pendientes

Revisá también:

- `organismos/cnv/normas-cnv/vigencias.md`: líneas `- [ ]` con fecha **igual o anterior a hoy** (entradas en vigencia que corresponden a hoy o quedaron atrasadas).
- `organismos/cnv/normas-cnv/pendientes.md`: líneas `- [ ]` de tipo `infoleg`.

Si hay alguna, agregalas al mensaje del Especialista CNV, o mandale uno aunque no haya RG nuevas:

```
Corrida <AAAAMMDD>.
Entra en vigencia hoy: <una línea por entrada de vigencias.md>
Pendientes InfoLEG abiertos: <una línea por ítem>
Activá las vigencias con scripts/normas/activar_vigencias.py ANTES de escribir el informe y seguí docs/especialista.md.
```

Si hay vigencias del día, esperá el informe `cnv` en el paso 4 aunque no haya RG nuevas: el especialista lo escribe con la sección "Entra en vigencia hoy". Si solo hay pendientes InfoLEG, no lo esperes.

## 4. Esperar los informes

Corré en segundo plano (`run_in_background`), con los slugs a los que escribiste (`temas` para el Analista):

```bash
python3 scripts/esperar_informes.py <AAAAMMDD> cnv bcra temas --minutos 45 --hasta 07:15
```

## 5. Enviar el mail

Con la herramienta de Gmail, enviá un mail a **pedro.rossaroli@mitranicaballero.com**:

- Asunto: `BORA <DD/MM/AAAA> — <n> normas de organismos seguidos, <m> temas relevantes` (o `BORA <DD/MM/AAAA> — sin novedades`).
- Cuerpo, en este orden:
  0. **Entra en vigencia hoy** (solo si `vigencias.md` tiene entradas con la fecha de hoy): RG, ubicación en las Normas y una frase del informe del Especialista CNV sobre qué cambia. Si el informe no llegó, poné solo RG y ubicación.
  1. **Organismos**: por organismo (CNV, ATEP, BCRA Com. "A", AAIP), cada norma con número, firmantes y el resumen del informe del especialista. Si un organismo no publicó nada, una línea "Sin publicaciones".
  2. **Temas de interés**: los relevantes y tangenciales según `informes/<AAAAMMDD>/temas.md`. Mencioná cuántos falsos positivos se descartaron.
  3. Link a cada norma en el Boletín Oficial (campo `url`).
- Si algún informe no llegó a tiempo, armá esa parte con los datos de `runs/<AAAAMMDD>.json` (número, firmantes, link) y aclarala como "sin análisis del especialista".

Si no hubo normas de organismos ni candidatos, mandá igual el mail "sin novedades" con la cantidad total de avisos de la edición.

## 6. Cierre

Respondé con un resumen de 3 a 5 líneas (se usa como notificación push).
