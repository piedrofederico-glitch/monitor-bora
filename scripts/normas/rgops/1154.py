import normas as N, fichas
n = 1154
N.VIGENCIAS[n] = '13/07/2026'
b = lambda k: N.md(N.bloque(n, k))
N.glosario(N.definiciones(b(1)), n=n, art_rg=1)
N.sustituir_articulo('VI', 'V', '2', b(2), n, 2, seccion='II')
N.incorporar_articulo('XVIII', 'V', b(3), n, 3, despues_de='28')
fichas.ficha(n, [
    'Redefine "Sujeto Restringido" en el glosario del Tít. I: precisa las exclusiones (Tesoro Nacional, FGS, sociedades con participación estatal mayoritaria que cotizan, entidades financieras y sus controladas de servicios financieros).',
    'Sustituye el art. 2° de la Secc. II del Cap. V del Tít. VI: los límites a operaciones de Sujetos Restringidos se miden en volumen nominal, por Mercado, sobre las cinco jornadas anteriores con negociación (o 5% del saldo en circulación si no hay volumen), y admite DDJJ del Sujeto Restringido.',
    'Incorpora el art. 29 del Cap. V del Tít. XVIII: los límites de volumen no se aplican a valores en cartera adquiridos antes de la RG 1154.'],
    vigencia='13/07/2026', vigencia_txt='art. 4°: desde el día de su publicación en el BO',
    notas=['El texto del art. 29 incorporado termina sin punto final; se respeta la redacción publicada.'])
