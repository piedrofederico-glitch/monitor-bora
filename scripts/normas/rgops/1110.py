import normas as N, fichas
n = 1110
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
defs = [p for p in md(1) if p.startswith('“')]
assert len(defs) == 1
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1, 'Término “Régimen General” o “Régimen ordinario” incorporado',
                     det_extra='término “Régimen General” o “Régimen ordinario”')
N.incorporar_seccion('II', 'V', md(2), n, 2)
fichas.ficha(n, [
    'Incorpora la Secc. XIV ("Cambio de régimen") al Cap. V del Tít. II (arts. 127 a 133): las Emisoras del Régimen General o del Régimen PyME CNV pueden pedir pasar a un régimen especial con menores requisitos, y viceversa.',
    'El cambio requiere asamblea extraordinaria (o el órgano o consentimiento de tenedores que corresponda si sólo hay deuda), comunicación como Hecho Relevante y, en su caso, OPA con precio justificado.',
    'Regula el reemplazo del órgano de fiscalización colegiado por uno unipersonal y la tramitación simultánea de reformas estatutarias.',
    'Incorpora al glosario del Tít. I la definición de "Régimen General" o "Régimen ordinario".'],
    notas=['Antecedente: consulta pública de la RG 1104/2026.',
           'La definición se publicó con comillas de cierre antes del punto final ("...régimen especial”."): se transcribe tal cual.'])
