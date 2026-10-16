import normas as N, fichas
n = 1141
N.VIGENCIAS[n] = '23/05/2026'
A = {a['num']: a for a in N.rg_articulos(n)}
ps = N.md(A[1]['citas'][0])
a = ps.index('1. Cheques.')
nuevo = [p for p in ps[a:] if p != '(…)']
N.modificar_articulo('XI', None, '3', N.tramo('1. Cheques.', '2. Transferencias en el país.', nuevo), n, 1, 'Inciso 1 sustituido', seccion='II', det_extra='inc. 1')
fichas.ficha(n, [
    'Sustituye el inciso 1 ("Cheques") del art. 3° de la Secc. II del Tít. XI (modalidades de pago y control en la recepción y entrega de fondos de clientes).',
    'Distingue cheques físicos y electrónicos: los físicos deben librarse contra cuentas del cliente (o a su favor con endoso completo, si lo manifiesta); para los electrónicos no hay límite de endosos, con trazabilidad.',
    'Mantiene el tope de dos pagos por día y por cliente con cheques, librados a la orden del cliente o "no a la orden" y cruzados.'],
    vigencia='23/05/2026', vigencia_txt='art. 2°: a partir del día siguiente de su dictado (22/05/2026)',
    notas=['El PDF publicado por la CNV es una imagen escaneada sin texto: se usó el texto publicado en el Boletín Oficial (edición del 27/05/2026), cotejado con InfoLEG.',
           'Rige desde el día siguiente a su dictado, antes de su publicación en el BO (27/05/2026).'])
