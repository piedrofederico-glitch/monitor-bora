import normas as N, fichas
n = 1116
A = {a['num']: a for a in N.rg_articulos(n)}
N.sustituir_articulo('V', 'IV', '18', N.md(A[1]['citas'][0]), n, 1, seccion='IX')
fichas.ficha(n, [
    'Sustituye el art. 18 de la Secc. IX del Cap. IV del Tít. V (fideicomisos financieros: programas globales y fiduciantes).',
    'Permite denominar igual y numerar correlativamente los fideicomisos de un mismo Programa Global que mantengan el Fiduciario y la identidad sustancial de los Fiduciantes.',
    'Considera que hay identidad sustancial del Fiduciante si no hubo sustitución, extinción o disolución que altere de manera relevante el activo subyacente y las condiciones de riesgo.',
    'Se aplica también a los fideicomisos constituidos bajo regímenes de autorización automática.'])
