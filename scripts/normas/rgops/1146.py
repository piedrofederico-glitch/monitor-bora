import normas as N, fichas
n = 1146
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
N.glosario(N.definiciones(md(1)), n=n, art_rg=1)
N.sustituir_articulo('V', 'IV', '6', md(2), n, 2, seccion='IV')
N.sustituir_articulo('V', 'IV', '11', md(3), n, 3, seccion='IX')
for k, blk in N.por_articulo(md(4)):
    N.sustituir_articulo('V', 'IV', k, blk, n, 4, seccion='IX')
N.incorporar_articulo('V', 'IV', md(5), n, 5, despues_de='19', seccion='IX')
ant = '21'
for k, blk in N.por_articulo(N.md(N.bloque(n, 6))):
    N.incorporar_articulo('V', 'IV', blk, n, 6, despues_de=ant, seccion='X')
    ant = k
N.sustituir_seccion('V', 'IV', 'XXI', md(7), n, 7)
N.sustituir_articulo('V', 'IV', '67', md(8), n, 8, seccion='XXIII')
N.sustituir_seccion('V', 'IV', 'XXIV', md(9), n, 9)
N.incorporar_seccion('V', 'IV', md(10), n, 10)
N.incorporar_articulo('XVIII', 'II', md(11), n, 11, despues_de='2')
fichas.ficha(n, [
    'Actualiza los regímenes de oferta pública de fideicomisos financieros con autorización automática (Cap. IV del Tít. V): sustituye la Secc. XXI y la Secc. XXIV e incorpora la Secc. XXV (arts. 81 a 94).',
    'Sustituye los arts. 6° (Secc. IV), 11, 18 y 19 (Secc. IX) y 67 (Secc. XXIII); el art. 11 permite optar, en cada emisión, por cualquiera de los regímenes, incluso en forma alternada.',
    'Incorpora el art. 19 BIS (Secc. IX) y los arts. 21 BIS y 21 TER (Secc. X): distribución de documentos de oferta preliminares con leyendas según el régimen, en línea con la RG 1129 para Emisoras.',
    'Incorpora el art. 3° del Cap. II del Tít. XVIII (disposición transitoria) y agrega al glosario del Tít. I las denominaciones de los regímenes de FF con autorización automática y el "Régimen General de FF".'],
    notas=['Antecedente: consulta pública de la RG 1133/2026.',
           'El art. 6° de la RG contiene leyendas entre comillas dentro del texto citado; se extrajo como bloque para no perder el art. 21 TER.'])
