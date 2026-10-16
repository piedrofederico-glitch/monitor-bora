import normas as N, fichas, re
n = 1163
N.VIGENCIAS[n] = '23/10/2026'
b = lambda k: N.md(N.bloque(n, k))
E = ('(…)', '(...)', '(…).', '(…)”.')
N.sustituir_articulo('V', 'I', '31 BIS', b(1), n, 1, seccion='VII')
N.sustituir_articulo('V', 'II', '5', b(2), n, 2, seccion='I')
for k, blk in N.por_articulo(b(3)):
    N.sustituir_articulo('V', 'II', k, blk, n, 3, seccion='V')
N.sustituir_seccion('V', 'II', 'VI', b(4), n, 4)
N.sustituir_anexo('V', 'III', 'II', b(5), n, 5)
for k, blk in N.por_articulo(b(6)):
    N.sustituir_articulo('V', 'VII', k, blk, n, 6, seccion='VII')
# art. 7°: apartados D, E, P y Q del art. 11 del Cap. I del Tít. XV
ps = [p for p in b(7) if p not in E and not N.clave_art(p)]
idx = [i for i, p in enumerate(ps) if re.match(r'^[A-Z]\) [A-ZÁÉÍÓÚ ]', p)] + [len(ps)]
bloques = {ps[a][0]: ps[a:c] for a, c in zip(idx, idx[1:])}
assert sorted(bloques) == ['D', 'E', 'P', 'Q']
C = N.Cap('XV', 'I'); i, j = C.rango_art('11')
cab = {p[0]: p for p in C.pars[i:j] if re.match(r'^[A-T]\) [A-ZÁÉÍÓÚ ]', p)}
sig = {'D': 'E', 'E': 'F', 'P': 'Q', 'Q': 'R'}
def f7(pars):
    for L in ('D', 'E', 'P', 'Q'):
        pars = N.tramo(cab[L], cab[sig[L]], bloques[L])(pars)
    return pars
N.modificar_articulo('XV', 'I', '11', f7, n, 7, 'Apartados D), E), P) y Q) sustituidos', det_extra='apartados D), E), P) y Q)')
fichas.ficha(n, [
    'Reformula el procedimiento de modificación de reglamentos de gestión de FCI: sustituye la Secc. VI del Cap. II del Tít. V (arts. 75, 75 BIS y 76) y el Anexo II del Cap. III del Tít. V (reglamento de gestión tipo).',
    'Sustituye el art. 31 BIS de la Secc. VII del Cap. I del Tít. V (Ficha Única de FCI abiertos), el art. 5° de la Secc. I y los arts. 68 y 69 de la Secc. V del Cap. II, y los arts. 27 TER y 27 QUATER de la Secc. VII del Cap. VII (FCIA ETF).',
    'Sustituye los apartados D), E), P) y Q) del art. 11 del Cap. I del Tít. XV (formularios AIF de Sociedades Gerentes, Depositarias, ACDI y ACD de FCI).',
    'Entra en vigencia a los 45 días hábiles contados desde el día siguiente a su publicación (art. 8°).'],
    vigencia='23/10/2026', vigencia_txt='art. 8°: 45 días hábiles desde el día siguiente a la publicación; fecha calculada para este texto, ver notas',
    notas=['Vigencia diferida y todavía no alcanzada al 16/10/2026: se aplica igual, con la nota "vigente desde 23/10/2026" en cada cambio, como se hizo con la RG 1090.',
           'La fecha 23/10/2026 es un cálculo propio: 45 días hábiles administrativos desde el 21/08/2026, descontando sábados, domingos y el feriado del 12/10/2026. No contempla días no laborables o asuetos administrativos que puedan correrla; confirmar con la CNV.'])
