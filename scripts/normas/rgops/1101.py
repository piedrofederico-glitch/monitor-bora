import normas as N, fichas
n = 1101
A = {a['num']: a for a in N.rg_articulos(n)}
caps = [(r, nom, N.md(x)) for r, nom, x in N.dividir_capitulos(A[1]['citas'][0])]
assert [c[0] for c in caps] == ['I', 'II', 'III']
N.sustituir_titulo('III', caps, n, 1)
fichas.ficha(n, [
    'Sustituye completo el Título III (retiro de la oferta pública, cancelaciones, ofertas públicas de adquisición y aportes irrevocables).',
    'Precisa qué órganos sociales pueden decidir el retiro y la cancelación de la oferta pública.',
    'Incorpora supuestos de cancelación automática, en particular al vencer el plazo de la última clase o serie emitida.',
    'Reescribe el Cap. II ("Ofertas públicas de adquisición o canje") y el Cap. III (aportes irrevocables a cuenta de futuras emisiones y capitalización de deudas).'])
