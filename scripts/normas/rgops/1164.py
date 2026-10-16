import normas as N, fichas, re
n = 1164
N.VIGENCIAS[n] = '04/09/2026'
b = lambda k: N.md(N.bloque(n, k))
E = ('(…)', '(...)', '(…).', '(…)”.')
N.glosario(N.definiciones(b(1)), n=n, art_rg=1)
N.glosario(N.definiciones(b(2)), n=n, art_rg=2, num='3')
i3 = [p for p in b(3) if p.startswith('3. ')]
assert len(i3) == 1
C = N.Cap('II', 'V'); i, j = C.rango_art('74', 'IX')
viejo3 = [p for p in C.pars[i:j] if p.startswith('3. ')]
assert len(viejo3) == 1
k3 = C.pars.index(viejo3[0])
sig = C.pars[k3 + 1][:40] if k3 + 1 < j else None
N.modificar_articulo('II', 'V', '74', N.tramo(viejo3[0], sig, i3), n, 3, 'Inciso 3. sustituido', seccion='IX', det_extra='inc. 3.')
caps = [(r, nom, N.md(x)) for r, nom, x in N.dividir_capitulos(N.bloque(n, 4))]
assert [c[0] for c in caps] == ['I', 'II', 'III']
N.sustituir_titulo('IX', caps, n, 4)
A = {a['num']: a for a in N.rg_articulos(n)}
Ls = N.rg_lineas(n)[A[5]['ini']:A[5]['fin']]
k = next(x for x, l in enumerate(Ls) if l and re.match(r'^\s*ANEXO V\s*$', l))
anexo = N.md(Ls[k:])
assert anexo[0] == '### ANEXO V'
N.sustituir_anexo('XVI', 'II', 'V', anexo, n, 5)
N.derogar_articulo('XVIII', 'VII', '1', n, 6, seccion='I')
fichas.ficha(n, [
    'Simplifica y sustituye completo el Título IX (Agentes de Calificación de Riesgos): Cap. I, disposiciones comunes a ACR sociedades anónimas y universidades públicas; Cap. II, específicas de ACR S.A.; Cap. III, específicas de ACR-UP.',
    'Sustituye el inciso 3. del art. 74 (Secc. IX, Cap. V, Tít. II): la calificación de riesgo de la Entidad de Garantía debe estar actualizada.',
    'Sustituye el Anexo V del Cap. II del Tít. XVI (facultades delegadas en la Gerencia de Agentes y Mercados).',
    'Deroga el art. 1° de la Secc. I del Cap. VII del Tít. XVIII (cronograma de patrimonio neto mínimo de los ACR).',
    'Incorpora al glosario del Tít. I la sigla RNR (Registro Nacional de Reincidencia) y a las expresiones del art. 3° la de "Calificación Pública".'],
    vigencia='04/09/2026', vigencia_txt='art. 7°: desde el día de su publicación en el BO',
    notas=['El texto del Anexo V se publicó sin comillas: se tomó desde el encabezado "ANEXO V" hasta el art. 6° de la RG.'])
