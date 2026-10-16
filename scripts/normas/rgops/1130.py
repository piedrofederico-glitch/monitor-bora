import normas as N, fichas
n = 1130
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k, i=0: N.md(A[k]['citas'][i])
defs = N.definiciones(md(1))
assert len(defs) == 1
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1, 'Término “Cauciones Tomadoras Netas” incorporado', det_extra='término “Cauciones Tomadoras Netas”')
N.sustituir_articulo('VII', 'II', '25', md(2), n, 2)
ant = '35'
for cita in (md(3, 0), md(3, 1)):
    for k, blk in N.por_articulo(cita):
        N.incorporar_articulo('VII', 'II', blk, n, 3, despues_de=ant)
        ant = k
sub = [p for p in md(4) if p[:3] in ('45)', '46)', '47)')]
assert len(sub) == 3
N.modificar_articulo('XV', 'I', '11', N.insertar_despues('44) AGE_ 033–Pasivos Financieros – complementario', sub), n, 4,
                     'Subincisos 45), 46) y 47) del inciso L) incorporados', det_extra='inc. L), subincs. 45) a 47)')
ant = '22'
for k, blk in N.por_articulo(md(5)):
    N.incorporar_articulo('XVIII', 'V', blk, n, 5, despues_de=ant)
    ant = k
fichas.ficha(n, [
    'Crea un régimen informativo diario de tenencias en moneda extranjera de los ALyC (art. 36, Cap. II, Tít. VII), excepto Participantes Directos y entidades financieras.',
    'Establece indicadores financieros con límites prudenciales de liquidez (índices I a III) y de apalancamiento (general y computable) para los ALyC alcanzados (arts. 37 a 41).',
    'Sustituye el art. 25 del Cap. II del Tít. VII (régimen informativo del ALyC) e incorpora los formularios MUG_036, MUG_037 y MUG_038 al inc. L) del art. 11 del Cap. I del Tít. XV.',
    'Fija cronogramas de adecuación progresiva (desde mayo de 2026) de los límites mínimos de liquidez y máximos de apalancamiento (arts. 23 a 27, Cap. V, Tít. XVIII); el Agente que no subsane el incumplimiento debe abstenerse de funcionar.',
    'Incorpora al glosario del Tít. I la definición de "Cauciones Tomadoras Netas".'],
    notas=['Los cuadros de los cronogramas se transcriben como texto preformateado.',
           'El subinciso 47) se publicó sin punto final: se respeta.'])
