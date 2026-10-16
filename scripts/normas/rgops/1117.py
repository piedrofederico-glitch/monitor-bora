import normas as N, fichas
n = 1117
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
defs = N.definiciones(md(1))
assert len(defs) == 5, defs
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1, 'Términos de los regímenes de oferta pública con autorización automática incorporados',
                     det_extra='5 términos de regímenes con autorización automática')
for k, num, sec in ((2, '64', 'IX'), (3, '71', 'IX'), (4, '82', 'XI'), (5, '92', 'XI')):
    N.sustituir_articulo('II', 'V', num, md(k), n, k, seccion=sec)
fichas.ficha(n, [
    'Habilita la oferta pública con autorización automática a inversores minoristas por Emisoras del Régimen General que cumplan su régimen informativo.',
    'Sustituye los arts. 64 y 71 (Secc. IX, ON por su bajo impacto) y 82 y 92 (Secc. XI, ON por su mediano impacto) del Cap. V del Tít. II.',
    'En bajo impacto, pueden adquirir en colocación y negociación secundaria inversores no calificados en emisiones PyME CNV Garantizadas, en las garantizadas por Entidades de Garantía y en las de Emisoras del Régimen General.',
    'En mediano impacto, admite la transferencia a inversores no calificados cuando la Emisora está en el Régimen General.',
    'Incorpora al glosario del Tít. I los nombres de los cinco regímenes de autorización automática (Secciones IX a XIII del Cap. V del Tít. II).'],
    notas=['Las cinco definiciones remiten a "la Sección ... del Título II" sin mencionar el Capítulo V: se transcriben tal como se publicaron.'])
