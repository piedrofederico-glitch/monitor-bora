import normas as N, fichas
n = 1138
A = {a['num']: a for a in N.rg_articulos(n)}
h = [p for p in N.md(A[1]['citas'][0]) if p.startswith('h) ')]
assert len(h) == 1
N.modificar_articulo('XII', 'V', '10', N.insertar_antes('Para su alta en el registro de idóneos', h), n, 1, 'Inciso h) incorporado', det_extra='inc. h)')
fichas.ficha(n, [
    'Incorpora el inciso h) al art. 10 de la Secc. I del Cap. V del Tít. XII (eximición de módulos del examen de idóneos).',
    'Exime de los Módulos 4, 5 y 6 a quienes acrediten la Maestría en Dirección de Finanzas y Control (orientación Finanzas de Empresas y Mercado de Capitales) de la UADE; deben rendir los Módulos 1, 2 y 3.'],
    notas=['La cita reproduce también el párrafo final del artículo con otra grafía ("Registro de Idóneos", sin punto final). Como el art. 1° sólo ordena incorporar el inciso h), se mantuvo el párrafo final vigente.'])
