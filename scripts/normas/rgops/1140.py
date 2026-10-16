import normas as N, fichas
n = 1140
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
ps = md(1); a = ps.index('2. Transferencias en el país.')
nuevo = [p for p in ps[a + 1:] if p not in ('(…)',)]
assert nuevo[0].startswith('a) Recibos de clientes.') and len(nuevo) == 3
N.modificar_articulo('XI', None, '3', N.tramo('a) Recibos de clientes. Deberán efectuarse desde cuentas bancarias', 'b) Pagos a clientes. Deberán cursarse', nuevo),
                     n, 1, 'Subinciso a) del inciso 2. sustituido', seccion='II', det_extra='inc. 2., subinc. a)')
N.sustituir_anexo('XVI', 'II', 'IV', md(2), n, 2)
fichas.ficha(n, [
    'Rectifica un error material de la RG 1139 en el subinciso a) del inciso 2. del art. 3° de la Secc. II del Tít. XI: el convenio de liquidación con un AN de corretaje de granos corresponde al "ALyC Integral" (no al "ALyC I AGRO").',
    'Sustituye el Anexo IV del Cap. II del Tít. XVI: la inscripción y cancelación en los Registros de Auditores Externos y de Asociaciones de Profesionales Auditores pasa a la Gerencia y Subgerencia de Control de Auditores.',
    'Mantiene en la Gerencia de Registro y Control las advertencias y la inscripción y cancelación en el Registro de PSAV, y en las Subgerencias de Control Societario y Contable las conformidades estatutarias y los registros digitales.'],
    notas=['El PDF publicado por la CNV es una imagen escaneada sin texto: se usó el texto publicado en el Boletín Oficial (aviso de la edición del 21/05/2026), cotejado con InfoLEG.',
           'En el Anexo IV el BO publica el contenido como tabla; se transcribe un renglón por facultad.'])
