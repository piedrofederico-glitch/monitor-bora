import normas as N, fichas
n = 1148
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
N.sustituir_articulo('V', 'III', '20', md(1), n, 1, seccion='I')
N.sustituir_seccion('V', 'III', 'III', md(2), n, 2)
N.sustituir_anexo('XVI', 'II', 'II', md(3), n, 3)
N.incorporar_seccion('XVIII', 'III', N.md(N.bloque(n, 4)), n, 4)
fichas.ficha(n, [
    'Establece un procedimiento de autorización automática de oferta pública para FCI cerrados: sustituye la Secc. III del Cap. III del Tít. V (arts. 26 a 37).',
    'Sustituye el art. 20 de la Secc. I del Cap. III del Tít. V.',
    'Sustituye el Anexo II del Cap. II del Tít. XVI (facultades delegadas en la Gerencia de Fondos Comunes de Inversión).',
    'Incorpora la Secc. XII del Cap. III del Tít. XVIII: los trámites iniciados antes de la RG que opten por el régimen automático quedan sin efecto y se canalizan con la publicación del prospecto y del reglamento en la AIF.'],
    notas=['Antecedente: consulta pública de la RG 1135/2026.',
           'El texto citado del art. 4° no tiene comilla de cierre: se tomó hasta el fin del artículo. Remite a "lo dispuesto en el artículo siguiente", que la RG no incorpora (la Secc. XII sólo tiene el art. 26): se transcribe tal cual.'])
