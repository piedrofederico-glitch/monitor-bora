import normas as N, fichas
n = 1107
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
defs = [p for p in md(1) if p.startswith('“')]
assert [d[:6] for d in defs] == ['“FCE M', '“VNEI”'], defs
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1, 'Términos “FCE MiPyMEs” y “VNEI” incorporados',
                     det_extra='términos “FCE MiPyMEs” y “VNEI”')
N.sustituir_articulo('VI', 'VI', '17', md(2), n, 2, seccion='X')
N.incorporar_articulo('XVIII', 'XI', md(3), n, 3, despues_de='6')
fichas.ficha(n, [
    'Incorpora al glosario del Tít. I las definiciones de "FCE MiPyMEs" y "VNEI" (valores negociables de emisión individual).',
    'Sustituye el art. 17 de la Secc. X del Cap. VI del Tít. VI (régimen de la RG 1090): los Agentes no pueden emitir o librar VNEI salvo ALyC Participante Directo, ALyC Integral-Agroindustrial, AN RUCA o ALyC bancos, o si se trata de FCE MiPyMEs o VNEI del segmento avalado.',
    'Incorpora el art. 7° del Cap. XI del Tít. XVIII: los ACRyP deben adecuar sus sistemas al canje de VNEI (art. 5°, Cap. VI, Tít. VI) antes del 6 de abril de 2026.'],
    notas=['La definición de "FCE MiPyMEs" dice "facturas de crédito eElectrónicas MiPyMEs": se transcribe tal como se publicó.'])
