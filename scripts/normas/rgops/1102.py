import normas as N, fichas
n = 1102
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
# art. 1°: inciso 2 del art. 2°, Secc. I, Cap. I, Tít. V
nuevo = [p for p in md(1) if p.startswith('2. AN')]
N.modificar_articulo('V', 'I', '2', N.tramo('2. AN respecto de la inscripción ACyD de FCI; y', '3. Sociedades Gerentes', nuevo), n, 1,
                     'Inciso 2 sustituido', det_extra='inc. 2')
# art. 2°: inciso 3 del art. 7°, Secc. II
ps = md(2); k = next(i for i, p in enumerate(ps) if p.startswith('3. administración'))
N.modificar_articulo('V', 'I', '7', N.tramo('3. administración de carteras', None, ps[k:]), n, 2, 'Inciso 3 sustituido', det_extra='inc. 3')
# art. 3°: art. 10, Secc. II
N.sustituir_articulo('V', 'I', '10', md(3), n, 3)
# art. 4°: primer párrafo del art. 20, Secc. VI
nuevo = [p for p in md(4) if p.startswith('ARTÍCULO 20')]
N.modificar_articulo('V', 'I', '20', N.tramo('ARTÍCULO 20°. - Podrán actuar', 'Sin perjuicio de la colocación', nuevo), n, 4,
                     'Primer párrafo sustituido', det_extra='primer párrafo')
# art. 5°: arts. 21 a 26 del Cap. I del Tít. VII
ps = md(5)
idx = [i for i, p in enumerate(ps) if N.clave_art(p)] + [len(ps)]
ant = '20'
for a, b in zip(idx, idx[1:]):
    N.incorporar_articulo('VII', 'I', ps[a:b], n, 5, despues_de=ant)
    ant = N.clave_art(ps[a])
# art. 6°: art. 37, Secc. XII, Cap. I, Tít. VIII
N.sustituir_articulo('VIII', 'I', '37', md(6), n, 6, seccion='XII')
fichas.ficha(n, [
    'Permite que los AN se inscriban también como Sociedad Gerente de FCI y que las Sociedades Gerentes se inscriban como AN (salvo AN RUCA) o ALyC, con incompatibilidades (ACyDI y AN; entidades financieras y AN).',
    'Modifica en el Cap. I del Tít. V el inc. 2 del art. 2°, el inc. 3 del art. 7°, el art. 10 y el primer párrafo del art. 20 (ACyDI de FCI).',
    'Incorpora los arts. 21 a 26 al Cap. I del Tít. VII: segregación funcional, pautas de actuación, idoneidad, responsable de cumplimiento regulatorio y control interno, exposición en EECC y limitaciones del AN que también es Sociedad Gerente.',
    'Sustituye el art. 37 de la Secc. XII del Cap. I del Tít. VIII (depositantes autorizados ante el ADCVN).'],
    notas=['En el art. 20 del Cap. I del Tít. V la RG cita también el epígrafe "AGENTES DE COLOCACIÓN Y DISTRIBUCIÓN INTEGRAL DE FONDOS COMUNES DE INVERSIÓN (ACyDI DE FCI)."; sólo se reemplazó el primer párrafo, como indica el art. 4°.'])
