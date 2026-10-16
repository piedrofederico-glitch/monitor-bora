import normas as N, fichas
n = 1090
N.VIGENCIAS[n] = '02/02/2026'
A = {a['num']: a for a in N.rg_articulos(n)}
cita = lambda k, i=0: N.md(A[k]['citas'][i])

# art. 1°: sustituye art. 29, Secc. IX, Cap. I, Tít. VI
N.sustituir_articulo('VI', 'I', '29', cita(1), n, 1, seccion='IX')
# art. 2°: deroga secciones del Cap. V del Tít. VI
for s in ['X', 'XI', 'XII', 'XIV', 'XV', 'XVI', 'XVII', 'XX', 'XXI']:
    N.derogar_seccion('VI', 'V', s, n, 2)
# arts. 4° y 5°: renumera artículos (antes de renumerar las secciones, para ubicarlos por sección)
for viejo, nuevo in zip(range(65, 70), range(27, 32)):
    N.renumerar_articulo('VI', 'V', str(viejo), str(nuevo), n, 4, seccion='XVIII')
for viejo, nuevo in zip(range(70, 73), range(32, 35)):
    N.renumerar_articulo('VI', 'V', str(viejo), str(nuevo), n, 5, seccion='XIX')
# art. 3°: renumera secciones
N.renumerar_seccion('VI', 'V', 'XVIII', 'X', n, 3)
N.renumerar_seccion('VI', 'V', 'XIX', 'XI', n, 3)
# art. 6°: incorpora Capítulo VI del Título VI
ps = cita(6)
assert ps[0].startswith('CAPITULO VI - ')
N.sustituir_capitulo('VI', 'VI', 'NEGOCIACIÓN SECUNDARIA DE VALORES NEGOCIABLES DE EMISION INDIVIDUAL QUE GOZAN DE OFERTA PÚBLICA.',
                     ps[1:], n, 6, nota_tipo='Capítulo incorporado')
# art. 7°: art. 14 del Cap. IV del Tít. XVIII ; art. 8°: art. 6° del Cap. XI del Tít. XVIII
N.incorporar_articulo('XVIII', 'IV', cita(7), n, 7, despues_de='13')
N.incorporar_articulo('XVIII', 'XI', cita(8), n, 8, despues_de='5')

fichas.ficha(n, [
    'Reformula el régimen de negociación secundaria de valores negociables de emisión individual (cheques de pago diferido, pagarés, letras de cambio, facturas de crédito electrónicas MiPyMEs, certificados de depósito y warrants, plazos fijos, letras hipotecarias).',
    'Concentra ese régimen en un nuevo Capítulo VI del Título VI, con disposiciones comunes, reglas para ACRyP y Mercados, segmentos de negociación (avalado, directo garantizado y no garantizado) y secciones por instrumento.',
    'Deroga las Secciones X a XII, XIV a XVII, XX y XXI del Cap. V del Tít. VI y renumera las Secciones XVIII (remates) y XIX (hacedor de mercado) como X y XI, con sus artículos 65 a 72 como 27 a 34.',
    'Sustituye el art. 29 del Cap. I del Tít. VI: los Mercados deben habilitar un mecanismo gratuito de difusión de información sobre los instrumentos de emisión individual y sus libradores.',
    'Ordena a Mercados y ACRyP adecuar sus reglamentaciones antes de la entrada en vigencia (arts. 14 del Cap. IV y 6° del Cap. XI del Tít. XVIII).'],
    vigencia='02/02/2026', vigencia_txt='art. 9°: entra en vigencia el 2 de febrero de 2026',
    notas=['No figura en el PDF base (texto CNV del 12/12/2025) por su vigencia diferida: se aplicó antes de la RG 1095 (ver normas-cnv/base.md).',
           'Las secciones derogadas se retiraron de vigente/ y su texto completo está en historial/titulo-VI/capitulo-V.md; en su lugar queda una nota de derogación.',
           'La Sección XIII del Cap. V ya estaba derogada (RG 1046) y conserva su número.'])
