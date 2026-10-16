import normas as N, fichas, re
n = 1131
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
# art. 1°: primer párrafo del art. 2°
p1 = [p for p in md(1) if p.startswith('ARTÍCULO 2')]
assert len(p1) == 1
def f1(pars):
    assert pars[0].startswith('ARTÍCULO 2º.- A los fines de las presentes Normas, los siguientes')
    return p1 + pars[1:]
N.modificar_articulo('I', 'II', '2', f1, n, 1, 'Primer párrafo sustituido', det_extra='primer párrafo')
# art. 2°: términos nuevos
nuevos = N.definiciones(md(2))
assert len(nuevos) == 6, nuevos
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(nuevos), n, 2, 'Términos “ACyR”, “CABA”, “CPCCN”, “FCICI”, “RG” y “ROS” incorporados',
                     det_extra='términos “ACyR”, “CABA”, “CPCCN”, “FCICI”, “RG” y “ROS”')
# art. 3°: definiciones sustituidas
d3 = N.definiciones(md(3))
assert [x[:6] for x in d3] == ['“ACD” ', '“ACDI”', '“LPA” '], d3
def f3(pars):
    pars = N.parrafo('“ACyD” significa', [d3[0]])(pars)
    pars = N.parrafo('“ACyDI” significa', [d3[1]])(pars)
    return N.parrafo('“LPA” significa', [d3[2]])(pars)
N.modificar_articulo('I', 'II', '2', f3, n, 3, 'Definiciones “ACD” (antes “ACyD”), “ACDI” (antes “ACyDI”) y “LPA” sustituidas',
                     det_extra='definiciones “ACD”, “ACDI” y “LPA”')
# art. 4°: expresión sustituida en el art. 3°
d4 = N.definiciones(md(4))
assert len(d4) == 1
N.modificar_articulo('I', 'II', '3', N.parrafo('“Agentes inscriptos en el registro a cargo de la CNV”', d4), n, 4,
                     'Expresión “Agentes inscriptos en el registro a cargo de la CNV” sustituida', det_extra='expresión “Agentes inscriptos...”')
# art. 5°: expresiones nuevas en el art. 3°
d5 = [x for x in N.definiciones(md(5)) if x != '“(…)']
assert len(d5) == 4, d5
N.modificar_articulo('I', 'II', '3', N.termino_nuevo(d5), n, 5, 'Expresiones “Conducta Infractora”, “Conductor de Sumario”, “Presentación a la CNV” y “Tribunales arbitrales” incorporadas',
                     det_extra='4 expresiones nuevas')
# art. 6°: Título XIII
caps = [(r, nom, N.md(x)) for r, nom, x in N.dividir_capitulos(N.bloque(n, 6))]
assert [c[0] for c in caps] == ['I', 'II', 'III']
N.sustituir_titulo('XIII', caps, n, 6)
# art. 7°: ACyD -> ACD ; ACyDI -> ACDI
tot = N.reemplazo_global([(r'\bACyDI\b', 'ACDI'), (r'\bACyD\b', 'ACD')], n, 7, 'siglas “ACyD” → “ACD” y “ACyDI” → “ACDI”')
print('reemplazos', tot)
fichas.ficha(n, [
    'Simplifica y sustituye completo el Título XIII (procedimiento de investigaciones, procedimiento sumarial y publicidad de resoluciones disciplinarias), con Anexo I en el Cap. II.',
    'Reformula el primer párrafo del art. 2° del glosario: las definiciones rigen también para notas, informes, dictámenes, resoluciones y demás documentos de la CNV.',
    'Incorpora los términos ACyR, CABA, CPCCN, FCICI, RG y ROS; sustituye las definiciones de ACD, ACDI y LPA; redefine "Agentes inscriptos en el registro a cargo de la CNV" o "Agentes Registrados" e incorpora las expresiones "Conducta Infractora", "Conductor de Sumario", "Presentación a la CNV" y "Tribunales arbitrales".',
    f'Reemplaza en todas las Normas las siglas "ACyD" por "ACD" y "ACyDI" por "ACDI" (art. 7°; {tot} ocurrencias en el texto consolidado).'],
    notas=['El reemplazo del art. 7° se aplicó sobre vigente/ (sin tocar notas de vigencia ni historial). Cada archivo afectado tiene una nota al inicio y una entrada de historial con las ubicaciones; el texto anterior es idéntico salvo las siglas.',
           'El art. 99 de la Secc. XII del Cap. V del Tít. II dice "actúen como ACy." desde la RG 1095 (errata del original): no coincide con "ACyD" y se dejó tal cual.'])
