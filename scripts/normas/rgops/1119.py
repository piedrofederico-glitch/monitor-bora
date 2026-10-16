import normas as N, fichas
n = 1119
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
N.sustituir_articulo('II', 'IX', '14', md(1), n, 1, seccion='III')
N.sustituir_articulo('VI', 'IV', '11', md(2), n, 2, seccion='III')
fichas.ficha(n, [
    'Reduce a UN (1) día hábil el plazo de difusión y colocación primaria para los Emisores Frecuentes, con un mínimo de cinco horas de difusión.',
    'Sustituye el art. 11 de la Secc. III del Cap. IV del Tít. VI (colocación primaria) para prever esa reducción.',
    'Sustituye el art. 14 de la Secc. III del Cap. IX del Tít. II (prospecto): el período mínimo de difusión remite ahora al Cap. IV del Tít. VI.'],
    notas=['Antecedentes citados por la RG: consultas públicas de las RG 746 y 826.'])
