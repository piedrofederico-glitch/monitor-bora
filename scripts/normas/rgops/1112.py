import normas as N, fichas
n = 1112
A = {a['num']: a for a in N.rg_articulos(n)}
defs = N.definiciones(N.md(A[1]['citas'][0]))
assert len(defs) == 5, defs
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1, 'Términos “CAFCI”, “FCIA”, “FCIC”, “GDE” y “RLPA” incorporados',
                     det_extra='términos “CAFCI”, “FCIA”, “FCIC”, “GDE” y “RLPA”')
caps = [(r, nom, N.md(x)) for r, nom, x in N.dividir_capitulos(N.bloque(n, 2))]
assert [c[0] for c in caps] == ['I', 'II']
N.sustituir_titulo('XVI', caps, n, 2)
fichas.ficha(n, [
    'Sustituye completo el Título XVI ("Disposiciones generales"): Cap. I, "Notificaciones. Otras disposiciones", y Cap. II, "Delegación de facultades en Gerencias y Subgerencias", con siete anexos.',
    'Elimina el fax como medio de presentación, incorpora el horario de la mesa de entradas y reordena por área el listado de trámites que se gestionan por TAD.',
    'En la notificación al deudor cedido (arts. 70 a 72 de la Ley 24.441) admite "otro medio de identificación fehaciente".',
    'Amplía la delegación de decisiones técnicas u operativas del Directorio en las Gerencias y Subgerencias.',
    'Incorpora al glosario del Tít. I los términos CAFCI, FCIA, FCIC, GDE y RLPA.'],
    notas=['El texto del Título XVI tiene comillas de cierre sueltas (p. ej., "Ley para el Financiamiento de la Vivienda y la Construcción”"); se extrajo como bloque desde la comilla de apertura hasta el fin del art. 2° de la RG y se transcribió tal cual.',
           'La definición de CAFCI se publicó sin comillas en el término: se respeta.'])
