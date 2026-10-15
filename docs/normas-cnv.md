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
    modificaciones.md           índice inverso: ubicación → RG que la tocaron
    base.md                     de qué fuente y fecha sale la base, y verificaciones hechas
  rg/
    RG-1094-2025.md             una ficha por RG
```

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

## Mantenimiento diario (Especialista CNV)

Cuando llega una RG nueva:
1. Ficha en `rg/`.
2. Si modifica las Normas: aplicala con historial, como en el paso 3.
3. Control contra InfoLEG del capítulo afectado. Si InfoLEG todavía no lo actualizó, anotalo como pendiente en `base.md` y revisalo en la corrida siguiente.
4. En el informe del día, indicá qué artículos cambiaron y enlazá la redacción anterior en `historial/`.
