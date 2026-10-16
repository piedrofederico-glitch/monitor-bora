import normas as N, fichas
n = 1109
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
defs = [p for p in md(1) if p.startswith('“')]
assert len(defs) == 1
N.modificar_articulo('I', 'II', '3', N.termino_nuevo(defs), n, 1, 'Expresión “Agentes inscriptos en el registro a cargo de la CNV” incorporada',
                     det_extra='expresión “Agentes inscriptos en el registro a cargo de la CNV”')
N.derogar_capitulo_y_quitar('XIX', None, n, 2)
N.sustituir_seccion('XXI', 'I', 'I', md(3), n, 3)
fichas.ficha(n, [
    'Reglamenta el Decreto N° 1017/2024 (anotación de boletos, art. 10): sustituye la Secc. I del Cap. I del Tít. XXI y amplía quiénes pueden prestar el servicio de anotación (ACRyP, Cámaras Compensadoras, Mercados, ADCVN, entidades financieras y bolsas de comercio, entre otros).',
    'Para ACRyP, Cámaras, Mercados y ADCVN el servicio es actividad afín o complementaria: deben informarlo, mantener actualizada la nómina y no usar la matrícula CNV en esa actividad; no se exige mayor patrimonio neto mínimo.',
    'Deroga el Título XIX (Entidades Representativas Regionales).',
    'Incorpora a las expresiones del art. 3° del Cap. II del Tít. I la aclaración de que las menciones a categorías de Agentes se refieren a Agentes inscriptos en el registro de la CNV.'],
    notas=['El Título XIX no tenía capítulos: su archivo se retiró de vigente/ y el texto derogado está en historial/titulo-XIX/titulo-XIX-derogado-RG-1109-2026.md.'])
