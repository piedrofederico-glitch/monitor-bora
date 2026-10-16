import normas as N, fichas
n = 1162
b = lambda k: N.md(N.bloque(n, k))
N.glosario(N.definiciones(b(1)), n=n, art_rg=1)
caps = [(r, nom, N.md(x)) for r, nom, x in N.dividir_capitulos(N.bloque(n, 2))]
assert [c[0] for c in caps] == ['I', 'II', 'III', 'IV', 'V', 'VI']
N.sustituir_titulo('XII', caps, n, 2)
fichas.ficha(n, [
    'Simplifica y sustituye completo el Título XII ("Transparencia en el ámbito de la oferta pública"), con sus seis capítulos y los Anexos I a V del Cap. VI.',
    'Actualiza el régimen de Hechos Relevantes: adapta los supuestos a la práctica, menciona expresamente los EECC o EEFF anuales e intermedios como base de cálculo y agrega supuestos nuevos.',
    'Alinea el régimen informativo con buenas prácticas internacionales de gobierno corporativo y armoniza la redacción con el resto de las Normas.',
    'Incorpora al glosario del Tít. I la sigla "UTs" (uniones transitorias de empresas).'])
