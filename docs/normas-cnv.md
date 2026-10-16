# Normas CNV (N.T. 2013 y mod.) — texto consolidado con historial

Objetivo: que el Especialista CNV conozca el cuerpo completo de las Normas y la historia de cada artículo desde la RG 1094/2025 (BO 11/12/2025).

## Estructura

```
organismos/cnv/
  fuentes/                      PDF base provisto por el usuario (no se edita)
  normas-cnv/
    vigente/                    texto vigente, un archivo por capítulo
      titulo-XIV/capitulo-III.md
    historial/                  redacciones derogadas o sustituidas, mismo árbol que vigente/
      titulo-XIV/capitulo-III.md
    diferido/                   textos publicados que todavía no rigen (mismo árbol que vigente/)
      titulo-V/capitulo-II.md           el capítulo completo tal como rige desde la fecha diferida
      titulo-V/capitulo-II.historial.md lo que deja de regir ese día (pasa a historial/ al activarlo)
    vigencias.md                vigencias diferidas: una línea por archivo de diferido/
    pendientes.md               verificaciones pendientes (InfoLEG y otras): una línea por ítem
    modificaciones.md           índice inverso: ubicación → RG que la tocaron (se genera desde datos/)
    datos/                      modificaciones.json y titulos.json (los escriben las herramientas; no editar a mano)
    base.md                     de qué fuente y fecha sale la base, y verificaciones hechas
  rg/
    RG-1094-2025.md             una ficha por RG
    fuentes/                    texto de cada RG (<n>.txt, del PDF de la CNV o del BORA) y meta.json
scripts/normas/                 herramientas (ver "Herramientas")
```

`vigente/` es siempre **lo que rige hoy**. Una RG publicada con vigencia futura va a `diferido/` y se pasa a `vigente/` el día que empieza a regir.

### Archivos de `vigente/`

Un archivo por capítulo (o por sección si el capítulo es muy largo). Encabezado:

```
# Título XIV — Capítulo III: PSAV
Última modificación: RG 1172/2026 (BO 15/10/2026)
```

Cada artículo conserva su numeración y lleva al final una nota de vigencia entre corchetes, igual que InfoLEG:
`[Artículo sustituido por art. 2° de la RG 1172/2026, BO 15/10/2026]`.

### Archivos de `historial/`

Cada vez que un artículo, sección o capítulo se sustituye o deroga, su redacción anterior se mueve acá **antes** de reemplazarla:

```
## Artículo 40
- Vigente desde: <fecha o "anterior a la base">
- Vigente hasta: 15/10/2026
- Reemplazado/derogado por: RG 1172/2026, art. 2°
- Texto:
> ...
```

Nada se borra sin dejar constancia en `historial/`. El historial de git es un respaldo, no la fuente de consulta.

### Fichas `rg/RG-<número>-<año>.md`

Número, código GDE, fecha de firma, publicación en el BO y vigencia, firmantes, resumen (3 a 6 viñetas), y una tabla de afectaciones:

| Ubicación en las Normas | Operación | Artículo de la RG |
|---|---|---|
| Tít. XIV, Cap. III (completo) | sustituye | 2° |
| Tít. XVIII, Cap. XIV, art. 5° | incorpora | 4° |

Operaciones: sustituye, incorpora, deroga, modifica parcialmente, renumera. Las RG que no tocan las Normas (por ejemplo, designaciones o consultas públicas) también llevan ficha, con la tabla de afectaciones vacía.

## Construcción inicial (una sola vez)

Terminada el 16/10/2026 (última RG aplicada: 1173/2026). Se deja como referencia.

1. **Base.** Convertí el PDF de `organismos/cnv/fuentes/` a texto y dividilo en `vigente/` por título y capítulo. Registrá en `base.md` el nombre del archivo y la fecha de actualización que declara el PDF.
2. **Verificar el punto de corte.** Comprobá con el texto de la RG 1094/2025 si el PDF ya la incluye: buscá los artículos que esa RG sustituye o incorpora y compará la redacción. Anotá el resultado en `base.md`.
   - Si la incluye: la base es el estado posterior a la 1094. Su ficha indica "incorporada en la base".
   - Si no la incluye: aplicá la 1094 como primera RG del paso 3.
   - Si el PDF incluye RG posteriores a la 1094, ajustá el punto de partida y dejalo documentado.
3. **Aplicar las RG en orden cronológico**, desde la siguiente al corte hasta la última publicada. El listado completo está en `https://www.cnv.gov.ar/sitioWeb/MarcoRegulatorio?panel=2`. El texto de cada RG se saca del Boletín Oficial (`scripts/bora.py` resuelve la descarga por fecha) o del sitio de la CNV. Para cada RG:
   1. Escribí la ficha.
   2. Pasá las redacciones afectadas a `historial/`.
   3. Actualizá `vigente/` con las notas de vigencia.
   4. Actualizá `modificaciones.md`.
   5. Hacé **un commit por RG**: `normas-cnv: aplica RG <n>/<año>`.
4. **Control contra InfoLEG.** InfoLEG publica el texto actualizado de las Normas: es el anexo de la RG 622/2013, `https://servicios.infoleg.gob.ar/infolegInternet/anexos/215000-219999/219405/texact.htm` y sus vínculos por título. Al terminar, compará por capítulo `vigente/` contra InfoLEG. Registrá las diferencias en `base.md`, con la explicación de cada una (error propio, demora de InfoLEG, criterio de consolidación).

5. **Cierre.** Si mientras trabajabas se publicaron RG nuevas, aplicalas también. Al final, escribí en la primera línea de `base.md`: `Estado: construcción terminada (última RG aplicada: <n>/<año>)`. Desde ese momento, el mantenimiento pasa al Especialista CNV.

## Mantenimiento diario (Especialista CNV)

El mail de la corrida depende del informe del día, así que **el informe va primero** y la consolidación después.

Cuando llega una RG nueva de la CNV:

1. **Informe del día** (`docs/especialista.md`), commit y push. Si la RG modifica las Normas, decilo en el informe y aclará que la consolidación sigue.
2. **Ficha y aplicación con historial.** Con las herramientas (ver abajo): preparar la RG, escribir `scripts/normas/rgops/<n>.py`, correrlo, revisar el diff y commitear: `normas-cnv: aplica RG <n>/<año>`. Las RG que no tocan las Normas también llevan ficha.
   - Si la RG tiene vigencia diferida (rige desde una fecha posterior al día siguiente de su publicación), aplicala en `diferido/` y agregá la línea en `vigencias.md` (ver "Vigencias diferidas").
   - Si la RG toca un capítulo que tiene una versión en `diferido/`, aplicala a las dos versiones (ver "Vigencias diferidas").
3. **Control contra InfoLEG del capítulo afectado** (texto actualizado de la RG 622/2013: `https://servicios.infoleg.gob.ar/infolegInternet/anexos/215000-219999/219405/texact.htm` y sus páginas por título y capítulo). Si InfoLEG todavía no incorporó la RG, agregá una línea `infoleg` en `pendientes.md`.
4. **Completá el informe** con los artículos que cambiaron y el enlace a la redacción anterior en `historial/` (o a `diferido/`), en un segundo commit.

En cada corrida, aunque no haya RG nuevas:
- Revisá `pendientes.md`: reintentá los controles `infoleg` abiertos y cerrá los que ya se puedan cerrar (`[x]` y ` → resuelto AAAA-MM-DD: <cómo>`).
- Revisá `vigencias.md`: si alguna fecha llegó, activala (ver "Vigencias diferidas").

## Herramientas (`scripts/normas/`)

Todas se corren desde la raíz del repo. Antes de usarlas por primera vez en una sesión, corré la prueba:

```bash
python3 scripts/normas/prueba.py        # reaplica la RG 1172 sobre el estado anterior; tiene que decir OK
```

**1. Preparar la RG** (texto y metadatos en `organismos/cnv/rg/fuentes/`):

```bash
python3 scripts/normas/preparar_rg.py <n> --bora organismos/cnv/normas/<AAAAMMDD>_<id>_resolucion-general-<n>-<año>.md
```

Busca el PDF de la CNV en el listado de RG y lo convierte con `pdftotext -layout`. Si la CNV todavía no lo subió, usa el texto del BORA y lo avisa: en ese caso revisá a mano las tablas. Cuando aparezca el PDF podés volver a correrlo con `--pdf <url>`.

**2. Escribir el script de la RG** en `scripts/normas/rgops/<n>.py`. Hay uno por cada RG aplicada desde la 1090: copiá el de una RG parecida. Esquema:

```python
import normas as N, fichas
n = 1172
b = lambda k: N.md(N.bloque(n, k))        # párrafos del texto citado en el art. k de la RG
N.glosario(N.definiciones(b(1)), n=n, art_rg=1)                       # términos del art. 2° del Tít. I
ps = b(2); assert ps[0] == 'CAPÍTULO III'
N.sustituir_capitulo('XIV', 'III', ps[1], ps[2:], n, 2)               # capítulo completo
N.modificar_articulo('XV', 'I', '11', N.parrafo('18) PSAV_014 - …', [nuevo], hasta_siguiente_termino=False),
                     n, 3, 'Subinciso 18) del inciso S) sustituido', det_extra='inc. S), subinc. 18)')
N.incorporar_articulo('XVIII', 'XIV', b(4), n, 4, despues_de='4')
fichas.ficha(n, ['resumen en 3 a 6 viñetas'], notas=['notas de consolidación'])
```

Operaciones disponibles en `normas.py`: `sustituir_articulo`, `modificar_articulo` (con `parrafo`, `tramo`, `insertar_antes`, `insertar_despues`, `ultimo_parrafo`), `incorporar_articulo`, `derogar_articulo`, `sustituir_seccion`, `derogar_seccion`, `incorporar_seccion`, `sustituir_capitulo` (también para incorporar uno nuevo, con `nota_tipo='Capítulo incorporado'`), `derogar_capitulo`, `renumerar_articulo/seccion/capitulo`, `sustituir_titulo`, `incorporar_anexo`, `sustituir_anexo`, `suprimir_anexo`, `glosario`, `suprimir_terminos`, `reemplazo_global`, `sustituir_denominacion_titulo`. Cada una guarda la redacción anterior en `historial/`, agrega la nota de vigencia y registra la afectación en `datos/modificaciones.json` y `modificaciones.md`. Para la ficha de una consulta pública: `fichas.ficha_consulta(n)`. Si la vigencia no es la del día siguiente a la publicación, poné `N.VIGENCIAS[n] = 'dd/mm/aaaa'` al principio del script.

Cuidado con `parrafo(...)`: por defecto reemplaza también los párrafos siguientes hasta el próximo término “…” significa del glosario. Fuera del glosario usá `hasta_siguiente_termino=False`, y aun en el glosario revisá el diff (así se perdieron dos párrafos al aplicar la RG 1131).

**3. Correr, revisar y cerrar:**

```bash
cd scripts/normas && PYTHONPATH=. python3 rgops/<n>.py && cd ../..
git diff --stat organismos/cnv          # revisá vigente/, historial/, modificaciones.md y la ficha
python3 -c "import sys; sys.path.insert(0, 'scripts/normas'); import normas; normas.cierre(<n>)"   # INDICE.md y línea de estado de base.md
```

Si algo salió mal: `git checkout -- organismos/cnv && git clean -fd organismos/cnv` y volvé a correr. Después, commit y push.

## Vigencias diferidas

`vigente/` tiene lo que rige hoy; lo publicado que rige desde una fecha futura está en `diferido/` y en `vigencias.md`.

Formato de `vigencias.md`, una línea por archivo de `diferido/`:

```
- [ ] AAAA-MM-DD · RG n/año · ubicación · diferido/titulo-X/capitulo-Y.md
```

**Aplicar una RG de vigencia diferida:** poné `N.VIGENCIAS[n] = 'dd/mm/aaaa'` en el script y corrélo contra `diferido/`:

```bash
cd scripts/normas && NORMAS_VIG=../../organismos/cnv/normas-cnv/diferido PYTHONPATH=. python3 rgops/<n>.py && cd ../..
```

Las herramientas copian el capítulo desde `vigente/` la primera vez, escriben las redacciones que dejarán de regir en `diferido/<capítulo>.historial.md` y marcan la afectación en `modificaciones.md` con "rige desde …". Agregá una línea en `vigencias.md` por cada archivo de `diferido/` que haya tocado la RG. La ficha va a `rg/` como siempre.

**Una RG común que toca un capítulo con versión en `diferido/`:** aplicala dos veces. Primero normal (vigente/ e historial/). Después, sobre la copia diferida y sin volver a registrar el historial:

```bash
cd scripts/normas && NORMAS_VIG=../../organismos/cnv/normas-cnv/diferido NORMAS_SIN_REGISTRO=1 PYTHONPATH=. python3 rgops/<n>.py && cd ../..
```

Si la RG cambia justo un texto que la RG diferida también reemplaza, revisá a mano `diferido/<capítulo>.historial.md`: tiene que guardar la redacción que rige hasta la fecha diferida.

**El día de entrada en vigencia** (lo avisa la corrida diaria):

```bash
python3 scripts/normas/activar_vigencias.py --ver     # qué hay pendiente
python3 scripts/normas/activar_vigencias.py           # activa todo lo que vence hoy o antes
```

Para cada línea vencida: pasa a `historial/` lo que deja de regir (`diferido/<capítulo>.historial.md`), mueve `diferido/<capítulo>.md` a `vigente/`, quita la marca "rige desde" de `modificaciones.md`, regenera `INDICE.md` y marca la línea con `[x]`. Revisá el diff y commiteá: `normas-cnv: <fecha> entra en vigencia RG <n>/<año>`. Mencionalo en el informe del día.

## Pendientes

`pendientes.md`, un ítem por línea:

```
- [ ] AAAA-MM-DD · tipo (infoleg|otro) · ubicación · detalle
```

La fecha es la de alta. `infoleg`: el control del capítulo contra InfoLEG que no se pudo hacer porque InfoLEG todavía no incorporó la RG. Al cerrar: `- [x] … → resuelto AAAA-MM-DD: <cómo>`.

## Consultas

Para responder con el texto literal qué cambió una RG o cómo era un artículo, usá `consultar.py` (lee `vigente/`, `historial/`, `diferido/` y `datos/modificaciones.json`):

```bash
# ¿Qué cambió la RG 1172 en las Normas? Lista de afectaciones y dónde está cada texto anterior
python3 scripts/normas/consultar.py --rg 1172
python3 scripts/normas/consultar.py --rg 1172 --completo                          # con todos los textos anteriores

# ¿Cómo era el art. 40 del Cap. III del Tít. XIV antes de la RG 1172, y cómo quedó?
python3 scripts/normas/consultar.py --ubicacion "Tít. XIV Cap. III art. 40" --rg 1172

# ¿Qué decía el art. 40 al 1/10/2026?
python3 scripts/normas/consultar.py --ubicacion "Tít. XIV Cap. III art. 40" --fecha 2026-10-01

# Todas las redacciones de un artículo, de la más vieja a la vigente (y la diferida, si hay)
python3 scripts/normas/consultar.py --ubicacion "Tít. V Cap. VII art. 27 TER"
```

La ubicación acepta `Tít.`, `Cap.`, `Secc.`, `art.` (con BIS, TER, etc.) y `Anexo`. Si el número de artículo se repite en el capítulo, agregá la sección. Cada respuesta indica de qué archivo sale el texto y entre qué fechas rigió.

Para leer la salida conviene saber:
- Una entrada del historial marcada "fragmento" guarda sólo la parte reemplazada (un inciso, un término del glosario); el resto del artículo era igual al de la versión siguiente.
- "Vigente desde: … o antes" significa que es la fecha de la última modificación conocida desde la base. Lo anterior a la RG 1094/2025 figura como "anterior a la base": para eso no hay historial en el repo.
- Sin la herramienta, la misma respuesta sale de: `modificaciones.md` (qué ubicaciones tocó la RG y en qué archivo), `historial/<capítulo>.md` (buscar "por: RG <n>/": ahí están el texto anterior y sus fechas) y `vigente/<capítulo>.md` o `diferido/<capítulo>.md` (el texto posterior, con la nota de la RG).
