import normas as N, fichas
n = 1108
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
defs = [p for p in md(1) if p.startswith('Ley de ')]
assert len(defs) == 2, defs
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1, 'Términos “Ley de Régimen Penal Tributario” y “Ley de Prevención de la Evasión Fiscal” incorporados',
                     det_extra='términos “Ley de Régimen Penal Tributario” y “Ley de Prevención de la Evasión Fiscal”')
N.incorporar_seccion('XI', None, md(2), n, 2)
fichas.ficha(n, [
    'Reglamenta en el ámbito de la CNV el "Régimen de Declaración Jurada Simplificada para el Impuesto a las Ganancias" (Ley de Régimen Penal Tributario N° 27.799).',
    'Incorpora la Secc. VI del Tít. XI (arts. 14 a 17): los sujetos obligados pueden recibir de clientes adheridos depósitos en efectivo, transferencias de valores negociables y de activos virtuales, sin los límites de monto del art. 3° de la Secc. II del Tít. XI.',
    'Exige que el cliente esté adherido al régimen y sea titular o cotitular de una cuenta en la entidad receptora, y excluye jurisdicciones no cooperantes.',
    'Incorpora al glosario del Tít. I las referencias a la Ley de Régimen Penal Tributario (N° 27.799) y a la Ley de Prevención de la Evasión Fiscal (N° 25.345).'],
    notas=['Las dos definiciones se publicaron sin comillas de apertura y con comillas de cierre antes del punto ("...significa Ley N° 27.799”."): se transcriben tal como figuran en la RG y en InfoLEG.'])
