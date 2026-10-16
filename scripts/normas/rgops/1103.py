import normas as N, fichas
n = 1103
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
nuevo = [p for p in md(1) if p.startswith('b) ')]
assert len(nuevo) == 1
N.modificar_articulo('XVII', 'I', '3', N.tramo('b) Los Agentes Depositarios Centrales', 'c) Las Emisoras de Acciones', nuevo), n, 1,
                     'Inciso b) sustituido', det_extra='inc. b)')
for k, ps in N.por_articulo(md(2)):
    N.sustituir_articulo('XVII', 'I', k, ps, n, 2)
N.incorporar_articulo('XVII', 'I', md(3), n, 3, despues_de='12')
N.sustituir_seccion('XVIII', 'XV', 'V', md(4), n, 4)
fichas.ficha(n, [
    'Adecua tasas y aranceles del Tít. XVII a la resolución del Ministerio de Economía que actualizó los montos que percibe la CNV.',
    'Sustituye el inc. b) del art. 3° (sujetos y fechas de la tasa de fiscalización y control de ADCVN, ACR, ACRyP, AN, AN RUCA, AAGI, ALyC y otros agentes).',
    'Reemplaza los arts. 5° (arancel de autorización de ON y fideicomisos financieros, autónomos y por programa) y 6° (arancel del régimen de Emisor Frecuente).',
    'Incorpora el art. 13: pago de la tasa de "otros servicios" al pedir el certificado de vigencia.',
    'Sustituye la Secc. V del Cap. XV del Tít. XVIII (creada por la RG 1098): mantiene la suspensión de la tasa 2026 y fija la nueva fecha de pago (arts. 9° y 10).'])
