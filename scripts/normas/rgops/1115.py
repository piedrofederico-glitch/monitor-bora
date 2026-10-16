import normas as N, fichas
n = 1115
A = {a['num']: a for a in N.rg_articulos(n)}
defs = N.definiciones(N.md(A[1]['citas'][0]))
assert len(defs) == 2, defs
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1,
                     'Términos “Ley de Administración Financiera y de los Sistemas de Control del Sector Público Nacional” y “Resolución Técnica” o “RT” incorporados',
                     det_extra='términos “Ley de Administración Financiera...” y “Resolución Técnica” o “RT”')
caps = [(r, nom, N.md(x)) for r, nom, x in N.dividir_capitulos(N.bloque(n, 2))]
assert [c[0] for c in caps] == ['I', 'II', 'III']
N.sustituir_titulo('IV', caps, n, 2)
fichas.ficha(n, [
    'Sustituye completo el Título IV ("Régimen informativo periódico"): Cap. I (régimen informativo), Cap. II (otra información periódica de las Emisoras) y Cap. III (forma de presentación y criterios de valuación de los estados financieros, con sus Anexos I a IV).',
    'Reduce a tres períodos o ejercicios la serie máxima de la Reseña Informativa.',
    'Elimina el artículo de fianzas y avales, que duplicaba la obligación de informar de las entidades financieras.',
    'Unifica criterios sobre plazos de presentación de estados contables y adecua la terminología.',
    'Incorpora al glosario del Tít. I la "Ley de Administración Financiera y de los Sistemas de Control del Sector Público Nacional" (N° 24.156) y "Resolución Técnica" o "RT".'],
    notas=['El art. 2° de la RG tiene varias citas internas entre comillas; el texto del Título se extrajo como bloque completo hasta el fin del artículo.',
           'Los modelos y cuadros de los anexos del Cap. III se transcriben como texto preformateado; su alineación puede diferir del PDF.'])
