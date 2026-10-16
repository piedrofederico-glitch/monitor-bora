import normas as N, fichas
n = 1151
N.VIGENCIAS[n] = '11/06/2026'
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
N.glosario(N.definiciones(md(1)), n=n, art_rg=1)
N.glosario(N.definiciones(md(2)), n=n, art_rg=2)
for k, blk in N.por_articulo(md(3)):
    N.sustituir_articulo('VI', 'V', k, blk, n, 3, seccion='II')
N.sustituir_articulo('VI', 'V', '6', md(4), n, 4, seccion='III')
fichas.ficha(n, [
    'Define a los "Sujetos Restringidos" (entidades que administran recursos públicos o previsionales, como el FGS) en el glosario del Tít. I y sustituye la definición de "FGS".',
    'Sustituye los arts. 2° (regla general de negociación en sistemas con prioridad precio-tiempo) y 3° (excepción de segmentos bilaterales no garantizados) de la Secc. II del Cap. V del Tít. VI.',
    'Los Agentes sólo pueden cursar operaciones de Sujetos Restringidos bajo esa regla y con límites de volumen diario por especie (25% del promedio) y de renta fija pública; los segmentos bilaterales no pueden usar precios de referencia de esas operaciones.',
    'Sustituye el art. 6° de la Secc. III del Cap. V del Tít. VI (concepto de cartera propia y cartera propia ampliada).'],
    vigencia='11/06/2026', vigencia_txt='art. 5°: desde el día de su publicación en el BO')
