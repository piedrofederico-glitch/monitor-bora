import normas as N, fichas
n = 1128
A = {a['num']: a for a in N.rg_articulos(n)}
N.sustituir_articulo('XVIII', 'V', '6 TER', N.md(A[1]['citas'][0]), n, 1)
fichas.ficha(n, [
    'Sustituye el art. 6° TER del Cap. V del Tít. XVIII (operaciones de clientes con CDI, CIE y CUIT: plazos mínimos de permanencia para transferencias de valores negociables al exterior y a entidades depositarias del exterior).',
    'Agrega el supuesto (4): títulos de cualquier ley de emisión y plazo de amortización que se hayan mantenido en subcuentas comitentes del ordenante no menos de 365 días corridos desde su acreditación en el ADCVN; los Agentes deben constatar el cumplimiento previo y conservar la documentación en el legajo.',
    'Agrega un epígrafe al artículo ("OPERACIONES DE CLIENTES CON C.D.I. o C.I.E. y C.U.I.T.") y adecua la terminología al glosario del Tít. I (AN, ALyC, ACVN, BCRA, UIF, FCIA, BOPREAL, CNV).'],
    notas=['La remisión "(Ver CRI88)" del texto anterior no figura en la nueva redacción.'])
