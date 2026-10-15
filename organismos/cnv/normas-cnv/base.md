Estado: construcción en curso (última RG aplicada: 1115/2026)

# Base del texto consolidado de las Normas CNV (N.T. 2013 y mod.)

## Fuente

- **Archivo:** `organismos/cnv/fuentes/NORMAS CNV 2013 HASTA RG 1094 (NO INCLUYE RG 1090).pdf`.
- **Datos del PDF:** 989 páginas A4; creado el 12/12/2025 12:20 UTC con Microsoft Word 365; título interno "TOC2013"; autores "Piacentini Franco; Ramos María Alejandra".
- **Fecha de actualización que declara:** portada, "Última actualización incorporada mediante R.G. N° 1094 (B.O. 11/12/2025)".
- **Nombre del archivo:** declara que no incluye la RG 1090/2025. Verificado abajo.

## Conversión a `vigente/`

- Texto extraído con `pdftotext -layout`. Se quitaron encabezados y pies de página ("NORMAS — AÑO 2013", "COMISIÓN NACIONAL DE VALORES", número de página), las páginas 1 a 20 (índice) y las carátulas de cada título.
- Un archivo por capítulo (`titulo-II/capitulo-V.md`); los títulos sin capítulos (I, X, XI, XIX) van en `titulo-<n>/titulo-<n>.md`. El índice de archivos está en `vigente/INDICE.md`.
- Los renglones del PDF se unieron en párrafos. Las secciones y anexos van como encabezados `### `; el epígrafe de cada artículo queda en el renglón anterior a "ARTÍCULO N".
- **Tablas y formularios:** las zonas con columnas se copiaron como bloques de texto preformateado (```), con la disposición del PDF. Son legibles, pero la alineación de columnas puede no ser exacta; ante duda, consultar el PDF (cada archivo indica las páginas de origen).
- **Control de integridad:** se compararon las palabras de `vigente/` contra las del PDF (págs. 21 a 989). Las únicas diferencias son los nombres de título y capítulo que pasaron al encabezado de cada archivo y las carátulas.
- El PDF no trae notas de vigencia por artículo. Las notas `[Artículo sustituido por ...]` se agregan sólo para las RG aplicadas desde la base.

## Verificación del punto de corte

### RG 1094/2025 (BO 11/12/2025): incorporada

Se buscó en el PDF cada texto que la RG 1094 sustituye o incorpora:

| Disposición de la RG 1094 | Ubicación en las Normas | Resultado en el PDF |
|---|---|---|
| Art. 1°: inciso viii) del art. 25 | Tít. VII, Cap. II | presente (pág. 611): "viii) Con periodicidad mensual, dentro del tercer (3er) día hábil..." |
| Art. 2°: art. 35 "RÉGIMEN INFORMATIVO DE PASIVOS FINANCIEROS" | Tít. VII, Cap. II | presente (pág. 613) |
| Art. 3°: apartado 43 del inc. L) del art. 11 | Tít. XV, Cap. I | presente (pág. 879): "43) AGE_ 030– Pasivos Financieros." |
| Art. 4°: art. 21 "CRONOGRAMA DE CUMPLIMIENTO" | Tít. XVIII, Cap. V | presente (pág. 935) |
| Art. 5°: deroga la RG 624 | fuera de las Normas | no aplica |

Conclusión: la base es el estado posterior a la RG 1094. Ficha: `rg/RG-1094-2025.md`.

### RG 1090/2025 (BO 14/11/2025): no incorporada, vigencia diferida

- La RG 1090 ("Valores negociables de emisión individual") se publicó antes que la 1094, pero su art. 9° fija la entrada en vigencia el **2 de febrero de 2026**. Por eso la CNV no la volcó en el texto ordenado del 12/12/2025, que refleja sólo normas vigentes a esa fecha.
- Comprobación en el PDF: el art. 29 de la Secc. IX del Cap. I del Tít. VI conserva la redacción anterior; el Cap. V del Tít. VI mantiene las Secciones X a XXI (cheques de pago diferido, pagarés, etc.) y el Tít. VI no tiene Capítulo VI.
- Qué modifica: sustituye el art. 29 (Tít. VI, Cap. I, Secc. IX); deroga las Secciones X, XI, XII, XIV, XV, XVI, XVII, XX y XXI del Cap. V del Tít. VI; renumera las Secciones XVIII y XIX como X y XI y sus artículos 65 a 72 como 27 a 34; incorpora el Cap. VI del Tít. VI ("Negociación secundaria de valores negociables de emisión individual que gozan de oferta pública") y los arts. 14 del Cap. IV y 6° del Cap. XI del Tít. XVIII.
- Tratamiento: se aplica como primera RG, antes de la 1095, con vigencia indicada en cada nota ("vigente desde 02/02/2026"). La RG 1107/2026 (BO 13/02/2026) volvió a modificar ese régimen y se aplica en su orden.

### Otras RG anteriores a la 1094 con vigencia diferida

Se revisaron los artículos de vigencia de las RG 1033 a 1094:

| RG | Vigencia | ¿Reflejada en el PDF? |
|---|---|---|
| 1033/2024 (prorrogada por RG 1045 y 1052) | 16/01/2025 | sí (vigente antes del corte) |
| 1077/2025 | 01/09/2025 | sí: Secc. III del Cap. I y art. 9° de la Secc. II del Cap. II del Tít. XIII presentes |
| 1082/2025 | 15/09/2025 | sí: Anexo II del Cap. II del Tít. XVI; su Secc. XXIX del Cap. III del Tít. XVIII fue absorbida por la reordenación de la RG 1089 |
| 1092/2025 | 01/12/2025 | sí: inciso b) del art. 15 (Tít. V, Cap. II) con la redacción de la RG 1092 |
| 1093/2025 | desde su dictado (28/11/2025) | sí: art. 6° TER del Cap. V del Tít. XVIII |
| 1090/2025 | 02/02/2026 | **no** (ver arriba) |

Otras disposiciones con plazos de cumplimiento futuros (RG 1046, 1048, 1058, 1080) ya están en el texto del PDF: son plazos de adecuación dentro de normas vigentes, no vigencias diferidas.

## Punto de partida

Base = PDF CNV actualizado a la RG 1094/2025 (BO 11/12/2025), sin la RG 1090/2025. Orden de aplicación: RG 1090/2025 y luego las RG 1095/2025 a la última publicada, en orden de número (coincide con el orden de publicación en el BO).

## Control contra InfoLEG

Pendiente: se hace al terminar de aplicar las RG.
