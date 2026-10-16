import normas as N, fichas
n = 1120
N.VIGENCIAS[n] = '13/03/2026'
A = {a['num']: a for a in N.rg_articulos(n)}
N.sustituir_articulo('XVIII', 'IV', '15', N.md(A[1]['citas'][0]), n, 1)
fichas.ficha(n, [
    'Sustituye el art. 15 del Cap. IV del Tít. XVIII (cronograma de la RG 1113 para el régimen informativo de posiciones en futuros y opciones).',
    'Unifica en el 31 de marzo de 2026 el plazo para remitir la información de agosto de 2025 a enero de 2026 (detalle semanal) y la de febrero de 2026 en adelante (detalle diario).',
    'Sus disposiciones se aplican desde el 10 de marzo de 2026 (art. 2°), por ser más favorables al administrado.'],
    vigencia='13/03/2026', vigencia_txt='art. 3°: desde el día de su publicación; aplicable desde el 10/03/2026 según art. 2°')
