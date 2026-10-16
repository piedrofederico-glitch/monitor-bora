import normas as N, fichas
n = 1150
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
N.glosario(N.definiciones(md(1)), n=n, art_rg=1)
for art, sec in ((2, 'I'), (3, 'I'), (4, 'I'), (5, 'III'), (6, 'IV'), (7, 'VI'), (8, 'VIII'), (9, 'IX')):
    for k, blk in N.por_articulo(md(art)):
        N.sustituir_articulo('XXII', 'I', k, blk, n, art, seccion=sec)
fichas.ficha(n, [
    'Amplía la tokenización (Tít. XXII): admite la representación digital de todos los valores negociables emitidos bajo los distintos regímenes de oferta pública, incluidos los de autorización automática.',
    'Sustituye los arts. 1°, 2°, 5° y 10 (Secc. I), 14 (Secc. III), 18 (Secc. IV), 28 (Secc. VI), 36 (Secc. VIII) y 38 y 39 (Secc. IX, sandbox regulatorio) del Cap. I del Tít. XXII.',
    'Prorroga el sandbox regulatorio de tokenización (arts. 38 y 39).',
    'Incorpora al glosario del Tít. I las siglas AAPIC y TRD (Tecnología de Registro Distribuido).'],
    notas=['Antecedente: consulta pública de la RG 1137/2026.'])
