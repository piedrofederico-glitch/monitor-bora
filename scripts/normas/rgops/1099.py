import normas as N, fichas
n = 1099
A = {a['num']: a for a in N.rg_articulos(n)}
# art. 1°: inciso 1 del art. 70, Secc. IX, Cap. V, Tít. II
ps = N.md(A[1]['citas'][0])
nuevo = [p for p in ps if p.startswith('1. Presentar')]
assert len(nuevo) == 1
N.modificar_articulo('II', 'V', '70', N.tramo('1. Presentar por ante', '2. Mantener a disposición', nuevo), n, 1,
                     'Inciso 1 sustituido', det_extra='inc. 1')
# art. 2°: Capítulo I del Tít. XVIII
(rom, nom, L), = N.dividir_capitulos(A[2]['citas'][0])
N.sustituir_capitulo('XVIII', 'I', nom, N.md(L), n, 2)
# art. 3°: art. 1° del Cap. IV del Tít. XVIII
N.sustituir_articulo('XVIII', 'IV', '1', N.md(A[3]['citas'][0]), n, 3)
# arts. 4° y 5°
N.derogar_capitulo_y_quitar('XVIII', 'XVII', n, 4)
N.renumerar_capitulo('XVIII', 'XVIII', 'XVII', n, 5)
fichas.ficha(n, [
    'Deroga disposiciones que quedaron abstractas tras la RG 1095 y uniforma la terminología con las definiciones del nuevo Título I.',
    'Sustituye el inciso 1 del art. 70 (Secc. IX, Cap. V, Tít. II): la información del art. 14, inc. 6, se presenta dentro de los 10 días hábiles del cierre de la colocación, salvo PyME CNV Garantizada y Régimen PyME CNV.',
    'Reemplaza el Cap. I del Tít. XVIII (disposiciones transitorias de Emisoras), que fija el 19 de diciembre de 2025 como fecha de corte para las emisiones PyME CNV Garantizadas y VCP previas.',
    'Sustituye el art. 1° del Cap. IV del Tít. XVIII (reglamentos de los Mercados para el régimen PyME CNV Garantizada, ahora en la Secc. IX del Cap. V del Tít. II).',
    'Deroga el Cap. XVII del Tít. XVIII (entidades de garantía) y renumera el Cap. XVIII (régimen de regularización de activos, Ley 27.743) como Cap. XVII.'],
    notas=['El archivo del capítulo derogado se retiró de vigente/; su texto está en historial/titulo-XVIII/capitulo-XVII.md (entrada "Derogado").',
           'El ex Cap. XVIII ahora es vigente/titulo-XVIII/capitulo-XVII.md; su historial anterior, si lo hubiera, se movió con él.'])
