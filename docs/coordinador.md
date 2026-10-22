# Coordinador del Monitor BORA

Rol de la sesión "BORA | Titiritero de Especialistas" (`session_01H94fzoiF4eNv1jsU863j4c`). La usa el usuario para diseñar, supervisar y corregir el sistema. Si el contexto se reinicia, leé este archivo y `CLAUDE.md` antes de responder.

## Qué coordina

| Pieza | Dónde |
|---|---|
| Corrida diaria: tarea "Monitor BORA diario" (`trig_01Tf6rjzxoETqWzweExb7gBg`), lunes a viernes 05:55 ART, Sonnet 5.5, conector Gmail, repo como fuente | `docs/corrida-diaria.md` |
| Análisis diario: subagentes lanzados por la corrida (especialistas por organismo + Analista de Temas). Las tareas programadas **no pueden** escribirles a otras sesiones | `docs/especialista.md`, `docs/analista-temas.md` |
| Sesiones persistentes para consultas del usuario (Sonnet 5.5) | `config/sesiones.json` |
| Normas CNV consolidadas (vigente, historial, diferido, vigencias, pendientes, consultas literales) | `docs/normas-cnv.md`, `scripts/normas/` |
| Mail diario a pedro.rossaroli@mitranicaballero.com antes de las 07:30, push al celular | paso 5 de `docs/corrida-diaria.md` |

Sesión "BORA · Construcción Normas CNV" (`session_01P8UW4YhrMt93x9k3my9KTD`, Opus): terminó la consolidación. **No tocarla** sin pedido del usuario.

## Lecciones aprendidas

- Una tarea programada solo puede pushear si el repo está cargado como **fuente** de la tarea. Eso lo agrega el usuario en claude.ai: `update_trigger` no permite cambiar fuentes. Síntoma: push 403 y memoria perdida al día siguiente.
- Las sesiones que abre una tarea no tienen `mcp__claude-code-remote__send_message`, así que el reparto se hace con subagentes (`Agent`).
- Los conectores (Gmail) tampoco se pueden asignar a una tarea desde una sesión. Los agrega el usuario en claude.ai.
- El modelo de una sesión existente no se puede cambiar: hay que crear una sesión nueva. El esfuerzo no se puede fijar por herramienta.
- **El sitio del BORA bloquea la nube** ("Connection reset by peer", 22/10/2026). Ninguna sesión, tarea ni subagente cloud lo evita: salen por la misma red. `bora.py` cae solo al PDF del día de ARSAT (`s3.arsat.com.ar/cdn-bo-001/pdf-del-dia/primera.pdf`), que trae texto, firmantes e IDs de aviso, pero no los anexos publicados solo en la web, y se pisa al día siguiente. Para tener anexos, la alternativa es una sesión en una computadora del usuario (IP argentina).
- Para revisar una corrida: `get_trigger` → `last_run.session_id` → `list_events` (kinds `result`), y `git pull` para ver commits, `runs/` e `informes/`.

## Otro sistema del usuario (no es Monitor BORA)

Seguimiento de privatizaciones, coordinado por la sesión "Nodriza de Privatizaciones" (`session_01FETWx2qdebcoAFXHjEKajd`), repo `piedrofederico-glitch/privatizaciones-ycrt-nasa`, 5 tareas "Privatizaciones · …" (Termoeléctricas, ENARSA, NASA, CNEA, Río Turbio). El 21/10/2026 tenían el mismo problema de fuentes; el usuario las corrigió ese día. El 22/10 se le compartió el respaldo por PDF de ARSAT (commit 737d7cd).

## Estado y pendientes

Actualizar esta sección cada vez que cambie algo.

- 23/10/2026 07:40 ART: revisión programada (`trig_01EGg62n3cvTjZmQ13BRMkkG`) de la entrada en vigencia de la RG CNV 1163 (5 entradas en `organismos/cnv/normas-cnv/vigencias.md`) y del mail con "Entra en vigencia hoy".
- `organismos/cnv/normas-cnv/pendientes.md`: 7 verificaciones manuales abiertas (3 diferencias PDF/InfoLEG, 3 anexos en imagen, fecha de vigencia de la RG 1163). Las 3 diferencias y la fecha conviene que las revise alguien del estudio.
- Validar que el primer push de las 5 tareas de privatizaciones funcione (corrida del 22/10).

## Estilo con el usuario

Español rioplatense con voseo, técnico y conciso, sin preámbulos ni cierres tipo "En resumen". Antes de acciones externas o irreversibles, confirmar con el usuario.
