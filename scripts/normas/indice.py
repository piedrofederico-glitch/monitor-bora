"""Genera vigente/INDICE.md a partir de los encabezados de cada archivo."""
import glob, os, re
import normas as N


def orden(p):
    r = os.path.relpath(p, N.VIG)
    m = re.match(r'titulo-([IVXL]+)/(capitulo-([IVXL]+|preliminar)|titulo-[IVXL]+)\.md', r)
    t = N.rom(m.group(1)); c = m.group(3)
    return (t, -2 if c is None else (-1 if c == 'preliminar' else N.rom(c)))


def generar():
    import json
    tits = json.load(open(N.TITJ))
    fs = sorted(glob.glob(f'{N.VIG}/titulo-*/*.md'), key=orden)
    out = ['# Normas CNV (N.T. 2013 y mod.) — índice del texto vigente', '',
           'Un archivo por capítulo (o por título cuando el título no tiene capítulos). '
           'Cada archivo indica su última modificación; el detalle por artículo está en `../modificaciones.md`.', '',
           ]
    por_tit = {}
    for f in fs:
        por_tit.setdefault(os.path.relpath(f, N.VIG).split('/')[0][7:], []).append(f)
    for t in sorted(tits, key=N.rom):
        out += ['', f"## Título {t} — {tits[t]['nombre']}"]
        if tits[t].get('nota'):
            out.append(tits[t]['nota'])
        if t not in por_tit:
            out.append('Sin texto vigente.' if tits[t].get('derogado') else '')
            continue
        out += ['', '| Archivo | Contenido | Última modificación |', '|---|---|---|']
        for f in por_tit[t]:
            h = open(f).read().split('\n')[:2]
            r = os.path.relpath(f, N.VIG)
            out.append(f"| [`{r}`]({r}) | {h[0][2:]} | {h[1].replace('Última modificación: ', '')} |")
    open(f'{N.VIG}/INDICE.md', 'w').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    generar()
