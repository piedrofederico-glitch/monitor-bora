import normas as N, fichas
n = 1166
N.VIGENCIAS[n] = '15/09/2026'
N.sustituir_articulo('XI', None, '3', N.md(N.bloque(n, 1)), n, 1, seccion='II')
fichas.ficha(n, [
    'Sustituye el art. 3° de la Secc. II del Tít. XI: los sujetos obligados reciben y entregan fondos de clientes exclusivamente por transferencias bancarias en el país (con las excepciones para ALyC I AGRO, ALyC Integral con AN agroindustrial e inversores extranjeros con custodio local).',
    'Elimina los cheques como medio de recepción y pago de fondos de clientes, para asegurar la disponibilidad inmediata de los fondos y evitar rechazos.',
    'Aclara que no afecta la negociación de cheques de pago diferido.'],
    vigencia='15/09/2026', vigencia_txt='art. 2°: desde el día de su publicación en el BO')
