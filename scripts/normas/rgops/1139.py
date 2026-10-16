import normas as N, fichas, json
n = 1139
A = {a['num']: a for a in N.rg_articulos(n)}
md = lambda k: N.md(A[k]['citas'][0])
defs = N.definiciones(md(1))
assert len(defs) == 5
N.modificar_articulo('I', 'II', '2', N.termino_nuevo(defs), n, 1, 'Términos “ALyC I AGRO”, “CSNU”, “CVU”, “PEN” y “PSP” incorporados',
                     det_extra='términos “ALyC I AGRO”, “CSNU”, “CVU”, “PEN” y “PSP”')
d2 = N.definiciones(md(2))
assert len(d2) == 1 and d2[0].startswith('“PLA/FT/FP”')
N.modificar_articulo('I', 'II', '2', N.parrafo('“PLAFTFP” y significa', d2), n, 2, 'Definición de “PLAFTFP” sustituida por “PLA/FT/FP”',
                     det_extra='definición “PLAFTFP” → “PLA/FT/FP”')
ps = md(3)
assert ps[0] == 'TÍTULO XI'
nombre = ps[1]
N.sustituir_titulo('XI', [(None, nombre, ps[2:])], n, 3)
d = json.load(open(N.TITJ)); d['XI']['nombre'] = nombre.rstrip('.'); json.dump(d, open(N.TITJ, 'w'), ensure_ascii=False, indent=1)
t = md(4); k = t.index('T) SUJETOS OBLIGADOS PLA/FT/FP.')
N.modificar_articulo('XV', 'I', '11', N.insertar_despues('22) PSAV_018 - Acta Constitutiva y Estatuto vigente PSAV.', t[k:]), n, 4,
                     'Inciso T) incorporado', det_extra='inc. T)')
(rom, nom, L), = N.dividir_capitulos(A[5]['citas'][0])
N.sustituir_capitulo('XVIII', 'X', nom, N.md(L), n, 5)
fichas.ficha(n, [
    'Sustituye completo el Título XI, que pasa a denominarse "Prevención del lavado de activos y financiación del terrorismo y de la proliferación de armas de destrucción masiva" (Secciones I a V y Anexo I).',
    'Define los sujetos obligados del mercado de capitales (AN, ALyC, ACD de FCI, AAGI, fiduciarios financieros, PFC y PSAV) y los deberes de cumplimiento de la Ley de Lavado, la UIF y las decisiones del CSNU.',
    'Agrega el inciso T) al art. 11 del Cap. I del Tít. XV con los formularios LAV de la AIF para sujetos obligados PLA/FT/FP.',
    'Sustituye el Cap. X del Tít. XVIII (disposiciones transitorias PLA/FT): entre otras, difiere al 1° de julio de 2026 obligaciones de remisión de información para PSAV y sujetos obligados.',
    'En el glosario del Tít. I incorpora ALyC I AGRO, CSNU, CVU, PEN y PSP y reemplaza "PLAFTFP" por "PLA/FT/FP".'],
    notas=['El Título XI no tiene capítulos: vigente/titulo-XI/titulo-XI.md. La denominación nueva figura en vigente/INDICE.md.',
           'El art. 4° cita el encabezado del art. 11 del Cap. I del Tít. XV con comillas internas; se tomó el inciso T) completo desde su encabezado.'])
