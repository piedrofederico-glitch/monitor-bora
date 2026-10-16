import normas as N, fichas
n = 1147
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
inc1 = [p for p in md(1) if p.startswith('1. Administración')]
N.modificar_articulo('V', 'I', '6', N.tramo('1. Administración:', '2. Representación:', inc1), n, 1, 'Inciso 1 sustituido', seccion='II', det_extra='inc. 1')
N.sustituir_seccion('V', 'II', 'I', md(2), n, 2)
N.sustituir_articulo('V', 'II', '38', md(3), n, 3, seccion='III')
N.sustituir_seccion('V', 'II', 'VI', md(4), n, 4)
N.derogar_seccion('V', 'II', 'VII', n, 5)
ant = '27'
for k, blk in N.por_articulo(md(6)):
    N.incorporar_articulo('V', 'VII', blk, n, 6, despues_de=ant, seccion='VII')
    ant = k
ps = md(7); a = ps.index('5. FONDOS COMUNES DE INVERSIÓN:'); b = len(ps) - 1 - ps[::-1].index('(…)')
N.modificar_articulo('XVI', 'I', '7', N.tramo('5. FONDOS COMUNES DE INVERSIÓN:', '6. REGISTRO Y CONTROL:', ps[a:b]), n, 7, 'Apartado 5 sustituido', seccion='II', det_extra='apartado 5')
N.incorporar_seccion('XVIII', 'III', md(8), n, 8)
fichas.ficha(n, [
    'Establece un procedimiento de autorización automática de oferta pública para FCI abiertos: sustituye la Secc. I del Cap. II del Tít. V (arts. 1° a 6°, con el nuevo art. 4° BIS).',
    'Sustituye la Secc. VI del Cap. II (modificación de reglamentos de gestión, arts. 75, 75 BIS y 76), el art. 38 (Secc. III) y el inc. 1 del art. 6° de la Secc. II del Cap. I del Tít. V (funciones de administración de la Sociedad Gerente).',
    'Deroga la Secc. VII del Cap. II del Tít. V e incorpora los arts. 27 BIS, 27 TER y 27 QUATER a la Secc. VII del Cap. VII (FCIA ETF).',
    'Actualiza el apartado 5 ("Fondos Comunes de Inversión") del listado de trámites por TAD del art. 7° del Cap. I del Tít. XVI e incorpora la Secc. XI del Cap. III del Tít. XVIII (disposición transitoria).'],
    notas=['Antecedente: consulta pública de la RG 1134/2026.'])
