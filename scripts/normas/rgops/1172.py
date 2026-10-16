import normas as N, fichas
n = 1172
b = lambda k: N.md(N.bloque(n, k))
N.glosario(N.definiciones(b(1)), n=n, art_rg=1)
ps = b(2); assert ps[0] == 'CAPÍTULO III' and ps[1] == 'PSAV'
N.sustituir_capitulo('XIV', 'III', ps[1], ps[2:], n, 2)
nuevo = [p for p in b(3) if p.startswith('18)')]
assert len(nuevo) == 1
N.modificar_articulo('XV', 'I', '11', N.parrafo('18) PSAV_014 - Informe Mensual Clientes y Operaciones.', nuevo, hasta_siguiente_termino=False),
                     n, 3, 'Subinciso 18) del inciso S) sustituido', det_extra='inc. S), subinc. 18)')
N.incorporar_articulo('XVIII', 'XIV', b(4), n, 4, despues_de='4')
fichas.ficha(n, [
    'Sustituye íntegramente el Cap. III del Tít. XIV (PSAV): procedimiento para incorporar nuevas categorías de actividades o cambiar la denominación social; incorpora al texto los Criterios Interpretativos N° 95, 96 y 97 (sociedades locales y sucursales o representaciones de sociedades extranjeras, patrimonio neto mínimo, capital y aportes irrevocables, objeto y estatuto social) y los deja sin efecto; condiciones para la cancelación de la inscripción o el cese de categorías (aviso previo a clientes, tratamiento de saldos); nuevas modalidades de presentación del inciso b) del art. 40.',
    'Incorpora el Anexo I del Cap. III del Tít. XIV: instructivo del régimen informativo de los PSAV.',
    'Incorpora al glosario (art. 2°, Cap. II, Tít. I) los términos “ARS” o “PESOS”, “BTC”, “USD”, “USDC” y “USDT”.',
    'Sustituye el subinciso 18) del inc. S) del art. 11 del Cap. I del Tít. XV: formulario “PSAV_014-Informe Mensual: Clientes, Operaciones y Custodia”.',
    'Incorpora el art. 5° del Cap. XIV del Tít. XVIII: la información periódica del inc. b) del art. 40 del Cap. III del Tít. XIV se aplica desde el 1° de noviembre de 2026.'],
    notas=['Los Criterios Interpretativos N° 95, 96 y 97 no forman parte del texto de las Normas; su supresión se registra sólo en esta ficha.'])
