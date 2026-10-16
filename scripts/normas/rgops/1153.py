import normas as N, fichas
n = 1153
N.VIGENCIAS[n] = '18/06/2026'
A = {a['num']: a for a in N.rg_articulos(n)}
N.incorporar_seccion('XVIII', 'III', N.md(N.bloque(n, 1)), n, 1)
fichas.ficha(n, [
    'Incorpora la Secc. XIII al Cap. III del Tít. XVIII (arts. 27 a 29): suspende transitoriamente la suscripción de cuotapartes, la autorización de nuevos fondos y las reformas de reglamentos de FCIA para inversores calificados con inversiones en activos del exterior.',
    'Vinculada al tope de patrimonio de los fondos para inversores calificados en moneda extranjera previsto en la disposición transitoria de una RG anterior que cita en sus considerandos.'],
    vigencia='18/06/2026', vigencia_txt='art. 2°: desde el día de su publicación en el BO')
