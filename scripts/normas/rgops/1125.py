import normas as N, fichas
n = 1125
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
ps = N.definiciones(md(1))
inc13 = [p for p in ps if p.startswith('13) ')]
nuevos = [p for p in ps if p.startswith('“') and not p.startswith('“Inversor Calificado”')]
assert len(inc13) == 1 and len(nuevos) == 5, (inc13, nuevos)
def fn(pars):
    pars = N.parrafo('13) Personas humanas o jurídicas, distintas', inc13, hasta_siguiente_termino=False)(pars)
    return N.termino_nuevo(nuevos)(pars)
N.modificar_articulo('I', 'II', '2', fn, n, 1,
                     'Inciso 13) de “Inversor Calificado” sustituido y términos “Activos Virtuales”, “Financiamiento Colectivo” y de los regímenes de financiamiento colectivo incorporados',
                     det_extra='“Inversor Calificado” inc. 13) y 5 términos nuevos')
N.sustituir_articulo('II', 'V', '83', md(2), n, 2, seccion='XI')
N.sustituir_articulo('II', 'V', '113', md(3), n, 3, seccion='XIII')
for rom, L in N.dividir_secciones(A[4]['citas'][0]):
    N.incorporar_seccion('II', 'V', N.md(L), n, 4)
fichas.ficha(n, [
    'Crea la oferta pública con autorización automática de valores negociables mediante financiamiento colectivo, en sus modalidades de bajo y mediano impacto (nuevas Secciones XV, XVI y XVII del Cap. V del Tít. II, arts. 144 a 152).',
    'Permite la participación de inversores no calificados con límites por inversor: UVA 3.000 por emisión, UVA 10.000 en el conjunto de emisiones y hasta 5% y 10% de su patrimonio, acreditable por DDJJ.',
    'La colocación puede hacerse por los mecanismos del Cap. IV del Tít. VI o a través de PFC registradas.',
    'Sustituye los arts. 83 (Secc. XI) y 113 (Secc. XIII) del Cap. V del Tít. II (montos máximos de los regímenes de mediano impacto).',
    'En el glosario del Tít. I agrega "Activos Virtuales", "Financiamiento Colectivo" y los tres regímenes nuevos, y reformula el inc. 13) de "Inversor Calificado" (residentes en el país; computa también inversiones en el exterior y en activos virtuales).'],
    notas=['Antecedente: consulta pública de la RG 1111/2026.',
           'El art. 1° dice "Incorporar" el inciso 13) de la definición de "Inversor Calificado", que ya existía con otra redacción: se aplicó como sustitución de ese inciso (la redacción anterior está en historial/).',
           'El inciso 13) citado termina con comillas de cierre ("...(350.000).”"): se transcribe tal cual.'])
