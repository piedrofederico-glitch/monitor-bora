import normas as N, fichas
n = 1170
b = lambda k: N.md(N.bloque(n, k))
N.sustituir_articulo('VI', 'VI', '7', b(1), n, 1, seccion='II')
N.sustituir_articulo('VI', 'VI', '17', b(2), n, 2, seccion='X')
N.sustituir_articulo('VIII', 'II', '2', b(3), n, 3, seccion='I')
N.sustituir_articulo('VIII', 'II', '13', b(4), n, 4, seccion='IV')
fichas.ficha(n, [
    'Habilita a los ACRyP, como actividad afín o complementaria, a registrar transferencias de VNEI vencidos e impagos bajo su custodia y previamente negociados en un Mercado, para que los tenedores puedan venderlos por tratativas privadas (a su ALyC o AN o a terceros por su intermedio).',
    'Sustituye el art. 2° (Secc. I) y el art. 13 (Secc. IV, patrimonio neto mínimo) del Cap. II del Tít. VIII: esa actividad no exige el incremento del 25% del patrimonio neto mínimo.',
    'Sustituye el art. 7° (Secc. II) del Cap. VI del Tít. VI (entrega del documento habilitante para la ejecución de VNEI impagos).',
    'Sustituye el art. 17 (Secc. X) del Cap. VI del Tít. VI: incluye entre los Agentes que pueden ser emisores o libradores de VNEI al ALyC I AGRO que simultáneamente sea ACDI.'])
