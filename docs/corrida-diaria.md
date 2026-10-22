# Corrida diaria

La ejecuta la tarea programada de lunes a viernes a las 05:55 (hora Argentina). Cada corrida arranca en una sesión nueva.

**Objetivo horario:** el mail tiene que salir entre las 07:00 y las 07:30. Nunca después de las 07:30: si algo se demora, mandá lo que tengas.

## 1. Descargar

```bash
python3 scripts/bora.py --esperar-minutos 50   # fecha de hoy (hora Argentina)
```

Si la edición todavía no está publicada, el script reintenta cada 5 minutos hasta 50 minutos. Corrélo en segundo plano (`run_in_background`) para no chocar con el timeout de comandos.

**Sitio del BORA bloqueado:** www.boletinoficial.gob.ar suele cortar las conexiones desde la nube ("Connection reset by peer"). El script lo detecta solo y baja el PDF del día de ARSAT (`s3.arsat.com.ar/cdn-bo-001/pdf-del-dia/primera.pdf`). **No hagas chequeos previos con curl ni bucles propios:** corré el script tal cual. Si `runs/<AAAAMMDD>.json` dice `"fuente": "pdf-arsat"`, los anexos publicados solo en la web no están: aclaralo en el mail con una línea al final. El PDF solo trae la edición del día, así que una edición perdida no se puede recuperar al día siguiente por esta vía.

Leé `runs/<AAAAMMDD>.json`. Si `total_avisos` es 0 después de esperar (feriado o edición demorada), terminá sin mensajes a especialistas y mandá un mail corto: "BORA <DD/MM/AAAA> — edición no publicada a las <hora>".

## 2. Commitear

Trabajá sobre `main` (la sesión puede arrancar en otra rama):

```bash
git checkout main && git pull --rebase origin main
git add organismos temas runs && git commit -m "corrida: <AAAAMMDD> descarga" && git push origin main
```

Si el push a `main` se rechaza, reintentá con `git pull --rebase` (hasta 4 veces). Si sigue rechazado, explicalo en el resumen final.

## 3. Análisis por subagentes

Las sesiones de la tarea programada **no tienen** la herramienta para escribirles a las sesiones especialistas. El análisis diario lo hacen **subagentes** (herramienta `Agent`), uno por destinatario, **en paralelo**. Cada subagente cumple el rol y escribe en el repo. La memoria vive en el repo (dossiers, informes y Normas consolidadas), así que las sesiones especialistas persistentes, que el usuario usa para consultas, la leen con `git pull`.

Destinatarios:

- un subagente por cada organismo con normas nuevas en `runs/<AAAAMMDD>.json`;
- un subagente para el Analista de Temas, si `temas_candidatos` no está vacío;
- un subagente Especialista CNV aunque no haya RG nuevas, si `organismos/cnv/normas-cnv/vigencias.md` tiene líneas `- [ ]` con fecha igual o anterior a hoy, o `pendientes.md` tiene líneas `- [ ]` de tipo `infoleg`.

Prompt de cada subagente (completá los datos):

```
Trabajás en /home/user/monitor-bora (rama main). Sos el <Especialista de organismo <slug> | Analista de Temas> del Monitor BORA.
Leé CLAUDE.md y <docs/especialista.md | docs/analista-temas.md> y seguilos al pie de la letra para la corrida <AAAAMMDD>.
Normas nuevas: <una línea por norma: título — archivo>   (Analista: candidatos en temas/candidatos/<AAAAMMDD>.md)
[Solo CNV, si corresponde] Entra en vigencia hoy: <líneas de vigencias.md>. Activalas con scripts/normas/activar_vigencias.py ANTES del informe.
[Solo CNV, si corresponde] Pendientes InfoLEG abiertos: <líneas>.
Prioridad: informes/<AAAAMMDD>/<slug>.md commiteado y pusheado a main antes de las 07:10 (hora Argentina). Después, dossier y consolidación.
Usá git pull --rebase antes de cada push: otros subagentes escriben en paralelo.
Al terminar, respondé en 3 líneas qué escribiste.
```

Si un subagente falla o no termina a tiempo, seguí con el mail y marcá esa parte como "sin análisis del especialista".

## 4. Verificar los informes

```bash
git pull --rebase origin main && ls informes/<AAAAMMDD>/
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
