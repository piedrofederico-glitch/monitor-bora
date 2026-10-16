import normas as N, fichas
n = 1144
N.VIGENCIAS[n] = '01/06/2026'
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
N.glosario(N.definiciones(md(1)), n=n, art_rg=1)
for k, blk in N.por_articulo(md(2)):
    N.sustituir_articulo('VII', 'II', k, blk, n, 2)
N.sustituir_articulo('VII', 'II', '41', md(3), n, 3)
for k, blk in N.por_articulo(md(4)):
    N.sustituir_articulo('XVIII', 'V', k, blk, n, 4)
fichas.ficha(n, [
    'Reformula el régimen de la RG 1130 sobre tenencias en moneda extranjera e indicadores financieros de los ALyC: sustituye los arts. 36 a 39 y 41 del Cap. II del Tít. VII.',
    'Distingue la "Posición en Moneda Extranjera Bruta" y la "Neta" (art. 36), definidas también en el glosario del Tít. I.',
    'Sustituye los arts. 23 a 26 del Cap. V del Tít. XVIII (cronogramas de adecuación de los límites de liquidez y apalancamiento).'],
    vigencia='01/06/2026', vigencia_txt='art. 5°: desde el día de su publicación en el BO')
