# Monitor BORA

Monitoreo diario de la primera sección del Boletín Oficial de la República Argentina (BORA).

## Piezas

- `scripts/bora.py`: descarga la edición del día, baja texto y anexos de cada aviso y separa:
  - normas de los organismos de `config/organismos.json` → `organismos/<slug>/normas/`
  - candidatos por palabras clave de `config/temas.json` → `temas/textos/` y `temas/candidatos/<AAAAMMDD>.md`
  - resumen de la corrida → `runs/<AAAAMMDD>.json`
- `config/sesiones.json`: IDs de las sesiones especialistas (una por organismo + Analista de Temas).
- `informes/<AAAAMMDD>/<slug>.md`: informe del día de cada especialista.
- `organismos/<slug>/dossier.md` y `temas/<tema>/dossier.md`: memoria acumulada de cada especialista.

## Roles

| Rol | Instrucciones |
|---|---|
| Corrida diaria (tarea programada) | `docs/corrida-diaria.md` |
| Especialista de organismo (CNV, ATEP, BCRA, AAIP) | `docs/especialista.md` |
| Analista de Temas | `docs/analista-temas.md` |

## Reglas comunes

- Redactá en español rioplatense, técnico y conciso. Citá siempre número de norma, código GDE y firmantes tal como figuran en el texto.
- No inventes contenido: si un anexo no se publicó o no se pudo bajar, decilo.
- Antes de commitear: `git pull --rebase origin main`. Si el push falla por conflicto, repetí pull --rebase y push (hasta 4 veces).
- Mensajes de commit en español, cortos: `<rol>: <fecha> <qué>`.
