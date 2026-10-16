import normas as N, fichas
n = 1126
A = {a['num']: a for a in N.rg_articulos(n)}
ps = N.md(A[1]['citas'][0])
k = next(i for i, p in enumerate(ps) if p.startswith('b) Que se constituyan'))
N.modificar_articulo('V', 'II', '15', N.tramo('b) Que se constituyan como Fondos Comunes de Dinero', None, ps[k:]), n, 1,
                     'Inciso b) sustituido', det_extra='inc. b)')
fichas.ficha(n, [
    'Sustituye completo el inciso b) del art. 15 (Secc. II, Cap. II, Tít. V): reglas de margen de liquidez y cartera de los Fondos Comunes de Dinero, Clásicos (b.1) y Dinámicos (b.2).',
    'En los Fondos Comunes de Dinero Clásicos eleva al 60% el tope de plazos fijos precancelables en período de precancelación (b.1.2) y prevé un supuesto especial vinculado con la vida promedio ponderada de la cartera (segundo párrafo de b.1.1).',
    'Agrega para los Fondos Comunes de Dinero Dinámicos el subinciso b.2.4) sobre inversiones adicionales admitidas.',
    'Retoma la distinción entre fondos Clásicos y Dinámicos introducida por la RG 1038.'])
