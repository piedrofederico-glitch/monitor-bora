import normas as N, fichas, re
n = 1167
b = lambda k: N.md(N.bloque(n, k))
N.glosario(N.definiciones(b(1)), n=n, art_rg=1)
ps = b(2)
assert ps[0] == 'CAPÍTULO X'
nombre = ps[1].lstrip('“')
N.sustituir_capitulo('V', 'X', nombre, ps[2:], n, 2, nota_tipo='Capítulo incorporado')
A = {a['num']: a for a in N.rg_articulos(n)}
Ls = N.rg_lineas(n)[A[3]['ini']:A[3]['fin']]
k = next(x for x, l in enumerate(Ls) if l and l.strip().startswith('"SECCIÓN VII'))
Ls = [l for l in Ls[k:]]
Ls[0] = Ls[0].replace('"', '', 1)
for x in range(len(Ls) - 1, -1, -1):
    if Ls[x] and Ls[x].rstrip().endswith('".'):
        Ls[x] = Ls[x].rstrip()[:-2] + '.'; break
N.incorporar_seccion('XI', None, N.md(Ls), n, 3)
fichas.ficha(n, [
    'Reglamenta los Fondos de Asistencia Laboral (FAL) de la Ley de Modernización Laboral N° 27.802 y su Decreto Reglamentario N° 408/2026 como productos de inversión colectiva: incorpora el Cap. X del Tít. V ("PIC FAL"), con disposiciones comunes (Secc. I), FCIA FAL (Secc. II) y FF FAL (Secc. III).',
    'Regula las Entidades Habilitadas (EH) para administrar PIC FAL, la Ficha FAL, el ID FAL y las cuentas individuales de los empleadores.',
    'Incorpora la Secc. VII del Tít. XI: las EH pagan al trabajador que indique el cliente ante la extinción de la relación laboral (art. 58 de la Ley 27.802), con excepción del procedimiento de entrega de fondos del art. 3° de la Secc. II del Tít. XI.',
    'Agrega al glosario del Tít. I once términos del régimen FAL.'],
    notas=['Antecedente: consulta pública de la RG 1161/2026.',
           'El nombre del Capítulo X se publicó con una comilla de apertura sin cierre ("“PRODUCTOS DE INVERSIÓN COLECTIVA..."); se omitió en el encabezado del archivo.',
           'El art. 3° usa comillas rectas; la Sección VII se tomó entre ellas. La definición de "PIC FAL" también tiene comillas desbalanceadas en el original y se transcribe tal cual.'])
