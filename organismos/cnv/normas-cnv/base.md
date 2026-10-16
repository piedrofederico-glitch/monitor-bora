Estado: construcción terminada (última RG aplicada: 1173/2026)

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

Hecho el 16/10/2026 contra el texto actualizado de la RG 622/2013 en InfoLEG (`servicios.infoleg.gob.ar/infolegInternet/anexos/215000-219999/219405/texact.htm` y sus 88 páginas por título y capítulo). InfoLEG ya incorpora la RG 1173/2026 (Cap. XVIII del Tít. XVIII), así que el punto de corte es el mismo.

**Método:** por cada página de InfoLEG se tomó el o los archivos de `vigente/` equivalentes; se quitaron las notas de vigencia de ambos lados ("(Artículo sustituido por…)" y "[… RG n/aaaa …]") y se compararon las secuencias de palabras normalizadas (sin tildes, mayúsculas ni puntuación). Se descartaron los bloques que sólo cambian de lugar (tablas y glosario en otro orden) y se revisó a mano cada diferencia restante.

**Resultado:** 47 de las 88 páginas coinciden palabra por palabra con `vigente/`. En 31 las diferencias son de forma: tablas y formularios con otra disposición de columnas, erratas de uno u otro lado ("fncionar", "circnstancia", "trascurso", "habite"), "http/gob" frente a "https/gov", las anotaciones "Ver CRI n" del PDF de la CNV, que InfoLEG no trae, y siglas "ACyD/ACyDI" que InfoLEG no reemplazó. InfoLEG omite en varios capítulos la nota de RG aplicadas acá (por ejemplo, las RG 1090, 1095, 1107, 1144 y 1155), aunque su texto ya las refleja. Las 10 páginas restantes tienen las diferencias de fondo que siguen.

Diferencias de fondo:

| Ubicación | Diferencia | Tratamiento |
|---|---|---|
| Tít. I, Cap. II, arts. 2° y 3° | Faltaban en `vigente/` el párrafo “Mercado de Capitales”, “Oferta Pública”… “tienen el alcance previsto en el artículo 2º de la Ley Nº 26.831” y el de sinónimos de “Aportes irrevocables”. Se suprimieron por error al consolidar los arts. 3° y 4° de la RG 1131/2026, que no los modifican. | **Corregido** (commit "normas-cnv: corrige glosario…"), con nota en el texto, en el historial y en la ficha de la RG 1131. |
| Tít. I, Cap. II, art. 2° | InfoLEG conserva, junto a la redacción nueva, las versiones anteriores de “CEVA”, “IOSCO”, “Programa de CEDEAR o CEVA” y “Prospecto del Programa”. | Error de InfoLEG. Acá sólo figura la versión vigente. |
| Tít. V, Cap. II | InfoLEG puso la nueva Sección VI de la RG 1163/2026 en el lugar de la Sección IV (le faltan los arts. 53 a 55, criterios de valuación) y mantiene la Sección VI anterior (régimen de "adenda"). | Error de InfoLEG. La RG 1163, art. 4°, sustituye la Sección VI; acá está aplicada así, con vigencia desde el 23/10/2026. |
| Tít. V, Cap. III, Anexo III (Ficha Única, RG 1121/2026) | InfoLEG ubica el anexo en el Cap. III, igual que acá, pero no trae su contenido (publicado como imagen). | Se mantiene la transcripción de la imagen. Queda resuelta la duda de ubicación anotada en la ficha de la RG 1121. |
| Tít. V, Cap. VI, art. 9° | InfoLEG trae un cuarto párrafo ("En su caso, la Sociedad Gerente deberá proceder a la difusión de la información periódica reportada por los vehículos elegibles…") que no está en el PDF base. La RG 1089/2025, art. 14, sustituye el tercer párrafo y deja "(…)" después, lo que sugiere que el párrafo existe. | **No incorporado:** viene de antes de la base y la única fuente es InfoLEG. Pendiente de verificar contra la RG que lo dictó. |
| Tít. VI, Cap. I | InfoLEG mantiene la Sección XXXIV (art. 72, "Régimen informativo especial", incorporada por la RG 624/2014). | La RG 1094/2025, art. 5°, derogó la RG 624. Coincide con el PDF base, que no la trae. |
| Tít. VI, Cap. I, art. 70, inc. a.29) | InfoLEG: "Documentación vinculada para la previa aprobación de reglamentaciones dictadas por los Mercados"; PDF base: "Lista de Agentes autorizados por el Mercado para Acceso Directo al Mercado y los sistemas que se utilizarán". | Diferencia anterior a la base. Se mantiene el PDF de la CNV. |
| Tít. VI, Cap. I, Anexos III a V; Tít. VIII, Cap. I, anexo FIX | InfoLEG transcribe los "Lineamientos para la emisión de valores negociables temáticos" y el anexo de mensajería FIX; el PDF base sólo da el enlace. A la inversa, el PDF trae el texto de los Anexos IV y V (ISO 20022) que InfoLEG publica como archivo. | Diferencia de formato de la fuente. No se agregó texto. |
| Tít. VIII, Cap. I, art. 8°, inc. a) | InfoLEG: "a) Estatuto Social: Copia autenticada del estatuto social inscripto en el Registro Público de Comercio…"; el PDF base repite en el inc. a) el texto del inc. b) ("Prever en su objeto social…"). | Probable errata del PDF base, anterior a la RG 1094. Se mantiene el PDF; pendiente. |
| Tít. II, Cap. III, Anexo VI | Los dos textos conservan el Anexo VI de la RG 939/2022, que la RG 1127/2026 no menciona. | Coincide con el tratamiento de acá (ver la ficha de la RG 1127). |
| Tít. IV, Cap. III; Tít. XVI, Anexo II (RG 1165 y 1168); Tít. XIV, Cap. III, Anexo I (RG 1172) | InfoLEG no trae los modelos de estados contables, el cuadro de patrimonio neto mínimo por categoría, o los trae con otra disposición. | Diferencia de formato. Acá están como bloques preformateados. |
| Tít. XIV, Cap. II; Tít. XIX | InfoLEG conserva la página con la nota de derogación (RG 1118/2026 y RG 1109/2026). | Coincide: derogados. El texto anterior está en `historial/`. |

## Pendientes y vigencias diferidas

- Los pendientes de verificación están en `pendientes.md` (formato fijo, uno por línea).
- Las RG publicadas que todavía no rigen están en `vigencias.md`; su texto, en `diferido/`. `vigente/` es siempre lo que rige hoy. Desde el 16/10/2026 la RG 1163/2026 (vigencia 23/10/2026) está en `diferido/`.
- Observaciones de los textos originales, sin acción pendiente: la RG 1098/2025 repite la numeración del art. 5° (Secc. V, Cap. XV, Tít. XVIII), que la RG 1103/2026 reemplazó después por los arts. 9° y 10; el art. 26 de la Secc. XII del Cap. III del Tít. XVIII (RG 1148/2026) remite a un "artículo siguiente" que no existe.

## Herramientas

`scripts/normas/` (instructivo en `docs/normas-cnv.md`): aplicación de RG con historial, preparación de RG nuevas, consulta de redacciones por fecha o por RG, activación de vigencias diferidas y una prueba de reproducción. El texto de cada RG aplicada y sus metadatos están en `organismos/cnv/rg/fuentes/`; el índice de modificaciones y las denominaciones de los títulos, en `datos/`.
