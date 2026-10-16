import normas as N, fichas, re
n = 1169
b = lambda k: N.md(N.bloque(n, k))
E = ('(…)', '(...)', '(…).', '(…)”.')
N.glosario(N.definiciones(b(1)), n=n, art_rg=1)
N.sustituir_seccion('VI', 'I', 'XXI', b(2), n, 2)
N.sustituir_articulo('VI', 'I', '56', b(3), n, 3, seccion='XXIV')
N.incorporar_articulo('VI', 'I', b(4), n, 4, despues_de='56 BIS', seccion='XXIV')
for rom, L in N.dividir_secciones(N.bloque(n, 5)):
    N.sustituir_seccion('VI', 'IV', rom, N.md(L), n, 5)
N.sustituir_articulo('VI', 'IV', '13', b(6), n, 6, seccion='V')
N.sustituir_articulo('VI', 'IV', '16', b(7), n, 7, seccion='V')
A = {a['num']: a for a in N.rg_articulos(n)}
Ls = N.rg_lineas(n)[A[8]['ini']:A[8]['fin']]
k = next(x for x, l in enumerate(Ls) if l and l.strip().startswith('"ANEXO I'))
Ls = Ls[k:]; Ls[0] = Ls[0].replace('"', '', 1)
for x in range(len(Ls) - 1, -1, -1):
    if Ls[x] and Ls[x].rstrip().endswith('”.'):
        Ls[x] = Ls[x].rstrip()[:-2] + '.'; break
N.incorporar_anexo('VI', 'IV', N.md(Ls), n, 8)
ps = [re.sub(r'\s*\(…\)$', '', p) for p in b(9) if p not in E and not N.clave_art(p)]
grupos = {}; cur = None
for p in ps:
    if re.match(r'^[A-Z](\.\d)?\) [A-ZÁÉÍÓÚ]', p): cur = p; grupos[cur] = []
    else: grupos[cur].append(p)
anclas = {'A.1) EMISORAS:': 'A. 2) EMISORAS PYMES CNV:', 'G) MERCADOS:': 'H) CÁMARAS COMPENSADORAS:',
          'K) AGENTES DE NEGOCIACIÓN (AN):': 'L) AGENTES DE LIQUIDACIÓN Y COMPENSACIÓN (ALyC):',
          'L) AGENTES DE LIQUIDACIÓN Y COMPENSACIÓN (ALyC):': 'M) AGENTES PRODUCTORES (AP):'}
assert set(grupos) == set(anclas), grupos.keys()
def f9(pars):
    for g, anc in anclas.items():
        pars = N.insertar_antes(anc, grupos[g])(pars)
    return pars
N.modificar_articulo('XV', 'I', '11', f9, n, 9, 'Subincisos 27 a 30 del inc. A.1), 53 a 55 del inc. G), 41 a 43 del inc. K) y 48 a 50 del inc. L) incorporados',
                     det_extra='incs. A.1), G), K) y L): subincisos nuevos')
N.sustituir_articulo('XV', 'II', '3', b(10), n, 10)
N.incorporar_articulo('XVIII', 'IV', b(11), n, 11, despues_de='15')
N.incorporar_articulo('XVIII', 'V', b(12), n, 12, despues_de='29')
fichas.ficha(n, [
    'Reformula la colocación primaria: sustituye las Secciones I a IV del Cap. IV del Tít. VI (disposiciones generales, ingreso de ofertas, disposiciones particulares y estabilización) y los arts. 13 y 16 de la Secc. V, e incorpora el Anexo I del Cap. IV (información a remitir por los Mercados, o ALyC y AN en colocaciones internacionales).',
    'Sustituye la Secc. XXI del Cap. I del Tít. VI (requisitos para autorizar sistemas informáticos de negociación) y el art. 56, e incorpora el art. 56 TER (Secc. XXIV).',
    'Agrega formularios AIF de reportes de colocaciones primarias (EMI_067 a EMI_070) para Emisoras, Mercados, AN y ALyC y sustituye el art. 3° del Cap. II del Tít. XV.',
    'Incorpora disposiciones transitorias: art. 16 del Cap. IV y art. 30 del Cap. V del Tít. XVIII.',
    'Agrega al glosario del Tít. I los términos de la colocación (Agente Colocador Principal, Agentes Colocadores, Agente Interviniente, Sujetos Intervinientes, TIR) y redefine Cartera Propia, Cartera Propia Ampliada, Cartera Propia Restringida y Emisor.'],
    notas=['Antecedente: consulta pública de la RG 1157/2026.',
           'El Anexo I del art. 8° se publicó entre comillas rectas; se tomó entre ellas.',
           'En el art. 9° algunos subincisos citados terminan con "(…)" (elipsis de la cita); se omitió esa marca.'])
