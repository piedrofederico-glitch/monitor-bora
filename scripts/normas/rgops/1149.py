import normas as N, fichas
n = 1149
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
ult = lambda k: [p for p in md(k) if p not in ('(…)', '(...)') and not N.clave_art(p)]
p1 = ult(1); assert len(p1) == 1
N.modificar_articulo('II', 'V', '14', N.ultimo_parrafo(p1, reemplazar=False), n, 1, 'Último párrafo incorporado', seccion='III', det_extra='último párrafo')
N.sustituir_articulo('II', 'V', '26', md(2), n, 2, seccion='IV')
for k, blk in N.por_articulo(md(3)):
    N.sustituir_articulo('II', 'V', k, blk, n, 3, seccion='IV')
N.sustituir_articulo('II', 'V', '41', md(4), n, 4, seccion='VI')
for art, num in ((5, '19'), (6, '30'), (7, '34')):
    N.sustituir_articulo('II', 'VI', num, md(art), n, art, seccion='III')
for art, num, sec in ((8, '25', 'III'), (9, '42', 'IV')):
    p = ult(art); assert len(p) == 1
    N.modificar_articulo('II', 'VIII', num, N.ultimo_parrafo(p), n, art, 'Último párrafo sustituido', seccion=sec, det_extra='último párrafo')
N.sustituir_articulo('II', 'IX', '5', md(10), n, 10, seccion='I')
N.sustituir_anexo('XVI', 'II', 'I', md(11), n, 11)
N.incorporar_seccion('XVIII', 'I', md(12), n, 12)
fichas.ficha(n, [
    'Elimina la autorización previa de la CNV para prórrogas de programas globales, actualizaciones de prospecto y modificaciones de términos y condiciones o aumentos de monto en programas globales, Emisores Frecuentes, Régimen PyME CNV, ON autónomas, CEDEAR y CEVA: se consideran autorizadas automáticamente al presentar la documentación.',
    'Sustituye los arts. 26, 28 y 29 (Secc. IV) y 41 (Secc. VI) del Cap. V; 19, 30 y 34 (Secc. III) del Cap. VI; y 5° (Secc. I) del Cap. IX del Tít. II; agrega un último párrafo al art. 14 (Secc. III, Cap. V) y sustituye el último párrafo de los arts. 25 y 42 del Cap. VIII.',
    'Sustituye el Anexo I del Cap. II del Tít. XVI (facultades delegadas en la Gerencia de Emisoras).',
    'Incorpora la Secc. V del Cap. I del Tít. XVIII (art. 6°): régimen de los trámites en curso a la entrada en vigencia.'],
    notas=['Antecedente: consulta pública de la RG 1136/2026.',
           'El último párrafo incorporado al art. 14 se ubicó después del cuadro de costos de emisión que cierra el artículo.'])
