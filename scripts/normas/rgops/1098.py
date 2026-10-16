import normas as N, fichas
n = 1098
A = {a['num']: a for a in N.rg_articulos(n)}
N.incorporar_seccion('XVIII', 'XV', N.md(A[1]['citas'][0]), n, 1)
fichas.ficha(n, [
    'Incorpora la Secc. V al Cap. XV del Tít. XVIII: suspende transitoriamente la percepción de la tasa de fiscalización y control del año 2026 hasta el 2 de febrero de 2026 inclusive.',
    'Alcanza a los sujetos y fechas de pago de los incisos a), b), c), e) y f) del art. 3° del Cap. I del Tít. XVII.',
    'No beneficia a quienes estén en mora con la tasa de años anteriores.'],
    notas=['El artículo incorporado lleva el número 5°, que ya existe en la Secc. II del mismo capítulo: se transcribe tal como lo publicó la RG.',
           'El texto citado termina sin punto final ("...años anteriores"); se respeta la redacción publicada.'])
