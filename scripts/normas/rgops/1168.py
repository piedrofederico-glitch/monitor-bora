import normas as N, fichas
n = 1168
N.VIGENCIAS[n] = '23/09/2026'
ax = N.md(N.rg_anexo(n, inicio=r'^\s*MATRIZ DE COMPATIBILIDADES\s*$'))
ax = ['### ANEXO II',
      '[Nota de consolidación: texto del Anexo IF-2026-91311509-APN-GAYM#CNV, que reemplaza al Anexo de la RG 1165/2026 por sustitución del art. 6° de esa RG (art. 1° de la RG 1168/2026). '
      'El documento no lleva el rótulo "ANEXO II"; el cuadro de la matriz se transcribe como texto preformateado.]'] + ax
N.sustituir_anexo('XVI', 'I', 'II', ax, n, 1)
fichas.ficha(n, [
    'Sustituye el art. 6° de la RG 1165 para reemplazar el Anexo de la Matriz de Compatibilidades (Anexo II del Cap. I del Tít. XVI) por un nuevo documento (IF-2026-91311509-APN-GAYM#CNV).',
    'Corrige el patrimonio neto mínimo total (PNMT) de la categoría ALyC I AGRO, consignado por error en la versión anterior.',
    'Reescribe las referencias de los Agentes del Tít. V (FCI y FF) con los montos de PNMT y contrapartida líquida mínima total (CLMT) y las excepciones, y agrega remisiones a los artículos de las Normas que rigen cada categoría.',
    'Usa las siglas ACD y ACDI en el cuadro.'],
    vigencia='23/09/2026', vigencia_txt='art. 2°: desde el día de su publicación en el BO',
    notas=['La RG 1168 no modifica formalmente las Normas sino el art. 6° de la RG 1165; como su efecto es sustituir el texto del Anexo II del Cap. I del Tít. XVI, se registró como sustitución de ese anexo.'])
