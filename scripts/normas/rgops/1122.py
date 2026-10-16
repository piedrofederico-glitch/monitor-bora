import normas as N, fichas
n = 1122
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
N.sustituir_articulo('VII', 'II', '35', md(1), n, 1)
sub = [p for p in md(2) if p.startswith('44)')]
assert len(sub) == 1
N.modificar_articulo('XV', 'I', '11', N.insertar_despues('43) AGE_ 030– Pasivos Financieros.', sub), n, 2,
                     'Subinciso 44) del inciso L) incorporado', det_extra='inc. L), subinc. 44)')
N.incorporar_articulo('XVIII', 'V', md(3), n, 3, despues_de='21')
fichas.ficha(n, [
    'Sustituye el art. 35 del Cap. II del Tít. VII (régimen informativo de pasivos financieros de los ALyC, creado por la RG 1094): incluye los pasivos asumidos dentro o fuera de los Mercados.',
    'Agrega el formulario "AGE_033 – Pasivos Financieros – complementario" como subinciso 44) del inc. L) del art. 11 del Cap. I del Tít. XV.',
    'Incorpora el art. 22 del Cap. V del Tít. XVIII: información histórica de cauciones, pases, cheques y pagarés (agosto de 2025 a febrero de 2026) hasta el 1/05/2026; cierre de marzo de 2026 hasta el 15/04/2026; desde abril de 2026, el plazo general del art. 35.'],
    notas=['El art. 35 sustituido termina sin punto final ("...carácter de DDJJ"); el subinciso 44) tampoco lleva punto: se transcriben tal como se publicaron.'])
