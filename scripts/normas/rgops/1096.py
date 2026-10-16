import normas as N, fichas
n = 1096
A = {a['num']: a for a in N.rg_articulos(n)}
nuevos = N.sin_elipsis(N.md(A[1]['citas'][0]))
assert nuevos[0].startswith('b.1) Particularmente')
N.modificar_articulo('V', 'II', '15', N.tramo('b.1) Particularmente', 'b.2) Aquellos fondos', nuevos), n, 1,
                     'Inciso b.1) sustituido', det_extra='inc. b.1)')
fichas.ficha(n, [
    'Sustituye el inciso b.1) del art. 15 (Secc. II, Cap. II, Tít. V): reglas de cartera de los "Fondos Comunes de Dinero Clásicos".',
    'Permite hasta 50% en plazos fijos no precancelables (valuados a devengamiento) y hasta 50% en plazos fijos precancelables en período de precancelación; la suma de ambos no puede superar el 70% del patrimonio neto.',
    'Limita al 35% los otros activos valuados a devengamiento y al 50% el total de activos valuados a devengamiento.',
    'Admite hasta 20% en títulos de deuda con vencimiento final no mayor a un año.'])
