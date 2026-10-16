import normas as N, fichas
n = 1114
A = {a['num']: a for a in N.rg_articulos(n)}
N.sustituir_articulo('XXI', 'I', '1', N.md(A[1]['citas'][0]), n, 1, seccion='I')
fichas.ficha(n, [
    'Sustituye el art. 1° de la Secc. I del Cap. I del Tít. XXI (anotación de boletos, art. 10 del Decreto N° 1017/2024), redactado una semana antes por la RG 1109.',
    'Agrega a la Bolsa de Comercio de Bahía Blanca S.A. entre las entidades que pueden llevar el servicio de anotación.',
    'El resto del artículo se mantiene; el texto nuevo termina sin punto final ("...actividades complementarias permitidas").'])
