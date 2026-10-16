import normas as N, fichas
n = 1121
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
defs = N.definiciones(md(1))
assert len(defs) == 1
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1, 'Término “IOSCO” incorporado', det_extra='término “IOSCO”')
N.incorporar_articulo('V', 'I', md(2), n, 2, despues_de='31', seccion='VII')

comun = lambda tipo, filas, digital: [
    f'### ANEXO III - MODELO FICHA UNICA FCI ABIERTOS CONFORME ARTICULO 31 BIS DE LA SECCION VII DEL CAPITULO I DEL TITULO V {tipo}',
    '| LOGOTIPO SOCIEDAD GERENTE | NOMBRE COMPLETO DEL FCI Fecha del reporte | LOGOTIPO SOCIEDAD DEPOSITARIA |\n|---|---|---|',
    'DESCRIPCIÓN DEL FCI. OBJETIVO Y POLÍTICA DE INVERSIÓN',
    'INFORMACIÓN DEL FCI',
    'Patrimonio neto:\nMoneda del FCI:\nMonto mínimo de suscripción:\nPlazo de pago de rescates:\nClasificación:\nHorizonte de inversión:\nIndicador de riesgo: Bajo/Medio/Alto\nPerfil de inversor: Conservador/Moderado/Agresivo\nNúmero de registro ante CNV:\nFecha de inicio de operaciones:\nIdentificación de los Auditores del FCI:\nCorreo electrónico de contacto:\nCalificación de riesgo y Benchmark, de corresponder:',
    'RENDIMIENTO HISTÓRICO',
    '| Valor Cuotaparte | CLASE A | CLASE B | CLASE C |\n|---|---|---|---|\n' + '\n'.join(filas),
    'COMPOSICIÓN DE LA CARTERA',
    '[Gráfico de torta de ejemplo: Disponibilidades; 45,43% — Operaciones a Plazo; 40,66% — Títulos de Deuda; 10,86% — Otros Activos y Pasivos; 3,04%]',
    'HONORARIOS, GASTOS Y COMISIONES',
    '| | CLASE A | CLASE B | CLASE C |\n|---|---|---|---|\n| Honorarios Sociedad Gerente y Sociedad Depositaria (*) (**) | % | % | % |\n| Comisiones suscripción, de rescate y de transferencia | % | % | % |\n| Honorarios de éxito | % | % | % |\n| Gastos ordinarios de gestión (Promedio últimos 3 meses) | % | % | % |',
    '(*) Los Honorarios de la Sociedad Depositaria incluyen IVA,',
    '(**) Incluye la retribución de los Agentes de la Colocación de las cuotapartes.',
    'PRINCIPALES TENENCIAS',
    '[Gráfico de barras de ejemplo con tenencias por cuenta corriente bancaria (valores ilustrativos).]',
    'EVOLUCIÓN VALOR CUOTAPARTE',
    '[Gráfico de línea de ejemplo con la evolución diaria del valor de la cuotaparte (valores ilustrativos).]',
    'TRATAMIENTO IMPOSITIVO',
    'Enlace directo de acceso público al régimen impositivo aplicable',
] + (['ACCESO DIGITAL', 'Enlace directo de acceso público al comparador de FCI disponible en el sitio web de la CAFCI (Fondos de Dinero)'] if digital else []) + [
    'Las inversiones en cuotas del FCI no constituyen depósitos en… (denominación de la entidad financiera interviniente), a los fines de la Ley de Entidades Financieras ni cuentan con ninguna de las garantías que tales depósitos a la vista o a plazo puedan gozar de acuerdo a la legislación y reglamentación aplicables en materia de depósitos en entidades financieras. Asimismo, (denominación de la entidad financiera interviniente) se encuentra impedida por normas del BCRA de asumir, tácita o expresamente, compromiso alguno en cuanto al mantenimiento, en cualquier momento, del valor del capital invertido, al rendimiento, al valor de rescate de las cuotapartes o al otorgamiento de liquidez a tal fin.']
f1 = ['| 7 días | TNA | TNA | TNA |', '| 1 mes | TNA | TNA | TNA |', '| 90 días | TNA | TNA | TNA |', '| 180 días | TNA | TNA | TNA |', '| En el año | TNA | TNA | TNA |', '| 12 meses | TNA | TNA | TNA |']
f2 = ['| 1 mes | Directo | Directo | Directo |', '| 90 días | Directo | Directo | Directo |', '| 180 días | Directo | Directo | Directo |', '| En el año | Directo | Directo | Directo |', '| 12 meses | Directo | Directo | Directo |']
aviso = ('[Nota de consolidación: el Anexo (IF-2026-30433786-APN-GAL#CNV) se publicó como dos páginas de imagen. Se transcriben sus títulos, rótulos, tablas y textos; '
         'los gráficos de ejemplo se describen entre corchetes. El art. 3° de la RG 1121/2026 lo incorpora como Anexo III del Capítulo III del Título V, '
         'aunque el art. 31 BIS (Secc. VII, Cap. I, Tít. V) remite al "Anexo III del presente Capítulo".]')
anexo = comun('FONDOS COMUNES DE DINERO', f1, True)
anexo = [anexo[0], aviso] + anexo[1:] + ['ANEXO III - MODELO FICHA UNICA FCI ABIERTOS CONFORME ARTICULO 31 BIS DE LA SECCION VII DEL CAPITULO I DEL TITULO V OTROS FCI (DISTINTOS DE FONDOS COMUNES DE DINERO)'] + comun('', f2, False)[1:]
N.incorporar_anexo('V', 'III', anexo, n, 3, nombre='Anexo III')
N.incorporar_seccion('XVIII', 'III', md(4), n, 4)
fichas.ficha(n, [
    'Crea la "Ficha Única" mensual de cada FCI abierto (art. 31 BIS, Secc. VII, Cap. I, Tít. V): la Sociedad Gerente la publica en su sitio web dentro de los primeros 10 días hábiles de cada mes y los colocadores la difunden en sus canales.',
    'Fija el contenido mínimo: descripción y política de inversión, datos del fondo, rendimiento histórico por clase, composición de cartera, principales tenencias, honorarios y gastos, tratamiento impositivo, advertencia y, para Fondos Comunes de Dinero, enlace al comparador de la CAFCI.',
    'Aprueba el modelo de Ficha Única (Anexo) para Fondos Comunes de Dinero y para los demás FCI.',
    'Da plazo de 30 días hábiles (Fondos Comunes de Dinero) y 60 días hábiles (resto) para implementarla (Secc. X, Cap. III, Tít. XVIII).',
    'Incorpora al glosario del Tít. I la sigla IOSCO.'],
    notas=['Antecedente: consulta pública de la RG 1106/2026.',
           'El Anexo se publicó como imagen (págs. 7 y 8 del PDF CNV): se transcribió su texto y se describieron los gráficos de ejemplo.',
           'Discrepancia de ubicación: el art. 3° lo incorpora como Anexo III del Capítulo III del Título V (FCI cerrados), mientras que el art. 31 BIS del Capítulo I remite al "Anexo III del presente Capítulo". Se aplicó literalmente el art. 3°; queda pendiente verificar el criterio de InfoLEG y de la CNV.'])
