import normas as N, fichas
n = 1118
A = {a['num']: a for a in N.rg_articulos(n)}
N.derogar_capitulo_y_quitar('XIV', 'II', n, 1)
den = N.md(A[2]['citas'][0])
assert den[0] == 'TÍTULO XIV.'
N.sustituir_denominacion_titulo('XIV', den[1], n, 2)
fichas.ficha(n, [
    'Deroga el Cap. II del Tít. XIV ("Hub de Innovación e Inclusión Financiera", creado por la RG 926), que según la CNV se había convertido en una instancia adicional sin los resultados buscados.',
    'Sustituye la denominación del Tít. XIV: "PLATAFORMA DE FINANCIAMIENTO COLECTIVO. REGISTRO DE PROVEEDORES DE SERVICIOS DE ACTIVOS VIRTUALES".',
    'El Cap. III (PSAV) conserva su número.'],
    notas=['La denominación de cada Título figura en vigente/INDICE.md; la anterior quedó en historial/titulo-XIV/denominacion.md.',
           'El texto derogado del Cap. II está en historial/titulo-XIV/capitulo-II-derogado-RG-1118-2026.md.'])
