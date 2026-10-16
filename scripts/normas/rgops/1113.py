import normas as N, fichas
n = 1113
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
N.incorporar_articulo('VI', 'I', md(1), n, 1, despues_de='56', seccion='XXIV')
anexo = md(2)
assert anexo[0].startswith('### ANEXO IX')
tabla = ('| Fecha | Nombre producto / Subyacente | Unidad de medida o Moneda | Lado | Denominación ALyC (de contar con este dato) | CUIT ALyC | Nro Cuenta Comitente | '
         'Posición abierta (delta contratos/lotes) | Posición Abierta (delta um) | Posición abierta (en valores $ o USD) | Porcentaje | '
         'Interés Abierto Total Mercado (delta contratos/lotes) | Interés Abierto Total Mercado (en valores $ o USD) |\n'
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|')
anexo = anexo + ['[Tabla publicada como imagen en la RG 1113/2026 (pág. 2 del PDF CNV). Transcripción de los encabezados de columna; las filas están vacías en el original.]', tabla]
N.incorporar_anexo('VI', 'I', anexo, n, 2)
N.incorporar_articulo('XVIII', 'IV', md(3), n, 3, despues_de='14')
fichas.ficha(n, [
    'Crea un régimen informativo semanal de posiciones abiertas en futuros y opciones: los Mercados remiten a la CNV, dentro de los dos días de cada semana, el detalle diario por ALyC y comitente (art. 56 BIS, Secc. XXIV, Cap. I, Tít. VI).',
    'Excluye a los ALyC Participantes Directos, a los que son entidades financieras y a la cartera propia ampliada.',
    'Incorpora el Anexo IX del Cap. I del Tít. VI con los campos a informar (posición abierta e interés abierto total del Mercado).',
    'Fija un cronograma inicial (art. 15, Cap. IV, Tít. XVIII): agosto de 2025 a enero de 2026 antes del 31/03/2026 y desde febrero de 2026 antes del 10/03/2026.'],
    notas=['El Anexo IX es una tabla publicada como imagen: se transcribieron sus encabezados y se dejó constancia en vigente/.',
           'El texto del art. 15 incorporado termina sin punto final; se respeta la redacción publicada.'])
