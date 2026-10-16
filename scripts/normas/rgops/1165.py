import normas as N, fichas
n = 1165
b = lambda k: N.md(N.bloque(n, k))
N.glosario(N.definiciones(b(1)), n=n, art_rg=1)
N.sustituir_articulo('VIII', 'I', '7', b(2), n, 2, seccion='II')
N.sustituir_articulo('VIII', 'I', '10', b(3), n, 3, seccion='IV')
N.sustituir_articulo('VIII', 'I', '12', b(4), n, 4, seccion='IV')
N.incorporar_seccion('XVI', 'I', b(5), n, 5)
ax = N.md(N.rg_anexo(n, inicio=r'^\s*MATRIZ DE COMPATIBILIDADES\s*$'))
ax = ['### ANEXO II',
      '[Nota de consolidación: el Anexo (IF-2026-85043558-APN-GAL#CNV) no lleva el rótulo "ANEXO II"; se agrega como encabezado según el art. 6° de la RG 1165/2026. '
      'Tiene carátula gráfica (pág. 7 del PDF CNV) y el cuadro de la matriz se transcribe como texto preformateado; las referencias numeradas remiten a las celdas del cuadro.]'] + ax
N.incorporar_anexo('XVI', 'I', ax, n, 6, nombre='Anexo II')
fichas.ficha(n, [
    'Crea la Matriz de Compatibilidades entre Agentes registrados, Mercados, Cámaras Compensadoras y otros sujetos registrados (Secc. III del Cap. I del Tít. XVI, art. 9°, y Anexo II): sistematiza qué categorías pueden combinarse y con qué patrimonio neto mínimo y contrapartida líquida.',
    'La matriz no crea ni modifica categorías y prevalecen las normas de cada categoría ante cualquier diferencia.',
    'Sustituye los arts. 7° (Secc. II) y 10 y 12 (Secc. IV) del Cap. I del Tít. VIII (patrimonio neto mínimo del ADCVN y supuestos de inscripción simultánea, por ejemplo como Fiduciario Financiero).',
    'Incorpora un término al glosario del Tít. I.'],
    notas=['El cuadro de la matriz usa las siglas "ACyD" y "ACyDI" (anteriores a la RG 1131); se transcriben tal como se publicaron.'])
