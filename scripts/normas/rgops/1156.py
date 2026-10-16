import normas as N, fichas
n = 1156
N.sustituir_articulo('VII', 'II', '39', N.md(N.bloque(n, 1)), n, 1)
fichas.ficha(n, [
    'Sustituye el art. 39 del Cap. II del Tít. VII (cálculo de los indicadores financieros de los ALyC, régimen de las RG 1130 y 1144).',
    'Para los ALyC I AGRO excluye del cálculo las partidas contables que correspondan a su actividad agroindustrial (antes, sólo las disponibilidades).',
    'Se aplica desde el 29 de abril de 2026 (art. 2°), por ser más favorable al administrado.'],
    vigencia_txt='aplicable desde el 29/04/2026 según art. 2°')
